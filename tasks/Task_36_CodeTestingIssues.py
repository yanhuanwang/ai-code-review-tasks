#!/usr/bin/env python3
"""
Task 36: Code Testing Issues Challenge

This file contains several intentional testing issues for code review practice.
The task is to identify and fix the following testing problems:

1. Untestable Code:
   - ServiceManager: global state
   - DataManager: hidden dependencies
   - ProcessManager: static methods

2. Missing Test Coverage:
   - UserManager: untested edge cases
   - DataProcessor: missing error cases
   - ValidationManager: incomplete validation

3. Brittle Tests:
   - OrderManager: hard-coded values
   - CacheManager: time-dependent tests
   - FileManager: file system dependencies

4. Test Duplication:
   - TestUserManager: repeated setup
   - TestDataManager: similar test cases
   - TestValidationManager: copied assertions

5. Poor Test Organization:
   - TestManager: mixed test types
   - TestProcessor: unclear test names
   - TestValidator: scattered test cases

6. Non-Deterministic Tests:
   - RandomManager: random values
   - TimeManager: time-based operations
   - NetworkManager: external dependencies

7. Slow Tests:
   - DatabaseManager: real database
   - FileSystemManager: real file system
   - NetworkManager: real network calls

8. Complex Test Setup:
   - ServiceManager: complex initialization
   - DataManager: many dependencies
   - ProcessManager: global state setup

Review the code and identify these testing issues.
"""

import unittest
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

# Bug: Untestable Code
class ServiceManager:
    """
    Service manager with untestable code due to global state and hidden dependencies.
    """
    # Bug: Global state
    _instance = None
    _initialized = False

    def __new__(cls):
        # Bug: Singleton pattern makes testing difficult
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Bug: Hidden dependencies
        if not self._initialized:
            self.db = self._get_database()  # Hidden dependency
            self.cache = self._get_cache()  # Hidden dependency
            self.logger = self._get_logger()  # Hidden dependency
            self._initialized = True

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Global state usage
        # Bug: Hidden dependencies
        try:
            self.db.execute("INSERT INTO data VALUES (?)", (json.dumps(data),))
            self.cache[data["id"]] = data
            self.logger.info(f"Processing data: {data}")
            return data
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {"error": str(e)}

    @staticmethod
    def _get_database():
        # Bug: Static method with hidden implementation
        return sqlite3.connect(":memory:")

    @staticmethod
    def _get_cache():
        # Bug: Static method with hidden implementation
        return {}

    @staticmethod
    def _get_logger():
        # Bug: Static method with hidden implementation
        return logging.getLogger(__name__)

# Bug: Missing Test Coverage
class UserManager:
    """
    User manager with missing test coverage.
    """
    def __init__(self):
        self.users = {}

    def add_user(self, user_data: Dict[str, Any]) -> str:
        # Bug: Missing edge case handling
        # Bug: Missing validation
        # Bug: Missing error cases
        user_id = str(random.randint(1, 1000000))
        self.users[user_id] = user_data
        return user_id

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        # Bug: Missing edge cases
        # Bug: Missing validation
        # Bug: Missing error handling
        if user_id in self.users:
            self.users[user_id].update(updates)
            return True
        return False

    def delete_user(self, user_id: str) -> None:
        # Bug: Missing edge cases
        # Bug: Missing validation
        # Bug: Missing error handling
        if user_id in self.users:
            del self.users[user_id]

# Bug: Brittle Tests
class OrderManager:
    """
    Order manager with brittle tests.
    """
    def __init__(self):
        # Bug: Hard-coded values
        self.min_order_amount = 10.0
        self.max_order_amount = 1000.0
        self.supported_currencies = ["USD", "EUR", "GBP"]
        self.tax_rates = {"USD": 0.1, "EUR": 0.2, "GBP": 0.15}
        self.shipping_rates = {"USD": 5.0, "EUR": 7.0, "GBP": 6.0}
        self.discount_threshold = 100.0
        self.discount_rate = 0.1

    def calculate_order_total(self, order: Dict[str, Any]) -> float:
        # Bug: Hard-coded business logic
        # Bug: Time-dependent calculations
        # Bug: External dependencies
        try:
            amount = order["amount"]
            currency = order["currency"]

            if currency not in self.supported_currencies:
                raise ValueError(f"Unsupported currency: {currency}")

            if amount < self.min_order_amount:
                raise ValueError(f"Amount below minimum: {amount}")

            if amount > self.max_order_amount:
                raise ValueError(f"Amount above maximum: {amount}")

            # Calculate tax
            tax = amount * self.tax_rates[currency]

            # Calculate shipping
            shipping = self.shipping_rates[currency]

            # Calculate discount
            discount = 0.0
            if amount >= self.discount_threshold:
                discount = amount * self.discount_rate

            # Calculate total
            total = amount + tax + shipping - discount

            return round(total, 2)
        except Exception as e:
            raise ValueError(f"Error calculating total: {e}")

