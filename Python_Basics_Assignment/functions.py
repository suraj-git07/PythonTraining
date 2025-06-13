"""

This script provides functionality to generate Fibonacci sequences using both
explicit parameter passing and default argument usage. It demonstrates basic
function usage and default parameters in Python.

Functions:
- generate_fib(n): Returns the Fibonacci sequence up to n terms.
- generate_fib_default(n=5): Returns the Fibonacci sequence with default 5 terms.
"""

# Function to generate Fibonacci series up to n terms
def generate_fib(n):
    """
    Generates a list containing the Fibonacci sequence up to n terms.
    """
    fib_series = []
    a, b = 0, 1
    for i in range(n):
        fib_series.append(a)
        a, b = b, a + b
    return fib_series

# Function to generate Fibonacci with default value (default argument)
def generate_fib_default(n=5):
    """
    Generates a default Fibonacci sequence of 5 terms if no argument is passed.
    """
    return generate_fib(n)


print("Generate fib sequence for n = 7:")
print(generate_fib(7))  # Parameter passing

print("\nGenerate default fib sequence:")
print(generate_fib_default())  # Default argument

