# tests/test_manager.py
from geofence_lib.core import CircularGeofence
from geofence_lib.manager import GeofenceManager

def test_geofence_entry_exit():
    geofence = CircularGeofence(1, "TestCircle", (40.7128, -74.0060), 100)
    manager = GeofenceManager([geofence])

    # Track triggered events
    events_triggered = []

    # Define callback function for tracking events
    def event_callback(event_data):
        events_triggered.append(event_data)

    # Subscribe to events
    manager.subscribe_to_events(event_callback)

    # Simulate user movement
    manager.check_position(user_id=101, point=(40.7128, -74.0060))  # Entry
    manager.check_position(user_id=101, point=(40.7138, -74.0160))  # Exit

    # Check results
    assert len(events_triggered) == 2, "Expected two events: entry and exit"
    assert events_triggered[0]["event"] == "entry"
    assert events_triggered[1]["event"] == "exit"