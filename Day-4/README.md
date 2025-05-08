# README: Log File Renaming Program

## Overview

This program is a simple Python script designed to rename all `.log` files in the current directory by appending a `.bak` extension to them. This can be particularly useful for archiving or backing up log files before further processing or deletion.

## Dependencies

* Python 3.x
* `os` module (built-in with Python)

## How It Works

1. The program uses the `os` module to interact with the file system.
2. It iterates through all files in the current directory.
3. For each file that ends with `.log`, it renames the file by appending `.bak` to the filename.

## Implementation

Below is a breakdown of the program, line by line:

```python
# Import the OS module to interact with the file system
import os

# Iterate over all files in the current directory
for file in os.listdir("."):
    # Check if the file ends with '.log'
    if file.endswith(".log"):
        # Rename the file by appending '.bak'
        os.rename(file, file + ".bak")
```

### Line-by-Line Breakdown

* `import os`: Imports the `os` module, which provides a way to interact with the file system, including listing directory contents and renaming files.

* `for file in os.listdir("."):`: Loops through each file in the current directory (`.` refers to the current working directory).

* `if file.endswith(".log"):`: Checks if the current file ends with the `.log` extension, identifying it as a log file.

* `os.rename(file, file + ".bak")`: Renames the file by appending `.bak` to the filename. For example, `error.log` will be renamed to `error.log.bak`.

## Example

Suppose the current directory contains the following files:

* error.log
* server.log
* data.txt

After running the script, the directory will be updated to:

* error.log.bak
* server.log.bak
* data.txt

## Usage

1. Copy the script into a `.py` file (e.g., `rename_logs.py`).
2. Navigate to the directory containing the `.log` files.
3. Run the script using the command:

```bash
python rename_logs.py
```

4. The `.log` files will be renamed to `.log.bak`.

## Notes

* The script only modifies files in the current working directory.
* Ensure that there are no file permission issues that may prevent renaming.

## Future Enhancements

* Add error handling for missing files or permission issues.
* Allow the user to specify a different directory.
* Implement logging to keep track of renamed files.
