# CLI Log Tailing Tool

### Description

This program is a command-line interface (CLI) tool designed to monitor a log file in real-time. It continuously reads new content added to a specified log file and prints it to the console, similar to the `tail -f` command in Unix/Linux systems. The program uses basic file I/O operations, loops, and a sleep mechanism to provide real-time monitoring.

### Features:

* Monitors a specified log file in real-time.
* Displays new content as it is added to the file.
* Handles cases where the file is not found.

### Prerequisites:

* Python 3.x

### Usage:

1. Ensure that a file named `logfile.log` exists in the same directory as the script.
2. Run the program using the command:

   ```bash
   python log_tailer.py
   ```
3. Add new content to `logfile.log` to observe real-time updates in the console.

### How It Works:

The program follows these steps:

1. Checks if `logfile.log` exists using the `os.path.exists()` method.
2. Opens the file in read mode using the `with open()` statement to ensure proper file closure.
3. Moves the file pointer to the end using `f.seek(0, os.SEEK_END)`. This ensures that the program only reads new content added after the program starts.
4. Enters an infinite loop that reads the next line using `f.readline()`. If a new line is found, it is printed to the console. Otherwise, the program sleeps for 0.5 seconds and checks again.

### Code Breakdown:

```python
import os
import time
```

* `os`: Provides functions for interacting with the operating system.
* `time`: Provides time-related functions, such as sleep.

```python
if not os.path.exists("logfile.log"):
    print("File Not found")
```

* Checks whether the `logfile.log` file exists in the current directory. If not, it prints an error message.

```python
else:
    with open("logfile.log", "r") as f:
```

* Opens `logfile.log` in read mode. The `with` statement ensures that the file is properly closed after reading.

```python
        f.seek(0, os.SEEK_END)
```

* Moves the file pointer to the end of the file to only read new content as it is added.

```python
        while True:
```

* Enters an infinite loop to continuously monitor the log file.

```python
            line = f.readline()
            if line:
                print(line, end="")
```

* Reads the next line using `readline()`. If the line is not empty, it is printed to the console.

```python
            else:
                time.sleep(0.5)
```

* If no new content is found, the program waits for 0.5 seconds before checking again.

### Potential Improvements:

* Allow the log file path to be specified as a command-line argument.
* Implement error handling for file read/write operations.
* Add a termination mechanism (e.g., by pressing `Ctrl + C`).
