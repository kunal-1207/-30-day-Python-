# Challenge: Automatically rotate Nginx logs and archive old ones.
# Focus: cron, script automation
# Example Hint: Use logrotate configs or pure Python
#!/usr/bin/env python3

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
