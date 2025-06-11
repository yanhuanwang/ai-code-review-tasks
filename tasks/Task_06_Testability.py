#!/usr/bin/env python3
"""
Task 06: Testing and Testability Challenge

This file contains several intentional testing and testability issues for code review practice.
The task is to identify and fix the following issues:
1. Untestable code due to direct system calls in FileProcessor
2. Non-deterministic behavior in OrderProcessor
3. Hidden dependencies in UserService
4. Lack of proper test boundaries in DataValidator
5. Difficult to mock external services in PaymentGateway
6. Untestable side effects in CacheManager
7. Lack of proper test data setup in ReportService
8. Non-isolated tests in TestRunner

Review the code and identify these testing and testability issues.
"""

import os
import time
import random
import uuid
import json
import sqlite3
import requests
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
from pathlib import Path

# Global state (testing issue)
CURRENT_USER = None
DATABASE_CONNECTION = None

class FileProcessor:
    """
    Processes files in the system.
    Bug: Direct system calls make it untestable.
    """
    def process_file(self, filepath: str) -> bool:
        """Process a file and return success status."""
        # Bug: Direct system calls, hard to test
        if not os.path.exists(filepath):
            return False

        # Bug: Direct file system operations
        os.chmod(filepath, 0o644)
        os.utime(filepath, (time.time(), time.time()))

        # Bug: Direct system command
        os.system(f"gzip -f {filepath}")
        return True

class OrderProcessor:
    """
    Processes customer orders.
    Bug: Non-deterministic behavior makes testing difficult.
    """
    def __init__(self):
        self.orders = set()

    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> str:
        """Create a new order."""
        # Bug: Non-deterministic order ID
        order_id = str(uuid.uuid4())

        # Bug: Time-dependent behavior
        order = {
            "id": order_id,
            "user_id": user_id,
            "items": items,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }

        # Bug: Random behavior
        if random.random() < 0.1:  # 10% chance of failure
            raise Exception("Random order creation failure")

        self.orders.add(order_id)
        return order_id

    def get_order_status(self, order_id: str) -> str:
        """Get the status of an order."""
        # Bug: Time-dependent status
        if order_id in self.orders:
            # Simulate order processing time
            time.sleep(0.1)
            return random.choice(["pending", "processing", "completed", "failed"])
        return "not_found"

class UserService:
    """
    Manages user operations.
    Bug: Hidden dependencies and global state.
    """
    def __init__(self):
        global DATABASE_CONNECTION
        # Bug: Hidden dependency on global state
        self.db = DATABASE_CONNECTION or sqlite3.connect("users.db")
        self.cache = {}

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        # Bug: Hidden dependency on global state
        global CURRENT_USER
        if CURRENT_USER and CURRENT_USER.get("id") == user_id:
            return CURRENT_USER

        # Bug: Hidden dependency on database
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None

    def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update user data."""
        # Bug: Multiple side effects
        if user_id in self.cache:
            del self.cache[user_id]

        # Bug: Hidden dependency on global state
        global CURRENT_USER
        if CURRENT_USER and CURRENT_USER.get("id") == user_id:
            CURRENT_USER.update(data)

        # Bug: Direct database operation
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (data.get("name"), data.get("email"), user_id)
        )
        self.db.commit()
        return True

class DataValidator:
    """
    Validates data according to rules.
    Bug: No clear test boundaries and mixed responsibilities.
    """
    def __init__(self):
        self.rules = {}
        self._load_rules()

    def _load_rules(self) -> None:
        """Load validation rules."""
        # Bug: Direct file system dependency
        if os.path.exists("validation_rules.json"):
            with open("validation_rules.json", "r") as f:
                self.rules = json.load(f)
        else:
            # Bug: Hard-coded fallback rules
            self.rules = {
                "user": {"name": "str", "email": "email", "age": "int"},
                "order": {"items": "list", "total": "float"}
            }

    def validate(self, data_type: str, data: Dict[str, Any]) -> List[str]:
        """Validate data against rules."""
        errors = []
        # Bug: Mixed validation logic
        if data_type not in self.rules:
            errors.append(f"Unknown data type: {data_type}")
            return errors

        rules = self.rules[data_type]
        for field, rule in rules.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif rule == "email" and "@" not in str(data[field]):
                errors.append(f"Invalid email format: {data[field]}")
            elif rule == "int" and not isinstance(data[field], int):
                errors.append(f"Field {field} must be an integer")
            elif rule == "float" and not isinstance(data[field], (int, float)):
                errors.append(f"Field {field} must be a number")

        return errors

class PaymentGateway:
    """
    Handles payment processing.
    Bug: Difficult to mock external service calls.
    """
    def __init__(self):
        self.api_key = os.getenv("PAYMENT_API_KEY", "test_key")
        self.api_url = "https://api.payment-service.com/v1"

    def process_payment(self, amount: float, card_number: str) -> Dict[str, Any]:
        """Process a payment."""
        # Bug: Direct external service call
        response = requests.post(
            f"{self.api_url}/payments",
            json={
                "amount": amount,
                "card_number": card_number,
                "api_key": self.api_key
            },
            timeout=30
        )
        return response.json()

    def get_payment_status(self, payment_id: str) -> str:
        """Get payment status."""
        # Bug: Direct external service call
        response = requests.get(
            f"{self.api_url}/payments/{payment_id}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30
        )
        return response.json()["status"]

class CacheManager:
    """
    Manages caching of data.
    Bug: Untestable side effects and time-dependent behavior.
    """
    def __init__(self):
        self._cache = {}
        self._last_cleanup = time.time()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Bug: Time-dependent cleanup
        if time.time() - self._last_cleanup > 3600:  # 1 hour
            self._cleanup()

        # Bug: Non-deterministic expiration
        if key in self._cache:
            item = self._cache[key]
            if random.random() < 0.1:  # 10% chance of expiration
                del self._cache[key]
                return None
            return item
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        # Bug: Non-deterministic behavior
        if random.random() < 0.05:  # 5% chance of cache miss
            return

        self._cache[key] = value

    def _cleanup(self) -> None:
        """Clean up expired cache entries."""
        # Bug: Time-dependent cleanup
        self._last_cleanup = time.time()
        expired = []
        for key, value in self._cache.items():
            if random.random() < 0.2:  # 20% chance of expiration
                expired.append(key)
        for key in expired:
            del self._cache[key]

class ReportService:
    """
    Generates various reports.
    Bug: Lack of proper test data setup.
    """
    def __init__(self):
        self.db = sqlite3.connect("reports.db")
        self._setup_database()

    def _setup_database(self) -> None:
        """Setup database tables."""
        # Bug: No proper test data setup
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                type TEXT,
                data TEXT,
                created_at TIMESTAMP
            )
        """)
        self.db.commit()

    def generate_report(self, report_type: str) -> Dict[str, Any]:
        """Generate a report."""
        # Bug: Direct database dependency
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT data FROM reports
            WHERE type = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (report_type,))
        result = cursor.fetchone()

        if not result:
            # Bug: No test data generation
            return {"error": "No data available"}

        return json.loads(result[0])

