import os
from .misc import is_subdirectory


def write_file_content(working_directory, file_path, content):
    if not is_subdirectory(working_directory, file_path):
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

