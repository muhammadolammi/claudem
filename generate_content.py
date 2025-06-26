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
- You can always start with the get_files_info function first if you dont know where to start.
- When asked to fix a bug instead of creating new files you are to find the responsible file for that error and fix.
"""



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)




# def generate_content(client, user_prompt, verbose):
#     messages = [
#     types.Content(role="user", parts=[types.Part(text=user_prompt)]),
#         ]
#     for i in range(20):
#         generated_content = client.models.generate_content(
#                     model="gemini-2.0-flash-001",
            
#                 contents=messages,
#                 config=types.GenerateContentConfig(
#                     tools=[available_functions],
#                     system_instruction=system_prompt
#                     ),
#                 )
        
#         for candidate in generated_content.candidates:
#             # append  candidate to messages to use in next iteration
#             messages.append(candidate.content)
#            #iterate through all the parts and call all functions if any.
#             for part in candidate.content.parts:
#                 function_call_part = part.function_call
#                 if function_call_part:
#                     function_call_result = call_function(function_call_part, verbose)
#                     if not function_call_result.parts[0].function_response.response :
#                         raise Exception("Fatal no response from function call")
#                     # append the function  result to messages
#                     messages.append(function_call_result)
#                     if verbose:

#                         print(f"-> {function_call_result.parts[0].function_response.response}")
#         if generated_content.function_calls:
#             continue
#         else:
#             print(generated_content.text)
#             if verbose:
#                 print(f"User prompt: {user_prompt}")
#                 print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}") 
#                 print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}") 

#             break
       



def generate_content(client, user_prompt, verbose):
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
  
    for i in range(20):
        generated_content = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
        
        new_parts = []
        function_call_made = False

        for candidate in generated_content.candidates:
            if candidate.content:
                messages.append(candidate.content)  # Add assistant reply
                # check if there are parts , some error were thrown when parts is None.
                if candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            function_call_made = True
                            function_result = call_function(part.function_call, verbose)
                            messages.append(function_result)
                            
                            if verbose:
                                print(f"-> {function_result.parts[0].function_response.response}")
                        elif hasattr(part, "text"):
                            new_parts.append(part.text)
        
        if not function_call_made:
            final_output = "\n".join(new_parts)
            print(final_output)

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}") 
                print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}") 
            break
