import json

from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input_json_str: str) -> str:
    # First we need to parse the json.
    try:
        parsed = json.loads(input_json_str)
    except Exception as e:
        # Give the LLM visibility of the error, to give it an opportunity to correct.
        response = str(e)
        return response

    print('input_json:')
    import pprint
    pprint.pprint(parsed)
    
    response = '{"weather": "Clear and warm with a slight breeze; perfect early summer weather."}'
    return response