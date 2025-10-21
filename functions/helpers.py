import os
import subprocess
import sys

class Helpers:
    MAX_CHARS = 10000

    @classmethod
    def is_subdirectory(cls, parent, path):
        try:
            parent_path = os.path.realpath(parent)
            target_path = os.path.realpath(os.path.join(parent_path, path))
            return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, target_path])
        except ValueError:
            # Happens if paths are on different drives (Windows)
            return False

    
    @classmethod
    def get_files_info(cls, working_directory, directory="."):
        path = os.path.join(working_directory, directory)
        if not os.path.isdir(path):
            return f'    Error: "{directory}" is not a directory'

        if cls.is_subdirectory(working_directory, directory):
            base = "current" if directory == "." else f"'{directory}'"
            all_things = os.listdir(path)
            info = [
                f" - {thing}: file_size={os.path.getsize(os.path.join(path, thing))} bytes, is_dir={os.path.isdir(os.path.join(path, thing))}"
                for thing in all_things
            ]
            return f"Result for {base} directory:\n" + '\n'.join(info)

        return f"Result for {directory} directory:\n    Error: Cannot list \"{directory}\" as it is outside the permitted working directory"


    @classmethod
    def get_file_content(cls, working_directory, file_path):
        full_path = os.path.realpath(os.path.join(working_directory, file_path))

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not cls.is_subdirectory(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(full_path, "r") as f:
            file_content_string = f.read(Helpers.MAX_CHARS)
            if len(file_content_string) == Helpers.MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {Helpers.MAX_CHARS} characters]'
            return file_content_string


    @classmethod
    def write_file(cls, working_directory, file_path, content):
        if not cls.is_subdirectory(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        parent_path = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(parent_path, file_path))
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        try:
            with open(target_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except PermissionError: 
            return f'Error: Lack of write permissions prevents writing to "{file_path}"'
        except (IOError, OSError) as e:
            return f'Error: Cannot write to "{file_path}" - {e.message}'


    @classmethod
    def run_python_file(cls, working_directory, file_path, args=[]):
        if not cls.is_subdirectory(working_directory, file_path):
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
