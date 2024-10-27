from typing import List, Tuple, Union
from shapes.circle import Circle
from shapes.polygon import Polygon

class GeofenceManager:
    def __init__(self):
        self.geofences = {}

    def add_geofence(self, geofence_id: str, shape: Union[Circle, Polygon]):
        self.geofences[geofence_id] = shape

    def check_point(self, point: Tuple[float, float]) -> List[str]:
        return [
            geofence_id for geofence_id, shape in self.geofences.items()
            if shape.contains(point)
        ]
