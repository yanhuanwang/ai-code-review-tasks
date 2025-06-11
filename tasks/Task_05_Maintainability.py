#!/usr/bin/env python3
"""
Task 05: Code Maintainability and Design Challenge

This file contains several intentional design and maintainability issues for code review practice.
The task is to identify and fix the following issues:
1. Violation of Single Responsibility Principle in UserManager
2. Tight coupling in NotificationSystem
3. Inconsistent error handling across the codebase
4. Lack of proper abstraction in DataProcessor
5. Violation of Open/Closed Principle in PaymentProcessor
6. Poor separation of concerns in ReportGenerator
7. Inconsistent naming conventions
8. Lack of proper documentation and type hints

Review the code and identify these maintainability and design issues.
"""

from typing import List, Dict, Any, Optional, Union
import json
import datetime
import random
import string
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
from enum import Enum

# Global variables (design issue)
CONFIG = {
    "db_path": "database.db",
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 30
}

# Inconsistent naming (snake_case vs camelCase)
class userStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Violation of Single Responsibility Principle
class UserManager:
    """
    Manages user operations.
    Bug: Violates SRP by handling too many responsibilities.
    """
    def __init__(self):
        self.users = {}
        self.logger = logging.getLogger(__name__)
        self.db_connection = None
        self.cache = {}

    def create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Create a new user."""
        # Bug: Mixing business logic, validation, and persistence
        if not self._validate_email(email):
            raise ValueError("Invalid email")

        user = {
            "username": username,
            "email": email,
            "status": userStatus.ACTIVE.value,
            "created_at": datetime.datetime.now().isoformat()
        }

        self._save_to_db(user)
        self._update_cache(user)
        self._send_welcome_email(email)
        self._log_user_creation(username)

        return user

    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        return "@" in email

    def _save_to_db(self, user: Dict[str, Any]) -> None:
        """Save user to database."""
        # Simulate database operation
        self.users[user["username"]] = user

    def _update_cache(self, user: Dict[str, Any]) -> None:
        """Update user cache."""
        self.cache[user["username"]] = user

    def _send_welcome_email(self, email: str) -> None:
        """Send welcome email."""
        # Simulate email sending
        print(f"Sending welcome email to {email}")

    def _log_user_creation(self, username: str) -> None:
        """Log user creation."""
        self.logger.info(f"Created user: {username}")

# Tight coupling
class NotificationSystem:
    """
    Handles system notifications.
    Bug: Tightly coupled with specific notification methods.
    """
    def __init__(self):
        self.email_sender = EmailSender()
        self.sms_sender = SMSSender()
        self.push_sender = PushNotificationSender()

    def notify(self, user: Dict[str, Any], message: str) -> None:
        """Send notification to user."""
        # Bug: Hard-coded notification logic
        if "email" in user:
            self.email_sender.send(user["email"], message)
        if "phone" in user:
            self.sms_sender.send(user["phone"], message)
        if "device_id" in user:
            self.push_sender.send(user["device_id"], message)

class EmailSender:
    def send(self, email: str, message: str) -> None:
        print(f"Sending email to {email}: {message}")

class SMSSender:
    def send(self, phone: str, message: str) -> None:
        print(f"Sending SMS to {phone}: {message}")

class PushNotificationSender:
    def send(self, device_id: str, message: str) -> None:
        print(f"Sending push notification to {device_id}: {message}")

# Inconsistent error handling
class DataProcessor:
    """
    Processes data from various sources.
    Bug: Inconsistent error handling and lack of proper abstraction.
    """
    def process_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Process data from file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return self._process_data(data)
        except FileNotFoundError:
            # Bug: Inconsistent error handling
            return []
        except json.JSONDecodeError as e:
            # Bug: Different error handling style
            raise ValueError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            # Bug: Generic exception handling
            print(f"Error processing file: {e}")
            return None

    def _process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process the data."""
        # Bug: No proper abstraction for data processing
        result = []
        for item in data:
            if "value" in item:
                item["processed_value"] = item["value"] * 2
            if "date" in item:
                item["processed_date"] = item["date"].upper()
            result.append(item)
        return result

