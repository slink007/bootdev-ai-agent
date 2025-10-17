import os

MAX_CHARS = 10000

def is_subdirectory(parent, path):
    """
    Check if 'path' is a subdirectory (or file within a subdirectory) of 'parent'.
    Uses real absolute paths for safety.
    """
    try:
        parent_path = os.path.realpath(parent)
        target_path = os.path.realpath(os.path.join(parent, path))
        return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, target_path])
    except ValueError:
        # Happens if paths are on different drives (Windows)
        return False


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    if not os.path.isdir(path):
        return f'    Error: "{directory}" is not a directory'

    if is_subdirectory(working_directory, directory):
        base = "current" if directory == "." else f"'{directory}'"
        all_things = os.listdir(path)
        info = [
            f" - {thing}: file_size={os.path.getsize(os.path.join(path, thing))} bytes, is_dir={os.path.isdir(os.path.join(path, thing))}"
            for thing in all_things
        ]
        return f"Result for {base} directory:\n" + '\n'.join(info)

    return f"Result for {directory} directory:\n    Error: Cannot list \"{directory}\" as it is outside the permitted working directory"

