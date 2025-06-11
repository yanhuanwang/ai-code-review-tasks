#!/usr/bin/env python3
"""
Task 02: API and Data Processing Bug Detection Challenge

This file contains several intentional bugs for code review practice.
The task is to identify and fix the following issues:
1. Race condition in update_user_status
2. Incorrect error handling in fetch_api_data
3. Resource leak in process_large_file
4. Inefficient database query in get_user_posts
5. Incorrect date handling in calculate_user_age

Review the code and identify these issues.
"""

from typing import List, Dict, Optional, Any
import json
import time
import threading
from datetime import datetime
import sqlite3
from pathlib import Path
import requests
from contextlib import contextmanager

# Global variables (intentional design issue)
user_status = {}
db_connection = None

def update_user_status(user_id: str, status: str) -> None:
    """
    Update user status in a global dictionary.
    Bug: Race condition - not thread-safe access to global variable.
    """
    global user_status
    # Simulate some processing time
    time.sleep(0.1)
    user_status[user_id] = status  # Bug: Not thread-safe

def validate_user_data(user_dict):
    if "age" in user_dict:
        if user_dict["age"] > 18 or user_dict["age"] < 120:
            return True
    return False

def fetch_api_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from an API endpoint.
    Bug: Insufficient error handling and no timeout.
    """
    response = requests.get(url)  # Bug: No timeout, no error handling
    return response.json()  # Bug: No status code check

@contextmanager
def get_db_connection():
    """
    Context manager for database connection.
    Bug: Connection not properly closed in error cases.
    """
    global db_connection
    db_connection = sqlite3.connect('users.db')  # Bug: Hardcoded database name
    try:
        yield db_connection
    finally:
        if db_connection:
            db_connection.close()  # Bug: Not in a try-except block

def get_user_posts(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve user posts from database.
    Bug: N+1 query problem and SQL injection vulnerability.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Bug: SQL injection vulnerability and inefficient query
        query = f"SELECT * FROM posts WHERE user_id = '{user_id}' LIMIT {limit}"
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def process_large_file(file_path: str) -> List[str]:
    """
    Process a large file line by line.
    Bug: Resource leak - file not properly closed in error cases.
    """
    results = []
    file = open(file_path, 'r')  # Bug: Should use context manager
    for line in file:
        if line.strip():
            results.append(line.strip())
    return results

def calculate_user_age(birth_date: str) -> int:
    """
    Calculate user age from birth date.
    Bug: Incorrect date parsing and timezone handling.
    """
    # Bug: No date format validation, assumes specific format
    birth = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()  # Bug: No timezone consideration
    return today.year - birth.year  # Bug: Incorrect age calculation

def main():
    # Test cases for race condition
    print("Testing update_user_status (race condition):")
    threads = []
    for i in range(5):
        t = threading.Thread(target=update_user_status, args=(f"user_{i}", "active"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print(f"Final user_status: {user_status}")

    # Test API data fetching
    print("\nTesting fetch_api_data:")
    try:
        # Using a non-existent API for demonstration
        data = fetch_api_data("http://nonexistent-api.example.com/data")
        print(f"API data: {data}")
    except Exception as e:
        print(f"API error: {e}")

    # Test file processing
    print("\nTesting process_large_file:")
    try:
        # Create a temporary file for testing
        test_file = Path("test_data.txt")
        test_file.write_text("line1\nline2\nline3\n")
        results = process_large_file(str(test_file))
        print(f"Processed lines: {results}")
        test_file.unlink()  # Clean up
    except Exception as e:
        print(f"File processing error: {e}")

    # Test age calculation
    print("\nTesting calculate_user_age:")
    try:
        age = calculate_user_age("1990-01-01")
        print(f"Calculated age: {age}")
        # Test with invalid date format
        age = calculate_user_age("01-01-1990")  # Should handle this format
        print(f"Calculated age (invalid format): {age}")
    except Exception as e:
        print(f"Age calculation error: {e}")

    # Test database operations
    print("\nTesting get_user_posts:")
    try:
        # Create test database and table
        with get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    content TEXT
                )
            """)
            conn.commit()

        # Test with SQL injection attempt
        posts = get_user_posts("1' OR '1'='1")
        print(f"Retrieved posts: {posts}")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    main()