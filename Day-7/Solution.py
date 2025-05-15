# Day 7
# Challenge: Build a script that watches CPU usage and alerts if >80%.
# Focus: psutil
# Example Hint: Install with pip

import psutil

cpu = psutil.cpu_percent(interval=1)
if cpu > 80:
    print(f"ALERT! High CPU usage: {cpu}%")
else:
    print(f"CPU OK: {cpu}%")
