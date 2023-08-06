import ee

from hestia_earth.earth_engine.utils import get_required_param
from hestia_earth.earth_engine.gee_utils import load_region, area_km2
from hestia_earth.earth_engine.coordinates import _load_single as load_coordinates
from .utils import load


def _load_single(geometry, data: dict):
    collection = get_required_param(data, 'collection')
    ee_type = get_required_param(data, 'ee_type')
    return load(collection, ee_type, geometry, data)


def _load_region(geometry, data: dict):
    collections = data.get('collections', [])
    return [
        _load_single(geometry, v) for v in collections
    ] if len(collections) > 0 else _load_single(geometry, data)


def _load_centroid(point, data: dict):
    collections = data.get('collections', [])
    return [
        load_coordinates(point, v) for v in collections
    ] if len(collections) > 0 else load_coordinates(point, data)


def _get_region(data: dict):
    # required params
    try:
        gadm_id = get_required_param(data, 'gadm_id')
    except Exception:
        gadm_id = get_required_param(data, 'gadm-id')

    return load_region(gadm_id)


def get_size_km2(data):
    region = load_region(data) if isinstance(data, str) else _get_region(data)
    return area_km2(region.geometry()).getInfo()


def get_distance_to_coordinates(gadm_id: str, latitude: float, longitude: float):
    """
    Returns the distance between the coordinates and the GADM region, in meters.
    """
    region = load_region(gadm_id)
    coordinates = ee.Geometry.Point(longitude, latitude)
    return region.geometry().distance(coordinates).getInfo()


def run(data: dict):
    region = _get_region(data)
    use_centroid = str(data.get('centroid', 'false')).lower() == 'true'
    return _load_centroid(region.geometry().centroid(), data) if use_centroid else _load_region(region, data)
