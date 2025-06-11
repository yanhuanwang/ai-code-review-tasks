#!/usr/bin/env python3
"""
Task 19: Anti-pattern Implementation Challenge

This file contains several intentional anti-pattern implementations for code review practice.
The task is to identify and fix the following anti-patterns:

1. God Object Anti-pattern:
   - SystemManager: One class doing everything
   - Mixed responsibilities
   - No separation of concerns

2. Golden Hammer Anti-pattern:
   - DataProcessor: Using one solution for everything
   - Overuse of specific patterns
   - Inappropriate pattern application

3. Spaghetti Code Anti-pattern:
   - OrderProcessor: Unstructured, tangled code
   - Mixed control flow
   - No clear structure

4. Big Ball of Mud Anti-pattern:
   - ApplicationManager: Chaotic, unstructured code
   - No clear architecture
   - Mixed concerns

5. Cargo Cult Programming Anti-pattern:
   - CodeGenerator: Blindly following patterns
   - Unnecessary complexity
   - Copy-paste programming

6. Premature Optimization Anti-pattern:
   - PerformanceManager: Optimizing too early
   - Unnecessary complexity
   - Performance over clarity

7. Magic Numbers/Strings Anti-pattern:
   - ConfigManager: Hard-coded values
   - No constants
   - Magic values

8. Lasagna Code Anti-pattern:
   - ServiceManager: Too many layers
   - Over-abstraction
   - Unnecessary indirection

Review the code and identify these anti-pattern implementations.
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

# Bug: God Object Anti-pattern - One class doing everything
class SystemManager:
    """
    God Object anti-pattern: One class handling everything.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - database, cache, email, logging, etc.
        self.db = sqlite3.connect('system.db')
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')

        # Bug: Mixed responsibilities - configuration
        self.config = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'user': 'admin',
                'password': 'secret123'
            },
            'cache': {
                'host': 'localhost',
                'port': 6379,
                'ttl': 3600
            },
            'email': {
                'host': 'smtp.gmail.com',
                'port': 587,
                'user': 'app@gmail.com',
                'password': 'password123'
            },
            'logging': {
                'level': 'INFO',
                'file': 'app.log',
                'max_size': 10485760,
                'backup_count': 5
            }
        }

        # Bug: Mixed responsibilities - business rules
        self.validation_rules = {
            'user': {
                'name': {'min_length': 2, 'max_length': 50},
                'email': {'pattern': r'^[^@]+@[^@]+\.[^@]+$'},
                'password': {'min_length': 8, 'require_special': True}
            },
            'order': {
                'items': {'min_count': 1},
                'amount': {'min': 0, 'max': 10000}
            },
            'product': {
                'name': {'min_length': 2, 'max_length': 100},
                'price': {'min': 0, 'max': 1000000}
            }
        }

    def process_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities - validation, persistence, notification
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

        # Bug: Mixed responsibilities - database operations
        self.db.execute('''
            INSERT INTO users (id, name, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'],
              user['password'], user['created_at']))
        self.db.commit()

        # Bug: Mixed responsibilities - caching
        self.cache.set(f"user:{user_id}", json.dumps(user),
                      ex=self.config['cache']['ttl'])

        # Bug: Mixed responsibilities - email
        self._send_welcome_email(user['email'], user['name'])

        # Bug: Mixed responsibilities - logging
        logger.info(f"Created user: {user_id}")

        return user

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities - order processing
        if not self._validate_order_data(order_data):
            raise ValueError("Invalid order data")

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

        # Bug: Mixed responsibilities - database operations
        self.db.execute('''
            INSERT INTO orders (id, user_id, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order['id'], order['user_id'], json.dumps(order['items']),
              order['total'], order['status'], order['created_at']))
        self.db.commit()

        # Bug: Mixed responsibilities - caching
        self.cache.set(f"order:{order_id}", json.dumps(order),
                      ex=self.config['cache']['ttl'])

        # Bug: Mixed responsibilities - email
        self._send_order_confirmation(order)

        # Bug: Mixed responsibilities - logging
        logger.info(f"Created order: {order_id}")

        return order

    def _validate_user_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed responsibilities - validation
        rules = self.validation_rules['user']
        return ('name' in data and
                rules['name']['min_length'] <= len(data['name']) <=
                rules['name']['max_length'] and
                'email' in data and
                bool(re.match(rules['email']['pattern'], data['email'])) and
                'password' in data and
                len(data['password']) >= rules['password']['min_length'] and
                bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', data['password'])))

    def _validate_order_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed responsibilities - validation
        rules = self.validation_rules['order']
        return ('user_id' in data and
                'items' in data and
                len(data['items']) >= rules['items']['min_count'] and
                all(item['price'] >= rules['amount']['min'] and
                    item['price'] <= rules['amount']['max']
                    for item in data['items']))

    def _send_welcome_email(self, email: str, name: str) -> None:
        # Bug: Mixed responsibilities - email
        msg = MIMEText(f"Welcome {name}!")
        msg['Subject'] = 'Welcome to our service'
        msg['From'] = self.config['email']['user']
        msg['To'] = email
        self.smtp_server.send_message(msg)

    def _send_order_confirmation(self, order: Dict[str, Any]) -> None:
        # Bug: Mixed responsibilities - email
        msg = MIMEText(f"Order {order['id']} has been received.")
        msg['Subject'] = 'Order Confirmation'
        msg['From'] = self.config['email']['user']
        msg['To'] = self._get_user_email(order['user_id'])
        self.smtp_server.send_message(msg)

    def _get_user_email(self, user_id: str) -> str:
        # Bug: Mixed responsibilities - database
        cursor = self.db.execute(
            'SELECT email FROM users WHERE id = ?',
            (user_id,)
        )
        return cursor.fetchone()[0]

# Bug: Golden Hammer Anti-pattern - Using one solution for everything
class DataProcessor:
    """
    Golden Hammer anti-pattern: Using one solution (JSON) for everything.
    """
    def __init__(self):
        # Bug: Overuse of JSON for everything
        self.processors = {
            'user': self._process_user_json,
            'order': self._process_order_json,
            'product': self._process_product_json,
            'payment': self._process_payment_json,
            'inventory': self._process_inventory_json,
            'report': self._process_report_json,
            'config': self._process_config_json,
            'log': self._process_log_json
        }

    def process_data(self, data_type: str, data: Any) -> str:
        # Bug: Always converting to JSON regardless of data type
        if data_type not in self.processors:
            raise ValueError(f"Unknown data type: {data_type}")

        processor = self.processors[data_type]
        result = processor(data)

        # Bug: Always returning JSON string
        return json.dumps(result)

    def _process_user_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v).lower() for k, v in data.items()}

    def _process_order_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: float(v) if isinstance(v, (int, float)) else v
                for k, v in data.items()}

    def _process_product_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v).upper() for k, v in data.items()}

    def _process_payment_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v) for k, v in data.items()}

    def _process_inventory_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: int(v) if isinstance(v, (int, float)) else v
                for k, v in data.items()}

    def _process_report_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v) for k, v in data.items()}

    def _process_config_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v) for k, v in data.items()}

    def _process_log_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary JSON processing
        return {k: str(v) for k, v in data.items()}

