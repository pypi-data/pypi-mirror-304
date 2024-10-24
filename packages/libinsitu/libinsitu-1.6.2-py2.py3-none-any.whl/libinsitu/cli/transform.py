import argparse
import os.path
from os.path import basename, dirname

from libinsitu import update_qc_flags
from libinsitu.cdl import *
from libinsitu.common import *
from libinsitu.common import _prepare_properties
from libinsitu.handlers import HANDLERS, InSituHandler, listNetworks
from libinsitu.handlers.GenericCSVHandler import GenericCSVHandler
from libinsitu.log import debug, info, warning, logger, LogContext

DONE_SUFFIX = '.done'
ERR_SUFFIX = '.err'

BOUNDARY_TOLERANCE_PCT = 5

def check_boundaries(var, data) :
    """Check boundaries of a variable"""
    if not hasattr(var, VALID_MIN_ATTR) :
        return

    debug("Checking boundaries for %s" % var)

    minv = parse_value(getattr(var, VALID_MIN_ATTR))
    maxv = parse_value(getattr(var, VALID_MAX_ATTR))

    range = maxv - minv

    # Add tolerance
    minv = minv - range * BOUNDARY_TOLERANCE_PCT / 100
    maxv = maxv + range * BOUNDARY_TOLERANCE_PCT / 100

    def warn_boundary(idx, sign, bound) :
        if np.any(idx):
            warning("Boundary check : %d items of %s are %s %f: [%f:%f]",
                    np.sum(idx),
                    var.name,
                    sign,
                    bound,
                    np.min(data[idx]),
                    np.max(data[idx]))

    warn_boundary(data < minv, "<", minv)
    warn_boundary(data > maxv, ">", maxv)


def list_files(in_files, handler) :

    # Gather and sort files with pattern
    files = []
    for file_or_dir in in_files:
        if os.path.isdir(file_or_dir):
            files += handler.list_files(file_or_dir)
        else:
            files.append(file_or_dir)

    # Sort input files
    in_files = handler.sort_files(files)

    if len(in_files) == 0:
        warning("No input file found")
        sys.exit(-1)

    return in_files


def process_network(network, station_id, args) :

    # Get all properties
    properties = getProperties(
        network,
        station_id,
        custom_station_file=args.station_metadata,
        custom_network_file=args.network_metadata,
        check_network=(args.mapping is None))

    # Generic handler ?
    if args.mapping :

        if not args.station_metadata :
            raise Exception("Missing file path for custom station metadata")

        handler = GenericCSVHandler(properties, args.mapping)
    else:

        # Check network
        all_networks = listNetworks()
        if not network in all_networks:
            raise Exception("Bad Network %s. Should be one of %s" % (network, str(all_networks)))

        handler : InSituHandler = HANDLERS[network](properties)

    in_files = list_files(args.in_files, handler)

    new = not os.path.exists(args.out)

    # If file exists, put it in read only until we process an input file, to avoid changing its mtime
    mode = "w" if new else "r"
    ncfile = Dataset(args.out, mode=mode)

    if new :
        # Nc File does not exist ==> create it
        info("File '%s' was not there. Initializing it.", args.out)
        init_nc(
            ncfile,
            properties,
            data_vars=[],
            custom_cdl=args.cdl)

    min_date = None
    max_date = None

    # Loop on input files
    for infile in in_files :

        info("processing chunk : %s", infile)

        with LogContext(file=os.path.basename(infile)):

            # Safe execution : do not stop on error
            try:

                # Incremental mode : check status files
                status_folder = args.status_folder or dirname(infile)
                status_file = os.path.join(status_folder, basename(infile) + DONE_SUFFIX)
                err_file = os.path.join(status_folder, basename(infile) + ERR_SUFFIX)

                # Incremental mode : if output was already there, don't proess input files having a more recent .done file
                if not new and args.incremental and os.path.exists(status_file) and older_than(infile, status_file):
                    info("File %s is older than status file %s : Skipping", infile, status_file)
                    continue

                # First processed file ? reopen the file in write mode => this will update its mtime
                if mode == "r" :
                    ncfile.close()
                    ncfile = Dataset(args.out, mode="a")
                    mode = "a"

                data = handler.read_chunk(infile)

                chunk_start, chunk_end = process_chunck(
                    data, ncfile, properties,
                    check=args.check,
                    strict_resolution=args.strict_resolution,
                    custom_cdl=args.cdl)

                # Store extent of update
                min_date = nmin(chunk_start, min_date)
                max_date = nmax(chunk_end, max_date)

                # Incremental mode : touch status file
                if args.incremental:
                    touch(status_file)

                    # err file was present : delete it
                    if os.path.exists(err_file) :
                        os.remove(err_file)

            # Don't intercept Ctrl-C : cancel the whole process
            except KeyboardInterrupt as e :
                raise e

            except Exception as e :

                # Write .err file
                if args.incremental:
                    touch(os.path.join(status_folder, basename(infile) + ERR_SUFFIX))

                # Do not fail : just log and process the next file
                logger.exception(e)

    if (not args.no_qc) and (min_date is not None) :
        # We need to wait for everything to be processed before computing QC (instead of computing it chunk by chunk),
        # because some provider split components into several input files (like SKYNET)
        info("Processing QC flags on [%s - %s]" % (min_date, max_date))

        update_qc_flags(
            ncfile,
            start_time=min_date,
            end_time=max_date)


