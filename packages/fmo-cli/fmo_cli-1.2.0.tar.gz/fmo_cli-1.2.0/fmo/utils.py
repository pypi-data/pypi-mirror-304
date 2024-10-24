from typing import Tuple
import geojson
import geojson.utils
import numpy as np
from datetime import datetime


def geojson_center(geo) -> Tuple[float, float]:
    """Return the center of the geojson feature (lng, lat)"""
    coords = geojson.utils.coords(geo)
    coords = np.array(list(coords))
    return np.mean(coords, axis=0).tolist()


def get_earliest_timestamp(geojson_data):
    timestamps = [
        feature["properties"]["timestamp"]
        for feature in geojson_data["features"]
        if "timestamp" in feature["properties"]
    ]

    # Convert timestamps to datetime objects and find the earliest one
    datetime_objects = [datetime.fromisoformat(ts) for ts in timestamps]
    earliest_timestamp = min(datetime_objects)

    return earliest_timestamp.isoformat()
