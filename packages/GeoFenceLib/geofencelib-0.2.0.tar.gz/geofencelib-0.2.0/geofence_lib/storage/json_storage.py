# GeoFenceLib/geofence_lib/storage/json_storage.py
import json
import os

class JSONStorage:
    def __init__(self, json_file):
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump([], f)  # Initialize with an empty list

    def create_geofence(self, geofence_id, name, shape, coordinates):
        geofences = self.get_geofences()
        geofences.append({
            "geofence_id": geofence_id,
            "name": name,
            "shape": shape,
            "coordinates": coordinates
        })
        self._save(geofences)

    def get_geofences(self):
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def get_geofence(self, geofence_id):
        geofences = self.get_geofences()
        for gf in geofences:
            if gf['geofence_id'] == geofence_id:
                return gf
        return None

    def update_geofence(self, geofence_id, name=None, shape=None, coordinates=None):
        geofences = self.get_geofences()
        for gf in geofences:
            if gf['geofence_id'] == geofence_id:
                if name is not None:
                    gf['name'] = name
                if shape is not None:
                    gf['shape'] = shape
                if coordinates is not None:
                    gf['coordinates'] = coordinates
                break
        self._save(geofences)

    def delete_geofence(self, geofence_id):
        geofences = self.get_geofences()
        geofences = [gf for gf in geofences if gf['geofence_id'] != geofence_id]
        self._save(geofences)

    def _save(self, geofences):
        with open(self.json_file, 'w') as f:
            json.dump(geofences, f, indent=4)