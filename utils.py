import textwrap
import json

def pretty_print(text: str, indent: str = ' ' * 4) -> None:
    """
    Pretty prints a string with actual line breaks.
    
    Args:
        text (str): The string to pretty print.
        indent (str): The indentation to add to each line break (default: '    ').
    """
    text = text.replace('\n', '\n' + textwrap.indent('', indent))
    print(text)

def convert_to_json(data):
    # Check if data is a string
    if isinstance(data, str):
        # Attempt to parse JSON from the string
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            # Handle JSON decode error
            print("Error: invalid JSON")
    return data