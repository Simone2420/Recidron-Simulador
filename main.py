import os
import platform
import subprocess
import sys
from time import sleep

def check_permissions():
    """Verifica que el usuario tenga permisos de escritura en el directorio actual."""
    current_dir = os.getcwd()
    if not os.access(current_dir, os.W_OK):
        print(f"No tienes permisos de escritura en el directorio: {current_dir}")
        print("Por favor, ejecuta el script en un directorio donde tengas permisos.")
        sys.exit(1)
    print("Permisos de escritura verificados.")

def create_hidden_virtualenv():
    """Crea un entorno virtual oculto (.venv) si no existe."""
    if not os.path.exists(".venv"):
        print("Creando entorno virtual oculto (.venv)...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        print("Entorno virtual oculto creado.")
    else:
        print("El entorno virtual oculto (.venv) ya existe.")

def are_dependencies_installed():
    """Verifica si todas las dependencias en requirements.txt están instaladas."""
    if not os.path.exists("requirements.txt"):
        print("No se encontró el archivo 'requirements.txt'.")
        sys.exit(1)

    print("Verificando dependencias instaladas...")
    pip_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "pip")

    # Obtener las dependencias instaladas en el entorno virtual
    result = subprocess.run(
        [pip_path, "freeze"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    installed_packages = {line.split("==")[0].lower(): line.split("==")[1] for line in result.stdout.splitlines()}

    # Leer las dependencias requeridas desde requirements.txt
    with open("requirements.txt", "r") as f:
        required_packages = {}
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignorar comentarios y líneas vacías
                package, version = line.split("==") if "==" in line else (line, None)
                required_packages[package.lower()] = version

    # Verificar si todas las dependencias requeridas están instaladas
    for package, version in required_packages.items():
        if package not in installed_packages:
            print(f"Falta la dependencia: {package}")
            return False
        if version and installed_packages[package] != version:
            print(f"Versión incorrecta para {package}. Requerida: {version}, Instalada: {installed_packages[package]}")
            return False

    print("Todas las dependencias están instaladas.")
    return True

def install_dependencies():
    """Instala las dependencias desde requirements.txt si no están instaladas."""
    if are_dependencies_installed():
        print("No es necesario instalar dependencias.")
        return

    print("Instalando dependencias desde requirements.txt...")
    pip_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencias instaladas.")
    
def run_reflex_app():
    """Ejecuta la aplicación Reflex."""
    print("Iniciando la aplicación Reflex...")
    subprocess.Popen(
        ["reflex", "run"],
    )
    


def main():
    """Función principal para automatizar el proceso."""
    try:
        # Paso 0: Verificar permisos
        check_permissions()

        # Paso 1: Crear entorno virtual oculto
        create_hidden_virtualenv()

        # Paso 2: Instalar dependencias
        install_dependencies()

        # Paso 3: Ejecutar la aplicación Reflex
        run_reflex_app()


    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
    except PermissionError as e:
        print("Error de permisos:")
        print(e)
        print("Por favor, asegúrate de tener permisos de escritura en el directorio actual.")
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()