"""
This script demonstrates object-oriented programming in Python using classes and inheritance.

Classes:
- Person: Base class representing a person.
- Student: Subclass that inherits from Person and adds student-specific attributes.

Includes methods to display and update information.
"""

class Person:
    """
    A class representing a person.

    Attributes:
        name (str): Name of the person.
        age (int): Age of the person.
        email (str): Email address of the person.
    """
    
    def __init__(self, name, age, email):
        """
        Initialize a Person instance.

        Args:
            name (str): Person's name.
            age (int): Person's age.
            email (str): Person's email.
        """
        self.name = name
        self.age = age
        self.email = email
    
    def display_info(self):
        """
        Display person's information.
        """
        print(f"Name: {self.name}, Age: {self.age}, Email: {self.email}")
    
    def update_age(self, new_age):
        """
        Update the person's age.

        Args:
            new_age (int): The new age to update.
        """
        self.age = new_age


class Student(Person):
    """
    A class representing a student, inherited from Person.

    Attributes:
        student_id (str): Unique student identifier.
        grade (str): Academic grade of the student.
    """
    
    def __init__(self, name, age, email, student_id, grade):
        """
        Initialize a Student instance using the Person attributes plus student-specific fields.

        Args:
            name (str): Student's name.
            age (int): Student's age.
            email (str): Student's email.
            student_id (str): Unique student ID.
            grade (str): Grade assigned to the student.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.grade = grade
    
    def display_info(self):
        """
        Display student information, including inherited and specific attributes.
        """
        super().display_info()
        print(f"Student ID: {self.student_id}, Grade: {self.grade}")
    
    def update_grade(self, new_grade):
        """
        Update the student's grade.

        Args:
            new_grade (str): The new grade to update.
        """
        self.grade = new_grade


# Demo usage
if __name__ == "__main__":
    person1 = Person("Suraj Mishra", 22, "surajmishra@email.com")
    student1 = Student("Aditya Raj", 23, "adity@email.com", "S1", "A+")

    print("Person Information:")
    person1.display_info()

    print("\nStudent Information:")
    student1.display_info()

    print("\nAfter updates:")
    person1.update_age(31)
    student1.update_grade("O")

    person1.display_info()
    print()
    student1.display_info()
