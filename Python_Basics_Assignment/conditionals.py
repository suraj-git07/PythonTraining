"""
This script demonstrates the use of conditional statements in Python through:
1. Age categorization using if-elif-else
2. Palindrome checking
3. Grade calculation based on score

Each section prints relevant outputs for better understanding of how conditions work.
"""

print("CONDITIONAL STATEMENTS DEMONSTRATION")

# ------------------------ IF-ELIF-ELSE ------------------------
print("\nIF-ELIF-ELSE")

age = 20
print(f"Age: {age}")

if age < 13:
    category = "Child"
elif age < 20:
    category = "Teenager"
elif age < 60:
    category = "Adult"
else:
    category = "Senior"

print(f"Category: {category}")

# ------------------------ PALINDROME CHECK ------------------------
print("\nPALINDROME CHECK")

def check_palindrome(text):
    """
    Checks if the input string is a palindrome (reads the same backward and forward).

    Args:
        text (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    reversed_text = text[::-1]

    print(f"Original text: '{text}'")
    print(f"Reversed text: '{reversed_text}'")

    if text == reversed_text:
        print(f"'{text}' is a PALINDROME!")
        return True
    else:
        print(f"'{text}' is NOT a palindrome.")
        return False

# Testing palindrome checker
test_words = ["naman", "suraj", "racecar"]

for word in test_words:
    check_palindrome(word)
    print()

# ------------------------ GRADE CALCULATOR ------------------------
print("\nGRADE CALCULATOR")

def calculate_grade(score):
    """
    Calculates a grade based on a numeric score.

    Args:
        score (int): The score to evaluate (expected between 0 and 100).

    Returns:
        str: The grade letter ('A', 'B', 'C', 'D', 'F', or 'Invalid').
    """
    print(f"Score: {score}")

    if score < 0 or score > 100:
        grade = "Invalid"
        message = "Score must be between 0 and 100"
    elif score >= 90:
        grade = "A"
        message = "Excellent"
    elif score >= 80:
        grade = "B"
        message = "Good job"
    elif score >= 70:
        grade = "C"
        message = "Satisfactory"
    elif score >= 60:
        grade = "D"
        message = "Needs improvement"
    else:
        grade = "F"
        message = "Failed"

    print(f"Grade: {grade}")
    print(f"Message: {message}")
    return grade

# Testing grade calculator
test_scores = [95, 87, 73, 65, 45, 102, -5]

for score in test_scores:
    calculate_grade(score)
    print()
