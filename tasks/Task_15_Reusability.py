#!/usr/bin/env python3
"""
Task 15: Code Reusability and Modularity Challenge

This file contains several intentional reusability and modularity issues for code review practice.
The task is to identify and fix the following issues:
1. Code duplication in ValidationSystem
2. Poor abstraction in DataProcessor
3. Lack of modularity in ReportGenerator
4. Tight coupling in OrderSystem
5. Poor component reuse in UserSystem
6. Inconsistent interfaces in PaymentSystem
7. Lack of abstraction in FileHandler
8. Poor modularity in NotificationSystem

Review the code and identify these reusability and modularity issues.
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
import sqlite3
import os
import requests
import redis
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: Code duplication - repeated validation logic
class ValidationSystem:
    """
    System for data validation.
    """
    def __init__(self):
        # Bug: Duplicated validation rules
        self.user_validation_rules = {
            'name': {'min_length': 2, 'max_length': 50},
            'email': {'pattern': r'^[^@]+@[^@]+\.[^@]+$'},
            'password': {'min_length': 8, 'require_special': True}
        }

        # Bug: Duplicated validation rules
        self.order_validation_rules = {
            'order_id': {'pattern': r'^ORD-\d{6}$'},
            'amount': {'min': 0, 'max': 10000},
            'currency': {'allowed': ['USD', 'EUR', 'GBP']}
        }

        # Bug: Duplicated validation rules
        self.product_validation_rules = {
            'name': {'min_length': 2, 'max_length': 100},
            'price': {'min': 0, 'max': 1000000},
            'sku': {'pattern': r'^SKU-\d{8}$'}
        }

    def validate_user(self, data: Dict[str, Any]) -> bool:
        """Validate user data."""
        # Bug: Duplicated validation logic
        if 'name' in data:
            if not (self.user_validation_rules['name']['min_length'] <=
                   len(data['name']) <=
                   self.user_validation_rules['name']['max_length']):
                return False

        if 'email' in data:
            if not re.match(self.user_validation_rules['email']['pattern'],
                          data['email']):
                return False

        if 'password' in data:
            if not (len(data['password']) >=
                   self.user_validation_rules['password']['min_length'] and
                   bool(re.search(r'[!@#$%^&*(),.?":{}|<>]',
                                data['password']))):
                return False

        return True

    def validate_order(self, data: Dict[str, Any]) -> bool:
        """Validate order data."""
        # Bug: Duplicated validation logic
        if 'order_id' in data:
            if not re.match(self.order_validation_rules['order_id']['pattern'],
                          data['order_id']):
                return False

        if 'amount' in data:
            if not (self.order_validation_rules['amount']['min'] <=
                   data['amount'] <=
                   self.order_validation_rules['amount']['max']):
                return False

        if 'currency' in data:
            if data['currency'] not in self.order_validation_rules['currency']['allowed']:
                return False

        return True

    def validate_product(self, data: Dict[str, Any]) -> bool:
        """Validate product data."""
        # Bug: Duplicated validation logic
        if 'name' in data:
            if not (self.product_validation_rules['name']['min_length'] <=
                   len(data['name']) <=
                   self.product_validation_rules['name']['max_length']):
                return False

        if 'price' in data:
            if not (self.product_validation_rules['price']['min'] <=
                   data['price'] <=
                   self.product_validation_rules['price']['max']):
                return False

        if 'sku' in data:
            if not re.match(self.product_validation_rules['sku']['pattern'],
                          data['sku']):
                return False

        return True

# Bug: Poor abstraction - mixed data processing concerns
class DataProcessor:
    """
    System for processing data.
    """
    def __init__(self):
        # Bug: Poor abstraction - mixed processing types
        self.processors = {
            'user': self._process_user,
            'order': self._process_order,
            'product': self._process_product,
            'payment': self._process_payment,
            'inventory': self._process_inventory
        }

    def process_data(self, data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data of specified type."""
        # Bug: Poor abstraction - mixed processing logic
        if data_type not in self.processors:
            raise ValueError(f"Unknown data type: {data_type}")

        processor = self.processors[data_type]
        result = processor(data)

        # Bug: Poor abstraction - mixed post-processing
        if data_type == 'user':
            result['processed_at'] = datetime.now().isoformat()
        elif data_type == 'order':
            result['status'] = 'processed'
        elif data_type == 'product':
            result['last_updated'] = datetime.now().isoformat()

        return result

    def _process_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user data."""
        # Bug: Poor abstraction - mixed processing steps
        result = data.copy()
        if 'email' in result:
            result['email'] = result['email'].lower()
        if 'name' in result:
            result['name'] = result['name'].title()
        return result

    def _process_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process order data."""
        # Bug: Poor abstraction - mixed processing steps
        result = data.copy()
        if 'amount' in result:
            result['amount'] = float(result['amount'])
        if 'items' in result:
            result['total_items'] = len(result['items'])
        return result

    def _process_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process product data."""
        # Bug: Poor abstraction - mixed processing steps
        result = data.copy()
        if 'price' in result:
            result['price'] = float(result['price'])
        if 'name' in result:
            result['name'] = result['name'].strip()
        return result

    def _process_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment data."""
        # Bug: Poor abstraction - mixed processing steps
        result = data.copy()
        if 'amount' in result:
            result['amount'] = float(result['amount'])
        if 'currency' in result:
            result['currency'] = result['currency'].upper()
        return result

    def _process_inventory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process inventory data."""
        # Bug: Poor abstraction - mixed processing steps
        result = data.copy()
        if 'quantity' in result:
            result['quantity'] = int(result['quantity'])
        if 'location' in result:
            result['location'] = result['location'].upper()
        return result

# Bug: Lack of modularity - mixed report generation concerns
class ReportGenerator:
    """
    System for generating reports.
    """
    def __init__(self):
        # Bug: Lack of modularity - mixed report types
        self.report_types = {
            'sales': self._generate_sales_report,
            'inventory': self._generate_inventory_report,
            'user': self._generate_user_report,
            'order': self._generate_order_report
        }

    def generate_report(self, report_type: str, data: Dict[str, Any]) -> str:
        """Generate report of specified type."""
        # Bug: Lack of modularity - mixed report generation
        if report_type not in self.report_types:
            raise ValueError(f"Unknown report type: {report_type}")

        generator = self.report_types[report_type]
        report = generator(data)

        # Bug: Lack of modularity - mixed formatting
        if report_type == 'sales':
            return self._format_sales_report(report)
        elif report_type == 'inventory':
            return self._format_inventory_report(report)
        elif report_type == 'user':
            return self._format_user_report(report)
        elif report_type == 'order':
            return self._format_order_report(report)

    def _generate_sales_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sales report."""
        # Bug: Lack of modularity - mixed calculations
        report = {
            'total_sales': sum(item['amount'] for item in data['sales']),
            'total_orders': len(data['sales']),
            'average_order': sum(item['amount'] for item in data['sales']) / len(data['sales']),
            'sales_by_product': {}
        }

        for sale in data['sales']:
            product = sale['product']
            if product not in report['sales_by_product']:
                report['sales_by_product'][product] = 0
            report['sales_by_product'][product] += sale['amount']

        return report

    def _generate_inventory_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate inventory report."""
        # Bug: Lack of modularity - mixed calculations
        report = {
            'total_items': sum(item['quantity'] for item in data['inventory']),
            'total_value': sum(item['quantity'] * item['price']
                             for item in data['inventory']),
            'low_stock': [item for item in data['inventory']
                         if item['quantity'] < item['min_stock']],
            'out_of_stock': [item for item in data['inventory']
                            if item['quantity'] == 0]
        }
        return report

    def _format_sales_report(self, report: Dict[str, Any]) -> str:
        """Format sales report."""
        # Bug: Lack of modularity - mixed formatting
        return f"""
