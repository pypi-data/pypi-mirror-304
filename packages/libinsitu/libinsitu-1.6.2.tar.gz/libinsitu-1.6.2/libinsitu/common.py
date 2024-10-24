import os
import re
import sys
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from csv import DictReader
from datetime import datetime
from functools import reduce
from pkgutil import get_data
from types import SimpleNamespace
from typing import Union
from urllib.parse import urlsplit, quote_plus

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from netCDF4 import *
from numpy import timedelta64, datetime64
from numpy.typing import NDArray
from pandas import DataFrame
from six import StringIO

from libinsitu._version import __version__
from libinsitu.log import warning

# Name of dimensions and variables
TIME_DIM = 'time'
TIME_VAR = "time"
GLOBAL_VAR = "GHI"
DIFFUSE_VAR = "DHI"
DIRECT_VAR = "BNI"
TEMP_VAR = "T2"
HUMIDITY_VAR = "RH"
PRESSURE_VAR = "P"
WIND_SPEED_VAR = "WS"
WIND_DIRECTION_VAR = "WD"

QC_FLAGS_VAR = "QC"
QC_RUN_VAR = "QC_run"
QC_LEVEL_VAR = "QC_level_%s"

QC_FLAGS_STANDARD_NAME="quality_flag"
QC_RUN_STANDARD_NAME="quality_flag_processed"

# Columns for station info, in order of apparition
VALID_COLS = [
    "ID",
    "UID",
    "WMOID",
    "Name",
    "Latitude",
    "Longitude",
    "Elevation",
    "Timezone",
    "StartDate",
    "EndDate",
    "TimeResolution",
    "Address",
    "City",
    "Region",
    "Country",
    "SurfaceType",
    "TopographyType",
    "RuralUrban",
    "Climate",
    "OperationStatus",
 #   "DataBegin",
 #   "DataEnd",
    "ContactName",
    "Institute",
    "Url",
    "CommissionDate",
    "DecommissionDate",
    "DNI_Col",
    "DHI_Col",
    "GHI_Col",
    "QualityStandard",
    "Comment"]

# Variable attributes
VALID_MIN_ATTR = "valid_min_"
VALID_MAX_ATTR = "valid_max_"
FILL_VALUE_ATTR = "_FillValue"

DEFAULT_FILL_VALUE = -999

# Alternate names often found for variables
ALTERNATE_COMP_NAMES = {
    DIFFUSE_VAR : ["DIF"],
    DIRECT_VAR : ["DNI"]
}

ALTERNATE_COMP_NAMES_INV = {
    val : key for key, vals in ALTERNATE_COMP_NAMES.items() for val in vals
}

# Meta data variables
LATITUDE_VAR = "latitude"
LONGITUDE_VAR = "longitude"
ELEVATION_VAR = "elevation"
STATION_NAME_VAR= "station_name"
STATION_LONG_NAME_VAR= "platform"


# Global attrs
GLOBAL_TIME_RESOLUTION_ATTR = "time_coverage_resolution"

CLIMATE_ATTRS = [
    "climate",
    "Station_KoeppenGeigerClimate"] # XXX Old convention

STATION_ID_ATTRS = [
    "station_id",
    "Station_Id",  # XXX Old convention
    "id"]

STATION_COUNTRY_ATTRS = [
    "station_country",
    "Station_Country"] # XXX Old conventions

NETWORK_NAME_ATTRS = [
    "Network_Name", # XXX Old convention
    "project"]

NETWORK_ID_ATTRS = [
    "network_id",
    "project"]

# Prefix for global properties
STATION_PREFIX = "Station_"
NETWORK_PREFIX = "Network_"

NA_VALUES=[-999.0, -99.9, -10.0, -9999.0, -99999.0]

CHUNK_SIZE=5000


# List of attributes to search station ID for
STATION_ID_ATTRS = ["Station_ID", "StationInfo_Abbreviation", "station_id", STATION_NAME_VAR]
NETWORK_ID_ATTRS = ["network_id", "Network_ShortName"]

