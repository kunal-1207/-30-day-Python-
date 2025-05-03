# Day 3
# Challenge: Build a simple calculator (add, subtract).
# Focus: CLI input, functions
# Example Hint: Handle invalid inputs

def calculator():
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+ or -): ")
        b = float(input("Enter second number: "))
        if op == '+':
            print(f"Result: {a + b}")
        elif op == '-':
            print(f"Result: {a - b}")
        else:
            print("Invalid operator")
    except ValueError:
        print("Invalid input")

calculator()

