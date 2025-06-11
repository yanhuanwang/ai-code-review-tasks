#!/usr/bin/env python3
"""
Task 25: Testing Issues Challenge

This file contains several intentional testing issues for code review practice.
The task is to identify and fix the following testing problems:

1. Insufficient Test Coverage:
   - Calculator: Missing edge cases
   - UserManager: Incomplete validation tests
   - DataProcessor: Missing error cases

2. Brittle Tests:
   - OrderProcessor: Hardcoded values
   - TimeManager: Time-dependent tests
   - FileManager: File system dependencies

3. Test Dependencies:
   - DatabaseTests: Shared database state
   - CacheTests: Shared cache state
   - UserTests: Shared user state

4. Non-Deterministic Tests:
   - RandomGenerator: Non-deterministic results
   - ConcurrentTests: Race conditions
   - AsyncTests: Timing issues

5. Test Data Issues:
   - DataValidator: Hardcoded test data
   - UserValidator: Missing test data
   - OrderValidator: Incomplete test data

6. Test Organization:
   - TestManager: Mixed test types
   - TestRunner: Poor test isolation
   - TestValidator: Mixed assertions

7. Mocking Issues:
   - ServiceTests: Incomplete mocks
   - APITests: Missing mock cleanup
   - DatabaseTests: Leaky mocks

8. Test Maintenance:
   - LegacyTests: Outdated tests
   - DuplicateTests: Test duplication
   - UnusedTests: Dead test code

Review the code and identify these testing issues.
"""

import unittest
import time
import random
import os
import json
import sqlite3
import threading
import asyncio
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import pytest
import coverage
from abc import ABC, abstractmethod

# Bug: Insufficient Test Coverage
class Calculator:
    """
    Calculator class with insufficient test coverage.
    """
    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def multiply(self, a: int, b: int) -> int:
        return a * b

    def divide(self, a: int, b: int) -> float:
        # Bug: Missing test for division by zero
        return a / b

    def power(self, a: int, b: int) -> int:
        # Bug: Missing test for negative exponents
        return a ** b

class CalculatorTests(unittest.TestCase):
    """
    Tests with insufficient coverage.
    """
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        # Bug: Missing edge cases
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        # Bug: Missing negative number tests
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self):
        # Bug: Missing zero multiplication test
        self.assertEqual(self.calc.multiply(4, 3), 12)

    # Bug: Missing test for divide
    # Bug: Missing test for power

# Bug: Brittle Tests
class OrderProcessor:
    """
    Order processor with brittle tests.
    """
    def __init__(self):
        self.orders = {}

    def process_order(self, order_id: str, amount: float) -> Dict[str, Any]:
        # Bug: Hardcoded business logic
        if amount > 1000:
            status = "requires_approval"
        else:
            status = "approved"

        order = {
            "id": order_id,
            "amount": amount,
            "status": status,
            "timestamp": datetime.now().isoformat()  # Bug: Time-dependent
        }
        self.orders[order_id] = order
        return order

class OrderProcessorTests(unittest.TestCase):
    """
    Brittle tests with hardcoded values and time dependencies.
    """
    def setUp(self):
        self.processor = OrderProcessor()

    def test_process_order(self):
        # Bug: Hardcoded test values
        order = self.processor.process_order("ORDER123", 500.0)
        self.assertEqual(order["status"], "approved")
        self.assertEqual(order["amount"], 500.0)

        # Bug: Time-dependent test
        self.assertIsNotNone(order["timestamp"])

    def test_process_large_order(self):
        # Bug: Hardcoded threshold
        order = self.processor.process_order("ORDER124", 1500.0)
        self.assertEqual(order["status"], "requires_approval")

# Bug: Test Dependencies
class DatabaseManager:
    """
    Database manager with test dependencies.
    """
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.setup_database()

    def setup_database(self):
        # Bug: Shared database state
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        self.db.commit()

    def add_user(self, user_id: str, name: str, email: str) -> None:
        self.db.execute(
            'INSERT INTO users (id, name, email) VALUES (?, ?, ?)',
            (user_id, name, email)
        )
        self.db.commit()

    def get_user(self, user_id: str) -> Optional[Dict[str, str]]:
        cursor = self.db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "email": row[2]}
        return None

class DatabaseTests(unittest.TestCase):
    """
    Tests with shared state dependencies.
    """
    def setUp(self):
        # Bug: Shared database instance
        self.db_manager = DatabaseManager()

    def test_add_user(self):
        # Bug: Test depends on shared state
        self.db_manager.add_user("user1", "John Doe", "john@example.com")
        user = self.db_manager.get_user("user1")
        self.assertEqual(user["name"], "John Doe")

    def test_get_nonexistent_user(self):
        # Bug: Test affected by other tests
        user = self.db_manager.get_user("nonexistent")
        self.assertIsNone(user)

# Bug: Non-Deterministic Tests
class RandomGenerator:
    """
    Random generator with non-deterministic tests.
    """
    def generate_id(self) -> str:
        # Bug: Non-deterministic output
        return f"ID_{random.randint(1000, 9999)}"

    def generate_timestamp(self) -> str:
        # Bug: Time-dependent output
        return datetime.now().isoformat()

