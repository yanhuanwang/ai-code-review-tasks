#!/usr/bin/env python3
"""
Task 13: Code Documentation and Comments Challenge

This file contains several intentional documentation and comments issues for code review practice.
The task is to identify and fix the following issues:
1. Missing documentation in UserManager
2. Misleading comments in DataProcessor
3. Outdated documentation in PaymentHandler
4. Inconsistent documentation in FileManager
5. Poor docstring quality in CacheService
6. Redundant comments in ValidationUtils
7. Missing parameter documentation in APIClient
8. Improper documentation in Logger

Review the code and identify these documentation and comments issues.
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from pathlib import Path
import re
import hashlib
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManager:
    """
    Manages users.
    """
    def __init__(self):
        # Bug: Missing documentation for initialization
        self.users = {}
        self.last_cleanup = time.time()
        self.max_users = 1000

    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        # Bug: Missing method documentation
        user_id = str(random.randint(1000, 9999))
        self.users[user_id] = {
            "name": name,
            "email": email,
            "created_at": datetime.now().isoformat()
        }
        return self.users[user_id]

    def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        # Bug: Missing parameter documentation
        if user_id in self.users:
            self.users[user_id].update(data)
            return True
        return False

    def delete_user(self, user_id: str) -> None:
        # Bug: Missing return value documentation
        if user_id in self.users:
            del self.users[user_id]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        # Bug: Missing exception documentation
        return self.users.get(user_id)

    def cleanup_old_users(self) -> int:
        # Bug: Missing implementation details
        count = 0
        current_time = time.time()
        for user_id, user in list(self.users.items()):
            if current_time - float(user.get("last_active", 0)) > 86400:
                del self.users[user_id]
                count += 1
        return count

class DataProcessor:
    """
    Processes data for the application.
    This class handles all data processing operations including validation,
    transformation, and storage of user data, order data, and system data.
    It also manages data cleanup and maintenance operations.
    """
    def __init__(self):
        # Bug: Misleading comment - doesn't actually initialize database
        # Initialize database connection and cache
        self.data = {}
        self.cache = {}

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data.

        Args:
            data: The data to process

        Returns:
            The processed data
        """
        # Bug: Misleading comment - transformation is not actually complex
        # Perform complex data transformation and validation
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip()
            else:
                result[key] = value
        return result

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate the input data.

        This method performs comprehensive validation of all data fields,
        including type checking, range validation, and business rule validation.
        It also handles special cases and edge conditions.
        """
        # Bug: Misleading comment - validation is actually very simple
        # Complex validation logic with multiple checks
        return all(isinstance(v, (str, int, float, bool)) for v in data.values())

    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Misleading comment - no actual encryption
        # Encrypt sensitive data and apply business rules
        return {k: str(v).upper() for k, v in data.items()}

    def store_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Misleading comment - no actual database
        # Store data in database with transaction support
        self.data.update(data)
        return True

class PaymentHandler:
    """
    Handles payment processing.

    This class is responsible for processing payments using various payment
    providers including Stripe, PayPal, and Square. It supports multiple
    currencies and payment methods, and includes comprehensive error handling
    and retry logic.

    Note: This implementation is deprecated and will be removed in version 2.0.
    Use the new PaymentProcessor class instead.
    """
    def __init__(self):
        # Bug: Outdated comment - no longer uses multiple providers
        # Initialize payment providers (Stripe, PayPal, Square)
        self.provider = "stripe"
        self.api_key = "test_key"

    def process_payment(self, amount: float, currency: str) -> Dict[str, Any]:
        """
        Process a payment.

        This method supports multiple payment providers and currencies,
        includes comprehensive error handling, and implements retry logic
        for failed payments.

        Args:
            amount: The payment amount
            currency: The currency code

        Returns:
            Payment result with transaction details

        Raises:
            PaymentError: If payment processing fails
        """
        # Bug: Outdated implementation comment
        # Process payment through multiple providers with fallback
        return {
            "status": "success",
            "provider": self.provider,
            "amount": amount,
            "currency": currency
        }

    def refund_payment(self, payment_id: str) -> bool:
        # Bug: Outdated comment - no longer supports partial refunds
        # Process refund with support for partial refunds
        return True

    def get_payment_status(self, payment_id: str) -> str:
        # Bug: Outdated comment - no longer supports multiple statuses
        # Get detailed payment status from provider
        return "completed"

class FileManager:
    """
    Manages file operations.
    """
    def save_file(self, filename: str, content: str) -> bool:
        """Save file to disk."""
        # Bug: Inconsistent documentation style
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False

    def read_file(self, filename: str) -> Optional[str]:
        """
        Read file from disk.

        Parameters:
            filename: The name of the file to read

        Returns:
            The file contents as a string, or None if the file doesn't exist
        """
        # Bug: Inconsistent documentation style
        try:
            with open(filename, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None

    def delete_file(self, filename: str) -> None:
        # Bug: Inconsistent documentation style
        """Delete a file from disk."""
        try:
            os.remove(filename)
        except Exception as e:
            logger.error(f"Error deleting file: {e}")

    def list_files(self, directory: str) -> List[str]:
        """
        List files in directory.

        Args:
            directory: The directory to list files from

        Returns:
            A list of filenames
        """
        # Bug: Inconsistent documentation style
        try:
            return os.listdir(directory)
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []

class CacheService:
    """
    Caching service.
    """
    def __init__(self):
        # Bug: Poor docstring quality
        self.cache = {}

    def get(self, key: str) -> Any:
        # Bug: Poor docstring quality
        """Get value from cache."""
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        # Bug: Poor docstring quality
        """Set value in cache."""
        self.cache[key] = value

    def delete(self, key: str) -> None:
        # Bug: Poor docstring quality
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        # Bug: Poor docstring quality
        """Clear cache."""
        self.cache.clear()

class ValidationUtils:
    """
    Utility functions for validation.
    """
    def validate_email(self, email: str) -> bool:
        # Bug: Redundant comment
        # Check if email is valid
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def validate_phone(self, phone: str) -> bool:
        # Bug: Redundant comment
        # Check if phone number is valid
        return bool(re.match(r"^\+?[\d\s-]+$", phone))

    def validate_password(self, password: str) -> bool:
        # Bug: Redundant comment
        # Check if password meets requirements
        return len(password) >= 8 and bool(re.search(r"[A-Z]", password))

    def validate_username(self, username: str) -> bool:
        # Bug: Redundant comment
        # Check if username is valid
        return bool(re.match(r"^[a-zA-Z0-9_]+$", username))

class APIClient:
    """
    API client for external services.
    """
    def __init__(self, base_url: str):
        # Bug: Missing parameter documentation
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint: str) -> Dict[str, Any]:
        # Bug: Missing parameter documentation
        response = self.session.get(f"{self.base_url}/{endpoint}")
        return response.json()

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Missing parameter documentation
        response = self.session.post(f"{self.base_url}/{endpoint}", json=data)
        return response.json()

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Missing parameter documentation
        response = self.session.put(f"{self.base_url}/{endpoint}", json=data)
        return response.json()

    def delete(self, endpoint: str) -> bool:
        # Bug: Missing parameter documentation
        response = self.session.delete(f"{self.base_url}/{endpoint}")
        return response.status_code == 204

class Logger:
    """
    Logging utility.

    This class provides logging functionality for the application.
    It supports multiple log levels and output formats.
    """
    def __init__(self):
        # Bug: Improper documentation - missing implementation details
        self.logger = logging.getLogger(__name__)

    def info(self, message: str) -> None:
        # Bug: Improper documentation - missing log level details
        """Log info message."""
        self.logger.info(message)

    def error(self, message: str) -> None:
        # Bug: Improper documentation - missing error handling
        """Log error message."""
        self.logger.error(message)

    def warning(self, message: str) -> None:
        # Bug: Improper documentation - missing usage context
        """Log warning message."""
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        # Bug: Improper documentation - missing debug level info
        """Log debug message."""
        self.logger.debug(message)

def main():
    # Test UserManager missing documentation
    print("Testing UserManager missing documentation:")
    user_manager = UserManager()
    user = user_manager.create_user("John Doe", "john@example.com")
    print(f"Created user: {user}")
    print(f"Retrieved user: {user_manager.get_user(user['id'])}")

    # Test DataProcessor misleading comments
    print("\nTesting DataProcessor misleading comments:")
    processor = DataProcessor()
    data = {"name": " John ", "age": 30}
    print(f"Processed data: {processor.process_data(data)}")
    print(f"Validated data: {processor.validate_data(data)}")

    # Test PaymentHandler outdated documentation
    print("\nTesting PaymentHandler outdated documentation:")
    payment_handler = PaymentHandler()
    result = payment_handler.process_payment(100.0, "USD")
    print(f"Payment result: {result}")
    print(f"Payment status: {payment_handler.get_payment_status('123')}")

    # Test FileManager inconsistent documentation
    print("\nTesting FileManager inconsistent documentation:")
    file_manager = FileManager()
    file_manager.save_file("test.txt", "Hello, World!")
    print(f"File content: {file_manager.read_file('test.txt')}")
    file_manager.delete_file("test.txt")

    # Test CacheService poor docstring quality
    print("\nTesting CacheService poor docstring quality:")
    cache = CacheService()
    cache.set("test_key", "test_value")
    print(f"Cached value: {cache.get('test_key')}")
    cache.delete("test_key")

    # Test ValidationUtils redundant comments
    print("\nTesting ValidationUtils redundant comments:")
    utils = ValidationUtils()
    print(f"Email valid: {utils.validate_email('test@example.com')}")
    print(f"Phone valid: {utils.validate_phone('+1-234-567-8900')}")
    print(f"Password valid: {utils.validate_password('Password123')}")

    # Test APIClient missing parameter documentation
    print("\nTesting APIClient missing parameter documentation:")
    client = APIClient("https://api.example.com")
    try:
        result = client.get("users")
        print(f"API response: {result}")
    except Exception as e:
        print(f"API error: {e}")

    # Test Logger improper documentation
    print("\nTesting Logger improper documentation:")
    logger = Logger()
    logger.info("Test info message")
    logger.error("Test error message")
    logger.warning("Test warning message")
    logger.debug("Test debug message")

if __name__ == "__main__":
    main()