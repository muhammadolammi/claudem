import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.call_function import call_function




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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the full content in a file, cropped out at 10000 characters, if chars > 10000",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to file to get contents from, relative to the working directory. If not provided, an error is returned.",
            ),
        },
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the provided python file as a subprocess.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
       properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to file run (must be a .py file), relative to the working directory. If not provided, an error is returned.",
            ),
        },
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write provided contents to the provided file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory. If not provided, the file is created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided, the file is created with no content.",
            ),
        },
    ),
)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)




def generate_content(client, user_prompt, verbose):
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    generated_content = client.models.generate_content(
    model="gemini-2.0-flash-001",
    
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        ),
    )

    if generated_content.function_calls:
        for candidate in generated_content.candidates:
            for part in candidate.content.parts:
                function_call_part = part.function_call
                if function_call_part:
                    function_call_result = call_function(function_call_part, verbose)
                    if not function_call_result.parts[0].function_response.response :
                        raise Exception("Fatal no response from function call")
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
        exit(0)
    print(generated_content.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}") 
        print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}") 


