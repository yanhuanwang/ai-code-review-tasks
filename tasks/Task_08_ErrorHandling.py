#!/usr/bin/env python3
"""
Task 08: Error Handling and Exception Management Challenge

This file contains several intentional error handling and exception management issues
for code review practice. The task is to identify and fix the following issues:
1. Swallowed exceptions in DataProcessor
2. Overly broad exception handling in FileManager
3. Improper error propagation in APIClient
4. Missing error recovery in DatabaseManager
5. Inconsistent error handling in UserService
6. Improper exception hierarchy in CustomExceptions
7. Silent failures in CacheService
8. Improper error context in Logger

Review the code and identify these error handling and exception management issues.
"""

import os
import sys
import json
import time
import logging
import sqlite3
import requests
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import traceback
from pathlib import Path
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Improper exception hierarchy
class CustomError(Exception):
    """Base custom error."""
    pass

class DatabaseError(CustomError):
    """Database related error."""
    pass

class NetworkError(CustomError):
    """Network related error."""
    pass

# Bug: Missing proper exception hierarchy
class ValidationError(Exception):
    """Validation error."""
    pass

class DataProcessor:
    """
    Processes data from various sources.
    Bug: Swallowed exceptions and improper error handling.
    """
    def __init__(self):
        self.processed_data = []

    def process_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Process data from file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return self._process_data(data)
        except Exception as e:
            # Bug: Swallowed exception
            print(f"Error processing file: {e}")
            return []

    def _process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process the data."""
        try:
            result = []
            for item in data:
                # Bug: Silent failure in data processing
                if "value" in item:
                    item["processed_value"] = item["value"] * 2
                if "date" in item:
                    item["processed_date"] = item["date"].upper()
                result.append(item)
            return result
        except Exception:
            # Bug: Swallowed exception with no logging
            return []

class FileManager:
    """
    Manages file operations.
    Bug: Overly broad exception handling.
    """
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def read_file(self, filename: str) -> str:
        """Read file contents."""
        try:
            # Bug: Overly broad exception handling
            with open(self.base_path / filename, 'r') as f:
                return f.read()
        except Exception as e:
            # Bug: Generic exception handling
            logger.error(f"Error reading file: {e}")
            return ""

    def write_file(self, filename: str, content: str) -> bool:
        """Write content to file."""
        try:
            # Bug: Overly broad exception handling
            with open(self.base_path / filename, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            # Bug: Generic exception handling
            logger.error(f"Error writing file: {e}")
            return False

class APIClient:
    """
    Client for making API requests.
    Bug: Improper error propagation and recovery.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def get_data(self, endpoint: str) -> Dict[str, Any]:
        """Get data from API endpoint."""
        try:
            # Bug: No timeout or retry logic
            response = self.session.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            # Bug: Improper error propagation
            logger.error(f"API request failed: {e}")
            return {}  # Bug: Silent failure

    def post_data(self, endpoint: str, data: Dict[str, Any]) -> bool:
        """Post data to API endpoint."""
        try:
            # Bug: No timeout or retry logic
            response = self.session.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            # Bug: Improper error propagation
            logger.error(f"API request failed: {e}")
            return False

class DatabaseManager:
    """
    Manages database operations.
    Bug: Missing error recovery and improper transaction handling.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self) -> None:
        """Connect to database."""
        try:
            # Bug: No connection pooling or retry logic
            self.connection = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            # Bug: No proper error recovery
            logger.error(f"Database connection failed: {e}")
            raise

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a database query."""
        try:
            # Bug: No transaction management
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            # Bug: No proper error recovery
            logger.error(f"Query execution failed: {e}")
            return []
        finally:
            # Bug: No proper connection cleanup
            if cursor:
                cursor.close()

