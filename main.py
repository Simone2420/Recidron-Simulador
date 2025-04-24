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

def run_simulator():
    """Runs the simulator."""
    print("Starting the simulator...")
    python_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "python")
    subprocess.run(
        [python_path, "simulator.py"],
    )

def run_reflex_app():
    """Runs the Reflex application."""
    print("Starting the Reflex application...")
    if platform.system() == "Windows":
        reflex_path = os.path.join(".venv", "Scripts", "reflex.exe")
        subprocess.Popen(
        [reflex_path, "run"],
        shell=True
    )
        if not os.path.exists(reflex_path):
            print("Reflex executable not found in virtual environment.")
            sys.exit(1)
    else:
        activate_script = os.path.join(".venv", "bin", "activate")
        if not os.path.exists(activate_script):
            print("Virtual environment activation script not found.")
            sys.exit(1)
            
        activate_cmd = f"source {activate_script} && reflex run"
        subprocess.run(
            [activate_cmd],
            shell=True,
            executable="/bin/bash"
        )

def main():
    """Main function to automate the process."""
    try:
        check_permissions()
        create_hidden_virtualenv()
        install_dependencies()
        run_simulator()
        run_reflex_app()

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except PermissionError as e:
        print("Permission error:")
        print(e)
        print("Please make sure you have write permissions in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()