def idx2slice(idx) :
    """If indices are regular, transform it into a slice : much faster for writing"""

    if len(idx) < 2 :
        return idx

    step = idx[1] - idx[0]

    if np.all(np.diff(idx) == step) :
        debug("Idx was slice")
        return slice(idx[0], idx[-1] + step, step)

    return idx

def check_and_assign(ncfile, data, times_idx, size_before, check=False) :

    # Check once for all if new chunk overlaps
    overlapping_mask = times_idx < size_before
    overlapping_indices = times_idx[overlapping_mask]

    for varname in data.columns:

        var = ncfile.variables[varname]
        new_values = data[[varname]].values.flatten()

        check_boundaries(var, new_values)

        # Overcoming this bug ; https://github.com/scipy/scipy/issues/6097
        if np.issubdtype(var.dtype, np.integer) :
            fill_value = getattr(var, FILL_VALUE_ATTR, DEFAULT_FILL_VALUE)
            new_values[np.isnan(new_values)] = fill_value

        if not np.any(overlapping_mask) or not check:
            # No overlap with previous data ? no need for check
            var[idx2slice(times_idx)] = new_values

        else :
            debug("Possible overlap, checking ...")

            if np.all(np.isnan(var[overlapping_indices])) :

                # All nans ? don't check further"
                write_mask = np.ones(new_values.shape, dtype=bool)

            else:
                # We won't override existing values with nans
                nan_mask = np.isnan(new_values)

                nna_overlapping_mask = overlapping_mask & ~nan_mask
                overlapping_idx = times_idx[nna_overlapping_mask]
                overlapping_values = new_values[nna_overlapping_mask]
                overlapped_values = var[overlapping_idx]

                conflicting_indices = ~np.isnan(overlapped_values) & ~np.isclose(overlapping_values, overlapped_values)

                if np.any(conflicting_indices) :

                    conflicting_overlapped =  overlapped_values[conflicting_indices]
                    conflicting_overlapping = overlapping_values[conflicting_indices]

                    warning("%d conflicting values for %s. Overriding [%f:%f] -> [%f:%f]",
                            np.sum(conflicting_indices),
                            varname,
                            np.nanmin(conflicting_overlapped), np.nanmin(conflicting_overlapped),
                            np.nanmin(conflicting_overlapping), np.nanmin(conflicting_overlapping))

                # Write NaN if they do not overlap with existing data (this extends the dimension)
                write_mask = nan_mask | ~overlapping_mask

            var[idx2slice(times_idx[write_mask])] = new_values[write_mask]

