# Day 1
# Challenge: Print all environment variables.
# Focus: os.environ, basics
# Example Hint: Use os.environ.items()

import os

for key, value in os.environ.items():
    print(f"{key}: {value}")