class TestRunner:
    """
    Runs tests for the application.
    Bug: Non-isolated tests and shared state.
    """
    def __init__(self):
        self.test_results = []
        self._setup_test_environment()

    def _setup_test_environment(self) -> None:
        """Setup test environment."""
        # Bug: Shared test environment
        global DATABASE_CONNECTION
        DATABASE_CONNECTION = sqlite3.connect(":memory:")

        # Bug: Global state modification
        global CURRENT_USER
        CURRENT_USER = {"id": "test_user", "name": "Test User"}

    def run_tests(self) -> List[Dict[str, Any]]:
        """Run all tests."""
        # Bug: Tests are not isolated
        self._test_user_service()
        self._test_payment_gateway()
        self._test_cache_manager()
        return self.test_results

    def _test_user_service(self) -> None:
        """Test user service."""
        service = UserService()
        # Bug: Tests depend on previous test state
        user = service.get_user("test_user")
        self.test_results.append({
            "test": "user_service",
            "passed": user is not None,
            "message": "User service test"
        })

    def _test_payment_gateway(self) -> None:
        """Test payment gateway."""
        gateway = PaymentGateway()
        # Bug: Tests depend on external service
        try:
            result = gateway.process_payment(100.0, "4111111111111111")
            self.test_results.append({
                "test": "payment_gateway",
                "passed": "status" in result,
                "message": "Payment gateway test"
            })
        except Exception as e:
            self.test_results.append({
                "test": "payment_gateway",
                "passed": False,
                "message": str(e)
            })

    def _test_cache_manager(self) -> None:
        """Test cache manager."""
        cache = CacheManager()
        # Bug: Non-deterministic test
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        self.test_results.append({
            "test": "cache_manager",
            "passed": value == "test_value",
            "message": "Cache manager test"
        })

def main():
    # Test FileProcessor
    print("Testing FileProcessor:")
    processor = FileProcessor()
    test_file = "test.txt"
    try:
        with open(test_file, "w") as f:
            f.write("test content")
        result = processor.process_file(test_file)
        print(f"File processing result: {result}")
    except Exception as e:
        print(f"File processing error: {e}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

    # Test OrderProcessor
    print("\nTesting OrderProcessor:")
    order_processor = OrderProcessor()
    try:
        order_id = order_processor.create_order("user1", [{"item": "test", "price": 10.0}])
        print(f"Created order: {order_id}")
        status = order_processor.get_order_status(order_id)
        print(f"Order status: {status}")
    except Exception as e:
        print(f"Order processing error: {e}")

    # Test UserService
    print("\nTesting UserService:")
    user_service = UserService()
    try:
        user = user_service.get_user("test_user")
        print(f"Retrieved user: {user}")
        updated = user_service.update_user("test_user", {"name": "Updated User"})
        print(f"User update result: {updated}")
    except Exception as e:
        print(f"User service error: {e}")

    # Test DataValidator
    print("\nTesting DataValidator:")
    validator = DataValidator()
    test_data = {
        "name": "Test User",
        "email": "invalid-email",
        "age": "not-a-number"
    }
    errors = validator.validate("user", test_data)
    print(f"Validation errors: {errors}")

    # Test PaymentGateway
    print("\nTesting PaymentGateway:")
    gateway = PaymentGateway()
    try:
        result = gateway.process_payment(100.0, "4111111111111111")
        print(f"Payment result: {result}")
    except Exception as e:
        print(f"Payment error: {e}")

    # Test CacheManager
    print("\nTesting CacheManager:")
    cache = CacheManager()
    cache.set("test_key", "test_value")
    value = cache.get("test_key")
    print(f"Cached value: {value}")

    # Test ReportService
    print("\nTesting ReportService:")
    report_service = ReportService()
    report = report_service.generate_report("user_activity")
    print(f"Generated report: {report}")

    # Test TestRunner
    print("\nTesting TestRunner:")
    test_runner = TestRunner()
    results = test_runner.run_tests()
    print("Test results:")
    for result in results:
        print(f"- {result['test']}: {'PASSED' if result['passed'] else 'FAILED'} - {result['message']}")

if __name__ == "__main__":
    main()