class RandomGeneratorTests(unittest.TestCase):
    """
    Non-deterministic tests.
    """
    def setUp(self):
        self.generator = RandomGenerator()

    def test_generate_id(self):
        # Bug: Non-deterministic test
        id1 = self.generator.generate_id()
        id2 = self.generator.generate_id()
        self.assertNotEqual(id1, id2)

    def test_generate_timestamp(self):
        # Bug: Time-dependent test
        timestamp = self.generator.generate_timestamp()
        self.assertIsNotNone(timestamp)

# Bug: Test Data Issues
class DataValidator:
    """
    Data validator with test data issues.
    """
    def validate_user(self, user_data: Dict[str, Any]) -> bool:
        # Bug: Hardcoded validation rules
        if not user_data.get("name"):
            return False
        if not user_data.get("email"):
            return False
        if not user_data.get("age"):
            return False
        if user_data["age"] < 18:  # Bug: Hardcoded business rule
            return False
        return True

class DataValidatorTests(unittest.TestCase):
    """
    Tests with test data issues.
    """
    def setUp(self):
        self.validator = DataValidator()

    def test_validate_user(self):
        # Bug: Hardcoded test data
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 25
        }
        self.assertTrue(self.validator.validate_user(user_data))

    # Bug: Missing test cases for invalid data
    # Bug: Missing edge cases

# Bug: Test Organization
class TestManager:
    """
    Test manager with poor organization.
    """
    def __init__(self):
        self.tests = []
        self.results = {}

    def add_test(self, test_name: str, test_func: callable) -> None:
        # Bug: Mixed test types
        self.tests.append((test_name, test_func))

    def run_tests(self) -> Dict[str, Any]:
        # Bug: Poor test isolation
        for test_name, test_func in self.tests:
            try:
                result = test_func()
                self.results[test_name] = {
                    "status": "passed",
                    "result": result
                }
            except Exception as e:
                self.results[test_name] = {
                    "status": "failed",
                    "error": str(e)
                }
        return self.results

class TestManagerTests(unittest.TestCase):
    """
    Tests with poor organization.
    """
    def setUp(self):
        self.test_manager = TestManager()

    def test_add_and_run_test(self):
        # Bug: Mixed test types
        def test_func():
            return 42

        self.test_manager.add_test("test1", test_func)
        results = self.test_manager.run_tests()
        self.assertEqual(results["test1"]["status"], "passed")

# Bug: Mocking Issues
class APIService:
    """
    API service with mocking issues.
    """
    def __init__(self):
        self.session = None

    def get_data(self, url: str) -> Dict[str, Any]:
        # Bug: Missing mock cleanup
        response = self.session.get(url)
        return response.json()

class APIServiceTests(unittest.TestCase):
    """
    Tests with mocking issues.
    """
    def setUp(self):
        self.service = APIService()
        # Bug: Incomplete mock
        self.service.session = Mock()

    def test_get_data(self):
        # Bug: Leaky mock
        self.service.session.get.return_value.json.return_value = {
            "data": "test"
        }
        result = self.service.get_data("http://api.example.com/data")
        self.assertEqual(result["data"], "test")

    # Bug: Missing mock cleanup in tearDown

# Bug: Test Maintenance
class LegacyCalculator:
    """
    Legacy calculator with outdated tests.
    """
    def add(self, a: int, b: int) -> int:
        # Bug: Outdated implementation
        return a + b + 1  # Legacy bug

    def subtract(self, a: int, b: int) -> int:
        # Bug: Outdated implementation
        return a - b - 1  # Legacy bug

class LegacyCalculatorTests(unittest.TestCase):
    """
    Outdated tests.
    """
    def setUp(self):
        self.calc = LegacyCalculator()

    def test_add(self):
        # Bug: Outdated test
        self.assertEqual(self.calc.add(2, 3), 6)  # Expects legacy behavior

    def test_subtract(self):
        # Bug: Outdated test
        self.assertEqual(self.calc.subtract(5, 3), 1)  # Expects legacy behavior

    # Bug: Duplicate test cases
    def test_add_again(self):
        self.assertEqual(self.calc.add(2, 3), 6)

    # Bug: Unused test
    def test_unused(self):
        pass

def main():
    # Run all test suites
    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(CalculatorTests),
        unittest.TestLoader().loadTestsFromTestCase(OrderProcessorTests),
        unittest.TestLoader().loadTestsFromTestCase(DatabaseTests),
        unittest.TestLoader().loadTestsFromTestCase(RandomGeneratorTests),
        unittest.TestLoader().loadTestsFromTestCase(DataValidatorTests),
        unittest.TestLoader().loadTestsFromTestCase(TestManagerTests),
        unittest.TestLoader().loadTestsFromTestCase(APIServiceTests),
        unittest.TestLoader().loadTestsFromTestCase(LegacyCalculatorTests)
    ]

    # Run tests with coverage
    cov = coverage.Coverage()
    cov.start()

    for suite in test_suites:
        unittest.TextTestRunner().run(suite)

    cov.stop()
    cov.save()

    # Print coverage report
    print("\nCoverage Report:")
    cov.report()

if __name__ == "__main__":
    main()