# Bug: Spaghetti Code Anti-pattern - Unstructured, tangled code
class OrderProcessor:
    """
    Spaghetti Code anti-pattern: Unstructured, tangled code.
    """
    def __init__(self):
        # Bug: Global state and mixed concerns
        self.db = sqlite3.connect('orders.db')
        self.cache = {}
        self.pending_orders = []
        self.processed_orders = []
        self.failed_orders = []
        self.retry_count = 0
        self.max_retries = 3
        self.last_error = None
        self.processing = False
        self.notification_sent = False

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Spaghetti code - mixed control flow and responsibilities
        try:
            if not self._validate_order(order_data):
                self.last_error = "Invalid order data"
                self.failed_orders.append(order_data)
                return self._handle_error("Invalid order data")

            order_id = self._generate_order_id()
            if order_id in self.cache:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    self.last_error = "Max retries exceeded"
                    return self._handle_error("Max retries exceeded")
                return self.process_order(order_data)

            self.processing = True
            order = self._create_order(order_id, order_data)
            self.pending_orders.append(order)

            if not self._save_order(order):
                self.last_error = "Failed to save order"
                self.failed_orders.append(order)
                return self._handle_error("Failed to save order")

            if not self._process_payment(order):
                self.last_error = "Payment failed"
                self.failed_orders.append(order)
                return self._handle_error("Payment failed")

            if not self._update_inventory(order):
                self.last_error = "Inventory update failed"
                self.failed_orders.append(order)
                return self._handle_error("Inventory update failed")

            self.processed_orders.append(order)
            self.cache[order_id] = order

            if not self.notification_sent:
                self._send_notification(order)
                self.notification_sent = True

            self.processing = False
            return order

        except Exception as e:
            self.last_error = str(e)
            self.failed_orders.append(order_data)
            return self._handle_error(str(e))

    def _validate_order(self, data: Dict[str, Any]) -> bool:
        # Bug: Spaghetti code - mixed validation logic
        if 'user_id' not in data or 'items' not in data:
            return False
        if not data['items']:
            return False
        for item in data['items']:
            if 'price' not in item or 'quantity' not in item:
                return False
            if item['price'] < 0 or item['quantity'] < 0:
                return False
        return True

    def _generate_order_id(self) -> str:
        # Bug: Spaghetti code - mixed ID generation
        return f"ORD-{random.randint(100000, 999999)}"

    def _create_order(self, order_id: str,
                     data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Spaghetti code - mixed order creation
        return {
            'id': order_id,
            'user_id': data['user_id'],
            'items': data['items'],
            'total': sum(item['price'] * item['quantity']
                        for item in data['items']),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

    def _save_order(self, order: Dict[str, Any]) -> bool:
        # Bug: Spaghetti code - mixed persistence
        try:
            self.db.execute('''
                INSERT INTO orders (id, user_id, items, total, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order['id'], order['user_id'], json.dumps(order['items']),
                  order['total'], order['status'], order['created_at']))
            self.db.commit()
            return True
        except Exception:
            return False

    def _process_payment(self, order: Dict[str, Any]) -> bool:
        # Bug: Spaghetti code - mixed payment processing
        try:
            # Simulate payment processing
            return random.random() > 0.1
        except Exception:
            return False

    def _update_inventory(self, order: Dict[str, Any]) -> bool:
        # Bug: Spaghetti code - mixed inventory update
        try:
            # Simulate inventory update
            return random.random() > 0.1
        except Exception:
            return False

    def _send_notification(self, order: Dict[str, Any]) -> None:
        # Bug: Spaghetti code - mixed notification
        print(f"Sending notification for order {order['id']}")

    def _handle_error(self, error: str) -> Dict[str, Any]:
        # Bug: Spaghetti code - mixed error handling
        return {
            'status': 'error',
            'error': error,
            'timestamp': datetime.now().isoformat()
        }

def main():
    # Test God Object anti-pattern
    print("Testing God Object anti-pattern:")
    system_manager = SystemManager()
    try:
        user = system_manager.process_user({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'Password123!'
        })
        print(f"Created user: {user}")

        order = system_manager.process_order({
            'user_id': user['id'],
            'items': [
                {'product': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Created order: {order}")
    except Exception as e:
        print(f"Error in system manager: {e}")

    # Test Golden Hammer anti-pattern
    print("\nTesting Golden Hammer anti-pattern:")
    data_processor = DataProcessor()
    try:
        result = data_processor.process_data('user', {
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        print(f"Processed data: {result}")
    except Exception as e:
        print(f"Error in data processor: {e}")

    # Test Spaghetti Code anti-pattern
    print("\nTesting Spaghetti Code anti-pattern:")
    order_processor = OrderProcessor()
    try:
        result = order_processor.process_order({
            'user_id': 'user1',
            'items': [
                {'product': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Processed order: {result}")
    except Exception as e:
        print(f"Error in order processor: {e}")

if __name__ == "__main__":
    main()