DATA_VARS = [GLOBAL_VAR, DIFFUSE_VAR, DIRECT_VAR, TEMP_VAR, HUMIDITY_VAR, PRESSURE_VAR, WIND_SPEED_VAR, WIND_DIRECTION_VAR]

STATION_INFO_PATTERN = "station-info/%s.csv"
NETWORK_INFO_FILE = "networks.csv"

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT_MIN= '%Y-%m-%dT%H:%M'
TIME_FORMAT_SEC= '%Y-%m-%dT%H:%M:%S'

STATION_START_DATA_ATTR = "time_coverage_start"

SECOND = timedelta64(1, 's')
CDL_PATH = "base.cdl"

def parseCSV(res_path, key = "ID", resource=True, as_objects=False) :
    """Generic parser """
    res = dict()

    file = read_res(res_path) if resource else open(res_path, 'r')
    rows = DictReader(file)
    for row in rows:

        # Skip commented lines
        if "#" in row[key] :
            continue

        # We force ID to stay a String
        res[row[key]] = {k: val if k == key else parse_value(val) for k, val in row.items()}

        if as_objects :
            res[row[key]] = SimpleNamespace(**res[row[key]])

    return res

def getStationsInfo(network) :
    """Read station info from CSV"""
    return parseCSV(STATION_INFO_PATTERN % network)

def getNetworksInfo() :
    return parseCSV(NETWORK_INFO_FILE)


def older_than(file1, file2) :
    """Return True if file1 is older than file2"""
    return os.stat(file1).st_mtime < os.stat(file2).st_mtime

def touch(filename):
    """ creates or update the time of a file """
    if os.path.exists(filename):
        os.utime(filename)
    else:
        with open(filename,'a') :
            pass

def getStationInfo(network, station_id, custom_file=None) :

    if custom_file :
        stations = parseCSV(custom_file, resource=False)
    else:
        stations = getStationsInfo(network)
    if not station_id in stations :
        raise Exception("Station %s not found in Station Info of %s" % (station_id, network))
    return stations[station_id]

def getNetworkInfo(network, custom_file=None, check=True) :

    if custom_file :
        networks = parseCSV(custom_file, resource=False)
    else:
        networks = getNetworksInfo()

    if not network in networks :
        if check:
            raise Exception("Network %s not found in Network info" % network)
        else:
            return dict()
    return networks[network]

def is_uniform(vector) :

    if type(vector) == list :
        vector = np.array(vector)

    if len(vector) <=1 :
        return True
    step = vector[1] - vector[0]
    ref = np.arange(vector[0], vector[-1] + step, step)
    return np.array_equal(ref, vector)

def get_origin_time(ncfile) -> datetime64 :
    timeVar = getTimeVar(ncfile)
    start_time = num2date(0, timeVar.units, timeVar.calendar)
    return np.datetime64(start_time)

def to_int(vals) :
    """Transform single val or array to int """
    if isinstance(vals, np.ndarray):
        return vals.astype(int)
    else:
        return int(vals)

def datetime64_to_sec(ncfile, dates : NDArray[datetime64], unit='s') -> NDArray[int] :
    """Transform datetime64 to number of seconds since origin date """
    origin = get_origin_time(ncfile)
    return to_int((dates - origin) / timedelta64(1, unit))

def str_to_date64(datestr) :
    for format in [TIME_FORMAT_SEC, TIME_FORMAT_MIN, DATE_FORMAT] :
        try :
            return np.datetime64(datetime.strptime(datestr, format))
        except:
            pass

    raise Exception("Unable to parse : " + datestr)


def start_date64(ncfile) :
    if  hasattr(ncfile, STATION_START_DATA_ATTR) :
        return str_to_date64(getattr(ncfile, STATION_START_DATA_ATTR))
    else:
        res = sec_to_datetime64(ncfile, getTimeVar(ncfile)[0])[()]
        warning("No start date set in meta data : taking the first value of ncfile : %s" % res)
        return res

def end_date64(ncfile):
    return sec_to_datetime64(ncfile, getTimeVar(ncfile)[-1])[()]

