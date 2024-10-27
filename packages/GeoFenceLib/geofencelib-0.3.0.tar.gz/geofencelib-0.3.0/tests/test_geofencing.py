import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from geofence_lib.shapes.circle import Circle
from geofence_lib.shapes.polygon import Polygon


class TestGeofencingShapes(unittest.TestCase):
    
    def test_circle_contains(self):
        # Create a circle centered at (37.7749, -122.4194) with a radius of 500 meters
        circle = Circle(center=(37.7749, -122.4194), radius=500)
        
        # Test point inside the circle
        point_inside = (37.7750, -122.4195)
        self.assertTrue(circle.contains(point_inside), "Point should be inside the circle")

        # Test point outside the circle
        point_outside = (37.7799, -122.4295)
        self.assertFalse(circle.contains(point_outside), "Point should be outside the circle")

    def test_polygon_contains(self):
        # Define a polygon with vertices in a roughly rectangular shape
        vertices = [
            (37.7749, -122.4194),  # Bottom-left
            (37.7749, -122.4144),  # Bottom-right
            (37.7799, -122.4144),  # Top-right
            (37.7799, -122.4194)   # Top-left
        ]
        polygon = Polygon(vertices=vertices)

        # Test point inside the polygon
        point_inside = (37.7770, -122.4160)
        self.assertTrue(polygon.contains(point_inside), "Point should be inside the polygon")

        # Test point outside the polygon
        point_outside = (37.7805, -122.4130)
        self.assertFalse(polygon.contains(point_outside), "Point should be outside the polygon")

        # Test point on the boundary
        point_on_boundary = (37.7749, -122.4170)
        self.assertTrue(polygon.contains(point_on_boundary), "Point on boundary should be considered inside the polygon")

if __name__ == "__main__":
    unittest.main()