# Bug: Test Duplication
class TestUserManager(unittest.TestCase):
    """
    Test user manager with duplicated test code.
    """
    def setUp(self):
        # Bug: Duplicated setup code
        self.manager = UserManager()
        self.test_user = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        self.test_user_id = self.manager.add_user(self.test_user)

    def test_add_user(self):
        # Bug: Duplicated assertions
        # Bug: Similar test cases
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "age": 25
        }
        user_id = self.manager.add_user(user_data)

        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, str)
        self.assertIn(user_id, self.manager.users)
        self.assertEqual(self.manager.users[user_id], user_data)

    def test_update_user(self):
        # Bug: Duplicated assertions
        # Bug: Similar test cases
        updates = {
            "name": "John Updated",
            "age": 31
        }
        result = self.manager.update_user(self.test_user_id, updates)

        self.assertTrue(result)
        self.assertEqual(self.manager.users[self.test_user_id]["name"], updates["name"])
        self.assertEqual(self.manager.users[self.test_user_id]["age"], updates["age"])
        self.assertEqual(self.manager.users[self.test_user_id]["email"], self.test_user["email"])

    def test_delete_user(self):
        # Bug: Duplicated assertions
        # Bug: Similar test cases
        self.manager.delete_user(self.test_user_id)

        self.assertNotIn(self.test_user_id, self.manager.users)
        self.assertEqual(len(self.manager.users), 0)

# Bug: Non-Deterministic Tests
class RandomManager:
    """
    Random manager with non-deterministic tests.
    """
    def __init__(self):
        self.values = []

    def generate_random_data(self) -> Dict[str, Any]:
        # Bug: Non-deterministic output
        # Bug: Random values
        # Bug: Time-dependent
        return {
            "id": random.randint(1, 1000000),
            "value": random.random(),
            "timestamp": time.time(),
            "items": [random.randint(1, 100) for _ in range(random.randint(1, 10))]
        }

    def process_random_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Non-deterministic processing
        # Bug: Random delays
        # Bug: Time-dependent
        time.sleep(random.random() * 0.1)  # Random delay
        data["processed"] = True
        data["process_time"] = time.time()
        return data

# Bug: Slow Tests
class DatabaseManager:
    """
    Database manager with slow tests.
    """
    def __init__(self):
        # Bug: Real database connection
        # Bug: Slow operations
        # Bug: External dependency
        self.conn = psycopg2.connect(
            dbname="test_db",
            user="test_user",
            password="test_password",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        # Bug: Slow setup
        # Bug: Real database operations
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_data (
                id SERIAL PRIMARY KEY,
                data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_data(self, data: Dict[str, Any]) -> int:
        # Bug: Slow operation
        # Bug: Real database write
        self.cursor.execute(
            "INSERT INTO test_data (data) VALUES (%s) RETURNING id",
            (json.dumps(data),)
        )
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def get_data(self, data_id: int) -> Dict[str, Any]:
        # Bug: Slow operation
        # Bug: Real database read
        self.cursor.execute(
            "SELECT data FROM test_data WHERE id = %s",
            (data_id,)
        )
        result = self.cursor.fetchone()
        return json.loads(result[0]) if result else None

# Bug: Complex Test Setup
class ProcessManager:
    """
    Process manager with complex test setup.
    """
    def __init__(self):
        # Bug: Complex initialization
        # Bug: Many dependencies
        # Bug: Global state
        self.db = self._setup_database()
        self.cache = self._setup_cache()
        self.logger = self._setup_logger()
        self.validator = self._setup_validator()
        self.transformer = self._setup_transformer()
        self.notifier = self._setup_notifier()
        self.metrics = self._setup_metrics()
        self.locks = self._setup_locks()
        self.state = self._setup_state()

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Complex processing
        # Bug: Many dependencies
        # Bug: Global state usage
        try:
            # Validate
            if not self.validator.validate(data):
                raise ValueError("Invalid data")

            # Transform
            transformed = self.transformer.transform(data)

            # Save to database
            self.db.execute("INSERT INTO data VALUES (?)", (json.dumps(transformed),))

            # Update cache
            self.cache[transformed["id"]] = transformed

            # Send notification
            self.notifier.notify(transformed)

            # Update metrics
            self.metrics.record(transformed)

            # Update state
            self.state.update(transformed)

            return transformed
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {"error": str(e)}

    def _setup_database(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return sqlite3.connect(":memory:")

    def _setup_cache(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return {}

    def _setup_logger(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return logging.getLogger(__name__)

    def _setup_validator(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return type("Validator", (), {"validate": lambda x: True})()

    def _setup_transformer(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return type("Transformer", (), {"transform": lambda x: x})()

    def _setup_notifier(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return type("Notifier", (), {"notify": lambda x: None})()

    def _setup_metrics(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return type("Metrics", (), {"record": lambda x: None})()

    def _setup_locks(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return {}

    def _setup_state(self):
        # Bug: Complex setup
        # Bug: Hidden dependencies
        return {}

def main():
    """
    Main function to demonstrate testing issues.
    """
    print("Code Testing Issues Demonstration:")
    print("================================")

    try:
        # Test ServiceManager
        service_manager = ServiceManager()
        result = service_manager.process_data({"id": 1, "value": "test"})
        print(f"ServiceManager result: {result}")

        # Test UserManager
        user_manager = UserManager()
        result = user_manager.add_user({"name": "John", "email": "john@example.com"})
        print(f"UserManager result: {result}")

        # Test OrderManager
        order_manager = OrderManager()
        result = order_manager.calculate_order_total({
            "amount": 100.0,
            "currency": "USD"
        })
        print(f"OrderManager result: {result}")

        # Test RandomManager
        random_manager = RandomManager()
        result = random_manager.generate_random_data()
        print(f"RandomManager result: {result}")

        # Test DatabaseManager
        db_manager = DatabaseManager()
        result = db_manager.save_data({"id": 1, "value": "test"})
        print(f"DatabaseManager result: {result}")

        # Test ProcessManager
        process_manager = ProcessManager()
        result = process_manager.process_data({"id": 1, "value": "test"})
        print(f"ProcessManager result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()