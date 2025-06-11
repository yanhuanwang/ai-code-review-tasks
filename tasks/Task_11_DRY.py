#!/usr/bin/env python3
"""
Task 11: Code Duplication and DRY Challenge

This file contains several intentional code duplication and DRY violations for code review practice.
The task is to identify and fix the following issues:
1. Repeated validation logic in UserValidator
2. Duplicated data transformation in DataProcessor
3. Repeated error handling in ServiceManager
4. Duplicated business logic in OrderProcessor
5. Repeated utility functions in HelperUtils
6. Duplicated configuration handling in ConfigManager
7. Repeated data access patterns in Repository
8. Duplicated logging patterns in Logger

Review the code and identify these code duplication and DRY violations.
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

class UserValidator:
    """
    Validates user data.
    Bug: Repeated validation logic across methods.
    """
    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate user name."""
        # Bug: Duplicated validation logic
        if not name:
            return False, "Name cannot be empty"
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        if len(name) > 50:
            return False, "Name must be at most 50 characters"
        if not name.replace(" ", "").isalpha():
            return False, "Name must contain only letters and spaces"
        return True, "Valid name"

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email address."""
        # Bug: Duplicated validation logic
        if not email:
            return False, "Email cannot be empty"
        if len(email) < 5:
            return False, "Email must be at least 5 characters"
        if len(email) > 100:
            return False, "Email must be at most 100 characters"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"
        return True, "Valid email"

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password."""
        # Bug: Duplicated validation logic
        if not password:
            return False, "Password cannot be empty"
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if len(password) > 50:
            return False, "Password must be at most 50 characters"
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"
        return True, "Valid password"

    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """Validate phone number."""
        # Bug: Duplicated validation logic
        if not phone:
            return False, "Phone number cannot be empty"
        if len(phone) < 10:
            return False, "Phone number must be at least 10 digits"
        if len(phone) > 15:
            return False, "Phone number must be at most 15 digits"
        if not re.match(r"^\+?[\d\s-]+$", phone):
            return False, "Invalid phone number format"
        return True, "Valid phone number"

