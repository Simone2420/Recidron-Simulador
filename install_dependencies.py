import os
import platform
import subprocess
import sys
from time import sleep
def check_permissions():
    """Verifies that the user has write permissions in the current directory."""
    current_dir = os.getcwd()
    if not os.access(current_dir, os.W_OK):
        print(f"You don't have write permissions in the directory: {current_dir}")
        print("Please run the script in a directory where you have permissions.")
        sys.exit(1)
    print("Write permissions verified.")


def create_hidden_virtualenv():
    """Creates a hidden virtual environment (.venv) if it doesn't exist and ensures pip is installed."""
    if not os.path.exists(".venv"):
        print("Creating hidden virtual environment (.venv)...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        print("Hidden virtual environment created.")
        
        # Ensure pip is installed and updated
        python_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "python")
        print("Installing and updating pip...")
        subprocess.run([python_path, "-m", "ensurepip", "--upgrade"])
        subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"])
        print("Pip installed and updated.")
    else:
        print("Hidden virtual environment (.venv) already exists.")


def are_dependencies_installed():
    """Verifies if all dependencies in requirements.txt are installed."""
    if not os.path.exists("requirements.txt"):
        print("requirements.txt file not found.")
        sys.exit(1)

    print("Verifying installed dependencies...")
    pip_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "pip")

    # Get installed dependencies in virtual environment
    result = subprocess.run(
        [pip_path, "freeze"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    installed_packages = {line.split("==")[0].lower(): line.split("==")[1] for line in result.stdout.splitlines()}

    # Read required dependencies from requirements.txt
    with open("requirements.txt", "r") as f:
        required_packages = {}
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore comments and empty lines
                package, version = line.split("==") if "==" in line else (line, None)
                required_packages[package.lower()] = version

    # Verify if all required dependencies are installed
    for package, version in required_packages.items():
        if package not in installed_packages:
            print(f"Missing dependency: {package}")
            return False
        if version and installed_packages[package] != version:
            print(f"Incorrect version for {package}. Required: {version}, Installed: {installed_packages[package]}")
            return False

    print("All dependencies are installed.")
    return True


def install_dependencies():
    """Installs dependencies from requirements.txt if not installed."""
    if are_dependencies_installed():
        print("No need to install dependencies.")
        return

    print("Installing dependencies from requirements.txt...")
    pip_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencies installed.")
if __name__ == "__main__":
    check_permissions()
    create_hidden_virtualenv()
    install_dependencies()