import subprocess
import sys
import os

def run(command, cwd):
    # On Windows, use 'start' to open a new terminal window
    if sys.platform == "win32":
        subprocess.Popen(f'start cmd /k "{command}"', cwd=cwd, shell=True)
    else:
        # On Unix, use x-terminal-emulator or gnome-terminal, etc.
        subprocess.Popen(['x-terminal-emulator', '-e', command], cwd=cwd)

# BACKEND/APIs
run("python run_api.py", "APP_ONE")
run("uvicorn receive_results_api:app --host 0.0.0.0 --port 8003 --reload", "APP_ONE")
run("uvicorn mcp_resource_api:app --host 0.0.0.0 --port 8004 --reload", "APP_ONE")
run("python run_api.py", "APP_TWO")

# UIs
run("streamlit run app_one_main.py", "APP_ONE")
run("streamlit run app_two_main.py", "APP_TWO")