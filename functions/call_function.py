from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types


functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file":write_file,
    "run_python_file":run_python_file
}


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    funcs_args = function_call_part.args
    funcs_args["working_directory"] = "./calculator"

    func = functions[function_call_part.name]
    if func:
        result = func(**funcs_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                    )
                ],
            )
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
       ],
      )
    