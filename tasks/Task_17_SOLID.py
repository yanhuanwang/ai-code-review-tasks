#!/usr/bin/env python3
"""
Task 17: SOLID Principle Violations Challenge

This file contains several intentional SOLID principle violations for code review practice.
The task is to identify and fix the following issues:

1. Single Responsibility Principle (SRP) Violations:
   - UserManager: Mixed user management, validation, and notification
   - OrderProcessor: Mixed order processing, payment, and inventory
   - ReportGenerator: Mixed report generation, formatting, and delivery

2. Open/Closed Principle (OCP) Violations:
   - PaymentHandler: Not open for extension
   - NotificationService: Hard-coded notification types
   - DataExporter: Not extensible for new export formats

3. Liskov Substitution Principle (LSP) Violations:
   - Animal hierarchy: Subtypes not substitutable
   - PaymentMethod hierarchy: Violated contract
   - Report hierarchy: Inconsistent behavior

4. Interface Segregation Principle (ISP) Violations:
   - DataProcessor: Fat interface
   - UserService: Mixed concerns in interface
   - StorageService: Unnecessary method requirements

5. Dependency Inversion Principle (DIP) Violations:
   - OrderService: High-level module depends on low-level
   - NotificationManager: Direct dependency on concrete classes
   - DataManager: Tight coupling to specific implementations

Review the code and identify these SOLID principle violations.
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple, Protocol
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from pathlib import Path
import re
import hashlib
from enum import Enum
import sqlite3
import os
import requests
import redis
import smtplib
from email.mime.text import MIMEText
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: SRP Violation - Mixed responsibilities in user management
class UserManager:
    """
    Violates SRP by mixing user management, validation, and notification.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - database, validation, and notification
        self.db = sqlite3.connect('users.db')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT,
                created_at TEXT
            )
        ''')

        # Bug: Mixed responsibilities - email configuration
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')

        # Bug: Mixed responsibilities - validation rules
        self.validation_rules = {
            'name': {'min_length': 2, 'max_length': 50},
            'email': {'pattern': r'^[^@]+@[^@]+\.[^@]+$'},
            'password': {'min_length': 8, 'require_special': True}
        }

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities - validation, persistence, and notification
        if not self._validate_user_data(user_data):
            raise ValueError("Invalid user data")

        user_id = str(random.randint(1000, 9999))
        user = {
            'id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'password': hashlib.sha256(user_data['password'].encode()).hexdigest(),
            'created_at': datetime.now().isoformat()
        }

        self.db.execute('''
            INSERT INTO users (id, name, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'],
              user['password'], user['created_at']))
        self.db.commit()

        self._send_welcome_email(user['email'], user['name'])
        self._log_user_creation(user)

        return user

    def _validate_user_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed responsibilities - validation logic
        if 'name' not in data or 'email' not in data or 'password' not in data:
            return False

        if not (self.validation_rules['name']['min_length'] <=
                len(data['name']) <=
                self.validation_rules['name']['max_length']):
            return False

        if not re.match(self.validation_rules['email']['pattern'],
                       data['email']):
            return False

        if not (len(data['password']) >=
                self.validation_rules['password']['min_length'] and
                bool(re.search(r'[!@#$%^&*(),.?":{}|<>]',
                             data['password']))):
            return False

        return True

    def _send_welcome_email(self, email: str, name: str) -> None:
        # Bug: Mixed responsibilities - email sending
        msg = MIMEText(f"Welcome {name}!")
        msg['Subject'] = 'Welcome to our service'
        msg['From'] = 'app@gmail.com'
        msg['To'] = email
        self.smtp_server.send_message(msg)

    def _log_user_creation(self, user: Dict[str, Any]) -> None:
        # Bug: Mixed responsibilities - logging
        logger.info(f"Created user: {user['id']}")

