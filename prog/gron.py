import json
import sys

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def gron(file):
    try:
        json_data = json.load(file)
        flattened_json = flatten_json(json_data)
        for path, value in flattened_json.items():
            print(f'json.{path} = {json.dumps(value)}')
        return 0
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit_status = 1
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            exit_status = gron(file)
    else:
        exit_status = gron(sys.stdin)
    sys.exit(exit_status)
