import os
import subprocess
import sys
from .misc import is_subdirectory


def run_python_file(working_directory, file_path, args=[]):
    if not is_subdirectory(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if file_path[-2:] != 'py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cp = subprocess.run([sys.executable, file_path] + args, cwd=os.path.realpath(working_directory),
            capture_output=True, timeout=30, text=True)
        result = ""
        if cp.stdout is not None:
            result += f"STDOUT: {cp.stdout}"  
        if cp.stderr is not None:
            result += f"STDERR: {cp.stderr}"
        if (cp.stdout is None) and (cp.stderr is None):
            result += "No output produced."
        return_code = cp.returncode
        if return_code != 0:
            result += f"\nProcess exited with code {return_code}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

