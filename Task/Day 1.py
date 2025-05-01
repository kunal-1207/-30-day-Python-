# Day 1
# Print all environment variables.

import os

for key, value in os.environ.items():
    print(f"{key}: {value}")