# Violation of Open/Closed Principle
class PaymentProcessor:
    """
    Processes different types of payments.
    Bug: Violates Open/Closed Principle - not extensible for new payment types.
    """
    def process_payment(self, payment_type: str, amount: float) -> bool:
        """Process a payment."""
        # Bug: Not extensible, violates OCP
        if payment_type == "credit_card":
            return self._process_credit_card(amount)
        elif payment_type == "paypal":
            return self._process_paypal(amount)
        elif payment_type == "bank_transfer":
            return self._process_bank_transfer(amount)
        else:
            raise ValueError(f"Unsupported payment type: {payment_type}")

    def _process_credit_card(self, amount: float) -> bool:
        return random.random() > 0.1  # Simulate 90% success rate

    def _process_paypal(self, amount: float) -> bool:
        return random.random() > 0.05  # Simulate 95% success rate

    def _process_bank_transfer(self, amount: float) -> bool:
        return random.random() > 0.02  # Simulate 98% success rate

# Poor separation of concerns
class ReportGenerator:
    """
    Generates various types of reports.
    Bug: Poor separation of concerns, mixing data retrieval and formatting.
    """
    def __init__(self):
        self.db_connection = None
        self.template_engine = None
        self.file_system = None

    def generate_user_report(self, user_id: str, report_type: str) -> str:
        """Generate a user report."""
        # Bug: Mixing data retrieval, processing, and formatting
        user_data = self._get_user_data(user_id)
        if not user_data:
            return "User not found"

        if report_type == "summary":
            return self._format_summary(user_data)
        elif report_type == "detailed":
            return self._format_detailed(user_data)
        elif report_type == "statistics":
            return self._format_statistics(user_data)
        else:
            return "Invalid report type"

    def _get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data from database."""
        # Simulate database query
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "activity": random.randint(0, 100),
            "last_login": datetime.datetime.now().isoformat()
        }

    def _format_summary(self, data: Dict[str, Any]) -> str:
        """Format summary report."""
        return f"Summary for {data['name']}: {data['activity']} activities"

    def _format_detailed(self, data: Dict[str, Any]) -> str:
        """Format detailed report."""
        return f"Detailed report for {data['name']}\n" + \
               f"Activity: {data['activity']}\n" + \
               f"Last login: {data['last_login']}"

    def _format_statistics(self, data: Dict[str, Any]) -> str:
        """Format statistics report."""
        return f"Statistics for {data['name']}\n" + \
               f"Activity score: {data['activity'] * 10}"

def main():
    # Test UserManager (SRP violation)
    print("Testing UserManager (SRP violation):")
    user_manager = UserManager()
    try:
        user = user_manager.create_user("testuser", "test@example.com")
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Test NotificationSystem (tight coupling)
    print("\nTesting NotificationSystem (tight coupling):")
    notification_system = NotificationSystem()
    user = {
        "email": "test@example.com",
        "phone": "1234567890",
        "device_id": "device123"
    }
    notification_system.notify(user, "Test notification")

    # Test DataProcessor (inconsistent error handling)
    print("\nTesting DataProcessor (inconsistent error handling):")
    processor = DataProcessor()
    # Test with non-existent file
    result = processor.process_file("nonexistent.json")
    print(f"Process non-existent file result: {result}")

    # Test PaymentProcessor (OCP violation)
    print("\nTesting PaymentProcessor (OCP violation):")
    payment_processor = PaymentProcessor()
    for payment_type in ["credit_card", "paypal", "bank_transfer", "crypto"]:
        try:
            result = payment_processor.process_payment(payment_type, 100.0)
            print(f"Payment {payment_type}: {'Success' if result else 'Failed'}")
        except ValueError as e:
            print(f"Payment {payment_type}: {e}")

    # Test ReportGenerator (poor separation of concerns)
    print("\nTesting ReportGenerator (poor separation of concerns):")
    report_generator = ReportGenerator()
    for report_type in ["summary", "detailed", "statistics", "invalid"]:
        report = report_generator.generate_user_report("user123", report_type)
        print(f"\n{report_type.upper()} Report:")
        print(report)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    main()