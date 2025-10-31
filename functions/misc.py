import os

def is_subdirectory(parent, path):
    try:
        parent_path = os.path.realpath(parent)
        target_path = os.path.realpath(os.path.join(parent_path, path))
        return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, target_path])
    except ValueError:
        # Happens if paths are on different drives (Windows)
        return False

