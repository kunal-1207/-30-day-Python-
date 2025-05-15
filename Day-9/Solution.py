# Day 9
# Challenge: Read a JSON config file and print formatted output.
# Focus: json, dictionaries
# Example Hint: json.load()

import json
def mask_sensitive(d, keys_to_mask=None):
    if keys_to_mask is None:
        keys_to_mask = {"password", "secret", "api_key", "token"}
    if isinstance(d, dict):
        return {k: ("***" if k in keys_to_mask else mask_sensitive(v, keys_to_mask)) for k, v in d.items()}
    elif isinstance(d, list):
        return [mask_sensitive(i, keys_to_mask) for i in d]
    return d

def load_and_print_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        masked_data = mask_sensitive(data)
        print(json.dumps(masked_data, indent=4))
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading JSON config: {e}")

load_and_print_config("config.json")
