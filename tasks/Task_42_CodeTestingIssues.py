#!/usr/bin/env python3
"""
Task 42: Code Testing Issues Challenge

This file contains several intentional testing issues for code review practice.
The task is to identify and fix the following testing problems:

1. Untestable Code:
   - Global state usage
   - Hidden dependencies
   - Static methods
   - Singleton patterns

2. Missing Test Coverage:
   - Untested edge cases
   - Missing validation tests
   - Incomplete error handling
   - Untested business logic

3. Brittle Tests:
   - Hard-coded values
   - Time-dependent tests
   - Order-dependent tests
   - Environment-dependent tests

4. Test Duplication:
   - Repeated setup code
   - Similar test cases
   - Duplicate assertions
   - Redundant test data

5. Non-Deterministic Tests:
   - Random values
   - Time-based operations
   - External dependencies
   - Unpredictable behavior

6. Slow Tests:
   - Real database connections
   - Network calls
   - File I/O operations
   - Heavy computations

7. Complex Test Setup:
   - Many dependencies
   - Complex initialization
   - Global state setup
   - External service setup

8. Poor Test Organization:
   - Mixed test types
   - Unclear test structure
   - Missing test documentation
   - Poor test naming

Review the code and identify these testing issues.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
from typing import List, Dict, Any, Optional, Union, Tuple, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import psycopg2
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict
import unittest

# Bug: Global State (Untestable Code)
DATABASE = sqlite3.connect(":memory:")  # Bug: Global database
CACHE = {}  # Bug: Global cache
LOGGER = logging.getLogger(__name__)  # Bug: Global logger
CONFIG = {}  # Bug: Global config

# Bug: Untestable Code
class UserManager:
    """
    User manager with untestable code.
    """
    _instance = None  # Bug: Singleton pattern

    def __new__(cls):
        # Bug: Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Bug: Global state
        # Bug: Hidden dependencies
        # Bug: Static initialization
        if not hasattr(self, 'initialized'):
            self.db = DATABASE  # Bug: Global dependency
            self.cache = CACHE  # Bug: Global dependency
            self.logger = LOGGER  # Bug: Global dependency
            self.config = CONFIG  # Bug: Global dependency
            self.initialized = True

    @staticmethod
    def validate_user(user_data: Dict[str, Any]) -> bool:
        # Bug: Static method
        # Bug: Global state usage
        # Bug: Hidden dependencies
        try:
            # Direct database access
            cursor = DATABASE.execute(
                "SELECT * FROM users WHERE email = ?",
                (user_data["email"],)
            )
            return cursor.fetchone() is None
        except Exception as e:
            LOGGER.error(f"Validation error: {e}")
            return False

# Bug: Missing Test Coverage
class OrderManager:
    """
    Order manager with missing test coverage.
    """
    def __init__(self):
        # Bug: Global state
        self.db = DATABASE
        self.cache = CACHE
        self.logger = LOGGER

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Missing edge cases
        # Bug: Incomplete validation
        # Bug: Untested error handling
        try:
            # No validation for required fields
            # No validation for data types
            # No validation for business rules

            # Process order
            order_id = str(random.randint(1, 1000000))
            self.db.execute(
                "INSERT INTO orders VALUES (?, ?)",
                (order_id, json.dumps(order_data))
            )
            self.db.commit()

            # No error handling for database failures
            # No error handling for invalid data
            # No error handling for business rule violations

            return {"order_id": order_id, "status": "processed"}
        except Exception as e:
            self.logger.error(f"Order processing error: {e}")
            return {"error": str(e)}

# Bug: Brittle Tests
class TestOrderManager(unittest.TestCase):
    """
    Brittle tests for OrderManager.
    """
    def setUp(self):
        # Bug: Hard-coded values
        # Bug: Time-dependent setup
        # Bug: Order-dependent setup
        self.manager = OrderManager()
        self.test_order = {
            "id": "12345",  # Bug: Hard-coded value
            "items": ["item1", "item2"],  # Bug: Hard-coded value
            "total": 100.0,  # Bug: Hard-coded value
            "timestamp": time.time()  # Bug: Time-dependent
        }

    def test_process_order(self):
        # Bug: Brittle test
        # Bug: Hard-coded assertions
        # Bug: Time-dependent test
        result = self.manager.process_order(self.test_order)

        # Bug: Hard-coded assertions
        self.assertEqual(result["order_id"], "12345")  # Bug: Hard-coded value
        self.assertEqual(result["status"], "processed")  # Bug: Hard-coded value

        # Bug: Time-dependent assertion
        self.assertLess(time.time() - self.test_order["timestamp"], 1.0)

# Bug: Test Duplication
class TestUserManager(unittest.TestCase):
    """
    Tests with duplication for UserManager.
    """
    def setUp(self):
        # Bug: Duplicate setup code
        self.manager = UserManager()
        self.test_user = {
            "name": "John",
            "email": "john@example.com",
            "password": "password123"
        }
        self.db = DATABASE
        self.cache = CACHE

    def test_create_user(self):
        # Bug: Duplicate test cases
        # Bug: Similar assertions
        # Bug: Redundant test data
        result = self.manager.create_user(self.test_user)
        self.assertIn("user_id", result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "created")

        # Duplicate validation
        user = self.db.execute(
            "SELECT * FROM users WHERE email = ?",
            (self.test_user["email"],)
        ).fetchone()
        self.assertIsNotNone(user)

        # Duplicate cache check
        cached = self.cache.get(result["user_id"])
        self.assertIsNotNone(cached)

    def test_create_duplicate_user(self):
        # Bug: Duplicate test structure
        # Bug: Similar assertions
        # Bug: Redundant setup
        # Create first user
        result1 = self.manager.create_user(self.test_user)
        self.assertIn("user_id", result1)
        self.assertIn("status", result1)
        self.assertEqual(result1["status"], "created")

        # Create duplicate user
        result2 = self.manager.create_user(self.test_user)
        self.assertIn("error", result2)
        self.assertEqual(result2["error"], "User already exists")

        # Duplicate validation
        user = self.db.execute(
            "SELECT * FROM users WHERE email = ?",
            (self.test_user["email"],)
        ).fetchone()
        self.assertIsNotNone(user)

# Bug: Non-Deterministic Tests
class TestRandomManager(unittest.TestCase):
    """
    Non-deterministic tests for RandomManager.
    """
    def setUp(self):
        # Bug: Random values
        # Bug: Time-dependent setup
        self.manager = RandomManager()
        self.test_data = {
            "id": random.randint(1, 1000000),  # Bug: Random value
            "value": random.random(),  # Bug: Random value
            "timestamp": time.time()  # Bug: Time-dependent
        }

    def test_process_data(self):
        # Bug: Non-deterministic test
        # Bug: Random assertions
        # Bug: Time-dependent test
        result = self.manager.process_data(self.test_data)

        # Bug: Random value assertion
        self.assertGreater(result["processed_value"], 0)

        # Bug: Time-dependent assertion
        self.assertLess(time.time() - result["timestamp"], 1.0)

        # Bug: Unpredictable behavior
        self.assertIn(result["status"], ["success", "pending", "failed"])

# Bug: Slow Tests
class TestDatabaseManager(unittest.TestCase):
    """
    Slow tests for DatabaseManager.
    """
    def setUp(self):
        # Bug: Real database connection
        # Bug: Slow setup
        self.manager = DatabaseManager()
        self.db = psycopg2.connect(  # Bug: Real database
            host="localhost",
            database="testdb",
            user="testuser",
            password="testpass"
        )
        self._setup_test_data()  # Bug: Slow operation

    def test_save_data(self):
        # Bug: Slow test
        # Bug: Real database operations
        # Bug: Network calls
        data = {
            "id": 1,
            "value": "test",
            "timestamp": time.time()
        }

        # Bug: Real database operation
        result = self.manager.save_data(data)

        # Bug: Real database query
        saved = self.db.execute(
            "SELECT * FROM data WHERE id = ?",
            (data["id"],)
        ).fetchone()

        self.assertIsNotNone(saved)
        self.assertEqual(saved["value"], data["value"])

# Bug: Complex Test Setup
class TestSystemManager(unittest.TestCase):
    """
    Tests with complex setup for SystemManager.
    """
    def setUp(self):
        # Bug: Many dependencies
        # Bug: Complex initialization
        # Bug: Global state setup
        # Bug: External service setup
        self.manager = SystemManager()
        self.db = DATABASE
        self.cache = CACHE
        self.logger = LOGGER
        self.config = CONFIG

        # Bug: Complex setup
        self._setup_database()
        self._setup_cache()
        self._setup_logger()
        self._setup_config()
        self._setup_external_services()
        self._setup_test_data()
        self._setup_mocks()
        self._setup_fixtures()

    def test_process_request(self):
        # Bug: Complex test
        # Bug: Many dependencies
        # Bug: Global state usage
        request = {
            "id": 1,
            "type": "test",
            "data": {"value": "test"}
        }

        # Bug: Complex test execution
        result = self.manager.process_request(request)

        # Bug: Complex assertions
        self._verify_database_state()
        self._verify_cache_state()
        self._verify_logger_state()
        self._verify_external_service_state()
        self._verify_result(result)

# Bug: Poor Test Organization
class TestMixedManager(unittest.TestCase):
    """
    Tests with poor organization.
    """
    def setUp(self):
        # Bug: Mixed test types
        # Bug: Unclear structure
        # Bug: Missing documentation
        self.manager = MixedManager()
        self.db = DATABASE
        self.cache = CACHE

    def test_1(self):
        # Bug: Poor test naming
        # Bug: Mixed test types
        # Bug: Unclear purpose
        result = self.manager.process_data({"id": 1})
        self.assertIsNotNone(result)

    def test_2(self):
        # Bug: Poor test naming
        # Bug: Mixed test types
        # Bug: Unclear purpose
        result = self.manager.validate_data({"id": 1})
        self.assertTrue(result)

    def test_3(self):
        # Bug: Poor test naming
        # Bug: Mixed test types
        # Bug: Unclear purpose
        result = self.manager.transform_data({"id": 1})
        self.assertIsNotNone(result)

def main():
    """
    Main function to demonstrate testing issues.
    """
    print("Code Testing Issues Demonstration:")
    print("================================")

    try:
        # Test UserManager (Untestable Code)
        user_manager = UserManager()
        result = user_manager.validate_user({
            "name": "John",
            "email": "john@example.com"
        })
        print(f"UserManager validation result: {result}")

        # Test OrderManager (Missing Test Coverage)
        order_manager = OrderManager()
        result = order_manager.process_order({
            "id": 1,
            "items": ["item1", "item2"],
            "total": 100.0
        })
        print(f"OrderManager result: {result}")

        # Run tests
        unittest.main(argv=['first-arg-is-ignored'], exit=False)

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()