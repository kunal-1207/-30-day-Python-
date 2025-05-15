#  Day 10
# Challenge: Retry Decorator
# Focus: decorators, error handling
# Example Hint: try/except, time.sleep()

import time
import random

def retry(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Retry {i+1}: {e}")
                time.sleep(2)
        raise Exception("Failed after 3 retries")
    return wrapper

@retry
def flaky():
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success"

print(flaky())