def seconds_to_idx(ncfile, dates : NDArray[int], ) -> NDArray[int] :
    """Transform seconds since origin to time idx, taking into account resolution and start date"""
    resolution_s = getTimeResolution(ncfile)
    start_sec = datetime64_to_sec(ncfile, start_date64(ncfile))
    return to_int((dates - start_sec) / resolution_s)

def sec_to_datetime64(ncfile, times_s: NDArray[int]) ->  NDArray[datetime64]:
    """Transform number of seconds since start time into datetime64 """
    start_time64 = get_origin_time(ncfile)
    return start_time64 + SECOND * times_s

def read_res(path, encoding="utf8") :
    """Read package resources and returns a fie like object (splitted lines)
    path should be relative to ./res/
    """
    return get_data(__name__, os.path.join("res", path)).decode(encoding).splitlines()

def parse_value(val, split=False) :
    """Parse string value, trying first int, then float. return str value if none are correct"""
    if not isinstance(val, str) :
        return val

    if val is None or val == "":
        return None

    val = val.strip()

    # String
    if val.startswith('"'):
        return val.strip('"')

    # List of things
    if split and "," in val :
        return list(parse_value(item) for item in val.split(","))

    try :
        return int(val)
    except:
        try:
            return float(val)
        except:
            return val


def getTimeResolution(ncfile) :
    """Returns time resolution, in seconds, as saved in meta data"""

    time_var = getTimeVar(ncfile)

    # Formatted as ISO8601 : P10M, P30S, ...
    if hasattr(ncfile, GLOBAL_TIME_RESOLUTION_ATTR) :
        dt = pd.Timedelta(getattr(ncfile, GLOBAL_TIME_RESOLUTION_ATTR))
        return dt.seconds

    if hasattr(time_var, "resolution") :
        # XXX - Support for old versions of NetCDF
        val = time_var.resolution
        val, unit = val.split()
        val = int(val)
        if "min" in unit :
            return val * 60
        elif "sec" in unit:
            return val
        else:
            raise Exception("Unknown unit for time resolution : '%s'" % unit)

    # Guessing from actual first values
    res = int(time_var[1] - time_var[0])
    warning("No resolution set. Guessing :%d seconds" % res)
    return res


def openNetCDF(filename, mode='r', user=None, password=None) :
    """ Open either a filename or OpenDAP URL with user /password"""
    if '://' in filename :
        if user :
            filename = with_auth(filename, user, password)
        filename = "[FillMismatch]" + filename
    return Dataset(filename, mode=mode)

def date_to_timeidx(nc, date) :
    """Transform date to NetCDF index along Time dimension"""
    if isinstance(date, datetime) :
        date = datetime64(date)
    time_sec = datetime64_to_sec(nc, date)
    return seconds_to_idx(nc, time_sec)


def re_pattern(pattern, properties=dict()) :
    """ Transform pattern to regexp matching groups for replacement """
    def subf(match):
        key = match.group(1)
        if key in properties:
            return str(properties[key])
        else:
            if key in ["M", "MM", "YY", "YYYY", "DDD"] :
                pattern = r'\d+' if key == "M" else r'\d' * len(key)
            else:
                pattern = "[A-Z_]+"
            return r'(?P<%s>%s)' % (key, pattern)

    # Transforms pattern to regular expression for matching
    re_pattern = pattern.replace("?", ".").replace("*", ".*")
    return re.sub(r'\{(\w+)\}', subf, re_pattern)

def to_range(year, month=0, day=1) :
    """ Transform a year or month inot a range of datatime """
    yearly=False
    if not month :
        month = 1
        yearly = True

    first = datetime(year, month, day)
    if yearly :
        last = first + relativedelta(years=1)
    else:
        last  = first + relativedelta(months=1)

    return (first, last)


def match_pattern(pattern, value, properties=dict()) :
    """Transforms pattern expression into regexp and extracts the keys """

    reg = re_pattern(pattern, properties)
    match = re.match(reg, value, flags=re.IGNORECASE)

    if not match :
        return False

    res = match.groupdict()

    if "M" in res:
        res["month"] = int(res["M"])
        del res["M"]

    if "MM" in res:
        res["month"]  = int(res["MM"])
        del res["MM"]

    if "DDD" in res:
        res["days"] = int(res["DDD"])
        del res["DDD"]

    if "YYYY" in res:
        res["year"] = int(res["YYYY"])
        del res["YYYY"]

    if "YY" in res:
        year = int(res["YY"])
        res["year"] = year + (2000 if year < 70 else 1900)
        del res["YY"]

    return res