class UserService:
    """
    Manages user operations.
    Bug: Inconsistent error handling and improper error types.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Create a new user."""
        try:
            # Bug: Inconsistent error handling
            if not self._validate_email(email):
                raise ValueError("Invalid email format")

            # Bug: Mixed exception types
            if self._user_exists(username):
                raise CustomError("User already exists")

            user_data = {
                "username": username,
                "email": email,
                "created_at": datetime.now().isoformat()
            }

            # Bug: No transaction management
            self.db_manager.execute_query(
                "INSERT INTO users (username, email, created_at) VALUES (?, ?, ?)",
                (username, email, user_data["created_at"])
            )

            return user_data
        except ValueError as e:
            # Bug: Inconsistent error handling
            logger.error(f"Validation error: {e}")
            return {}
        except CustomError as e:
            # Bug: Inconsistent error handling
            logger.error(f"Custom error: {e}")
            return {}
        except Exception as e:
            # Bug: Generic exception handling
            logger.error(f"Unexpected error: {e}")
            return {}

class CacheService:
    """
    Manages caching operations.
    Bug: Silent failures and improper error handling.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Bug: Silent failure on key error
        return self._cache.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache."""
        try:
            # Bug: No validation of input parameters
            with self._lock:
                self._cache[key] = {
                    "value": value,
                    "expires_at": time.time() + ttl
                }
        except Exception as e:
            # Bug: Silent failure
            pass

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            # Bug: No error handling for missing key
            del self._cache[key]
            return True
        except KeyError:
            # Bug: Silent failure
            return False

class Logger:
    """
    Custom logging implementation.
    Bug: Improper error context and logging.
    """
    def __init__(self, log_file: str):
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        try:
            # Bug: No proper error context
            logging.basicConfig(
                filename=self.log_file,
                level=logging.INFO,
                format='%(asctime)s - %(message)s'
            )
        except Exception as e:
            # Bug: Improper error handling
            print(f"Error setting up logging: {e}")

    def log_error(self, message: str, error: Exception) -> None:
        """Log an error."""
        try:
            # Bug: Missing error context
            logging.error(f"{message}: {str(error)}")
        except Exception as e:
            # Bug: Improper error handling
            print(f"Error logging error: {e}")

    def log_info(self, message: str) -> None:
        """Log an info message."""
        try:
            # Bug: No proper error context
            logging.info(message)
        except Exception as e:
            # Bug: Improper error handling
            print(f"Error logging info: {e}")

def main():
    # Test DataProcessor swallowed exceptions
    print("Testing DataProcessor swallowed exceptions:")
    processor = DataProcessor()
    result = processor.process_file("nonexistent.json")
    print(f"Process result: {result}")  # Should handle error properly

    # Test FileManager overly broad exception handling
    print("\nTesting FileManager overly broad exception handling:")
    file_manager = FileManager("nonexistent_dir")
    content = file_manager.read_file("test.txt")
    print(f"File content: {content}")  # Should handle specific exceptions

    # Test APIClient error propagation
    print("\nTesting APIClient error propagation:")
    client = APIClient("http://nonexistent-api.example.com")
    data = client.get_data("users")
    print(f"API data: {data}")  # Should propagate errors properly

    # Test DatabaseManager error recovery
    print("\nTesting DatabaseManager error recovery:")
    db_manager = DatabaseManager("nonexistent.db")
    try:
        db_manager.connect()
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")  # Should handle error properly

    # Test UserService inconsistent error handling
    print("\nTesting UserService inconsistent error handling:")
    user_service = UserService(db_manager)
    result = user_service.create_user("testuser", "invalid-email")
    print(f"User creation result: {result}")  # Should handle errors consistently

    # Test CacheService silent failures
    print("\nTesting CacheService silent failures:")
    cache = CacheService()
    cache.set("test_key", "test_value")
    value = cache.get("nonexistent_key")
    print(f"Cache value: {value}")  # Should handle missing keys properly

    # Test Logger improper error context
    print("\nTesting Logger improper error context:")
    logger = Logger("nonexistent_dir/log.txt")
    try:
        raise ValueError("Test error")
    except ValueError as e:
        logger.log_error("Test error occurred", e)  # Should provide proper error context

    # Test custom exception hierarchy
    print("\nTesting custom exception hierarchy:")
    try:
        raise ValidationError("Invalid data")
    except CustomError as e:
        print(f"Caught custom error: {e}")  # Should not catch ValidationError
    except ValidationError as e:
        print(f"Caught validation error: {e}")  # Should catch ValidationError

if __name__ == "__main__":
    main()