class DataProcessor:
    """
    Processes various types of data.
    Bug: Duplicated data transformation logic.
    """
    def process_user_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user data."""
        # Bug: Duplicated transformation logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().lower()
            elif isinstance(value, (int, float)):
                result[key] = float(value)
            elif isinstance(value, list):
                result[key] = [str(item).strip().lower() for item in value]
            elif isinstance(value, dict):
                result[key] = {k: str(v).strip().lower() for k, v in value.items()}
            else:
                result[key] = value
        return result

    def process_order_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process order data."""
        # Bug: Duplicated transformation logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().lower()
            elif isinstance(value, (int, float)):
                result[key] = float(value)
            elif isinstance(value, list):
                result[key] = [str(item).strip().lower() for item in value]
            elif isinstance(value, dict):
                result[key] = {k: str(v).strip().lower() for k, v in value.items()}
            else:
                result[key] = value
        return result

    def process_product_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process product data."""
        # Bug: Duplicated transformation logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().lower()
            elif isinstance(value, (int, float)):
                result[key] = float(value)
            elif isinstance(value, list):
                result[key] = [str(item).strip().lower() for item in value]
            elif isinstance(value, dict):
                result[key] = {k: str(v).strip().lower() for k, v in value.items()}
            else:
                result[key] = value
        return result

class ServiceManager:
    """
    Manages various services.
    Bug: Repeated error handling patterns.
    """
    def process_user_service(self, user_id: str) -> Dict[str, Any]:
        """Process user service request."""
        # Bug: Duplicated error handling
        try:
            if not user_id:
                return {"status": "error", "message": "User ID is required"}
            if not isinstance(user_id, str):
                return {"status": "error", "message": "User ID must be a string"}
            if len(user_id) < 1:
                return {"status": "error", "message": "User ID cannot be empty"}
            # Process user service
            return {"status": "success", "data": {"user_id": user_id}}
        except Exception as e:
            logger.error(f"Error processing user service: {e}")
            return {"status": "error", "message": str(e)}

    def process_order_service(self, order_id: str) -> Dict[str, Any]:
        """Process order service request."""
        # Bug: Duplicated error handling
        try:
            if not order_id:
                return {"status": "error", "message": "Order ID is required"}
            if not isinstance(order_id, str):
                return {"status": "error", "message": "Order ID must be a string"}
            if len(order_id) < 1:
                return {"status": "error", "message": "Order ID cannot be empty"}
            # Process order service
            return {"status": "success", "data": {"order_id": order_id}}
        except Exception as e:
            logger.error(f"Error processing order service: {e}")
            return {"status": "error", "message": str(e)}

    def process_payment_service(self, payment_id: str) -> Dict[str, Any]:
        """Process payment service request."""
        # Bug: Duplicated error handling
        try:
            if not payment_id:
                return {"status": "error", "message": "Payment ID is required"}
            if not isinstance(payment_id, str):
                return {"status": "error", "message": "Payment ID must be a string"}
            if len(payment_id) < 1:
                return {"status": "error", "message": "Payment ID cannot be empty"}
            # Process payment service
            return {"status": "success", "data": {"payment_id": payment_id}}
        except Exception as e:
            logger.error(f"Error processing payment service: {e}")
            return {"status": "error", "message": str(e)}

class OrderProcessor:
    """
    Processes orders with business logic.
    Bug: Duplicated business logic across methods.
    """
    def calculate_order_total(self, items: List[Dict[str, Any]]) -> float:
        """Calculate order total."""
        # Bug: Duplicated business logic
        total = 0.0
        for item in items:
            price = float(item.get("price", 0))
            quantity = int(item.get("quantity", 0))
            discount = float(item.get("discount", 0))
            tax_rate = float(item.get("tax_rate", 0.1))

            subtotal = price * quantity
            discount_amount = subtotal * (discount / 100)
            taxable_amount = subtotal - discount_amount
            tax_amount = taxable_amount * tax_rate

            total += taxable_amount + tax_amount
        return total

    def calculate_shipping_cost(self, items: List[Dict[str, Any]], address: Dict[str, Any]) -> float:
        """Calculate shipping cost."""
        # Bug: Duplicated business logic
        total_weight = 0.0
        for item in items:
            weight = float(item.get("weight", 0))
            quantity = int(item.get("quantity", 0))
            total_weight += weight * quantity

        base_rate = 10.0
        weight_rate = total_weight * 2.0
        distance_rate = 0.0

        if address.get("country") == "US":
            distance_rate = 5.0
        elif address.get("country") == "CA":
            distance_rate = 8.0
        else:
            distance_rate = 15.0

        return base_rate + weight_rate + distance_rate

    def calculate_discount(self, items: List[Dict[str, Any]], coupon: Optional[str] = None) -> float:
        """Calculate discount amount."""
        # Bug: Duplicated business logic
        subtotal = 0.0
        for item in items:
            price = float(item.get("price", 0))
            quantity = int(item.get("quantity", 0))
            subtotal += price * quantity

        discount_rate = 0.0
        if coupon == "SAVE10":
            discount_rate = 0.1
        elif coupon == "SAVE20":
            discount_rate = 0.2
        elif coupon == "SAVE30":
            discount_rate = 0.3

        return subtotal * discount_rate

class HelperUtils:
    """
    Utility functions.
    Bug: Repeated utility functions with similar logic.
    """
    def format_user_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format user data."""
        # Bug: Duplicated formatting logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().title()
            elif isinstance(value, (int, float)):
                result[key] = f"{value:.2f}"
            elif isinstance(value, datetime):
                result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[key] = value
        return result

    def format_order_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format order data."""
        # Bug: Duplicated formatting logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().title()
            elif isinstance(value, (int, float)):
                result[key] = f"{value:.2f}"
            elif isinstance(value, datetime):
                result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[key] = value
        return result

    def format_product_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format product data."""
        # Bug: Duplicated formatting logic
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip().title()
            elif isinstance(value, (int, float)):
                result[key] = f"{value:.2f}"
            elif isinstance(value, datetime):
                result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[key] = value
        return result