def get_df_resolution(df) :
    """Get resolution of a time series Dataframe in seconds. Either from metdata or from guessing it"""
    if GLOBAL_TIME_RESOLUTION_ATTR in df.attrs :
        return df.attrs[GLOBAL_TIME_RESOLUTION_ATTR]

    # Guess it from data
    return df.index.to_series().diff().median().total_seconds()

def netcdf_to_dataframe(
        ncfile : Union[Dataset, str],
        start_time: Union[datetime, datetime64]=None,
        end_time:Union[datetime, datetime64]=None,
        rel_start_time=None, # Start time, relative to actual end
        rel_end_time=None, # End time, relative to actual start
        drop_duplicates=True,
        skip_na=False,
        skip_qc=False,
        vars=None,
        user=None,
        password=None,
        chunked=False,
        chunk_size=CHUNK_SIZE,
        steps=1,
        rename_cols=False,
        expand_qc=False):
    """
        Load NETCDF in-situ file (or part of it) into a panda Dataframe, with time as index.


        :param ncfile: NetCDF Dataset or filename, or OpenDAP URL
        :param rename_cols: If True (default) rename solar irradiance columns as per convention (GHI, BNI, DHI)
        :param drop_duplicates: If true (default), duplicate rows are droppped
        :param skip_qc:

            If true, filters rows having any failing QC. False by default (no filter).

            You can also provide a list of flags to filter : `["T3C_bsrn_3cmp", "T2C_seri_kn_kt"]`

            Or filter on any flags but some, by prepending '!' : `["!T3C_bsrn_3cmp", "!T2C_seri_kn_kt"]`

            For full list of flags, see the [online doc](https://libinsitu.readthedocs.io/en/latest/qc.html)

        :param skip_na: If True, drop rows containing only nan values
        :param start_time: Start time (first record by default) : Datetime or datetime64
        :param end_time: End time (last record by default) : Datetile or datetime64
        :param rel_end_time: End time, relative to actual start time : relativedelta
        :param rel_start_time: Start time, relatie to actual end time : relativedelta
        :param vars: List of columns names to convert (all by default)
        :param user: Optional login for OpenDAP URL
        :param password: Optional password OpenDAP URL
        :param chunked: If True, does not load the whole file in memory at once : returns an iterator on Dataframe chunks.
        :param chunk_size: Size of chunks for chunked data
        :param steps: Downsampling (1 by default)
        :param expand_qc: If True, expand the QC bitmaps into one boolean column for each flag with name "QC.<flag>"

        :return: Pandas Dataframe, or iterator on Dataframes if chunking is activated
        """

    chunks = __nc2df(
        ncfile=ncfile,
        start_time=start_time,
        end_time=end_time,
        rel_start_time=rel_start_time,
        rel_end_time=rel_end_time,
        drop_duplicates=drop_duplicates,
        skip_na=skip_na,
        vars=vars,
        user=user,
        password=password,
        chunked=chunked,
        chunk_size=chunk_size,
        steps=steps,
        rename=rename_cols,
        skip_qc=skip_qc,
        expand_qc=expand_qc)

    # Handling either single result or chunked generator
    if not chunked :
        for result in chunks:
            return result
    else :
        return chunks


def getTimeVar(nc) :
    for key in nc.variables.keys() :
        if key.lower() == TIME_VAR.lower() :
            return nc.variables[key]
    raise Exception("No time var found")

def find_var_by_std_name(nc_or_df, std_name):
    """Find a variable having a specific standard_name """

    var_attrs = __all_attributes(nc_or_df)["variables"]

    for varname, attrs in var_attrs.items():
        if attrs.get("standard_name", None) == std_name :
            return varname
    return None


