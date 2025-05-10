# Retry Decorator Program

## Overview

This program demonstrates the use of a retry decorator that attempts to execute a given function up to three times in case of exceptions. It leverages Python's `time.sleep()` for introducing delays between retries and `try/except` for error handling. The `flaky()` function is a simulated unreliable function that has a 70% chance of failing to demonstrate the retry mechanism.

## Program Breakdown

### Importing Required Modules

```python
import time
import random
```

* `time` is used to introduce a delay between retries.
* `random` is used to simulate a function that fails randomly.

### Defining the Retry Decorator

```python
def retry(func):
```

* A decorator named `retry` is defined. It takes a function `func` as an argument.

```python
    def wrapper(*args, **kwargs):
```

* The inner function `wrapper` accepts any number of positional (`*args`) and keyword (`**kwargs`) arguments.

```python
        for i in range(3):
```

* A loop is initiated to allow up to three attempts to execute the decorated function.

```python
            try:
                return func(*args, **kwargs)
```

* The function `func` is executed with the provided arguments. If it succeeds, its result is immediately returned.

```python
            except Exception as e:
                print(f"Retry {i+1}: {e}")
                time.sleep(2)
```

* If an exception is raised during execution, it is caught and printed, indicating the retry attempt. A 2-second delay is introduced using `time.sleep()`.

```python
        raise Exception("Failed after 3 retries")
```

* If all three attempts fail, an exception is raised, indicating the failure.

```python
    return wrapper
```

* The `wrapper` function is returned, effectively replacing the original function with the retry logic.

### Applying the Retry Decorator

```python
@retry
```

* The `retry` decorator is applied to the `flaky()` function.

### Defining the Flaky Function

```python
def flaky():
```

* A function named `flaky` is defined to simulate unpredictable behavior.

```python
    if random.random() < 0.7:
        raise ValueError("Random failure")
```

* A random float between 0 and 1 is generated. If it is less than 0.7, a `ValueError` is raised, simulating a failure.

```python
    return "Success"
```

* If no exception is raised, the function returns "Success".

### Executing the Program

```python
print(flaky())
```

* The `flaky()` function is called, and its result is printed. If all retries fail, the exception message will be displayed.

## Example Output

```
Retry 1: Random failure
Retry 2: Random failure
Retry 3: Random failure
Exception: Failed after 3 retries
```

If the `flaky()` function succeeds within three attempts, the output will be:

```
Success
```

## Summary

* The program demonstrates how to implement a retry mechanism using decorators.
* It introduces basic error handling using `try/except` blocks and controlled delays using `time.sleep()`.
* This pattern is useful for functions that may occasionally fail and require re-execution, such as network requests or database operations.
