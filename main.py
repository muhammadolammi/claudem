import os
from dotenv import load_dotenv
from google import genai
import sys
from generate_content import generate_content
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



generate_content(client, user_prompt, VERBOSE)


