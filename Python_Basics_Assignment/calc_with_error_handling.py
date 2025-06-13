"""
This script demonstrates the use of the custom `math_utility_module` which includes:
- Calculating area of a circle and rectangle
- Finding the factorial of a number
- Checking if a number is prime
- Error handling for invalid inputs

The module is imported with an alias `math_utils` for convenience.
"""

import math_utility_module as math_utils

# Demonstrating calculations
print("Calculations")

circle_radius = 5.0
circle_area = math_utils.calculate_area_circle(circle_radius)
print(f"Area of circle with radius {circle_radius}: {circle_area}")

rectangle_length = 8.0
rectangle_width = 6.0
rectangle_area = math_utils.calculate_area_rectangle(rectangle_length, rectangle_width)
print(f"Area of rectangle ({rectangle_length} x {rectangle_width}): {rectangle_area}")

number = 7
factorial_result = math_utils.factorial(number)
print(f"Factorial of {number}: {factorial_result}")

test_number = 17
is_prime_result = math_utils.is_prime(test_number)
print(f"Is {test_number} prime? {is_prime_result}")

# Bonus: Demonstrate error handling
print("\nError Handling")

try:
    print("Calculate area of circle with negative radius...")
    negative_area = math_utils.calculate_area_circle(-5)
except ValueError as e:
    print(f"ValueError caught: {e}")
except TypeError as e:
    print(f"TypeError caught: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("Successfully calculated area.")
finally:
    print("Finished circle area calculation with error check.")