def dataframe_to_netcdf(
        data,
        out_filename,
        station_name,
        network_name=None,
        latitude=None,
        longitude=None,
        elevation=None,
        process_qc=True,
        close=True,
        network_props = dict(),
        station_props = dict(),
        custom_cdl=None) :
    """
    Transforms a Dataframe of solar irradiance to a well encoded NetCDF file.

    :param data: The dataframe. It should contain GHI, DHI, BNI columns in W.m-2 and be indexed by UTC time (Datetime index)
    :param out_filename: Name of output file
    :param station_name: Station name. Can also be passed as 'Name' in station properties
    :param network_name: Network name. Can also be passed as 'Name' in network properties
    :param latitude: Station latitude. Can also be passed as 'Latitude' in station properties
    :param longitude: Station longitude. Can also be passed as 'Longitude' in station properties
    :param elevation: Station elevation.  Can also be passed as 'Elevation' in station properties
    :param process_qc: Process and embed QC flags (true be default)
    :param close: Close netcdf file at the end of process
    :param network_props: Dict of additional network properties (without `Network_` prefix), as used in base.cdl
    :param station_props: Dict of additional station properties (without `Station_` prefix) as used in base.cdl
    :param custom_cdl: File path to custom schema.cdl file
    """

    properties = _prepare_properties(
        network_props,
        station_props)

    def update_props(key, value) :
        if value is not None and not key in properties :
            properties[key] = value

    update_props("Station_ID", station_name)
    update_props("Station_Name", station_name)
    update_props("Network_ID", network_name)
    update_props("Network_LongName", network_name)
    update_props("Station_Latitude", latitude)
    update_props("Station_Longitude", longitude)
    update_props("Station_Elevation", elevation)

    # Guess the resolution from the input
    res_sec = get_df_resolution(data)

    # Set global attribute for time resolution
    res_str = "%dM" % (res_sec // 60) if res_sec >= 60 else "%dS" % res_sec
    update_props("Station_TimeResolution", res_str)

    # Fill time extent
    start_time = data.index[0]
    end_time = data.index[-1]

    update_props("Station_StartDate", start_time.strftime("%Y-%m-%d"))
    update_props("LastData", time2str(end_time, seconds=True))

    # Create file
    ncfile = Dataset(out_filename, mode="w")
    try :
        init_nc(ncfile, properties, [])

        # Transform data
        process_chunck(
            data, ncfile, properties,
            custom_cdl=custom_cdl)

        if process_qc :
            update_qc_flags(ncfile)

    finally:
        if close :
            ncfile.close()

    return ncfile




def process_chunck(data, ncfile, properties, strict_resolution=False, check=False, custom_cdl=None):

    if data is None or len(data) == 0 :
        warning("Chunk is empty")
        return

    # Time resolution, in seconds
    resolution_s = getTimeResolution(ncfile)

    # Drop duplicates
    data = data[~data.index.duplicated(keep="last")]

    # Reshape : regular time is faster to write in NetCDF (as slice)
    data = data.asfreq("%dS" % resolution_s)

    # Transform time to seconds since start date and time idx
    chunk_dates : NDArray[datetime64] = data.index.values

    times_sec = datetime64_to_sec(ncfile, chunk_dates)

    columns = list(data.columns)

    # Create vars if not present yet
    missing_vars = list(col for col in columns if not col in ncfile.variables)
    if len(missing_vars) > 0:
        info("Adding missing vars : %s", missing_vars)
        init_nc(ncfile, properties, missing_vars, custom_cdl=custom_cdl)

    # Ensure all timestamps fall into resolution
    exact_idx = (times_sec % resolution_s) == 0
    nb_not_exact_times = len(times_sec) - np.sum(exact_idx)
    if nb_not_exact_times > 0:

        # Remove lines with wrong times
        data = data[exact_idx]
        times_sec = times_sec[exact_idx]

        warning("%d rows had timings not fitting the time resolution : skipping them" % nb_not_exact_times)


    # Seconds to time index, as per start date and resolution
    time_idx = seconds_to_idx(ncfile, times_sec)

    chunk_start = min(chunk_dates)
    chunk_end = max(chunk_dates)
    chunk_end_int = datetime64_to_sec(ncfile, chunk_end)

    info("chunck range: %s to %s. samples:%d", time2str(chunk_start), time2str(chunk_end), len(data.index))

    # Error if chunk starts before start time
    if sum(time_idx < 0) > 0 :
        raise Exception("Chunk start (%s) is before output start time (%s). Skipping" % (
            time2str(chunk_start), start_date64(ncfile)))

    # Warning if resolution seems different
    # Error if scrictREsolution is set
    if len(times_sec) >= 2:

        periods = get_periods(times_sec)
        if len(periods) >= 1 :
            actual_resolution, count = periods[0]

            if actual_resolution != resolution_s:
                warning("Resolution of input chunk (%d sec) differs from resolution of output (%d sec)" % (actual_resolution, resolution_s))
                if strict_resolution :
                    warning("Strict resolution requested : skipping")
                    return

    timeVar = getTimeVar(ncfile)

    # Fill time variable with proper values
    size_before = len(timeVar) # Remember the size of TIME before it is extended

    # Fill Time variable
    if len(timeVar) == 0 :
        next_time_sec =  datetime64_to_sec(ncfile, start_date64(ncfile))
    else:
        next_time_sec = timeVar[-1] + resolution_s

    end_time_sec = chunk_end_int + resolution_s
    new_times_sec = np.arange(next_time_sec, end_time_sec, resolution_s)
    next_time_idx = seconds_to_idx(ncfile, next_time_sec)
    end_time_idx = seconds_to_idx(ncfile, end_time_sec)
    timeVar[next_time_idx: end_time_idx] = new_times_sec

    # Store data values
    check_and_assign(ncfile, data, time_idx, size_before, check)

    info("Chunk processed successfully")

    return chunk_start, chunk_end


def sort_files(files) :
    """ Sort filenames named like xxxMMYY*"""
    def yearmonth(path):
        file = basename(path)
        year = file[5:7]
        month = file[3:5]
        if year.isnumeric() :
            year_num = int(year)
            year_num += 1900 if year_num > 70 else 2000
            year = str(year_num)
        res =  year + '-' + month + '-' + file[7:]
        return res

    return sorted(files, key=yearmonth)

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid folder")


def parser() :
    parser = argparse.ArgumentParser(description='Transforms In-Situ data into NetCDF files')
    parser.add_argument('out', metavar='<out.nc>', type=str, help='Output file')
    parser.add_argument('in_files', metavar='<file|dir>', nargs='+', help='Input files or folders')
    parser.add_argument('--network', '-n', help='Network name', required=False)
    parser.add_argument('--station-id', '-s', metavar='<SID>', help='Station ID', required=True)
    parser.add_argument('--mapping', '-m', metavar='<mapping.json>', help='Use a generic parser with custom mapping. Tu be used in conjonction with --station-metadata and network-metadata')
    parser.add_argument('--station-metadata', '-sm', metavar='<station-meta.csv>', help='Use custom station metadata (Station_* properties) instead of embedded ones.', default=None)
    parser.add_argument('--network-metadata', '-nm', metavar='<network-meta.csv>',
                        help='Use custom metadata for the Networks (Network_* properties), instead of mebedded ones', default=None)

    parser.add_argument('--cdl', metavar='<schema.cdl>', help="Use a custom CDL (NetCDF schema)")
    parser.add_argument(
        '--incremental', '-i', default=False, action='store_true',
        help="Incremental mode, skipping input files having a '.done' status files")
    parser.add_argument(
        '--strict-resolution', '-sr', default=False, action='store_true',
        help="Skip chunks having a different resulution")
    parser.add_argument('--no-qc', default=False, action='store_true', help="Do not compute QC flags")
    parser.add_argument('--check', '-c', default=False, action='store_true', help="Check potential override of data")
    parser.add_argument(
        '--status-folder', '-f',
        metavar='<folder>', type=dir_path,
        help='Folder for status files in incremental mode', default=None)
    return parser

def main():

    args = parser().parse_args()

    network = args.network

    if network is None and args.mapping is None :
        raise Exception("--network is mandatory if custom mapping / generic parser is not used")

    station_id  = args.station_id

    with LogContext(network=network, station_id=station_id):
        process_network(network, station_id, args)

if __name__ == '__main__':
    main()