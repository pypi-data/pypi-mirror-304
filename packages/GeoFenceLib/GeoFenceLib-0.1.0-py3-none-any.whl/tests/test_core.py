# tests/test_core.py
import pytest
from geofence_lib.core import CircularGeofence, PolygonGeofence

def test_circular_geofence_contains_point():
    geofence = CircularGeofence(1, "TestCircle", (40.7128, -74.0060), 100)
    point_inside = (40.7128, -74.0061)
    point_outside = (40.7138, -74.0160)

    assert geofence.contains(point_inside) is True, "Point should be inside the circular geofence"
    assert geofence.contains(point_outside) is False, "Point should be outside the circular geofence"

def test_polygon_geofence_contains_point():
    geofence = PolygonGeofence(2, "TestPolygon", [(40.7127, -74.0061), (40.7128, -74.0059), (40.7130, -74.0061), (40.7129, -74.0063)])
    point_inside = (40.7129, -74.0060)
    point_outside = (40.7135, -74.0070)

    assert geofence.contains(point_inside) is True, "Point should be inside the polygon geofence"
    assert geofence.contains(point_outside) is False, "Point should be outside the polygon geofence"