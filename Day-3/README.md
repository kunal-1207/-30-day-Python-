# Simple Calculator Program

## Overview

This program is a simple command-line interface (CLI) calculator that performs basic arithmetic operations (addition and subtraction). It allows users to input two numbers and select an operator (`+` or `-`). The program will then display the result of the calculation. Additionally, it handles invalid inputs gracefully by providing error messages.

## Purpose

This project is part of a coding challenge focused on learning how to accept user input through the CLI, define and use functions, and handle exceptions effectively.

## How to Use the Program

1. Run the program using a Python interpreter.
2. Enter the first number when prompted.
3. Enter the operator (`+` for addition or `-` for subtraction).
4. Enter the second number.
5. The program will calculate and display the result.

### Example:

```
Enter first number: 10
Enter operator (+ or -): +
Enter second number: 5
Result: 15.0
```

## Code Breakdown

### 1. Defining the Function

```python
def calculator():
```

* Defines a function named `calculator`. This function will handle the entire calculation process, from input collection to output display.

### 2. Exception Handling

```python
    try:
```

* Begins a `try` block to handle potential exceptions (e.g., invalid inputs).

### 3. Input Collection

```python
        a = float(input("Enter first number: "))
```

* Prompts the user to input the first number and converts it to a float. This allows for decimal inputs.

```python
        op = input("Enter operator (+ or -): ")
```

* Prompts the user to input the operator (`+` or `-`).

```python
        b = float(input("Enter second number: "))
```

* Prompts the user to input the second number and converts it to a float.

### 4. Conditional Logic

```python
        if op == '+':
            print(f"Result: {a + b}")
```

* If the operator is `+`, the program calculates and displays the sum of the two numbers.

```python
        elif op == '-':
            print(f"Result: {a - b}")
```

* If the operator is `-`, the program calculates and displays the difference between the two numbers.

```python
        else:
            print("Invalid operator")
```

* If the operator is not `+` or `-`, the program displays an error message.

### 5. Exception Handling

```python
    except ValueError:
        print("Invalid input")
```

* If a `ValueError` occurs (e.g., if the user inputs non-numeric data), the program will print an error message.

### 6. Function Invocation

```python
calculator()
```

* Calls the `calculator()` function to execute the program.

## Future Enhancements

* Add support for additional arithmetic operations (multiplication, division).
* Implement input validation for operators.
* Include a loop to allow multiple calculations without restarting the program.
