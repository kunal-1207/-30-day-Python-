# Day 11
# Challenge: Write a backup script for /var/log/ rotated daily.
# Focus: file automation
# Example Hint: Combine shutil + datetime

#!/usr/bin/env python3
import shutil
import os
import datetime
import gzip
import sys

def create_backup():
    # Create backup directory if it doesn't exist
    backup_root = "/var/log/backups"
    if not os.path.exists(backup_root):
        os.makedirs(backup_root)
    
    # Create date-stamped directory
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.join(backup_root, today)
    
    if os.path.exists(backup_dir):
        print(f"Backup for {today} already exists!", file=sys.stderr)
        return False
    
    os.makedirs(backup_dir)
    
    # Copy log files
    log_files = [f for f in os.listdir("/var/log") 
                if os.path.isfile(os.path.join("/var/log", f))]
    
    for log_file in log_files:
        src = os.path.join("/var/log", log_file)
        dst = os.path.join(backup_dir, log_file)
        
        try:
            # Skip currently open logs and special files
            if log_file in ['btmp', 'wtmp', 'lastlog']:
                continue
                
            # Copy and compress the log file
            with open(src, 'rb') as f_in:
                with gzip.open(f"{dst}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    
            print(f"Backed up: {log_file}")
            
        except Exception as e:
            print(f"Failed to backup {log_file}: {str(e)}", file=sys.stderr)
    
    print(f"Backup completed in {backup_dir}")
    return True

if __name__ == "__main__":
    print("Starting daily log backup...")
    create_backup()
