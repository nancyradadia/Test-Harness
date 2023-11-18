import json
import sys
import argparse

def json_to_gron(json_data):
    def recurse(json_object, base):
        lines = []
        if isinstance(json_object, dict):
            if base:
                lines.append(f"{base} = {{}};")
            # Custom sorting logic to replicate the Go implementation's behavior
            keys = sorted(json_object.keys())
            for key in keys:
                value = json_object[key]
                new_base = f"{base}.{key}" if base else key
                lines.extend(recurse(value, new_base))
        elif isinstance(json_object, list):
            lines.append(f"{base} = [];")
            for index, value in enumerate(json_object):
                new_base = f"{base}[{index}]"
                lines.extend(recurse(value, new_base))
        else:
            line = f"{base} = {json.dumps(json_object)};" if base else json.dumps(json_object)
            lines.append(line)
        return lines

    return recurse(json_data, 'json')

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        # Read JSON from STDIN
        data = json.load(sys.stdin)

    gron_lines = json_to_gron(data)
    for line in gron_lines:
        print(line)

if __name__ == "__main__":
    main()
