import json
import sys
import argparse

def json_to_gron(json_data):
    """
    Convert JSON data into Gron format.

    Parameters:
    json_data (dict or list): The JSON data to convert.

    Returns:
    list: A list of strings, each representing a line in Gron format.
    """
    def recurse(json_object, base):
        """
        Recursively traverse the JSON object to build Gron formatted lines.

        Parameters:
        json_object (dict, list, or scalar): The current JSON object being processed.
        base (str): The base string to prepend to each line.

        Returns:
        list: A list of Gron formatted lines for the current JSON object.
        """
        lines = []
        if isinstance(json_object, dict):
            # Handle JSON objects (dictionaries)
            if base:
                lines.append(f"{base} = {{}};")
            # Sort keys to ensure consistent output
            keys = sorted(json_object.keys())
            for key in keys:
                value = json_object[key]
                new_base = f"{base}.{key}" if base else key
                lines.extend(recurse(value, new_base))
        elif isinstance(json_object, list):
            # Handle JSON arrays
            lines.append(f"{base} = [];")
            for index, value in enumerate(json_object):
                new_base = f"{base}[{index}]"
                lines.extend(recurse(value, new_base))
        else:
            # Handle scalar values
            line = f"{base} = {json.dumps(json_object)};" if base else json.dumps(json_object)
            lines.append(line)
        return lines

    return recurse(json_data, 'json')

def main():
    """
    The main function to parse command-line arguments and convert the JSON input to Gron format.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Convert JSON to Gron format.')
    parser.add_argument('filename', nargs='?', help='JSON file to read (if empty, reads from stdin)', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    # Read JSON data from the file or stdin
    data = json.load(args.filename)

    # Convert JSON data to Gron format and print each line
    gron_lines = json_to_gron(data)
    for line in gron_lines:
        print(line)

if __name__ == "__main__":
    main()