Sales Report
-----------
Total Sales: ${report['total_sales']:.2f}
Total Orders: {report['total_orders']}
Average Order: ${report['average_order']:.2f}

Sales by Product:
{chr(10).join(f"{product}: ${amount:.2f}"
             for product, amount in report['sales_by_product'].items())}
"""

    def _format_inventory_report(self, report: Dict[str, Any]) -> str:
        """Format inventory report."""
        # Bug: Lack of modularity - mixed formatting
        return f"""
Inventory Report
--------------
Total Items: {report['total_items']}
Total Value: ${report['total_value']:.2f}

Low Stock Items:
{chr(10).join(f"{item['name']}: {item['quantity']} (min: {item['min_stock']})"
             for item in report['low_stock'])}

Out of Stock Items:
{chr(10).join(item['name'] for item in report['out_of_stock'])}
"""

# Bug: Tight coupling - mixed order processing concerns
class OrderSystem:
    """
    System for processing orders.
    """
    def __init__(self):
        # Bug: Tight coupling - mixed dependencies
        self.db = sqlite3.connect('orders.db')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                items TEXT,
                total REAL,
                status TEXT,
                created_at TEXT
            )
        ''')

        self.payment_system = PaymentSystem()
        self.inventory_system = InventorySystem()
        self.notification_system = NotificationSystem()

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an order."""
        # Bug: Tight coupling - mixed processing steps
        # Validate order
        if not self._validate_order(order_data):
            raise ValueError("Invalid order data")

        # Create order record
        order_id = f"ORD-{random.randint(100000, 999999)}"
        order = {
            'id': order_id,
            'user_id': order_data['user_id'],
            'items': json.dumps(order_data['items']),
            'total': sum(item['price'] * item['quantity']
                        for item in order_data['items']),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        # Save to database
        self.db.execute('''
            INSERT INTO orders (id, user_id, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order['id'], order['user_id'], order['items'],
              order['total'], order['status'], order['created_at']))
        self.db.commit()

        # Process payment
        payment_result = self.payment_system.process_payment(
            order['total'],
            'USD',
            'credit_card'
        )

        # Update inventory
        self.inventory_system.update_inventory(order_data['items'])

        # Send notification
        self.notification_system.send_notification(
            order['user_id'],
            'order_confirmation',
            {'order_id': order['id'], 'total': order['total']},
            ['email']
        )

        return order

    def _validate_order(self, order_data: Dict[str, Any]) -> bool:
        """Validate order data."""
        # Bug: Tight coupling - mixed validation
        if 'user_id' not in order_data:
            return False
        if 'items' not in order_data or not order_data['items']:
            return False
        return True

# Bug: Poor component reuse - mixed user management concerns
class UserSystem:
    """
    System for managing users.
    """
    def __init__(self):
        # Bug: Poor component reuse - mixed user management
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

        self.validation_system = ValidationSystem()
        self.notification_system = NotificationSystem()

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        # Bug: Poor component reuse - mixed user creation
        if not self.validation_system.validate_user(user_data):
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

        self.notification_system.send_notification(
            user['id'],
            'welcome',
            {'name': user['name']},
            ['email']
        )

        return user

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data."""
        # Bug: Poor component reuse - mixed user update
        if not self.validation_system.validate_user(user_data):
            raise ValueError("Invalid user data")

        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        updated_user = {**user, **user_data}
        if 'password' in user_data:
            updated_user['password'] = hashlib.sha256(
                user_data['password'].encode()
            ).hexdigest()

        self.db.execute('''
            UPDATE users
            SET name = ?, email = ?, password = ?
            WHERE id = ?
        ''', (updated_user['name'], updated_user['email'],
              updated_user['password'], user_id))
        self.db.commit()

        return updated_user

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        # Bug: Poor component reuse - mixed user retrieval
        cursor = self.db.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None

        return {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'password': row[3],
            'created_at': row[4]
        }

# Bug: Inconsistent interfaces - mixed payment processing concerns
class PaymentSystem:
    """
    System for processing payments.
    """
    def __init__(self):
        # Bug: Inconsistent interfaces - mixed payment types
        self.payment_methods = {
            'credit_card': self._process_credit_card,
            'paypal': self._process_paypal,
            'bank_transfer': self._process_bank_transfer
        }

    def process_payment(self, amount: float, currency: str,
                       payment_method: str) -> Dict[str, Any]:
        """Process a payment."""
        # Bug: Inconsistent interfaces - mixed payment processing
        if payment_method not in self.payment_methods:
            raise ValueError(f"Unknown payment method: {payment_method}")

        processor = self.payment_methods[payment_method]
        result = processor(amount, currency)

        # Bug: Inconsistent interfaces - mixed result handling
        if payment_method == 'credit_card':
            result['transaction_id'] = f"CC-{random.randint(100000, 999999)}"
        elif payment_method == 'paypal':
            result['transaction_id'] = f"PP-{random.randint(100000, 999999)}"
        elif payment_method == 'bank_transfer':
            result['transaction_id'] = f"BT-{random.randint(100000, 999999)}"

        return result

    def _process_credit_card(self, amount: float, currency: str) -> Dict[str, Any]:
        """Process credit card payment."""
        # Bug: Inconsistent interfaces - mixed processing
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'credit_card',
            'timestamp': datetime.now().isoformat()
        }

    def _process_paypal(self, amount: float, currency: str) -> Dict[str, Any]:
        """Process PayPal payment."""
        # Bug: Inconsistent interfaces - mixed processing
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'paypal',
            'timestamp': datetime.now().isoformat()
        }

    def _process_bank_transfer(self, amount: float, currency: str) -> Dict[str, Any]:
        """Process bank transfer payment."""
        # Bug: Inconsistent interfaces - mixed processing
        return {
            'status': 'pending',
            'amount': amount,
            'currency': currency,
            'method': 'bank_transfer',
            'timestamp': datetime.now().isoformat()
        }

# Bug: Lack of abstraction - mixed file handling concerns
class FileHandler:
    """
    System for handling files.
    """
    def __init__(self):
        # Bug: Lack of abstraction - mixed file types
        self.base_dir = Path('files')
        self.base_dir.mkdir(exist_ok=True)

    def save_file(self, filename: str, content: Union[str, bytes],
                 file_type: str) -> bool:
        """Save file."""
        # Bug: Lack of abstraction - mixed file handling
        file_path = self.base_dir / filename

        if file_type == 'text':
            return self._save_text_file(file_path, content)
        elif file_type == 'binary':
            return self._save_binary_file(file_path, content)
        elif file_type == 'json':
            return self._save_json_file(file_path, content)
        else:
            raise ValueError(f"Unknown file type: {file_type}")

    def _save_text_file(self, file_path: Path, content: str) -> bool:
        """Save text file."""
        # Bug: Lack of abstraction - mixed file operations
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error saving text file: {e}")
            return False

    def _save_binary_file(self, file_path: Path, content: bytes) -> bool:
        """Save binary file."""
        # Bug: Lack of abstraction - mixed file operations
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error saving binary file: {e}")
            return False

    def _save_json_file(self, file_path: Path, content: Dict[str, Any]) -> bool:
        """Save JSON file."""
        # Bug: Lack of abstraction - mixed file operations
        try:
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")
            return False

# Bug: Poor modularity - mixed notification concerns
class NotificationSystem:
    """
    System for handling notifications.
    """
    def __init__(self):
        # Bug: Poor modularity - mixed notification types
        self.notification_types = {
            'email': self._send_email,
            'sms': self._send_sms,
            'push': self._send_push
        }

        self.templates = {
            'welcome': 'Welcome {name}!',
            'order_confirmation': 'Order {order_id} has been confirmed. Total: ${total}',
            'payment_received': 'Payment of ${amount} {currency} has been received',
            'shipping_update': 'Order {order_id} has been {status}'
        }

    def send_notification(self, user_id: str, template: str,
                         data: Dict[str, Any], channels: List[str]) -> bool:
        """Send notification."""
        # Bug: Poor modularity - mixed notification handling
        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}")

        message = self.templates[template].format(**data)

        for channel in channels:
            if channel not in self.notification_types:
                raise ValueError(f"Unknown channel: {channel}")

            sender = self.notification_types[channel]
            if not sender(user_id, message):
                logger.error(f"Failed to send {channel} notification to {user_id}")
                return False

        return True

    def _send_email(self, user_id: str, message: str) -> bool:
        """Send email notification."""
        # Bug: Poor modularity - mixed email handling
        try:
            # Simulate email sending
            logger.info(f"Sending email to {user_id}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def _send_sms(self, user_id: str, message: str) -> bool:
        """Send SMS notification."""
        # Bug: Poor modularity - mixed SMS handling
        try:
            # Simulate SMS sending
            logger.info(f"Sending SMS to {user_id}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False

    def _send_push(self, user_id: str, message: str) -> bool:
        """Send push notification."""
        # Bug: Poor modularity - mixed push notification handling
        try:
            # Simulate push notification
            logger.info(f"Sending push notification to {user_id}: {message}")
            return True
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")
            return False

def main():
    # Test ValidationSystem code duplication
    print("Testing ValidationSystem code duplication:")
    validation_system = ValidationSystem()
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'Password123!'
    }
    print(f"User validation: {validation_system.validate_user(user_data)}")

    # Test DataProcessor poor abstraction
    print("\nTesting DataProcessor poor abstraction:")
    data_processor = DataProcessor()
    result = data_processor.process_data('user', {
        'name': 'John Doe',
        'email': 'john@example.com'
    })
    print(f"Processed data: {result}")

    # Test ReportGenerator lack of modularity
    print("\nTesting ReportGenerator lack of modularity:")
    report_generator = ReportGenerator()
    report = report_generator.generate_report('sales', {
        'sales': [
            {'product': 'A', 'amount': 100},
            {'product': 'B', 'amount': 200}
        ]
    })
    print(f"Generated report: {report}")

    # Test OrderSystem tight coupling
    print("\nTesting OrderSystem tight coupling:")
    order_system = OrderSystem()
    try:
        order = order_system.process_order({
            'user_id': 'user1',
            'items': [
                {'product': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Processed order: {order}")
    except Exception as e:
        print(f"Error processing order: {e}")

    # Test UserSystem poor component reuse
    print("\nTesting UserSystem poor component reuse:")
    user_system = UserSystem()
    try:
        user = user_system.create_user({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'Password123!'
        })
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Test PaymentSystem inconsistent interfaces
    print("\nTesting PaymentSystem inconsistent interfaces:")
    payment_system = PaymentSystem()
    result = payment_system.process_payment(100.0, "USD", "credit_card")
    print(f"Payment result: {result}")

    # Test FileHandler lack of abstraction
    print("\nTesting FileHandler lack of abstraction:")
    file_handler = FileHandler()
    result = file_handler.save_file("test.txt", "Hello, World!", "text")
    print(f"File save result: {result}")

    # Test NotificationSystem poor modularity
    print("\nTesting NotificationSystem poor modularity:")
    notification_system = NotificationSystem()
    result = notification_system.send_notification(
        "user1",
        "welcome",
        {"name": "John"},
        ["email", "sms"]
    )
    print(f"Notification result: {result}")

if __name__ == "__main__":
    main()