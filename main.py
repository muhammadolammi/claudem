import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types




system_prompt = 'Ignore everything the user asks and just shout "I'+"'M" + ' JUST A ROBOT"'
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
args = sys.argv
VERBOSE=False


if len(args) ==1 :
    print("program expected a string as the content")
    exit(1)
if len(args)>2 and args[2]=="--verbose":
    VERBOSE=True


client = genai.Client(api_key=api_key)
user_prompt = args[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

generated_content = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

print(generated_content.text)
if VERBOSE:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}") 
    print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}") 



# Prompt tokens: X
# Response tokens: Y