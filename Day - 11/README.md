# Backup Script

This Python script is designed to create daily backups of log files located in the `/var/log` directory. The script copies these log files to a designated backup directory, compresses them using gzip, and organizes the backups by date.

## How the Script Works

1. **Environment Declaration**

```python
#!/usr/bin/env python3
```

* This line specifies that the script should be executed using Python 3.

2. **Importing Required Modules**

```python
import shutil
import os
import datetime
import gzip
import sys
```

* `shutil`: Used for file operations such as copying data.
* `os`: Provides a way to interact with the operating system, such as file paths and directory creation.
* `datetime`: Handles date and time operations.
* `gzip`: Allows compression of files in gzip format.
* `sys`: Provides access to system-specific parameters and functions.

3. **Function Definition: `create_backup()`**

```python
def create_backup():
```

* The `create_backup()` function is responsible for creating the backup of log files.

4. **Creating the Backup Directory**

```python
backup_root = "/var/log/backups"
if not os.path.exists(backup_root):
    os.makedirs(backup_root)
```

* Defines the backup root directory.
* Checks if the directory exists, and creates it if it doesn't.

5. **Creating a Date-Stamped Directory**

```python
today = datetime.datetime.now().strftime("%Y-%m-%d")
backup_dir = os.path.join(backup_root, today)
```

* Creates a subdirectory named with the current date in `YYYY-MM-DD` format.
* If a directory for today's date already exists, it notifies the user and exits.

```python
if os.path.exists(backup_dir):
    print(f"Backup for {today} already exists!", file=sys.stderr)
    return False

os.makedirs(backup_dir)
```

6. **Copying and Compressing Log Files**

```python
log_files = [f for f in os.listdir("/var/log") if os.path.isfile(os.path.join("/var/log", f))]
```

* Collects all log files from the `/var/log` directory.

7. **Processing Each Log File**

```python
for log_file in log_files:
```

* Iterates over each log file and processes it for backup.

```python
if log_file in ['btmp', 'wtmp', 'lastlog']:
    continue
```

* Skips system files that are likely in use.

8. **Copying and Compressing Files**

```python
with open(src, 'rb') as f_in:
    with gzip.open(f"{dst}.gz", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
```

* Reads each log file in binary mode and writes it to a compressed `.gz` file.

9. **Error Handling**

```python
except Exception as e:
    print(f"Failed to backup {log_file}: {str(e)}", file=sys.stderr)
```

* Handles potential exceptions during the file processing stage.

10. **Completion Message**

```python
print(f"Backup completed in {backup_dir}")
```

* Notifies the user that the backup is complete and provides the backup directory path.

11. **Main Execution Block**

```python
if __name__ == "__main__":
    print("Starting daily log backup...")
    create_backup()
```

* If the script is run as the main program, it executes the `create_backup()` function.

## Usage

* Ensure that the script has executable permissions using the command:

```bash
chmod +x backup_script.py
```

* Run the script using:

```bash
sudo ./backup_script.py
```

* Ensure that the script is run as a user with appropriate permissions to access the `/var/log` directory.

## Dependencies

* Python 3
* gzip
* shutil
* datetime
* os
* sys

## Error Handling

* If any file fails to back up, a warning will be printed to the standard error output.
* If a backup for the current date already exists, the script will notify the user and exit without creating a new backup.