class ConfigManager:
    """
    Manages configuration settings.
    Bug: Duplicated configuration handling.
    """
    def __init__(self):
        self.config = {}

    def load_user_config(self, filepath: str) -> Dict[str, Any]:
        """Load user configuration."""
        # Bug: Duplicated configuration loading
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
                self._validate_config(config, ["username", "email", "preferences"])
                self._set_defaults(config, {
                    "notifications": True,
                    "theme": "light",
                    "language": "en"
                })
                self.config.update(config)
                return config
        except Exception as e:
            logger.error(f"Error loading user config: {e}")
            return {}

    def load_app_config(self, filepath: str) -> Dict[str, Any]:
        """Load application configuration."""
        # Bug: Duplicated configuration loading
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
                self._validate_config(config, ["app_name", "version", "environment"])
                self._set_defaults(config, {
                    "debug": False,
                    "log_level": "INFO",
                    "timeout": 30
                })
                self.config.update(config)
                return config
        except Exception as e:
            logger.error(f"Error loading app config: {e}")
            return {}

    def load_db_config(self, filepath: str) -> Dict[str, Any]:
        """Load database configuration."""
        # Bug: Duplicated configuration loading
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
                self._validate_config(config, ["host", "port", "database"])
                self._set_defaults(config, {
                    "pool_size": 5,
                    "timeout": 10,
                    "retry_attempts": 3
                })
                self.config.update(config)
                return config
        except Exception as e:
            logger.error(f"Error loading db config: {e}")
            return {}

    def _validate_config(self, config: Dict[str, Any], required_keys: List[str]) -> None:
        """Validate configuration."""
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")

    def _set_defaults(self, config: Dict[str, Any], defaults: Dict[str, Any]) -> None:
        """Set default values."""
        for key, value in defaults.items():
            if key not in config:
                config[key] = value

class Repository:
    """
    Data access layer.
    Bug: Duplicated data access patterns.
    """
    def __init__(self):
        self.data = {}

    def save_user(self, user: Dict[str, Any]) -> bool:
        """Save user data."""
        # Bug: Duplicated data access pattern
        try:
            if "id" not in user:
                user["id"] = str(random.randint(1000, 9999))
            if "created_at" not in user:
                user["created_at"] = datetime.now().isoformat()
            if "updated_at" not in user:
                user["updated_at"] = datetime.now().isoformat()

            if "users" not in self.data:
                self.data["users"] = {}
            self.data["users"][user["id"]] = user
            return True
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            return False

    def save_order(self, order: Dict[str, Any]) -> bool:
        """Save order data."""
        # Bug: Duplicated data access pattern
        try:
            if "id" not in order:
                order["id"] = str(random.randint(1000, 9999))
            if "created_at" not in order:
                order["created_at"] = datetime.now().isoformat()
            if "updated_at" not in order:
                order["updated_at"] = datetime.now().isoformat()

            if "orders" not in self.data:
                self.data["orders"] = {}
            self.data["orders"][order["id"]] = order
            return True
        except Exception as e:
            logger.error(f"Error saving order: {e}")
            return False

    def save_product(self, product: Dict[str, Any]) -> bool:
        """Save product data."""
        # Bug: Duplicated data access pattern
        try:
            if "id" not in product:
                product["id"] = str(random.randint(1000, 9999))
            if "created_at" not in product:
                product["created_at"] = datetime.now().isoformat()
            if "updated_at" not in product:
                product["updated_at"] = datetime.now().isoformat()

            if "products" not in self.data:
                self.data["products"] = {}
            self.data["products"][product["id"]] = product
            return True
        except Exception as e:
            logger.error(f"Error saving product: {e}")
            return False

