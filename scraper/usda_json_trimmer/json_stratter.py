import json


"""
prints the structure of a json, useful for quickly visualizing the hierarchy in big jsons / dicts
can also help with finding a JSON pointer if one needs something to put in an iterable loop
"""
def print_keys(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print("  " * indent + str(key))
            print_keys(value, indent + 1)
    elif isinstance(data, list):
        for item in data:
            print_keys(item, indent)

# Example usage with a file
with open("hummus.json") as f:
    json_data = json.load(f)

print_keys(json_data)