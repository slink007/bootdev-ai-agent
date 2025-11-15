import os
import sys


from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file_content, write_file_content


FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file_content": write_file_content,
}


def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args or {})
    args["working_directory"] = "./calculator"
    func_name = function_call_part.name

    if verbose:
        print(f"Calling function: {func_name}({args})")
        # print(type(args), args) 
    else:
        print(f" - Calling function: {func_name}")
    
    func = FUNCTIONS.get(func_name)
    result = func(**args)
    
    if not func:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=func_name,
                response={"error": f"Unknown function: {func_name}"},
            )],
        )
    
    result = func(**args)
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=func_name,
            response={"result": result},
        )],
    )

    


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
    available_functions = types.Tool(function_declarations=[schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file_content])

    prompt = ""
    response = ""
    messages = []
    
    try:
        prompt = sys.argv[1]
        messages = [types.Content(role="user", 
            parts=[types.Part(text=prompt)]),]
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=prompt))
    except IndexError:
        print("Error: no prompt provided")
        sys.exit(1)
    except genai.errors.ClientError:
        print("Google's genai is too busy at the moment. This is not your fault.")
        sys.exit(1)

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")        

    # Check if there are any function calls
    if response.function_calls:
        # Iterate over each function call part
        for function_call_part in response.function_calls:
            # Access the name and args
            call_result = call_function(function_call_part, verbose="--verbose" in sys.argv)
            print(call_result.parts[0].function_response.response['result'])
    else:
        # No function calls, just print the text
        print(response.text)
    
    # Check the candidates property of the response
    if response.candidates:
        for candidate in response.candidates:
            part = types.Part(text=candidate.content.parts[0].text)
            new_msg = types.Content(role="user", parts=[types.Part(text=candidate.content.parts[0].text),])
            # print(part)
            # print(candidate)
            # text_part = candidate.content.parts[0].text
            # print(text_part)



if __name__ == "__main__":
    main()
