from functions.helpers import isinsidewrkDIR
from functions.helpers import resolve_dir

import os 
import os.path as path


def get_file_content(working_directory, file_path):
    try:
        working_directory, file_path =  resolve_dir(working_directory, file_path)
        if not isinsidewrkDIR(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        output = ""
        with open(file_path, "r") as f:
            output = f.read()
        if len(output)>10000:
            output = output[:10000] + f' [...File "{file_path}" truncated at 10000 characters]'

        return output
    except Exception as e:
        return f'Error: {e}'