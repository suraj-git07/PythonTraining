"""
This script demonstrates the use of Python's built-in collection types:
- Lists
- Tuples
- Sets
- Dictionaries

Each section contains creation, manipulation, and key operations for better understanding.
Use this as a reference to explore how collections work in Python.
"""

def demonstrate_lists():
    """
    Demonstrates list creation, manipulation, and common operations.

    Operations shown:
    - Append, insert, remove, pop
    - Slicing
    - Handling mixed-type lists
    """
    print("\nLISTS")
   
    fruits = ['apple', 'banana', 'orange', 'apple']
    numbers = [1, 2, 3, 4, 5]
    mixed_list = ['hello', 42, 3.14, True]
    
    print(f"Fruits list: {fruits}")
    print(f"Numbers list: {numbers}")
    print(f"Mixed list: {mixed_list}")
    
    fruits.append('grape')
    print(f"After append: {fruits}")
    
    fruits.insert(1, 'mango')
    print(f"After insert at index 1: {fruits}")
    
    fruits.remove('apple')
    print(f"After removing 'apple': {fruits}")
    
    popped = fruits.pop()
    print(f"Popped element: {popped}")
    print(f"List after pop: {fruits}")
    
    print(f"First 3 fruits: {fruits[:3]}")
    print(f"Last 2 fruits: {fruits[-2:]}")


def demonstrate_tuples():
    """
    Demonstrates tuple creation and operations.

    Operations shown:
    - Accessing elements
    - Tuple unpacking
    - Tuple methods: count and index
    """
    print("\nTUPLES")
    
    coordinates = (10, 20)
    colors = ('red', 'green', 'blue', 'red')
    single_tuple = (42,)
    empty_tuple = ()
    
    print(f"Coordinates: {coordinates}")
    print(f"Colors: {colors}")
    print(f"Single element tuple: {single_tuple}")
    print(f"Empty tuple: {empty_tuple}")
    
    print(f"First coordinate: {coordinates[0]}")
    print(f"Second coordinate: {coordinates[1]}")
    
    x, y = coordinates
    print(f"Unpacked - x: {x}, y: {y}")
    
    print(f"Count of 'red' in colors: {colors.count('red')}")
    print(f"Index of 'blue': {colors.index('blue')}")


def demonstrate_sets():
    """
    Demonstrates set creation and operations.

    Operations shown:
    - Adding and discarding elements
    - Set arithmetic: union, intersection, difference
    """
    print("\nSETS")
    
    unique_numbers = {1, 2, 3, 4, 5}
    fruits_set = {'apple', 'banana', 'orange', 'apple'}
    empty_set = set() 
    
    print(f"Unique numbers: {unique_numbers}")
    print(f"Fruits set (duplicates removed): {fruits_set}")
    print(f"Empty set: {empty_set}")
    
    fruits_set.add('grape')
    print(f"After adding grape: {fruits_set}")
    
    fruits_set.discard('banana')
    print(f"After discarding banana: {fruits_set}")
    
    set1 = {1, 2, 3, 4}
    set2 = {3, 4, 5, 6}
    
    print(f"Set 1: {set1}")
    print(f"Set 2: {set2}")
    print(f"Union (|): {set1 | set2}")
    print(f"Intersection (&): {set1 & set2}")
    print(f"Difference (-): {set1 - set2}")


def demonstrate_dictionaries():
    """
    Demonstrates dictionary creation and operations.

    Operations shown:
    - Accessing values
    - Adding and updating key-value pairs
    - Using dictionary methods: keys(), values(), items()
    """
    print("\nDICTIONARIES")
    
    student = {
        'name': 'Alice',
        'age': 20,
        'grade': 'A',
        'subjects': ['Math', 'Physics', 'Chemistry']
    }
    
    empty_dict = {}
    
    print(f"Student dict: {student}")
    
    print(f"Student name: {student['name']}")
    print(f"Student age: {student.get('age', 'default')}")
    
    student['email'] = 'alice@email.com'
    student['age'] = 21
    print(f"After updates: {student}")
    
    print(f"Keys: {list(student.keys())}")
    print(f"Values: {list(student.values())}")
    print(f"Items: {list(student.items())}")


def main():
    """
    Calls all demonstration functions for collections.

    This will run only if the script is executed directly,
    not when imported as a module.
    """
    print("PYTHON COLLECTIONS")
    
    demonstrate_lists()
    demonstrate_tuples()
    demonstrate_sets()
    demonstrate_dictionaries()


if __name__ == "__main__":
    main()  # Ensures main() only runs when this script is directly executed
