import sqlite3
import datetime
import os

class DataBaseConnector:
    def __init__(self, db_path='./data_base/reports_trash_recolected.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")

    def create_table(self):
        """Crea la tabla register si no existe"""
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_registered TIMESTAMP NOT NULL,
                object_type TEXT NOT NULL,
                weight INTEGER NOT NULL,
                asigned_zone INTEGER NOT NULL
            )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Error al crear la tabla: {e}")

    def register_object(self, date, object_type, weight, asigned_zone):
        """Registra un objeto en la base de datos"""
        try:
            # Validar que el peso sea un número positivo
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError("El peso debe ser un número positivo.")
            
            # Validar que la zona asignada sea un entero
            if not isinstance(asigned_zone, int):
                raise ValueError("La zona asignada debe ser un número entero.")
            
            # Insertar los datos en la tabla
            self.cursor.execute('''
            INSERT INTO register (date_registered, object_type, weight, asigned_zone)
            VALUES (?, ?, ?, ?)
            ''', (date, object_type, weight, asigned_zone))
            
            self.conn.commit()
            print("Registro exitoso.")
        except Exception as e:
            print(f"Error al registrar el objeto: {e}")

    def get_all_records(self):
        """Obtiene todos los registros de la tabla"""
        try:
            self.cursor.execute("SELECT * FROM register")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar los registros: {e}")
            return []

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    db = DataBaseConnector()
    
    # Registrar un objeto
    db.register_object(datetime.datetime.now(), "Can", 2, 3)
    
    # Obtener todos los registros
    records = db.get_all_records()
    print("\nRegistros en la tabla:")
    for record in records:
        print(record)
    
    # Cerrar la conexión
    db.close()