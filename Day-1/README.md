# Environment Variables Program - Day 1

## Overview

This program is a simple Python script that iterates over all environment variables available in the operating system and prints each key-value pair. It is a basic example of how to access and display environment variables using the `os` module in Python.

## How It Works

The script performs the following steps:

1. **Import the `os` module:**

   * The `os` module provides a way of interacting with the operating system, including accessing environment variables.

2. **Access Environment Variables:**

   * The `os.environ` object is a dictionary-like object that contains all the environment variables as key-value pairs.

3. **Iterate through Environment Variables:**

   * The `for` loop iterates through each key-value pair in `os.environ.items()`.

4. **Print the Environment Variables:**

   * The program uses a formatted string to print each key and its corresponding value.

---

## Code Breakdown

```python
# Import the os module
import os
```

* The `os` module provides a way to interface with the underlying operating system. In this case, it is used to access environment variables.

```python
# Iterate through each environment variable and its value
for key, value in os.environ.items():
```

* The `os.environ.items()` method returns a view object containing all the environment variables as key-value pairs. The `for` loop iterates over each pair.

```python
    # Print the environment variable and its value
    print(f"{key}: {value}")
```

* The `print()` function is used to output each key-value pair in the format `KEY: VALUE`. The formatted string `f"{key}: {value}"` allows for inline variable substitution.

---

## Example Output

An example output of running this program might look like this:

```
HOME: /home/user
PATH: /usr/local/bin:/usr/bin:/bin
SHELL: /bin/bash
USER: user123
```

---

## Use Cases

* Displaying all environment variables for debugging purposes.
* Identifying specific environment variables for configuration settings.
* Checking the values of environment variables during script execution.

---

## Prerequisites

* Python 3.x

---

## How to Run

1. Save the script as `env_variables.py`.
2. Open a terminal and navigate to the directory where the script is saved.
3. Run the script using the command:

```bash
python env_variables.py
```

---

## Additional Notes

* The output may vary depending on the operating system and the configured environment variables.
* Avoid printing sensitive information such as API keys or secrets without proper handling.

---

That's the complete breakdown and explanation for the program. If you need further adjustments, let me know!
