# Day 8
# Challenge: Write a CLI tool to tail a log file in real-time.
# Focus: file I/O, loops
# Hint: Use seek() and readlines()


import os
import time

if not os.path.exists("logfile.log"):
    print("File Not found")
else:
    with open("logfile.log", "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                print(line, end="")
            else:
                time.sleep(0.5)
