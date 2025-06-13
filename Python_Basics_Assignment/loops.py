"""Demonstrates various Python loop constructs and their applications.

This module showcases different types of loops in Python, including for loops,
while loops, and loop control statements (break and continue). It includes examples
of iterating over ranges and lists, generating a multiplication table, producing
a Fibonacci sequence, and using loop control to filter numbers.

"""

print("LOOPS")


# 1. FOR LOOPS
print("\nFOR LOOPS")

# range
for i in range(5):
    print(f"Count: {i}")

# List iteration
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"Fruit: {fruit}")


# 2. WHILE LOOPS
print("\n WHILE LOOPS")

count = 1
while count <= 5:
    print(f"count: {count}")
    count += 1

# 3. TABLE
print("\n TABLE")

num = 5
for i in range(1, 11):
    print(f"{num} × {i} = {num * i}")

# 4. FIBONACCI SEQUENCE
print("\nFIBONACCI SEQUENCE")

n = 8
a, b = 0, 1
print(f"First {n} Fibonacci numbers:")
for i in range(1,n+1):
    if i <= 2:
        if(i==1):
            print(a, end=" ")
        else:
            print(b, end=" ")
    else:
        c = a + b
        print(c, end=" ")
        a, b = b, c
print()


# 5. LOOP CONTROL (BREAK & CONTINUE)
print("\n LOOP CONTROL")

# Find first even number > 10
for num in range(11, 20):
    if num % 2 != 0:
        continue  # Skip odd numbers
    print(f"First even number > 10: {num}")
    break

# Skip multiples of 3
print("Numbers 1-10 (skip multiples of 3):")
for i in range(1, 11):
    if i % 3 == 0:
        continue
    print(i, end=" ")
print()
