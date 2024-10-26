# GeoFenceLib/geofence_lib/core.py
from shapely.geometry import Point, Polygon
import math

class Geofence:
    def __init__(self, geofence_id, name, shape, coordinates):
        self.geofence_id = geofence_id
        self.name = name
        self.shape = shape
        self.coordinates = coordinates

class CircularGeofence:
    def __init__(self, id, name, center, radius):
        self.id = id
        self.name = name
        self.center = center  # Center is a tuple (latitude, longitude)
        self.radius = radius  # Radius in meters

    def contains(self, point):
        """Check if a point is within the circular geofence."""
        lat1, lon1 = self.center  # Center coordinates
        lat2, lon2 = point  # Point to check

        # Calculate distance using the haversine formula
        distance = self.haversine_distance((lat1, lon1), (lat2, lon2))
        radius_km = self.radius / 1000  # Convert radius to kilometers
        return distance <= radius_km

    @staticmethod
    def haversine_distance(coord1, coord2):
        """Calculate the Haversine distance between two points on Earth."""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371.0  # Earth radius in kilometers

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

class PolygonGeofence(Geofence):
    def __init__(self, geofence_id, name, vertices):
        super().__init__(geofence_id, name, 'polygon', vertices)
        self.polygon = Polygon(vertices)

    def contains(self, point):
        return self.polygon.contains(Point(point))