def find_qc_vars(nc_or_df) :
    """Find Qc variables from standard names"""
    qc_varname = find_var_by_std_name(nc_or_df, QC_FLAGS_STANDARD_NAME)
    qc_run_varname = find_var_by_std_name(nc_or_df, QC_RUN_STANDARD_NAME)
    return qc_varname, qc_run_varname


def __get_attributes(ncfile_or_var) :
    return dict((key, getattr(ncfile_or_var, key)) for key in ncfile_or_var.ncattrs())

def __all_attributes(ncfile_or_df) :
    """Get all attributes from a NcFile or a dataframe (parsed from NcFile). Atributes for vars are in 'variables' """

    if isinstance(ncfile_or_df, DataFrame) :
        return ncfile_or_df.attrs

    # Global attributes
    attrs = __get_attributes(ncfile_or_df)

    # Put single var meta data in global attributes
    # XXX Obsolete ? new CDL files integrate it already ?
    for varname in [LATITUDE_VAR, LONGITUDE_VAR, ELEVATION_VAR] :
        if varname in ncfile_or_df.variables :
            attrs[varname] = readSingleVar(ncfile_or_df.variables[varname])

    if STATION_NAME_VAR in ncfile_or_df.variables:
        attrs[STATION_NAME_VAR] = readShortname(ncfile_or_df)

    # Add meta data of variables
    attrs["variables"] = dict((varname, __get_attributes(var)) for varname, var in ncfile_or_df.variables.items())

    # Put time resolution in seconds in global var
    attrs[GLOBAL_TIME_RESOLUTION_ATTR] = getTimeResolution(ncfile_or_df) or 60

    return attrs

def _skip_qc_to_mask(df, flags) :

    # 32 ones bitmap
    ones_mask = 0xffffffff
    if flags is True:
        return ones_mask
    if not flags :
        return 0

    # At this point, flags is a list of flags or negative (!) flags

    # Extract (!)
    neg = [flag.startswith("!") for flag in flags]
    flags = list(flag.replace("!", "") for flag in flags)

    # Ensure not mixed negative and positive flags
    if neg[1:] != neg[:-1] :
        raise Exception("You cannot mix positive and negative (!) flags")

    masks = qc_masks(df)

    if neg[0]:
        # Negative flags
        return reduce(
            lambda a, b : a & ~b,
            list(masks[flag] for flag in flags),
            ones_mask)
    else:
        return reduce(
            lambda a, b: a | b,
            list(masks[flag] for flag in flags), 0)



def _expand_qc(df, qc_varname, qc_run_varname=None) :

    # Get bitmaps
    bitmaps = df[qc_varname]
    del df[qc_varname]

    # Get masks
    masks = qc_masks(df, qc_varname)

    # Dict of QC flag name => value
    res = {
        flagname: (bitmaps & mask > 0).astype(int)
        for flagname, mask in masks.items()}

    if qc_run_varname is  None:
        return res

    # Get QC run flags
    qc_run = df[qc_run_varname]
    del df[qc_run_varname]

    for flagname, flags in list(res.items()):

        mask = masks[flagname]

        res[flagname] = np.select(
            [qc_run & mask > 0], # Did this test run ?
            [flags], # Then take its value
            -1) # Else take -1

    return res


def _data_cols(df) :
    """Return only the list of data columns, skipping QC related ones"""
    var_attrs = __all_attributes(df)["variables"]
    return [col for col in df.columns if not "flag_meanings" in var_attrs[col]]


