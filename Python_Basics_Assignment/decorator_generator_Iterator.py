"""

This script demonstrates the use of:
- Decorators: Wrapping a function to print its name before execution.
- Generators: Yielding sequences of values using the `yield` keyword.
- Iterators: Creating a custom iterable class that mimics counting behavior.

Sections:
- Decorator functions and usage
- Generator functions for counting and fruits
- Custom iterator class with manual and for-loop iteration
"""

# ------------------------ DECORATOR ------------------------

def print_name(func):
    """
    A simple decorator that prints the name of the function before calling it.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The wrapped function with additional print behavior.
    """
    def wrapper():
        print(f"Calling function: {func.__name__}")
        return func()
    return wrapper

@print_name
def say_hello():
    """
    A simple decorated function that returns a greeting.

    Returns:
        str: A greeting message.
    """
    return "Hello World!"

@print_name
def get_number():
    """
    A decorated function that returns a number.

    Returns:
        int: The number 42.
    """
    return 42

# ------------------------ GENERATOR ------------------------

def count_up_to(max_num):
    """
    A generator that yields numbers from 1 up to a specified maximum.

    Args:
        max_num (int): The maximum number to count up to.

    Yields:
        int: The next number in the sequence.
    """
    num = 1
    while num <= max_num:
        yield num
        num += 1

def get_fruits():
    """
    A generator that yields a list of fruit names.

    Yields:
        str: The next fruit in the list.
    """
    fruits = ["apple", "banana", "orange"]
    for fruit in fruits:
        yield fruit

# ------------------------ ITERATOR ------------------------

class SimpleCounter:
    """
    A custom iterator that counts from 1 to a specified maximum number.

    Attributes:
        max_count (int): The maximum number to count up to.
        current (int): The current number in the iteration.
    """

    def __init__(self, max_count):
        """
        Initializes the counter.

        Args:
            max_count (int): The upper limit of the counter.
        """
        self.max_count = max_count
        self.current = 0

    def __iter__(self):
        """
        Returns the iterator object itself.

        Returns:
            SimpleCounter: The iterator instance.
        """
        return self

    def __next__(self):
        """
        Returns the next number in the count.

        Returns:
            int: The next count value.

        Raises:
            StopIteration: When the counter exceeds the maximum limit.
        """
        if self.current >= self.max_count:
            raise StopIteration
        self.current += 1
        return self.current

# ------------------------ MAIN EXECUTION ------------------------

# USING DECORATOR
print("DECORATOR")
message = say_hello()
print(message)

number = get_number()
print(f"Got number: {number}")

# USING GENERATOR
print("\nGENERATOR")
print("Counting up to 5:")
for num in count_up_to(5):
    print(num, end=" ")

print("\nFruits:")
for fruit in get_fruits():
    print(fruit)

# USING ITERATOR
print("\nITERATOR")
print("Simple counter up to 4:")
counter = SimpleCounter(4)
for count in counter:
    print(count, end=" ")

print("\nUsing next() manually:")
counter2 = SimpleCounter(3)
print(next(counter2))  
print(next(counter2))  
print(next(counter2))  
