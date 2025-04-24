import sqlite3
import datetime
import os
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
class DataBaseConnector:
    def __init__(self, db_path='./data_base/reports_trash_recolected.db'):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            self.conn.close()

    def execute_query(self, query, params=None):
        """Execute SQL query safely"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(f"Error executing query: {e}")

    def create_table(self):
        """Create register table if it doesn't exist"""
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_registered TIMESTAMP NOT NULL,
                object_type TEXT NOT NULL,
                object_material TEXT NOT NULL,
                weight INTEGER NOT NULL,
                asigned_zone INTEGER NOT NULL
            )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def register_object(self, date, object_type, object_material, weight, asigned_zone):
        """Register an object in the database"""
        try:
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError("Weight must be a positive number.")
            
            if not isinstance(asigned_zone, int):
                raise ValueError("Assigned zone must be an integer.")
            
            query = '''
            INSERT INTO register (date_registered, object_type, object_material, weight, asigned_zone)
            VALUES (?, ?, ?, ?, ?)
            '''
            self.execute_query(query, (date, object_type, object_material, weight, asigned_zone))
            print("Registration successful.")
        except Exception as e:
            print(f"Error registering object: {e}")

    def get_all_records(self):
        """Get all records from the table"""
        try:
            cursor = self.execute_query("SELECT * FROM register")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error querying records: {e}")
            return []

    def get_records_by_material(self, material):
        try:
            if not isinstance(material, str):
                raise ValueError("Material must be a text string")
            
            material = material.strip().lower()
            if not material:
                raise ValueError("Material cannot be empty")
            
            cursor = self.execute_query("SELECT * FROM register WHERE LOWER(object_material) = ?", (material,))
            records = cursor.fetchall()
            
            if not records:
                print(f"No records found for material: {material}")
            return records
        except Exception as e:
            print(f"Error querying records by material: {e}")
            return []

    def get_records_by_object_type(self, object_type):
        try:
            if not isinstance(object_type, str):
                raise ValueError("Object type must be a text string")

            object_type = object_type.strip().lower()
            if not object_type:
                raise ValueError("Object type cannot be empty")

            cursor = self.execute_query("SELECT * FROM register WHERE LOWER(object_type) = ?", (object_type,))
            records = cursor.fetchall()

            if not records:
                print(f"No records found for object type: {object_type}")
            return records
        except Exception as e:
            print(f"Error querying records by object type: {e}")
            return []

    def get_records_by_asigined_area(self, asigned_area):
        try:
            if not isinstance(asigned_area, int):
                raise ValueError("Assigned area must be an integer")

            asigned_area = int(asigned_area)
            if asigned_area <= 0:
                raise ValueError("Assigned area must be a positive number")

            cursor = self.execute_query("SELECT * FROM register WHERE asigned_zone =?", (asigned_area,))
            records = cursor.fetchall()

            if not records:
                print(f"No records found for assigned area: {asigned_area}")
            return records
        except Exception as e:
            print(f"Error querying records by assigned area: {e}")
            return []

    def get_objects_types(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT object_type FROM register")
            object_types = cursor.fetchall()
            return [object_type[0] for object_type in object_types]
        except Exception as e:
            print(f"Error getting object types: {e}")
            return []

    def get_assined_area(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT asigned_zone FROM register")
            assined_areas = cursor.fetchall()
            area = [assined_area[0] for assined_area in assined_areas]
            area.sort()
            return area
        except Exception as e:
            print(f"Error getting assigned areas: {e}")
            return []

    def get_objects_materials(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT object_material FROM register")
            object_materials = cursor.fetchall()
            return [object_material[0] for object_material in object_materials]
        except Exception as e:
            print(f"Error getting object materials: {e}")
            return []
# Ejemplo de uso
if __name__ == "__main__":
    db = DataBaseConnector()
    
    db.register_object(datetime.datetime.now(), "can","metal", 2, 3)
    db.register_object(datetime.datetime.now(), "bottle","plastic", 1, 2)
    db.register_object(datetime.datetime.now(), "plastic_cup","plastic", 1, 2)
    db.register_object(datetime.datetime.now(), "can","metal", 2, 3)
    db.register_object(datetime.datetime.now(), "bottle","plastic", 1, 2)
    # Obtener todos los registros
    records = db.get_all_records()
    record_plastic = db.get_records_by_material("plastic")
    print("\nRegistros en la tabla:")
    for record in records:
        print(record)
    print("\n")
    for record in record_plastic:
        print(record)
    # Cerrar la conexión
    db.close()