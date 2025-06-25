from functions.helpers import isinsidewrkDIR
import os.path as path
import os
from functions.helpers import resolve_dir
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_directory, resolved_file_path =  resolve_dir(working_directory, file_path)
        if not isinsidewrkDIR(working_directory, resolved_file_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not path.exists(resolved_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        command = ["python", resolved_file_path]

        process =  subprocess.run(
            command,
            capture_output=True,
            timeout=30,
            cwd=working_directory,

            )
        outputstr = "\n"
        outputstr += f'STDOUT:  {process.stdout}\n'
        outputstr += f'STDERR:  {process.stderr}\n'
        if process.returncode !=0:
            outputstr += f'Process exited with code {process.returncode}\n'
        if process.stdout =="":
            outputstr += f'No output produced\n'


        return outputstr
    except Exception as e:
        return f"Error: executing Python file: {e}"    

