# Day 5
# Challenge: Parse an Apache log to count 5xx errors.
# Focus: string parsing, file reading
# Example Hint: Read line-by-line

import os

log_file = "access.log"  # Path to the Apache log file
count = 0

try:
    with open(log_file) as f:
        for line in f:
            parts = line.split()
            # Check if the line has enough parts and the status code starts with '5'
            if len(parts) > 8 and parts[8].startswith("5"):
                count += 1
    print(f"5xx errors: {count}")
except FileNotFoundError:
    print(f"Error: The file '{log_file}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
