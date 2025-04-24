import os
import platform
import subprocess
import sys
from time import sleep
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
if __name__ == "__main__":
    run_reflex_app()