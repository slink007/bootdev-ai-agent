import os
import sys


from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
""" 
    available_functions = types.Tool(function_declarations=[schema_get_files_info,])

    prompt = ""
    response = ""
    
    try:
        prompt = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt))
    except IndexError:
        print("Error: no prompt provided")
        exit(1)
    
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Check if there are any function calls
    if response.function_calls:
        # Iterate over each function call part
        for function_call_part in response.function_calls:
            # Access the name and args
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        # No function calls, just print the text
        print(response.text)


if __name__ == "__main__":
    main()



