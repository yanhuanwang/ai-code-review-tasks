#!/usr/bin/env python3
"""
Task 30: Code Smells Challenge

This file contains several intentional code smells for code review practice.
The task is to identify and fix the following code smells:

1. Long Method:
   - DataProcessor: process_data method too long
   - UserManager: create_user method doing too much
   - OrderProcessor: process_order method complex

2. Large Class:
   - SystemManager: too many responsibilities
   - DataManager: too many methods
   - ServiceManager: too many dependencies

3. Primitive Obsession:
   - UserManager: using strings for user data
   - OrderManager: using dicts for order data
   - ConfigManager: using primitive types

4. Feature Envy:
   - OrderValidator: too much knowledge of Order
   - UserProcessor: too much knowledge of User
   - DataTransformer: too much knowledge of Data

5. Data Class:
   - User: just holding data
   - Order: just holding data
   - Config: just holding data

6. Refused Bequest:
   - SpecialUser: not using parent methods
   - SpecialOrder: not using parent methods
   - SpecialConfig: not using parent methods

7. Switch Statements:
   - PaymentProcessor: switch on payment type
   - OrderProcessor: switch on order status
   - NotificationManager: switch on notification type

8. Temporary Field:
   - DataProcessor: temporary processing state
   - UserManager: temporary session data
   - OrderManager: temporary order state

Review the code and identify these code smells.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import psycopg2
from abc import ABC, abstractmethod
from enum import Enum

# Bug: Long Method
class DataProcessor:
    """
    Data processor with long method smell.
    """
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Long method doing too many things
        try:
            # Validate input
            if not self._validate_input(data):
                raise ValueError("Invalid input")

            # Process data
            processed = {}
            for key, value in data.items():
                # Transform data
                if isinstance(value, str):
                    processed[key] = value.upper()
                elif isinstance(value, int):
                    processed[key] = value * 2
                elif isinstance(value, list):
                    processed[key] = [x * 2 for x in value]
                elif isinstance(value, dict):
                    processed[key] = self._process_nested_dict(value)
                else:
                    processed[key] = value

            # Validate output
            if not self._validate_output(processed):
                raise ValueError("Invalid output")

            # Store results
            self._store_results(processed)

            # Update metrics
            self._update_metrics(processed)

            # Log operation
            self._log_operation(processed)

            # Update cache
            self._update_cache(processed)

            # Notify subscribers
            self._notify_subscribers(processed)

            # Clean up temporary data
            self._cleanup()

            return processed
        except Exception as e:
            self._handle_error(e)
            raise

# Bug: Large Class
class SystemManager:
    """
    System manager with large class smell.
    """
    def __init__(self):
        # Bug: Too many responsibilities
        self.users = {}
        self.data = {}
        self.config = {}
        self.logger = logging.getLogger(__name__)
        self.db_connection = None
        self.cache = {}
        self.sessions = {}
        self.permissions = {}
        self.tasks = {}
        self.notifications = {}
        self.metrics = {}
        self.security = {}
        self.audit_log = {}
        self.system_state = {}

    # Bug: Too many methods
    def handle_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_data(self, data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_config(self, config: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_permission(self, permission_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_metric(self, metric_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_security(self, security_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_audit(self, audit_data: Dict[str, Any]) -> Dict[str, Any]: pass
    def handle_system_state(self, state_data: Dict[str, Any]) -> Dict[str, Any]: pass

# Bug: Primitive Obsession
class UserManager:
    """
    User manager with primitive obsession smell.
    """
    def create_user(self, name: str, email: str, age: int, address: str, phone: str) -> str:
        # Bug: Using primitive types instead of proper objects
        user_id = f"user_{int(time.time())}"
        self.users[user_id] = {
            "name": name,
            "email": email,
            "age": age,
            "address": address,
            "phone": phone,
            "created_at": time.time(),
            "status": "active",
            "last_login": None,
            "login_count": 0
        }
        return user_id

    def update_user(self, user_id: str, name: str = None, email: str = None,
                   age: int = None, address: str = None, phone: str = None) -> bool:
        # Bug: Using primitive types for complex data
        if user_id not in self.users:
            return False
        if name: self.users[user_id]["name"] = name
        if email: self.users[user_id]["email"] = email
        if age: self.users[user_id]["age"] = age
        if address: self.users[user_id]["address"] = address
        if phone: self.users[user_id]["phone"] = phone
        return True

# Bug: Feature Envy
class OrderValidator:
    """
    Order validator with feature envy smell.
    """
    def validate_order(self, order: Dict[str, Any]) -> bool:
        # Bug: Too much knowledge of Order structure
        if not order.get("id"):
            return False
        if not order.get("user_id"):
            return False
        if not order.get("items"):
            return False
        if not order.get("total"):
            return False
        if not order.get("status"):
            return False
        if not order.get("created_at"):
            return False
        if not order.get("shipping_address"):
            return False
        if not order.get("billing_address"):
            return False
        if not order.get("payment_method"):
            return False
        return True

    def validate_order_items(self, items: List[Dict[str, Any]]) -> bool:
        # Bug: Too much knowledge of OrderItem structure
        for item in items:
            if not item.get("id"):
                return False
            if not item.get("name"):
                return False
            if not item.get("price"):
                return False
            if not item.get("quantity"):
                return False
        return True

# Bug: Data Class
@dataclass
class User:
    """
    User class with data class smell.
    """
    # Bug: Just holding data without behavior
    id: str
    name: str
    email: str
    age: int
    address: str
    phone: str
    created_at: float
    status: str
    last_login: Optional[float]
    login_count: int

# Bug: Refused Bequest
class SpecialUser(User):
    """
    Special user with refused bequest smell.
    """
    def __init__(self, *args, **kwargs):
        # Bug: Not using parent class properly
        self.special_data = {}
        self.special_status = "pending"
        self.special_permissions = []

    def update_status(self, status: str) -> None:
        # Bug: Not using parent class methods
        self.special_status = status

    def add_permission(self, permission: str) -> None:
        # Bug: Not using parent class methods
        self.special_permissions.append(permission)

# Bug: Switch Statements
class PaymentProcessor:
    """
    Payment processor with switch statement smell.
    """
    def process_payment(self, payment_type: str, amount: float) -> bool:
        # Bug: Switch statement on type
        if payment_type == "credit_card":
            return self._process_credit_card(amount)
        elif payment_type == "debit_card":
            return self._process_debit_card(amount)
        elif payment_type == "paypal":
            return self._process_paypal(amount)
        elif payment_type == "bank_transfer":
            return self._process_bank_transfer(amount)
        elif payment_type == "crypto":
            return self._process_crypto(amount)
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")

# Bug: Temporary Field
class DataProcessor:
    """
    Data processor with temporary field smell.
    """
    def __init__(self):
        self.data = {}
        # Bug: Temporary fields
        self._temp_processing_state = None
        self._temp_validation_result = None
        self._temp_transformation_data = None
        self._temp_metrics = None
        self._temp_cache = None

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Using temporary fields
        self._temp_processing_state = "started"
        self._temp_validation_result = self._validate_data(data)
        if not self._temp_validation_result:
            self._temp_processing_state = "failed"
            return None

        self._temp_transformation_data = self._transform_data(data)
        self._temp_metrics = self._calculate_metrics(self._temp_transformation_data)
        self._temp_cache = self._update_cache(self._temp_transformation_data)

        self._temp_processing_state = "completed"
        return self._temp_transformation_data

def main():
    """
    Main function to demonstrate code smells.
    """
    print("Code Smells Demonstration:")
    print("========================")

    try:
        # Test DataProcessor
        data_processor = DataProcessor()
        result = data_processor.process_data({"name": "test", "value": 42})
        print(f"DataProcessor result: {result}")

        # Test SystemManager
        system_manager = SystemManager()
        result = system_manager.handle_user({"name": "John", "email": "john@example.com"})
        print(f"SystemManager result: {result}")

        # Test UserManager
        user_manager = UserManager()
        result = user_manager.create_user("John", "john@example.com", 30, "123 Main St", "555-0123")
        print(f"UserManager result: {result}")

        # Test OrderValidator
        order_validator = OrderValidator()
        result = order_validator.validate_order({
            "id": "order1",
            "user_id": "user1",
            "items": [{"id": "item1", "name": "Product", "price": 10.0, "quantity": 1}],
            "total": 10.0,
            "status": "pending",
            "created_at": time.time(),
            "shipping_address": "123 Main St",
            "billing_address": "123 Main St",
            "payment_method": "credit_card"
        })
        print(f"OrderValidator result: {result}")

        # Test User
        user = User(
            id="user1",
            name="John",
            email="john@example.com",
            age=30,
            address="123 Main St",
            phone="555-0123",
            created_at=time.time(),
            status="active",
            last_login=None,
            login_count=0
        )
        print(f"User: {user}")

        # Test SpecialUser
        special_user = SpecialUser(
            id="user2",
            name="Jane",
            email="jane@example.com",
            age=25,
            address="456 Oak St",
            phone="555-0124",
            created_at=time.time(),
            status="active",
            last_login=None,
            login_count=0
        )
        special_user.update_status("special")
        special_user.add_permission("admin")
        print(f"SpecialUser: {special_user}")

        # Test PaymentProcessor
        payment_processor = PaymentProcessor()
        result = payment_processor.process_payment("credit_card", 100.0)
        print(f"PaymentProcessor result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()