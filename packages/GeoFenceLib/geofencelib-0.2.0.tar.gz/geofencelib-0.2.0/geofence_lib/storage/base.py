# geofence_lib/storage/base.py
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def create_geofence(self, geofence_id, name, shape, coordinates):
        pass

    @abstractmethod
    def get_geofences(self):
        pass

    @abstractmethod
    def get_geofence(self, geofence_id):
        pass

    @abstractmethod
    def update_geofence(self, geofence_id, name=None, shape=None, coordinates=None):
        pass

    @abstractmethod
    def delete_geofence(self, geofence_id):
        pass