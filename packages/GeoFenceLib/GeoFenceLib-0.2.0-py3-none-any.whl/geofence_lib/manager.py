# GeoFenceLib/geofence_lib/manager.py
from .events import GeofenceEvent
from .storage_handler import StorageHandler

class UserGeofenceStatus:
    def __init__(self):
        self.status = {}

    def update_status(self, user_id, geofence_id, is_inside):
        if user_id not in self.status:
            self.status[user_id] = {}
        self.status[user_id][geofence_id] = is_inside

    def get_status(self, user_id, geofence_id):
        return self.status.get(user_id, {}).get(geofence_id, False)

class GeofenceManager:
    def __init__(self, storage_type="json", db_name="geofence_data.db", json_file="geofence_data.json"):
        self.storage_handler = StorageHandler(storage_type, db_name, json_file)
        self.geofences = self.storage_handler.get_geofences()  # Load existing geofences
        self.user_states = {}  # Track user states within geofences
        self.subscribers = []

    def subscribe_to_events(self, callback):
        """Allow functions to subscribe to geofence events."""
        self.subscribers.append(callback)

    def create_geofence(self, geofence_id, name, shape, coordinates):
        self.storage_handler.create_geofence(geofence_id, name, shape, coordinates)
        self.geofences.append(self.storage_handler.get_geofence(geofence_id))  # Update local cache
        event_data = {"event": "created", "geofence": name, "geofence_id": geofence_id}
        self._notify_subscribers(event_data)

    def get_geofences(self):
        return self.geofences

    def get_geofence(self, geofence_id):
        return self.storage_handler.get_geofence(geofence_id)

    def update_geofence(self, geofence_id, name=None, shape=None, coordinates=None):
        self.storage_handler.update_geofence(geofence_id, name, shape, coordinates)
        updated_geofence = self.storage_handler.get_geofence(geofence_id)
        event_data = {"event": "updated", "geofence": updated_geofence.name, "geofence_id": geofence_id}
        self._notify_subscribers(event_data)

    def delete_geofence(self, geofence_id):
        self.storage_handler.delete_geofence(geofence_id)
        self.geofences = [gf for gf in self.geofences if gf.geofence_id != geofence_id]  # Update local cache
        event_data = {"event": "deleted", "geofence_id": geofence_id}
        self._notify_subscribers(event_data)

    def check_position(self, user_id, point):
        """Check and trigger entry/exit events based on user position."""
        for geofence in self.geofences:
            is_within = geofence.contains(point)
            user_in_geofence = self.user_states.get(user_id, {}).get(geofence.geofence_id, False)

            if is_within and not user_in_geofence:
                # Entry event
                self.user_states.setdefault(user_id, {})[geofence.geofence_id] = True
                event_data = {"event": "entry", "geofence": geofence.name, "user_id": user_id}
                self._notify_subscribers(event_data)
            elif not is_within and user_in_geofence:
                # Exit event
                self.user_states[user_id][geofence.geofence_id] = False
                event_data = {"event": "exit", "geofence": geofence.name, "user_id": user_id}
                self._notify_subscribers(event_data)

    def _notify_subscribers(self, event_data):
        """Notify all subscribers with event data."""
        for callback in self.subscribers:
            callback(event_data)