# GeoFenceLib/geofence_lib/storage/sqlite_storage.py
import sqlite3

class SQLiteStorage:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS geofences (
                    geofence_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    shape TEXT NOT NULL,
                    coordinates TEXT NOT NULL
                )
            ''')

    def create_geofence(self, geofence_id, name, shape, coordinates):
        with self.connection:
            self.connection.execute('''
                INSERT INTO geofences (geofence_id, name, shape, coordinates)
                VALUES (?, ?, ?, ?)
            ''', (geofence_id, name, shape, str(coordinates)))

    def get_geofences(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM geofences')
        return [{"geofence_id": row[0], "name": row[1], "shape": row[2], "coordinates": eval(row[3])} for row in cursor.fetchall()]

    def get_geofence(self, geofence_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM geofences WHERE geofence_id = ?', (geofence_id,))
        row = cursor.fetchone()
        if row:
            return {"geofence_id": row[0], "name": row[1], "shape": row[2], "coordinates": eval(row[3])}
        return None

    def update_geofence(self, geofence_id, name=None, shape=None, coordinates=None):
        with self.connection:
            if name:
                self.connection.execute('UPDATE geofences SET name = ? WHERE geofence_id = ?', (name, geofence_id))
            if shape:
                self.connection.execute('UPDATE geofences SET shape = ? WHERE geofence_id = ?', (shape, geofence_id))
            if coordinates:
                self.connection.execute('UPDATE geofences SET coordinates = ? WHERE geofence_id = ?', (str(coordinates), geofence_id))

    def delete_geofence(self, geofence_id):
        with self.connection:
            self.connection.execute('DELETE FROM geofences WHERE geofence_id = ?', (geofence_id,))