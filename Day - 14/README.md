# Nginx Log Rotation Automation

## 📦 Overview

This project provides an automated solution for rotating and archiving Nginx logs using two distinct methods:

1. **logrotate (Linux/WSL-native)** - Recommended for Linux and WSL environments.
2. **Python Script** - A cross-platform alternative that can run on both Linux and Windows.

## 📌 Prerequisites

### For WSL/Linux setup:

* WSL 2 enabled on Windows (`wsl --install`)
* Ubuntu distribution (`wsl -d Ubuntu`)
* Nginx installed (`sudo apt install nginx`)

### For Python Script:

* Python 3.8+ installed
* Nginx installed (Windows/Linux)

## 🛠️ Setup Guide

### ✅ Option 1: Using logrotate (Linux/WSL)

1. **Install logrotate**:

```bash
sudo apt update && sudo apt install logrotate
```

* Updates the package list and installs the `logrotate` utility.

2. **Create the configuration file**:

```bash
sudo tee /etc/logrotate.d/nginx <<'EOF'
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
    endscript
}
EOF
```

* This command writes the log rotation configuration for Nginx logs.

  * `daily`: Rotate logs daily.
  * `missingok`: Continue if logs are missing.
  * `rotate 14`: Keep logs for 14 days.
  * `compress`: Compress rotated logs.
  * `delaycompress`: Delay compression until the next rotation cycle.
  * `notifempty`: Do not rotate empty logs.
  * `create`: Set permissions and ownership for new logs.
  * `postrotate`: Reload Nginx after log rotation.

3. **Test the configuration**:

```bash
sudo logrotate -vf /etc/logrotate.d/nginx
```

* Verbose testing of the logrotate configuration to ensure it functions correctly.

### ✅ Option 2: Python Script (Cross-Platform)

1. **Create the Python script**:

```python
#!/usr/bin/env python3
import os
import gzip
import shutil
from datetime import datetime, timedelta

LOG_DIR = "/var/log/nginx"
BACKUP_DIR = "/var/log/nginx/archive"
RETENTION_DAYS = 14

def rotate_logs():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d')

    for log in ('access.log', 'error.log'):
        src = os.path.join(LOG_DIR, log)
        if not os.path.exists(src):
            continue

        dest = f"{BACKUP_DIR}/{log}.{timestamp}.gz"
        with open(src, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        open(src, 'w').close()

    clean_old_logs()

def clean_old_logs():
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    for f in os.listdir(BACKUP_DIR):
        if f.endswith('.gz'):
            path = os.path.join(BACKUP_DIR, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime < cutoff:
                os.remove(path)

if __name__ == '__main__':
    rotate_logs()
```

* This script performs daily log rotation, compression, and cleanup for Nginx logs.
* Key sections:

  * **rotate\_logs()**: Compresses current logs and moves them to the archive directory.
  * **clean\_old\_logs()**: Deletes archived logs older than the specified retention period.

2. **Schedule the script execution**:

* **Linux/WSL (cron)**:

```bash
(sudo crontab -l 2>/dev/null; echo "0 0 * * * /usr/bin/python3 /path/to/script.py") | sudo crontab -
```

* **Windows (Task Scheduler)**:

  * Create a Basic Task to run `python.exe` with the script path as the argument.

## 🔍 Verification

1. **Check Archived Logs**:

```bash
ls -lh /var/log/nginx/archive/
```

2. **Verify Cron Execution**:

```bash
grep CRON /var/log/syslog
```

## 📜 License

MIT License - Free for modification and distribution.

## ⚠️ Security Notes

* Ensure backup directories are not web-accessible.
* Adjust file paths and permissions to match your environment.
* Consider encrypting archived logs for sensitive data.
