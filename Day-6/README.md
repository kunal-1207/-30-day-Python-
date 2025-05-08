# Log Compression Program

## Overview

This program is designed to compress log files that are older than a specified number of days (default is 7 days). The program leverages Python's `shutil` and `datetime` libraries to identify and compress these files into `.zip` archives. Once the files are compressed, the original log files are deleted to save space.

### Key Libraries and Modules:

* `os`: Used to interact with the file system.
* `shutil`: Provides high-level file operations, including creating archive files.
* `datetime`: Handles date and time operations.
* `typing.NoReturn`: Specifies that the function does not return any value.

## Function: `compress_old_logs`

```python
import os
import shutil
import datetime
from typing import NoReturn

```

* The necessary libraries are imported.
* `NoReturn` is used as the return type hint for the function to indicate that it does not return a value.

### Function Definition:

```python
def compress_old_logs(log_dir: str = "logs", days: int = 7) -> NoReturn:
```

* `log_dir`: Directory where log files are located. Defaults to `logs`.
* `days`: Number of days to determine the cutoff for old logs. Defaults to `7`.
* The function does not return any value, as indicated by the `NoReturn` type hint.

### Directory Existence Check:

```python
if not os.path.isdir(log_dir):
    print(f"[INFO] Log directory '{log_dir}' does not exist. No logs to compress.")
    return
```

* Checks if the specified log directory exists.
* If not, an informational message is printed, and the function exits.

### Cutoff Time Calculation:

```python
cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
files_compressed = 0
```

* Calculates the cutoff datetime by subtracting the specified number of days from the current date.
* `files_compressed` is initialized to keep track of the number of files compressed.

### Iterating Through Files:

```python
for file in os.listdir(log_dir):
```

* Iterates over all files in the specified directory.

### Path and File Check:

```python
path = os.path.join(log_dir, file)
if not os.path.isfile(path):
    continue
```

* Constructs the full file path.
* Skips non-file entries (e.g., directories).

### File Compression Logic:

```python
try:
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    if mtime >= cutoff:
        continue
```

* Retrieves the modification time (`mtime`) of the file.
* If the file is newer than the cutoff date, it is skipped.

### Creating Archive and Deleting Original:

```python
archive_path = os.path.splitext(path)[0]
shutil.make_archive(archive_path, 'zip', root_dir=log_dir, base_dir=file)
os.remove(path)
print(f"[COMPRESSED] {file} -> {archive_path}.zip")
files_compressed += 1
```

* Extracts the base file path (excluding extension) to create the archive path.
* Compresses the file into a `.zip` archive.
* Deletes the original file.
* Prints a success message and increments the `files_compressed` counter.

### Error Handling:

```python
except Exception as e:
    print(f"[ERROR] Failed to compress {file}: {e}")
```

* Catches and prints any exception encountered during the compression process.

### Completion Message:

```python
if files_compressed == 0:
    print("[INFO] No old log files found to compress.")
else:
    print(f"[DONE] Compressed {files_compressed} old log file(s).")
```

* If no files were compressed, an informational message is printed.
* Otherwise, a summary of the number of files compressed is displayed.

### Main Execution Block:

```python
if __name__ == "__main__":
    compress_old_logs()
```

* Executes the `compress_old_logs()` function if the script is run as the main module.

### Example Usage:

* To run the program with the default directory and days:

  ```bash
  python log_compressor.py
  ```
* To specify a custom directory and cutoff days:

  ```bash
  python log_compressor.py /path/to/logs 10
  ```

### Potential Improvements:

* Adding logging instead of print statements.
* Implementing command-line arguments using `argparse`.
* Enhancing error handling and reporting.

### Conclusion:

This program provides a simple and effective way to manage disk space by compressing old log files. It can be extended with more advanced logging mechanisms and improved user input handling.
