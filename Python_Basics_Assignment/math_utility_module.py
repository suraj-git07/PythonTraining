"""
Math utility functions module.
This module provides various mathematical utility functions
"""

import math


def calculate_area_circle(radius):
    """
    Calculate the area of a circle.
    - takes radius(float) as an argument
    - returns the area of circle (float)
    - raise a ValueError, if radius is negative
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    return math.pi * radius ** 2


def calculate_area_rectangle(length, width):
    """
    Calculate the area of a rectangle.
    - takes length (float) & width (float) as an argument
    - returns the area of rectangle (float)
    - raise a ValueError, if length or width is negative
    
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative")
    return length * width


def factorial(n):
    """
    Calculate the factorial of a number.
    - takes n (int) as an argument
    - returns  the factorial of n(int)
    - raise a ValueError, if n is negative or not an integer
    """
    if not (type(n) == int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n):
    """
    Check if a number is prime.
    - takes n (int): The number to check
    - Returns, True if the number is prime, False otherwise
    """
    if  not (type(n) == int) or n < 0:
        return False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


