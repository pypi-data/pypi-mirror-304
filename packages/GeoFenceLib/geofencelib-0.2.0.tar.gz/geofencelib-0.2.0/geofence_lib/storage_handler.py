# GeoFenceLib/geofence_lib/storage_handler.py
from .storage.sqlite_storage import SQLiteStorage
from .storage.json_storage import JSONStorage

class StorageHandler:
    def __init__(self, storage_type="json", db_name="geofence_data.db", json_file="geofence_data.json"):
        self.storage = None
        if storage_type == "sqlite":
            self.storage = SQLiteStorage(db_name)
        elif storage_type == "json":
            self.storage = JSONStorage(json_file)
        else:
            raise ValueError("Unsupported storage type. Use 'sqlite' or 'json'.")

    def create_geofence(self, geofence_id, name, shape, coordinates):
        self.storage.create_geofence(geofence_id, name, shape, coordinates)

    def get_geofences(self):
        return self.storage.get_geofences()

    def get_geofence(self, geofence_id):
        return self.storage.get_geofence(geofence_id)

    def update_geofence(self, geofence_id, name=None, shape=None, coordinates=None):
        self.storage.update_geofence(geofence_id, name, shape, coordinates)

    def delete_geofence(self, geofence_id):
        self.storage.delete_geofence(geofence_id)