# Bug: OCP Violation - Not open for extension
class PaymentHandler:
    """
    Violates OCP by not being open for extension.
    """
    def __init__(self):
        # Bug: Not open for extension - hard-coded payment methods
        self.payment_methods = {
            'credit_card': self._process_credit_card,
            'paypal': self._process_paypal,
            'bank_transfer': self._process_bank_transfer
        }

    def process_payment(self, amount: float, currency: str,
                       method: str) -> Dict[str, Any]:
        # Bug: Not open for extension - can't add new payment methods
        if method not in self.payment_methods:
            raise ValueError(f"Unsupported payment method: {method}")

        return self.payment_methods[method](amount, currency)

    def _process_credit_card(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Not open for extension - hard-coded implementation
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'credit_card',
            'transaction_id': f"CC-{random.randint(100000, 999999)}"
        }

    def _process_paypal(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Not open for extension - hard-coded implementation
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'paypal',
            'transaction_id': f"PP-{random.randint(100000, 999999)}"
        }

    def _process_bank_transfer(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Not open for extension - hard-coded implementation
        return {
            'status': 'pending',
            'amount': amount,
            'currency': currency,
            'method': 'bank_transfer',
            'transaction_id': f"BT-{random.randint(100000, 999999)}"
        }

# Bug: LSP Violation - Subtypes not substitutable
class Animal:
    """
    Base class for animals violating LSP.
    """
    def __init__(self, name: str):
        self.name = name

    def make_sound(self) -> str:
        return "Some sound"

    def move(self) -> str:
        return "Moving"

    def eat(self) -> str:
        return "Eating"

class Dog(Animal):
    """
    Dog class violating LSP.
    """
    def make_sound(self) -> str:
        return "Woof!"

    def move(self) -> str:
        # Bug: LSP violation - changed behavior
        return "Running on four legs"

    def eat(self) -> str:
        # Bug: LSP violation - changed behavior
        return "Eating dog food"

class Fish(Animal):
    """
    Fish class violating LSP.
    """
    def make_sound(self) -> str:
        # Bug: LSP violation - changed behavior
        raise NotImplementedError("Fish don't make sounds")

    def move(self) -> str:
        # Bug: LSP violation - changed behavior
        return "Swimming"

    def eat(self) -> str:
        # Bug: LSP violation - changed behavior
        return "Eating fish food"

# Bug: ISP Violation - Fat interface
class DataProcessor(ABC):
    """
    Interface violating ISP by requiring unnecessary methods.
    """
    @abstractmethod
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def save_data(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def load_data(self, data_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_data(self, data_id: str) -> None:
        pass

    @abstractmethod
    def export_data(self, data: Dict[str, Any], format: str) -> str:
        pass

    @abstractmethod
    def import_data(self, data: str, format: str) -> Dict[str, Any]:
        pass

class UserProcessor(DataProcessor):
    """
    Implementation of DataProcessor violating ISP.
    """
    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: ISP violation - forced to implement unnecessary methods
        return {k: str(v).lower() for k, v in data.items()}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        # Bug: ISP violation - forced to implement unnecessary methods
        return 'name' in data and 'email' in data

    def save_data(self, data: Dict[str, Any]) -> None:
        # Bug: ISP violation - forced to implement unnecessary methods
        pass

    def load_data(self, data_id: str) -> Dict[str, Any]:
        # Bug: ISP violation - forced to implement unnecessary methods
        return {}

    def delete_data(self, data_id: str) -> None:
        # Bug: ISP violation - forced to implement unnecessary methods
        pass

    def export_data(self, data: Dict[str, Any], format: str) -> str:
        # Bug: ISP violation - forced to implement unnecessary methods
        return json.dumps(data)

    def import_data(self, data: str, format: str) -> Dict[str, Any]:
        # Bug: ISP violation - forced to implement unnecessary methods
        return json.loads(data)

# Bug: DIP Violation - High-level module depends on low-level
class OrderService:
    """
    Service violating DIP by depending on concrete implementations.
    """
    def __init__(self):
        # Bug: DIP violation - depends on concrete implementations
        self.db = sqlite3.connect('orders.db')
        self.payment_processor = PaymentHandler()
        self.notification_service = NotificationService()
        self.inventory_service = InventoryService()

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: DIP violation - depends on concrete implementations
        order_id = f"ORD-{random.randint(100000, 999999)}"
        order = {
            'id': order_id,
            'user_id': order_data['user_id'],
            'items': order_data['items'],
            'total': sum(item['price'] * item['quantity']
                        for item in order_data['items']),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        # Bug: DIP violation - direct dependency on concrete implementations
        self.db.execute('''
            INSERT INTO orders (id, user_id, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order['id'], order['user_id'], json.dumps(order['items']),
              order['total'], order['status'], order['created_at']))
        self.db.commit()

        payment_result = self.payment_processor.process_payment(
            order['total'],
            'USD',
            'credit_card'
        )

        self.inventory_service.update_inventory(order['items'])

        self.notification_service.send_notification(
            order['user_id'],
            'order_confirmation',
            {'order_id': order['id'], 'total': order['total']}
        )

        return order

class NotificationService:
    """
    Service for sending notifications.
    """
    def send_notification(self, user_id: str, template: str,
                         data: Dict[str, Any]) -> None:
        # Simulate notification sending
        print(f"Sending {template} notification to {user_id}: {data}")

class InventoryService:
    """
    Service for managing inventory.
    """
    def update_inventory(self, items: List[Dict[str, Any]]) -> None:
        # Simulate inventory update
        print(f"Updating inventory for items: {items}")

def main():
    # Test SRP violation in UserManager
    print("Testing SRP violation in UserManager:")
    user_manager = UserManager()
    try:
        user = user_manager.create_user({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'Password123!'
        })
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Test OCP violation in PaymentHandler
    print("\nTesting OCP violation in PaymentHandler:")
    payment_handler = PaymentHandler()
    try:
        result = payment_handler.process_payment(100.0, "USD", "credit_card")
        print(f"Payment result: {result}")
    except Exception as e:
        print(f"Error processing payment: {e}")

    # Test LSP violation in Animal hierarchy
    print("\nTesting LSP violation in Animal hierarchy:")
    animals = [Dog("Rex"), Fish("Nemo")]
    for animal in animals:
        try:
            print(f"{animal.name} sound: {animal.make_sound()}")
            print(f"{animal.name} move: {animal.move()}")
            print(f"{animal.name} eat: {animal.eat()}")
        except Exception as e:
            print(f"Error with {animal.name}: {e}")

    # Test ISP violation in DataProcessor
    print("\nTesting ISP violation in DataProcessor:")
    user_processor = UserProcessor()
    try:
        result = user_processor.process_data({
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        print(f"Processed data: {result}")
    except Exception as e:
        print(f"Error processing data: {e}")

    # Test DIP violation in OrderService
    print("\nTesting DIP violation in OrderService:")
    order_service = OrderService()
    try:
        order = order_service.process_order({
            'user_id': 'user1',
            'items': [
                {'product': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Processed order: {order}")
    except Exception as e:
        print(f"Error processing order: {e}")

if __name__ == "__main__":
    main()