class Logger:
    """
    Logging utility.
    Bug: Duplicated logging patterns.
    """
    def log_user_action(self, user_id: str, action: str, details: Dict[str, Any]) -> None:
        """Log user action."""
        # Bug: Duplicated logging pattern
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "category": "user",
                "user_id": user_id,
                "action": action,
                "details": details
            }
            logger.info(json.dumps(log_entry))
        except Exception as e:
            logger.error(f"Error logging user action: {e}")

    def log_order_action(self, order_id: str, action: str, details: Dict[str, Any]) -> None:
        """Log order action."""
        # Bug: Duplicated logging pattern
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "category": "order",
                "order_id": order_id,
                "action": action,
                "details": details
            }
            logger.info(json.dumps(log_entry))
        except Exception as e:
            logger.error(f"Error logging order action: {e}")

    def log_system_action(self, action: str, details: Dict[str, Any]) -> None:
        """Log system action."""
        # Bug: Duplicated logging pattern
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "category": "system",
                "action": action,
                "details": details
            }
            logger.info(json.dumps(log_entry))
        except Exception as e:
            logger.error(f"Error logging system action: {e}")

def main():
    # Test UserValidator repeated validation
    print("Testing UserValidator repeated validation:")
    validator = UserValidator()
    print(f"Name validation: {validator.validate_name('John Doe')}")
    print(f"Email validation: {validator.validate_email('john@example.com')}")
    print(f"Password validation: {validator.validate_password('Password123')}")
    print(f"Phone validation: {validator.validate_phone('+1-234-567-8900')}")

    # Test DataProcessor duplicated transformation
    print("\nTesting DataProcessor duplicated transformation:")
    processor = DataProcessor()
    user_data = {"name": " John ", "age": 30, "scores": [85, 90, 95]}
    print(f"Processed user data: {processor.process_user_data(user_data)}")
    order_data = {"id": " 123 ", "total": 100.50, "items": ["item1", "item2"]}
    print(f"Processed order data: {processor.process_order_data(order_data)}")

    # Test ServiceManager repeated error handling
    print("\nTesting ServiceManager repeated error handling:")
    manager = ServiceManager()
    print(f"User service: {manager.process_user_service('user1')}")
    print(f"Order service: {manager.process_order_service('order1')}")
    print(f"Payment service: {manager.process_payment_service('payment1')}")

    # Test OrderProcessor duplicated business logic
    print("\nTesting OrderProcessor duplicated business logic:")
    processor = OrderProcessor()
    items = [
        {"price": 10.0, "quantity": 2, "discount": 10, "tax_rate": 0.1},
        {"price": 20.0, "quantity": 1, "discount": 0, "tax_rate": 0.1}
    ]
    print(f"Order total: {processor.calculate_order_total(items)}")
    print(f"Shipping cost: {processor.calculate_shipping_cost(items, {'country': 'US'})}")
    print(f"Discount: {processor.calculate_discount(items, 'SAVE10')}")

    # Test HelperUtils repeated utility functions
    print("\nTesting HelperUtils repeated utility functions:")
    utils = HelperUtils()
    user_data = {"name": " john doe ", "age": 30, "created_at": datetime.now()}
    print(f"Formatted user data: {utils.format_user_data(user_data)}")
    order_data = {"id": " order123 ", "total": 100.50, "created_at": datetime.now()}
    print(f"Formatted order data: {utils.format_order_data(order_data)}")

    # Test ConfigManager duplicated configuration
    print("\nTesting ConfigManager duplicated configuration:")
    config_manager = ConfigManager()
    # Note: These would normally load from files
    print("Config manager initialized")

    # Test Repository duplicated data access
    print("\nTesting Repository duplicated data access:")
    repo = Repository()
    user = {"name": "John Doe", "email": "john@example.com"}
    print(f"Saved user: {repo.save_user(user)}")
    order = {"user_id": user["id"], "total": 100.50}
    print(f"Saved order: {repo.save_order(order)}")

    # Test Logger duplicated logging
    print("\nTesting Logger duplicated logging:")
    logger = Logger()
    logger.log_user_action("user1", "login", {"ip": "127.0.0.1"})
    logger.log_order_action("order1", "created", {"total": 100.50})
    logger.log_system_action("startup", {"version": "1.0.0"})

if __name__ == "__main__":
    main()