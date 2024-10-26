# GeoFenceLib/geofence_lib/events.py
class GeofenceEvent:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        """Subscribe to an event with a callback function."""
        self.subscribers.append(callback)

    def trigger(self, event_data):
        for callback in self.subscribers:
            callback(event_data)