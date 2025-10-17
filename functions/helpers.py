import os

class Helpers:
    MAX_CHARS = 10000

    @classmethod
    def is_subdirectory(cls, parent, path):
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

