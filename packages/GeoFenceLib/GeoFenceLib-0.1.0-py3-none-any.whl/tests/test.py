from geofence_lib.core import CircularGeofence, PolygonGeofence
from geofence_lib.manager import GeofenceManager

# Define geofences
circular_geofence = CircularGeofence(1, "Office", (40.7128, -74.0060), 100)
polygon_geofence = PolygonGeofence(2, "Park", [(40.7127, -74.0061), (40.7128, -74.0059), (40.7130, -74.0061), (40.7129, -74.0063)])

# Initialize manager
manager = GeofenceManager([circular_geofence, polygon_geofence])

# Event handling
def on_geofence_event(event_data):
    print(f"Event: {event_data['event']} for user {event_data['user_id']} in geofence {event_data['geofence']}")

manager.subscribe_to_events(on_geofence_event)

# Check position
manager.check_position(user_id=101, point=(40.7129, -74.0060))