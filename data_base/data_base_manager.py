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
        """Ejecuta una consulta SQL de manera segura"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")

    def create_table(self):
        """Crea la tabla register si no existe"""
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
            print(f"Error al crear la tabla: {e}")

    def register_object(self, date, object_type, object_material, weight, asigned_zone):
        """Registra un objeto en la base de datos"""
        try:
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError("El peso debe ser un número positivo.")
            
            if not isinstance(asigned_zone, int):
                raise ValueError("La zona asignada debe ser un número entero.")
            
            query = '''
            INSERT INTO register (date_registered, object_type, object_material, weight, asigned_zone)
            VALUES (?, ?, ?, ?, ?)
            '''
            self.execute_query(query, (date, object_type, object_material, weight, asigned_zone))
            print("Registro exitoso.")
        except Exception as e:
            print(f"Error al registrar el objeto: {e}")

    def get_all_records(self):
        """Obtiene todos los registros de la tabla"""
        try:
            cursor = self.execute_query("SELECT * FROM register")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar los registros: {e}")
            return []
    def get_records_by_material(self, material):
        try:
            if not isinstance(material, str):
                raise ValueError("El material debe ser una cadena de texto")
            
            material = material.strip().lower()
            if not material:
                raise ValueError("El material no puede estar vacío")
            
            cursor = self.execute_query("SELECT * FROM register WHERE LOWER(object_material) = ?", (material,))
            records = cursor.fetchall()
            
            if not records:
                print(f"No se encontraron registros para el material: {material}")
            return records
        except Exception as e:
            print(f"Error al consultar los registros por material: {e}")
            return []
    def get_records_by_object_type(self, object_type):
        try:
            if not isinstance(object_type, str):
                raise ValueError("El tipo de objeto debe ser una cadena de texto")

            object_type = object_type.strip().lower()
            if not object_type:
                raise ValueError("El tipo de objeto no puede estar vacío")

            cursor = self.execute_query("SELECT * FROM register WHERE LOWER(object_type) = ?", (object_type,))
            records = cursor.fetchall()

            if not records:
                print(f"No se encontraron registros para el tipo de objeto: {object_type}")
            return records
        except Exception as e:
            print(f"Error al consultar los registros por tipo de objeto: {e}")
            return []
    def get_records_by_asigined_area(self, asigned_area):
        try:
            if not isinstance(asigned_area, int):
                raise ValueError("El área asignada debe ser un número entero")

            asigned_area = int(asigned_area)
            if asigned_area <= 0:
                raise ValueError("El área asignada debe ser un número positivo")

            cursor = self.execute_query("SELECT * FROM register WHERE asigned_zone =?", (asigned_area,))
            records = cursor.fetchall()

            if not records:
                print(f"No se encontraron registros para el área asignada: {asigned_area}")
            return records
        except Exception as e:
            print(f"Error al consultar los registros por área asignada: {e}")
            return []
    def close(self):
        if self.conn:
            self.conn.close()
    def get_objects_types(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT object_type FROM register")
            object_types = cursor.fetchall()
            return [object_type[0] for object_type in object_types]
        except Exception as e:
            print(f"Error al obtener los tipos de objetos: {e}")
            return []
    def get_assined_area(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT asigned_zone FROM register")
            assined_areas = cursor.fetchall()
            area = [assined_area[0] for assined_area in assined_areas]
            area.sort()
            return area
        except Exception as e:
            print(f"Error al obtener las áreas asignadas: {e}")
            return []
    def get_objects_materials(self):
        try:
            cursor = self.execute_query("SELECT DISTINCT object_material FROM register")
            object_materials = cursor.fetchall()
            return [object_material[0] for object_material in object_materials]
        except Exception as e:
            print(f"Error al obtener los materiales de los objetos: {e}")
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