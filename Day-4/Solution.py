# Day 4
# Challenge: Rename all .log files to .log.bak in a folder.
# Focus: os, file handling
# Example Hint: os.listdir(), os.rename()

import os

for file in os.listdir("."):
    if file.endswith(".log"):
        os.rename(file, file + ".bak")
