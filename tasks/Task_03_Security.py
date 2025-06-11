#!/usr/bin/env python3
"""
Task 03: Security Vulnerability Detection Challenge

This file contains several intentional security vulnerabilities for code review practice.
The task is to identify and fix the following issues:
1. Command injection in execute_command
2. Insecure password hashing in create_user
3. Path traversal vulnerability in read_file
4. Insecure deserialization in load_user_data
5. Hardcoded credentials in database connection
6. XSS vulnerability in format_user_message

Review the code and identify these security issues.
"""

import os
import sys
import json
import hashlib
import pickle
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path
import sqlite3
import html

# Global configuration (intentional security issue)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'super_secret_password123',  # Bug: Hardcoded credentials
    'database': 'users.db'
}

def execute_command(command: str) -> str:
    """
    Execute a system command and return the output.
    Bug: Command injection vulnerability - unsanitized input.
    """
    # Bug: Direct command execution without sanitization
    return subprocess.check_output(command, shell=True).decode()  # Bug: shell=True and no input validation

def create_user(username: str, password: str) -> Dict[str, Any]:
    """
    Create a new user in the system.
    Bug: Insecure password hashing - using MD5 and no salt.
    """
    # Bug: Using MD5 (cryptographically broken) and no salt
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    user_data = {
        'username': username,
        'password': hashed_password,  # Bug: Should use proper password hashing
        'created_at': '2024-03-20'
    }

    # Save user data (insecure storage)
    with open(f'users/{username}.json', 'w') as f:  # Bug: No path sanitization
        json.dump(user_data, f)

    return user_data

def read_file(filename: str) -> str:
    """
    Read a file from the filesystem.
    Bug: Path traversal vulnerability - no path sanitization.
    """
    # Bug: No path sanitization, allows directory traversal
    file_path = os.path.join('data', filename)
    with open(file_path, 'r') as f:
        return f.read()

def load_user_data(data: bytes) -> Dict[str, Any]:
    """
    Load user data from serialized format.
    Bug: Insecure deserialization - using pickle.
    """
    # Bug: Using pickle for deserialization (allows arbitrary code execution)
    return pickle.loads(data)

def get_database_connection() -> sqlite3.Connection:
    """
    Create a database connection.
    Bug: Hardcoded credentials and no connection pooling.
    """
    # Bug: Using hardcoded credentials from global config
    return sqlite3.connect(
        f"file:{DB_CONFIG['database']}?mode=rw",
        uri=True
    )

def format_user_message(username: str, message: str) -> str:
    """
    Format a user message for display.
    Bug: XSS vulnerability - no HTML escaping.
    """
    # Bug: No HTML escaping, allows XSS attacks
    return f"<div class='message'><strong>{username}</strong>: {message}</div>"

def main():
    # Test command injection
    print("Testing command injection:")
    try:
        # This should be sanitized
        result = execute_command("echo 'test'; rm -rf /")  # Dangerous command
        print(f"Command result: {result}")
    except Exception as e:
        print(f"Command execution error: {e}")

    # Test password hashing
    print("\nTesting password hashing:")
    try:
        user = create_user("testuser", "password123")
        print(f"Created user: {user}")
        # Demonstrate how easy it is to crack MD5
        cracked_hash = hashlib.md5("password123".encode()).hexdigest()
        print(f"Password hash: {user['password']}")
        print(f"Cracked hash: {cracked_hash}")
    except Exception as e:
        print(f"User creation error: {e}")

    # Test path traversal
    print("\nTesting path traversal:")
    try:
        # This should be prevented
        content = read_file("../../../etc/passwd")
        print(f"File content: {content[:100]}...")
    except Exception as e:
        print(f"File reading error: {e}")

    # Test insecure deserialization
    print("\nTesting insecure deserialization:")
    try:
        # Create a malicious pickle object
        class Malicious:
            def __reduce__(self):
                return (os.system, ('echo "Malicious code executed"',))

        malicious_data = pickle.dumps(Malicious())
        # This should be prevented
        result = load_user_data(malicious_data)
        print(f"Deserialized data: {result}")
    except Exception as e:
        print(f"Deserialization error: {e}")

    # Test XSS vulnerability
    print("\nTesting XSS vulnerability:")
    try:
        # This should be escaped
        malicious_message = "<script>alert('XSS')</script>"
        formatted = format_user_message("attacker", malicious_message)
        print(f"Formatted message: {formatted}")
        # Show how it would be rendered in a browser
        print("If rendered in browser, would execute the script")
    except Exception as e:
        print(f"Message formatting error: {e}")

    # Test database connection
    print("\nTesting database connection:")
    try:
        conn = get_database_connection()
        print("Database connection successful")
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('users', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    main()