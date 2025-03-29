import sqlite3
import datetime
import os

# Conectar a la base de datos (se creará un archivo llamado 'reports_trash_recolected.db' en la misma carpeta)
conn = sqlite3.connect('./data_base/reports_trash_recolected.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear una tabla llamada 'register' con algunas columnas básicas
cursor.execute('''
CREATE TABLE IF NOT EXISTS register (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_registered TIMESTAMP NOT NULL,
    object_type TEXT NOT NULL,
    weight INTEGER NOT NULL,
    asigned_zone INTEGER NOT NULL
)
''')

# Función para registrar un objeto en la base de datos
def register_object(date, object_type, weight, asigned_zone):
    try:
        # Validar que el peso sea un número positivo
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("El peso debe ser un número positivo.")
        
        # Validar que la zona asignada sea un entero
        if not isinstance(asigned_zone, int):
            raise ValueError("La zona asignada debe ser un número entero.")
        
        # Insertar los datos en la tabla usando parámetros para evitar inyecciones SQL
        cursor.execute('''
        INSERT INTO register (date_registered, object_type, weight, asigned_zone)
        VALUES (?, ?, ?, ?)
        ''', (date, object_type, weight, asigned_zone))
        
        # Guardar los cambios en la base de datos
        conn.commit()
        print("Registro exitoso.")
    except Exception as e:
        print(f"Error al registrar el objeto: {e}")

# Ejemplo de uso de la función
register_object(datetime.datetime.now(), "Can", 2, 3)

# Consultar todos los registros en la tabla
try:
    cursor.execute("SELECT * FROM register")
    resultados = cursor.fetchall()
    
    # Imprimir los resultados
    print("\nRegistros en la tabla:")
    for fila in resultados:
        print(fila)
except Exception as e:
    print(f"Error al consultar los registros: {e}")

# Cerrar la conexión a la base de datos
conn.close()