from pkgutil import extend_path
import os
import ee
from enum import Enum
from hestia_earth.utils.tools import current_time_ms

from .log import logger
from .boundary import run as run_boundary, get_size_km2 as get_size_km2_boundary
from .coordinates import run as run_coordinates
from .gadm import run as run_gadm, get_size_km2 as get_size_km2_gadm

__path__ = extend_path(__path__, __name__)

EE_ACCOUNT_ID = os.getenv('EARTH_ENGINE_ACCOUNT_ID')
EE_KEY_FILE = os.getenv('EARTH_ENGINE_KEY_FILE', 'ee-credentials.json')


def init_gee():
    now = current_time_ms()
    logger.debug(f"initializing ee using {EE_KEY_FILE}...")
    ee.Initialize(ee.ServiceAccountCredentials(EE_ACCOUNT_ID, EE_KEY_FILE))
    logger.debug(f"done initializing ee in {current_time_ms() - now} ms")


class RunType(Enum):
    BOUNDARY = 'boundary'
    COORDINATES = 'coordinates'
    GADM = 'gadm'


SIZE_KM2_BY_TYPE = {
    RunType.BOUNDARY: lambda v: get_size_km2_boundary(v),
    RunType.COORDINATES: lambda _v: None,
    RunType.GADM: lambda v: get_size_km2_gadm(v)
}


RUN_BY_TYPE = {
    RunType.BOUNDARY: lambda v: run_boundary(v),
    RunType.COORDINATES: lambda v: run_coordinates(v),
    RunType.GADM: lambda v: run_gadm(v)
}


def _get_run_type(data: dict):
    if data.get('latitude') and data.get('longitude'):
        return RunType.COORDINATES
    if data.get('boundary'):
        return RunType.BOUNDARY
    if data.get('gadm_id') or data.get('gadm-id'):
        return RunType.GADM
    raise Exception('Unkown type. Please set either a latitude and longitude, a boundary or gadm_id param.')


def get_size_km2(data: dict) -> float:
    """
    Get the size in km2 based on the data. Will not work on coordinates (latitude, longitude).

    Parameters
    ----------
    data : dict
        The parameters needed to run the queries.

    Returns
    -------
    float
        The size of the boundary or gadm region ID in km2.
    """
    return SIZE_KM2_BY_TYPE.get(_get_run_type(data), lambda v: v)(data)


def run(data: dict):
    """
    Run query against Google Earth Engine.
    This is specifically designed to work along the Hestia Engine Models library.

    Parameters
    ----------
    data : dict
        The parameters needed to run the queries.

    Returns
    -------
    dict
        The result from Earth Engine query.
    """
    now = current_time_ms()
    result = RUN_BY_TYPE.get(_get_run_type(data), lambda v: v)(data)
    logger.info('time=%s, unit=ms', current_time_ms() - now)
    return result
