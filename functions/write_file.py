from functions.helpers import isinsidewrkDIR
import os.path as path
import os
from functions.helpers import resolve_dir


def write_file(working_directory, file_path, content):
    try:
        working_directory, file_path = resolve_dir(working_directory, file_path)
        if not isinsidewrkDIR(working_directory, file_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        with open(file_path, "w") as f:
            f.write(content) 
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"ERROR: {e}"
