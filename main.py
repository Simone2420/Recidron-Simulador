import os
import platform
import subprocess
import sys
from time import sleep
from install_dependencies import *
from web_raiser import *


def run_simulator():
    """Runs the simulator."""
    print("Starting the simulator...")
    python_path = os.path.join(".venv", "Scripts" if platform.system() == "Windows" else "bin", "python")
    subprocess.run(
        [python_path, "simulator.py"],
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