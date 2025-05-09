# JSON Config File Masking Program

## Overview

This program reads a JSON configuration file, masks sensitive information (like passwords, secrets, API keys, and tokens), and prints the formatted output to the console. It is a simple implementation that focuses on working with JSON data and dictionaries in Python.

## Technologies Used:

* Python
* JSON

## Key Concepts:

* JSON Handling
* Dictionary Manipulation
* Exception Handling

## Dependencies:

* No external dependencies are required.

## How to Run the Program:

1. Save the script as `config_reader.py`.
2. Ensure that you have a valid `config.json` file in the same directory.
3. Run the program using the command:

   ```bash
   python config_reader.py
   ```

## Sample JSON (`config.json`):

```json
{
  "username": "user1",
  "password": "mysecretpassword",
  "api_key": "12345abcde",
  "token": "abcd1234",
  "nested": {
    "secret": "hiddenvalue",
    "other_key": "value"
  }
}
```

## Expected Output:

```json
{
    "username": "user1",
    "password": "***",
    "api_key": "***",
    "token": "***",
    "nested": {
        "secret": "***",
        "other_key": "value"
    }
}
```

## Code Breakdown:

### Importing the Required Module:

```python
import json
```

* The `json` module is imported to handle JSON operations such as reading and parsing JSON data.

### Defining the `mask_sensitive` Function:

```python
def mask_sensitive(d, keys_to_mask=None):
```

* This function masks sensitive keys in the dictionary.
* The `keys_to_mask` parameter is a set of keys to be masked. If not provided, it defaults to a set containing `"password"`, `"secret"`, `"api_key"`, and `"token"`.

#### Handling Dictionaries:

```python
if isinstance(d, dict):
    return {k: ("***" if k in keys_to_mask else mask_sensitive(v, keys_to_mask)) for k, v in d.items()}
```

* If the input is a dictionary, it iterates through each key-value pair.
* If the key is in the `keys_to_mask` set, the value is masked with `"***"`.
* Otherwise, it recursively processes nested dictionaries or lists.

#### Handling Lists:

```python
elif isinstance(d, list):
    return [mask_sensitive(i, keys_to_mask) for i in d]
```

* If the input is a list, it recursively applies the `mask_sensitive` function to each item in the list.

#### Handling Other Data Types:

```python
return d
```

* If the input is not a dictionary or list, it returns the value as-is.

### Defining the `load_and_print_config` Function:

```python
def load_and_print_config(path):
```

* This function attempts to open and read the JSON file from the specified `path`.

#### Reading the JSON File:

```python
with open(path, encoding="utf-8") as f:
    data = json.load(f)
```

* Opens the JSON file and reads its content using `json.load()`.

#### Applying Masking and Formatting Output:

```python
masked_data = mask_sensitive(data)
print(json.dumps(masked_data, indent=4))
```

* Applies the `mask_sensitive` function to the JSON data and prints the masked JSON with indentation for readability.

#### Error Handling:

```python
except (OSError, json.JSONDecodeError) as e:
    print(f"Error loading JSON config: {e}")
```

* Catches file reading errors or JSON parsing errors and prints a descriptive error message.

### Running the Program:

```python
load_and_print_config("config.json")
```

* Calls the `load_and_print_config` function with the default filename `config.json`.

---

Feel free to update the file with additional information or modify the code as needed.