def __nc2df(
        ncfile : Union[Dataset, str],
        start_time: Union[datetime, datetime64]=None,
        end_time:Union[datetime, datetime64]=None,
        rel_start_time=None,
        rel_end_time=None,
        drop_duplicates=True,
        skip_na=False,
        skip_qc=False,
        vars=None,
        user=None,
        password=None,
        chunked=False,
        chunk_size=CHUNK_SIZE,
        steps=1, rename=True,
        expand_qc=False) :

    """Private generator use by nc2df """

    if isinstance(ncfile, str) :
        ncfile = openNetCDF(ncfile, mode='r', user=user, password=password)

    timeVar = getTimeVar(ncfile)

    size = len(timeVar)

    if rel_start_time is not None :
        start_time = end_date64(ncfile).astype(datetime) + rel_start_time
    if rel_end_time is not None :
        end_time = start_date64(ncfile).astype(datetime) + rel_end_time

    start_idx = max(0, date_to_timeidx(ncfile, start_time)) if start_time else 0
    end_idx = min(date_to_timeidx(ncfile, end_time)+1, size) if end_time else size

    # List of data vars (along time)
    data_vars = []
    for varname, var in ncfile.variables.items() :
        if TIME_DIM in var.dimensions and var != timeVar :
            if vars is None or varname in vars :
                data_vars.append(varname)

    qc_varname, qc_run_varname = find_qc_vars(ncfile)

    def to_df(start_idx, end_idx) :

        times = sec_to_datetime64(ncfile, timeVar[start_idx:end_idx:steps])

        # Loop on data variables
        data = dict()
        for varname in data_vars :
            var = ncfile.variables[varname]
            values = var[start_idx:end_idx:steps]

            # Unmask int vars
            if np.ma.is_masked(values) and np.issubdtype(values.dtype, np.integer) :
                values = values.data

            data[varname] = values

        df = DataFrame(data, index=times)

        # Add meta data to attributes of the Dataframe
        df.attrs.update(__all_attributes(ncfile))

        # Drop duplicated : only keep last
        if drop_duplicates :
            df = df[~df.index.duplicated(keep="last")]

        # Drop NA ?
        if skip_na :
            subset = _data_cols(df)
            df = df.dropna(axis=0, how='all', subset=subset)

        if skip_qc and qc_varname is not None :
            qc_mask = _skip_qc_to_mask(df, skip_qc)
            df = df[(df[qc_varname] & qc_mask) == 0]

        if expand_qc and qc_varname is not None:
            flags = _expand_qc(df, qc_varname, qc_run_varname)

            # Save flag values in dataframe
            for col, values in flags.items() :
                df["QC.%s"  % col] = values

        # Rename variables
        if rename :
            for dest, sources in ALTERNATE_COMP_NAMES.items():
                for source in sources :
                    if source in df.columns :
                        warning("Renaming %s -> %s" % (source, dest))
                        df = df.rename(columns={source:dest})

        return df

    if chunked :
        chunk_size = chunk_size * steps
        for idx in range(start_idx, end_idx, chunk_size):
            yield to_df(start_idx=idx, end_idx=min(idx + chunk_size, end_idx))
    else :
        yield to_df(start_idx, end_idx)

def time2str(val, seconds=False) :
    """Format date to the minute """
    if val is None :
        return ""
    if isinstance(val, datetime64) :
        return np.datetime_as_string(val, unit='s' if seconds else 'm')
    elif isinstance(val, datetime) :

        return val.strftime(TIME_FORMAT_SEC if seconds else TIME_FORMAT_MIN)

    raise Exception("Unknown date type : %s" % type(val))

def str2time64(val) :
    if val is None or val == "":
        return None
    return np.datetime64(val)


MIN_STEP=0
MAX_STEP=7200

def get_periods(time_s) :
    """Compute list of periods, by occurrence. Return list of (period, count)"""

    steps = time_s[1:] - time_s[0:len(time_s) - 1]
    unique, counts = np.unique(steps, return_counts=True)

    filtered_unique = unique[(unique > MIN_STEP) & (unique < MAX_STEP)]
    filtered_counts = counts[(unique > MIN_STEP) & (unique < MAX_STEP)]

    indices = np.argsort(-filtered_counts)[:3]
    periods_dic =  dict((filtered_unique[idx], filtered_counts[idx]) for idx in indices)
    return list((int(period), count) for period, count in periods_dic.items())


def parseTimezone(val) :
    """Parse timezone UTC+HH:MM to timedelta"""
    val = val.strip("UTC")

    if ":" in val :
        hh, mm = val.split(":")
        hh= int(hh)
        mm = int(mm)
    else :
        hh = int(val)
        mm = 0

    if hh < 0 :
        mm = -mm

    return pd.to_timedelta(60*hh+mm, "min")

