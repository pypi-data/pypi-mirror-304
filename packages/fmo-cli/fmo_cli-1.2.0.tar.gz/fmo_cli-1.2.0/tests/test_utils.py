import pytest
from fmo.utils import geojson_center, get_earliest_timestamp

GEO = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -75.2,
                    38.8
                ]
            },
            "properties": {
                "timestamp": "2024-08-14T22:29:33.641583"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -75.4,
                    38.2
                ]
            },
            "properties": {
                "timestamp": "2024-08-14T22:29:34.641583"
            }
        },
    ]
}

def test_geojson_center():
    center = geojson_center(GEO)
    assert center[0] == pytest.approx(-75.3)
    assert center[1] == pytest.approx(38.5)

def test_earliest_timestamp():
    ts = get_earliest_timestamp(GEO)
    assert ts == "2024-08-14T22:29:33.641583"