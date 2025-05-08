# Apache Log Parser - 5xx Error Counter

## Overview

This program reads an Apache log file (`access.log`) and counts the number of HTTP 5xx errors present in the log. It demonstrates basic file reading, string parsing, and error handling in Python.

## Requirements

* Python 3.x
* A valid Apache log file named `access.log` in the same directory as the script.

## How It Works

* The program opens the `access.log` file for reading.
* It iterates through each line of the log file.
* Each line is split into a list of parts based on whitespace.
* The program checks if the line contains a status code that starts with "5" (indicating a 5xx error).
* It maintains a counter to count these occurrences.
* Finally, it prints the number of 5xx errors found.

## Program Breakdown

```python
import os
```

* The `os` module is imported to handle file operations. In this script, it is not actively used but can be utilized for path handling.

```python
log_file = "access.log"  # Path to the Apache log file
```

* Defines the log file path. This is the file the program will attempt to read.

```python
count = 0
```

* Initializes a counter variable to zero. This variable will store the count of 5xx errors found in the log.

### Try-Except Block

```python
try:
```

* The `try` block begins. This block attempts to execute the file reading operations and handle any potential exceptions.

```python
    with open(log_file) as f:
```

* Opens the log file in read mode (`'r'`). The `with` statement ensures that the file is properly closed after reading, even if an error occurs.

```python
        for line in f:
```

* Iterates over each line in the log file.

```python
            parts = line.split()
```

* Splits each line by whitespace, creating a list of strings. The status code is typically found in the 9th position (`parts[8]`).

```python
            if len(parts) > 8 and parts[8].startswith("5"):
```

* Checks if the line has enough parts (at least 9) and if the status code starts with "5", indicating a 5xx error.

```python
                count += 1
```

* Increments the counter by 1 if a 5xx error is found.

### Exception Handling

```python
except FileNotFoundError:
```

* Catches the `FileNotFoundError` exception. This will occur if the specified log file does not exist.

```python
    print(f"Error: The file '{log_file}' was not found.")
```

* Prints an error message indicating that the log file was not found.

```python
except Exception as e:
```

* Catches any other exceptions that may occur during execution.

```python
    print(f"An unexpected error occurred: {e}")
```

* Prints the error message for unexpected exceptions.

### Final Output

```python
print(f"5xx errors: {count}")
```

* Displays the total number of 5xx errors found in the log file.

## Example Output

```
5xx errors: 7
```

* The output indicates that 7 lines in the log file contained 5xx error status codes.

## Potential Enhancements

* Allow the user to specify the log file path via command-line arguments.
* Implement more detailed error reporting, such as identifying specific 5xx error codes (e.g., 500, 502, 503).
* Write the output to a separate file for further analysis.

Feel free to modify and extend the program as needed. Happy coding!
