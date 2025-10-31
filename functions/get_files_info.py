import os
from .misc import is_subdirectory
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


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

