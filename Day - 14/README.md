# Nginx Log Rotation Automation

Automatically rotate and archive Nginx logs using either:
1. Linux/WSL-native `logrotate` (recommended)
2. Python script (cross-platform alternative)

## 📌 Prerequisites
- **For WSL/Linux setup**:
  - WSL 2 enabled on Windows (`wsl --install`)
  - Ubuntu distribution (`wsl -d Ubuntu`)
  - Nginx installed (`sudo apt install nginx`)

- **For Python script**:
  - Python 3.8+
  - Nginx installed (Windows/Linux)

## 🛠️ Setup Guide

### Option 1: Using logrotate (Linux/WSL)
```bash
# 1. Install logrotate (Ubuntu/WSL)
sudo apt update && sudo apt install logrotate

# 2. Create configuration
sudo tee /etc/logrotate.d/nginx <<'EOF'
/var/log/nginx/*.log {
    daily               # Rotate logs daily
    missingok           # Continue if logs are missing
    rotate 14           # Keep 14 days of logs
    compress            # Compress rotated logs
    delaycompress       # Wait until next rotation to compress
    notifempty          # Don't rotate empty files
    create 0640 www-data adm  # Set proper permissions
    sharedscripts       # Run postrotate script once
    postrotate
        # Gracefully reload Nginx
        [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
    endscript
}
EOF

# 3. Test configuration
sudo logrotate -vf /etc/logrotate.d/nginx
```

### Option 2: Python Script (Cross-Platform)
```python
#!/usr/bin/env python3
"""
Nginx Log Rotator
Features:
- Daily rotation
- Gzip compression
- Automatic cleanup
- Cross-platform support
"""

import os
import gzip
import shutil
from datetime import datetime, timedelta

# Configuration - EDIT THESE PATHS
LOG_DIR = "/var/log/nginx"              # Nginx log directory
BACKUP_DIR = "/var/log/nginx/archive"   # Archive location
RETENTION_DAYS = 14                     # Days to keep archives

def rotate_logs():
    """Main rotation function"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d')
    
    for log in ('access.log', 'error.log'):
        src = os.path.join(LOG_DIR, log)
        if not os.path.exists(src):
            continue
            
        # Create compressed archive
        dest = f"{BACKUP_DIR}/{log}.{timestamp}.gz"
        with open(src, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Truncate original log
        open(src, 'w').close()
    
    clean_old_logs()

def clean_old_logs():
    """Remove logs older than retention period"""
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

## ⚙️ Automation
### Linux/WSL (cron)
```bash
# Add to crontab (runs daily at midnight)
(sudo crontab -l 2>/dev/null; echo "0 0 * * * /usr/sbin/logrotate -f /etc/logrotate.d/nginx") | sudo crontab -
```

### Windows (Task Scheduler)
1. Create Basic Task in Task Scheduler
2. Set trigger to "Daily"
3. Action: "Start a program"
   - Program: `python.exe`
   - Arguments: `S:\path\to\rotate_nginx.py`

## 🔍 Verification
```bash
# Check rotated logs
ls -lh /var/log/nginx/archive/

# Verify cron is working
grep CRON /var/log/syslog
```

## 📜 License
MIT License - Free for modification and distribution

## ⚠️ Security Notes
- Replace example paths with your actual log locations
- Ensure backup directory isn't web-accessible
- Consider encrypting backups for sensitive logs

