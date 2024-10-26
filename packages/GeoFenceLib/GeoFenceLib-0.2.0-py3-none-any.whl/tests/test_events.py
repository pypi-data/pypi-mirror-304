# tests/test_events.py
from geofence_lib.events import GeofenceEvent

def test_event_subscription_and_trigger():
    event = GeofenceEvent()
    triggered_data = []

    def mock_callback(data):
        triggered_data.append(data)

    event.subscribe(mock_callback)
    event_data = {"event": "entry", "user_id": 101, "geofence": "TestGeofence"}
    event.trigger(event_data)

    assert len(triggered_data) == 1, "Callback should be triggered once"
    assert triggered_data[0] == event_data, "Event data should match the triggered data"