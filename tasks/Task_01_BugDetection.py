#!/usr/bin/env python3
"""
Task 01: Bug Detection Challenge

This file contains several intentional bugs for code review practice.
The task is to identify and fix the following issues:
1. Logic error in the calculate_discount function
2. Potential division by zero in calculate_average
3. Incorrect string comparison in validate_user
4. Memory leak in process_data
5. Incorrect list comprehension in filter_even_numbers

Review the code and identify these issues.
"""

from typing import List, Dict, Optional
import time
from datetime import datetime

def calculate_discount(price: float, discount_percentage: float) -> float:
    """
    Calculate the discounted price.
    Bug: Incorrect discount calculation - subtracts discount from original price
    instead of applying percentage.
    """
    return price - discount_percentage  # Bug: Should be price * (1 - discount_percentage/100)

def calculate_average(numbers: List[float]) -> float:
    """
    Calculate the average of a list of numbers.
    Bug: No check for empty list, could cause division by zero.
    """
    return sum(numbers) / len(numbers)  # Bug: Should check if numbers is empty

def validate_user(username: str, password: str) -> bool:
    """
    Validate user credentials.
    Bug: Case-sensitive string comparison that should be case-insensitive.
    """
    valid_username = "admin"
    valid_password = "password123"
    return username == valid_username and password == valid_password  # Bug: Should use .lower()

def process_data(data: List[Dict]) -> List[Dict]:
    """
    Process a list of dictionaries.
    Bug: Memory leak due to growing list in loop.
    """
    result = []
    for item in data:
        # Bug: Creates new list in each iteration
        result = result + [item]  # Should use result.append(item)
        time.sleep(0.1)  # Simulate processing
    return result

def filter_even_numbers(numbers: List[int]) -> List[int]:
    """
    Filter even numbers from a list.
    Bug: Incorrect list comprehension syntax.
    """
    return [x for x in numbers if x % 2 = 0]  # Bug: Should be == instead of =

def main():
    # Test cases
    print("Testing calculate_discount:")
    print(f"Price: 100, Discount: 20% -> {calculate_discount(100, 20)}")  # Should be 80.0

    print("\nTesting calculate_average:")
    try:
        print(f"Average of [1, 2, 3] -> {calculate_average([1, 2, 3])}")
        print(f"Average of [] -> {calculate_average([])}")  # Should handle empty list
    except ZeroDivisionError:
        print("Error: Division by zero")

    print("\nTesting validate_user:")
    print(f"Valid credentials -> {validate_user('admin', 'password123')}")
    print(f"Case-insensitive test -> {validate_user('ADMIN', 'PASSWORD123')}")  # Should be True

    print("\nTesting process_data:")
    test_data = [{'id': i} for i in range(3)]
    result = process_data(test_data)
    print(f"Processed {len(result)} items")

    print("\nTesting filter_even_numbers:")
    try:
        numbers = [1, 2, 3, 4, 5, 6]
        print(f"Even numbers from {numbers} -> {filter_even_numbers(numbers)}")
    except SyntaxError:
        print("Error: Syntax error in list comprehension")

if __name__ == "__main__":
    main()