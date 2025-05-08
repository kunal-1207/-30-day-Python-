# Day 6
# Challenge: Create a function that compresses old logs (7+ days).
# Focus: shutil, datetime
# Example Hint: Use shutil.make_archive

import os
import shutil
import datetime
from typing import NoReturn

def compress_old_logs(log_dir: str = "logs", days: int = 7) -> NoReturn:
    if not os.path.isdir(log_dir):
        print(f"[INFO] Log directory '{log_dir}' does not exist. No logs to compress.")
        return

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    files_compressed = 0

    for file in os.listdir(log_dir):
        path = os.path.join(log_dir, file)
        if not os.path.isfile(path):
            continue
        try:
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            if mtime >= cutoff:
                continue
            archive_path = os.path.splitext(path)[0]
            shutil.make_archive(archive_path, 'zip', root_dir=log_dir, base_dir=file)
            os.remove(path)
            print(f"[COMPRESSED] {file} -> {archive_path}.zip")
            files_compressed += 1
        except Exception as e:
            print(f"[ERROR] Failed to compress {file}: {e}")

    if files_compressed == 0:
        print("[INFO] No old log files found to compress.")
    else:
        print(f"[DONE] Compressed {files_compressed} old log file(s).")

if __name__ == "__main__":
    compress_old_logs()
