"""Demonstrates Python operators and expressions with interactive output.

This module showcases various Python operators including arithmetic, comparison,
logical, bitwise, assignment, identity, and membership operators. It uses predefined
variables to illustrate their functionality through console output, including binary
representations for bitwise operations.

"""

# Headline for the script
print("PYTHON OPERATORS AND EXPRESSIONS DEMONSTRATION")

# Variables for demonstration of different operators
a = 15
b = 4
x = True
y = False
num1 = 12
num2 = 10

print("\nLet we have some variable:")
print(f"a = {a}, b = {b}")
print(f"x = {x}, y = {y}")
print(f"num1 = {num1}, in binary: {bin(num1)}")
print(f"num2 = {num2}, in binary: {bin(num2)}")

# 1. ARITHMETIC OPERATORS
print("\nARITHMETIC OPERATORS")
print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Floor Division: {a} // {b} = {a // b}")
print(f"Modulus: {a} % {b} = {a % b}")
print(f"Exponentiation: {a} ** {b} = {a ** b}")

# 2. COMPARISON OPERATORS
print("\nCOMPARISON OPERATORS")
print(f"Equal to: {a} == {b} is {a == b}")
print(f"Not equal to: {a} != {b} is {a != b}")
print(f"Greater than: {a} > {b} is {a > b}")
print(f"Less than: {a} < {b} is {a < b}")
print(f"Greater than or equal: {a} >= {b} is {a >= b}")
print(f"Less than or equal: {a} <= {b} is {a <= b}")

# 3. LOGICAL OPERATORS
print("\nLOGICAL OPERATORS")
print(f"AND: {x} and {y} = {x and y}")
print(f"OR: {x} or {y} = {x or y}")
print(f"NOT: not {x} = {not x}")

# 4. BITWISE OPERATORS
print("\nBITWISE OPERATORS")
print("Binary representation:")
print(f"num1 = {num1} = {bin(num1)}")
print(f"num2 = {num2} = {bin(num2)}")
print()

and_result = num1 & num2
or_result = num1 | num2
xor_result = num1 ^ num2
not_result = ~num1
left_shift = num1 << 2
right_shift = num1 >> 2

print(f"Bitwise AND: {num1} & {num2} = {and_result} ({bin(and_result)})")
print(f"Bitwise OR: {num1} | {num2} = {or_result} ({bin(or_result)})")
print(f"Bitwise XOR: {num1} ^ {num2} = {xor_result} ({bin(xor_result)})")
print(f"Bitwise NOT: ~{num1} = {not_result} ({bin(not_result)})")
print(f"Left Shift: {num1} << 2 = {left_shift} ({bin(left_shift)})")
print(f"Right Shift: {num1} >> 2 = {right_shift} ({bin(right_shift)})")

# 5. ASSIGNMENT OPERATORS
print("\nASSIGNMENT OPERATORS")
# Using copies of original variables
temp_a = a
temp_b = b

print(f"Initial: temp_a = {temp_a}")

temp_a += 5
print(f"After += 5: temp_a = {temp_a}")

temp_a -= 3
print(f"After -= 3: temp_a = {temp_a}")

temp_a *= 2
print(f"After *= 2: temp_a = {temp_a}")

temp_a //= 3
print(f"After //= 3: temp_a = {temp_a}")

temp_a %= 7
print(f"After %= 7: temp_a = {temp_a}")

temp_a **= 2
print(f"After **= 2: temp_a = {temp_a}")

# 6. IDENTITY AND MEMBERSHIP OPERATORS
print("\nIDENTITY AND MEMBERSHIP OPERATORS")
list1 = [1, 2, 3, 4, 5]
list2 = [1, 2, 3, 4, 5]
list3 = list1

print(f"list1 = {list1}")
print(f"list2 = {list2}")
print(f"list3 = list1 (create a reference to the same object)")
print()

# Identity operators
print("Identity operators (is, is not):")
print(f"list1 is list2: {list1 is list2}")  # False - as they are different objects
print(f"list1 is list3: {list1 is list3}")  # True - as they are referencing the same object in memory

# Membership operators
print("Membership operators (in, not in):")
print(f"3 in list1: {3 in list1}")
print(f"7 not in list1: {7 not in list1}")
