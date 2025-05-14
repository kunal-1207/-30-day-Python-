# Challenge: Automatically rotate Nginx logs and archive old ones.
# Focus: cron, script automation
# Example Hint: Use logrotate configs or pure Python
#!/usr/bin/env python3


import os
import shutil
import gzip
from datetime import datetime
import platform

NGINX_LOG_DIR = "/var/log/nginx"
ARCHIVE_DIR = "/var/log/nginx/archive"
LOG_FILES = ["access.log", "error.log"]

def rotate_and_archive():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    for log in LOG_FILES:
        log_path = os.path.join(NGINX_LOG_DIR, log)
        if os.path.exists(log_path):
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            archived_log = f"{log}.{timestamp}.gz"
            archived_path = os.path.join(ARCHIVE_DIR, archived_log)
            # Move and compress
            with open(log_path, 'rb') as f_in, gzip.open(archived_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            # Truncate original log
            open(log_path, 'w').close()
    # Signal Nginx to reopen logs (only on Linux)
    if platform.system() == "Linux":
        os.system("nginx -s reopen")

if __name__ == "__main__":
    rotate_and_archive()