def with_auth(url, user, password) :
    parts = urlsplit(url)
    return "%s://%s:%s@%s/%s" % (parts.scheme, quote_plus(user), quote_plus(password), parts.netloc, parts.path)


def fill_str(nc, varname, value) :

    var = nc.variables[varname]

    if var.dtype == str :

        # Variable length string
        var[0] = value
    else:

        dim = var.dimensions[0]
        size = nc.dimensions[dim].size

        # Transform to null terminated fixed length array of chars
        value_ = stringtochar(np.array(value, 'S%d' % size))
        var[:] = value_

def read_str(var) :

    if var.dtype == str :
        # Var length string
        return var[0]

    # Fixed char array
    char_array = var[:]

    # This is a 0D (no dimension) array !
    string_array = chartostring(char_array)

    return string_array[()]

def readSingleVar(var) :
    """Read a meta variable encoded as a single value variable """
    arr = var[:].flatten()
    if len(arr) == 0 :
        return None
    else:
        return arr[0]

def readShortname(ncfile) :
    # Then read the content of the dedicated var
    return read_str(ncfile.variables[STATION_NAME_VAR])

def getMult(attrs, keys):
    """Get value of dict or attribute in NCfile, looking several possbilities"""

    if isinstance(attrs, Dataset) :
        attrs  = dict((attr, getattr(attrs, attr)) for attr in attrs.ncattrs())

    for name in keys:
        if name in attrs:
            return attrs[name]
    return None

def getNetworkId(attributes_or_ncfile) :
    return getMult(attributes_or_ncfile, NETWORK_ID_ATTRS)

def getStationId(attributes_or_ncfile) :
    return getMult(attributes_or_ncfile, STATION_ID_ATTRS)

def _prepare_properties(
        network_properties,
        station_properties) :
    """Prefix properties with Network_ and Station_, and add 'live' properties """

    res = dict(
        **os.environ, # Add env vars
        **{STATION_PREFIX + k: v for k, v in station_properties.items()},
        **{NETWORK_PREFIX + k: v for k, v in network_properties.items()})

    # Add live properties
    now = datetime.now().isoformat()

    res["UpdateTime"] = now
    res["CreationTime"] = now
    res["Version"] = __version__
    return res


def getProperties(network_id, station_id, custom_station_file=None, custom_network_file=None, check_network=True) :
    """Gather Network_ and Station_ properties """

    return _prepare_properties(
        getNetworkInfo(network_id, custom_file=custom_network_file, check=check_network),
        getStationInfo(network_id, station_id, custom_file=custom_station_file))


def qc_masks(df, qc_varname=QC_FLAGS_VAR) :
    """Parse metadata of a QC bitmap and returns dict of flag name => mask"""
    attrs = df.attrs["variables"][qc_varname]
    return {meaning: mask for meaning, mask in zip(
        attrs["flag_meanings"].split(),
        attrs["flag_masks"]
    )}

def parse_bool(value) :
    return value in ["true", "True", "1", "yes", "Yes"]

def parallel_map(fn, iterable, parallel, max_workers=None) :
    """Helper util to map either seuquentially or in parallel """
    if parallel :
        exec = ThreadPoolExecutor(max_workers=max_workers)
        return exec.map(fn, iterable)
    else:
        return map(fn, iterable)

def df_to_csv(df, out=sys.stdout, **args) :
    """Output CSV to stdout"""
    output = StringIO()
    df.to_csv(output, **args)
    output.seek(0)
    out.write(output.read())

def df_to_json(df, out=sys.stdout, **args) :
    """Output CSV to stdout"""
    output = StringIO()
    df.to_json(output, **args)
    output.seek(0)
    out.write(output.read())

class DefaultDict(defaultdict) :
    """Default awnsering 'True' to X in dict """

    def __contains__(self, item):
        return True

def nmin(a, b):
    """Min which returns the other input if one is None"""

    if a is None :
        return b
    elif b is None :
        return a
    else :
        return min(a, b)

def nmax(a, b):
    """Max which returns the other input if one is None"""
    if a is None :
        return b
    elif b is None :
        return a
    else :
        return max(a, b)