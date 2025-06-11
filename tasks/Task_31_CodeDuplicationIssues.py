#!/usr/bin/env python3
"""
Task 31: Code Duplication Issues Challenge

This file contains several intentional code duplication issues for code review practice.
The task is to identify and fix the following duplication problems:

1. Copied Code:
   - ValidationManager: duplicate validation logic
   - DataProcessor: duplicate processing logic
   - UserManager: duplicate user handling

2. Repeated Logic:
   - OrderProcessor: similar order processing
   - PaymentProcessor: similar payment handling
   - NotificationManager: similar notification logic

3. Similar Methods:
   - DataManager: similar data operations
   - FileManager: similar file operations
   - CacheManager: similar cache operations

4. Duplicate Constants:
   - ConfigManager: repeated configuration values
   - ErrorManager: repeated error messages
   - StatusManager: repeated status codes

5. Repeated Patterns:
   - LogManager: similar logging patterns
   - SecurityManager: similar security checks
   - AuditManager: similar audit logging

6. Similar Classes:
   - UserManager/AdminManager: similar user handling
   - OrderManager/InvoiceManager: similar document handling
   - ProductManager/CategoryManager: similar item handling

7. Duplicate Error Handling:
   - DataProcessor: repeated try-except blocks
   - UserProcessor: repeated error checks
   - OrderProcessor: repeated validation

8. Repeated Business Logic:
   - PriceCalculator: similar price calculations
   - DiscountManager: similar discount logic
   - TaxCalculator: similar tax calculations

Review the code and identify these duplication issues.
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

# Bug: Copied Code
class ValidationManager:
    """
    Validation manager with code duplication.
    """
    def validate_user(self, user_data: Dict[str, Any]) -> bool:
        # Bug: Duplicate validation logic
        try:
            # Validate required fields
            required_fields = ["id", "name", "email", "age", "address", "phone"]
            for field in required_fields:
                if field not in user_data:
                    return False

            # Validate email
            if not self._validate_email(user_data["email"]):
                return False

            # Validate age
            if not self._validate_age(user_data["age"]):
                return False

            # Validate phone
            if not self._validate_phone(user_data["phone"]):
                return False

            return True
        except Exception as e:
            return False

    def validate_order(self, order_data: Dict[str, Any]) -> bool:
        # Bug: Duplicate validation logic
        try:
            # Validate required fields
            required_fields = ["id", "user_id", "items", "total", "status", "created_at"]
            for field in required_fields:
                if field not in order_data:
                    return False

            # Validate items
            if not self._validate_items(order_data["items"]):
                return False

            # Validate total
            if not self._validate_total(order_data["total"]):
                return False

            # Validate status
            if not self._validate_status(order_data["status"]):
                return False

            return True
        except Exception as e:
            return False

# Bug: Repeated Logic
class OrderProcessor:
    """
    Order processor with repeated logic.
    """
    def process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Repeated processing logic
        try:
            # Validate order
            if not self._validate_order(order):
                raise ValueError("Invalid order")

            # Calculate total
            total = self._calculate_total(order["items"])

            # Apply discounts
            total = self._apply_discounts(total, order.get("discounts", []))

            # Calculate tax
            tax = self._calculate_tax(total, order.get("tax_rate", 0.1))

            # Update order
            order["total"] = total
            order["tax"] = tax
            order["status"] = "processed"
            order["processed_at"] = time.time()

            return order
        except Exception as e:
            return {"error": str(e)}

    def process_invoice(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Similar processing logic
        try:
            # Validate invoice
            if not self._validate_invoice(invoice):
                raise ValueError("Invalid invoice")

            # Calculate total
            total = self._calculate_total(invoice["items"])

            # Apply discounts
            total = self._apply_discounts(total, invoice.get("discounts", []))

            # Calculate tax
            tax = self._calculate_tax(total, invoice.get("tax_rate", 0.1))

            # Update invoice
            invoice["total"] = total
            invoice["tax"] = tax
            invoice["status"] = "processed"
            invoice["processed_at"] = time.time()

            return invoice
        except Exception as e:
            return {"error": str(e)}

# Bug: Similar Methods
class DataManager:
    """
    Data manager with similar methods.
    """
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        # Bug: Similar save logic
        try:
            # Validate data
            if not self._validate_user_data(user_data):
                return False

            # Format data
            formatted_data = self._format_user_data(user_data)

            # Save to database
            self._save_to_db("users", formatted_data)

            # Update cache
            self._update_user_cache(formatted_data)

            # Log operation
            self._log_user_save(formatted_data)

            return True
        except Exception as e:
            return False

    def save_order(self, order_data: Dict[str, Any]) -> bool:
        # Bug: Similar save logic
        try:
            # Validate data
            if not self._validate_order_data(order_data):
                return False

            # Format data
            formatted_data = self._format_order_data(order_data)

            # Save to database
            self._save_to_db("orders", formatted_data)

            # Update cache
            self._update_order_cache(formatted_data)

            # Log operation
            self._log_order_save(formatted_data)

            return True
        except Exception as e:
            return False

# Bug: Duplicate Constants
class ConfigManager:
    """
    Config manager with duplicate constants.
    """
    # Bug: Duplicate status codes
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"
    STATUS_REFUNDED = "refunded"
    STATUS_PROCESSING = "processing"

    # Bug: Duplicate error messages
    ERROR_INVALID_INPUT = "Invalid input data"
    ERROR_MISSING_FIELD = "Required field is missing"
    ERROR_INVALID_FORMAT = "Invalid data format"
    ERROR_DATABASE_ERROR = "Database operation failed"
    ERROR_NETWORK_ERROR = "Network operation failed"
    ERROR_AUTH_ERROR = "Authentication failed"
    ERROR_PERMISSION_ERROR = "Permission denied"
    ERROR_VALIDATION_ERROR = "Validation failed"

# Bug: Repeated Patterns
class LogManager:
    """
    Log manager with repeated patterns.
    """
    def log_user_action(self, user_id: str, action: str, details: Dict[str, Any]) -> None:
        # Bug: Repeated logging pattern
        try:
            # Format log data
            log_data = {
                "timestamp": time.time(),
                "user_id": user_id,
                "action": action,
                "details": details,
                "level": "info",
                "source": "user_action"
            }

            # Write to log file
            self._write_to_log_file(log_data)

            # Update metrics
            self._update_user_metrics(user_id, action)

            # Notify if needed
            if self._should_notify(action):
                self._send_notification(log_data)
        except Exception as e:
            self._handle_log_error(e)

    def log_system_action(self, action: str, details: Dict[str, Any]) -> None:
        # Bug: Similar logging pattern
        try:
            # Format log data
            log_data = {
                "timestamp": time.time(),
                "action": action,
                "details": details,
                "level": "info",
                "source": "system_action"
            }

            # Write to log file
            self._write_to_log_file(log_data)

            # Update metrics
            self._update_system_metrics(action)

            # Notify if needed
            if self._should_notify(action):
                self._send_notification(log_data)
        except Exception as e:
            self._handle_log_error(e)

# Bug: Similar Classes
class UserManager:
    """
    User manager with similar class structure.
    """
    def __init__(self):
        self.users = {}
        self.logger = logging.getLogger(__name__)

    def create_user(self, user_data: Dict[str, Any]) -> str:
        # Bug: Similar user handling
        try:
            user_id = f"user_{int(time.time())}"
            self.users[user_id] = user_data
            self._log_user_creation(user_id)
            return user_id
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            raise

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        # Bug: Similar user handling
        try:
            if user_id not in self.users:
                return False
            self.users[user_id].update(updates)
            self._log_user_update(user_id)
            return True
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            return False

class AdminManager:
    """
    Admin manager with similar class structure.
    """
    def __init__(self):
        self.admins = {}
        self.logger = logging.getLogger(__name__)

    def create_admin(self, admin_data: Dict[str, Any]) -> str:
        # Bug: Similar admin handling
        try:
            admin_id = f"admin_{int(time.time())}"
            self.admins[admin_id] = admin_data
            self._log_admin_creation(admin_id)
            return admin_id
        except Exception as e:
            self.logger.error(f"Error creating admin: {e}")
            raise

    def update_admin(self, admin_id: str, updates: Dict[str, Any]) -> bool:
        # Bug: Similar admin handling
        try:
            if admin_id not in self.admins:
                return False
            self.admins[admin_id].update(updates)
            self._log_admin_update(admin_id)
            return True
        except Exception as e:
            self.logger.error(f"Error updating admin: {e}")
            return False

# Bug: Duplicate Error Handling
class DataProcessor:
    """
    Data processor with duplicate error handling.
    """
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Repeated error handling
        try:
            # Validate input
            if not self._validate_input(data):
                raise ValueError("Invalid input")

            # Process data
            processed = self._process_data(data)

            # Validate output
            if not self._validate_output(processed):
                raise ValueError("Invalid output")

            return processed
        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            return {"error": str(e)}
        except Exception as e:
            self.logger.error(f"Processing error: {e}")
            return {"error": str(e)}

    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Similar error handling
        try:
            # Validate input
            if not self._validate_input(data):
                raise ValueError("Invalid input")

            # Transform data
            transformed = self._transform_data(data)

            # Validate output
            if not self._validate_output(transformed):
                raise ValueError("Invalid output")

            return transformed
        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            return {"error": str(e)}
        except Exception as e:
            self.logger.error(f"Transformation error: {e}")
            return {"error": str(e)}

# Bug: Repeated Business Logic
class PriceCalculator:
    """
    Price calculator with repeated business logic.
    """
    def calculate_price(self, item: Dict[str, Any]) -> float:
        # Bug: Duplicate price calculation
        base_price = item["price"]
        quantity = item["quantity"]

        # Calculate subtotal
        subtotal = base_price * quantity

        # Apply discounts
        if "discount" in item:
            discount = subtotal * item["discount"]
            subtotal -= discount

        # Apply tax
        tax_rate = item.get("tax_rate", 0.1)
        tax = subtotal * tax_rate

        # Calculate total
        total = subtotal + tax

        return total

    def calculate_discount(self, item: Dict[str, Any]) -> float:
        # Bug: Similar price calculation
        base_price = item["price"]
        quantity = item["quantity"]

        # Calculate subtotal
        subtotal = base_price * quantity

        # Apply discount rate
        discount_rate = item.get("discount_rate", 0.1)
        discount = subtotal * discount_rate

        return discount

def main():
    """
    Main function to demonstrate code duplication issues.
    """
    print("Code Duplication Issues Demonstration:")
    print("====================================")

    try:
        # Test ValidationManager
        validation_manager = ValidationManager()
        result = validation_manager.validate_user({
            "id": "user1",
            "name": "John",
            "email": "john@example.com",
            "age": 30,
            "address": "123 Main St",
            "phone": "555-0123"
        })
        print(f"ValidationManager result: {result}")

        # Test OrderProcessor
        order_processor = OrderProcessor()
        result = order_processor.process_order({
            "id": "order1",
            "user_id": "user1",
            "items": [{"price": 10.0, "quantity": 2}],
            "discounts": [{"rate": 0.1}],
            "tax_rate": 0.1
        })
        print(f"OrderProcessor result: {result}")

        # Test DataManager
        data_manager = DataManager()
        result = data_manager.save_user({
            "id": "user1",
            "name": "John",
            "email": "john@example.com"
        })
        print(f"DataManager result: {result}")

        # Test LogManager
        log_manager = LogManager()
        log_manager.log_user_action("user1", "login", {"ip": "127.0.0.1"})
        print("LogManager: User action logged")

        # Test UserManager and AdminManager
        user_manager = UserManager()
        result = user_manager.create_user({"name": "John", "email": "john@example.com"})
        print(f"UserManager result: {result}")

        admin_manager = AdminManager()
        result = admin_manager.create_admin({"name": "Admin", "email": "admin@example.com"})
        print(f"AdminManager result: {result}")

        # Test DataProcessor
        data_processor = DataProcessor()
        result = data_processor.process_data({"name": "test", "value": 42})
        print(f"DataProcessor result: {result}")

        # Test PriceCalculator
        price_calculator = PriceCalculator()
        result = price_calculator.calculate_price({
            "price": 100.0,
            "quantity": 2,
            "discount": 0.1,
            "tax_rate": 0.1
        })
        print(f"PriceCalculator result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()