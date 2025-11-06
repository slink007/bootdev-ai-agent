import os
from .misc import is_subdirectory
from .constants.constants import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read contents from the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the contents from.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.realpath(os.path.join(working_directory, file_path))

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if not is_subdirectory(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

