#!/usr/bin/env python3
"""
Task 23: Security Vulnerabilities Challenge

This file contains several intentional security vulnerabilities for code review practice.
The task is to identify and fix the following security issues:

1. SQL Injection Vulnerabilities:
   - UserManager: Unsafe SQL queries
   - Direct string concatenation
   - Missing parameterization

2. Cross-Site Scripting (XSS):
   - ContentManager: Unsafe HTML rendering
   - Missing output encoding
   - Unsafe user input

3. Cross-Site Request Forgery (CSRF):
   - OrderManager: Missing CSRF tokens
   - Unsafe state changes
   - Missing validation

4. Insecure Deserialization:
   - DataManager: Unsafe object deserialization
   - Missing input validation
   - Direct eval usage

5. Insecure Direct Object References:
   - FileManager: Unsafe file access
   - Missing access control
   - Path traversal

6. Security Misconfiguration:
   - ConfigManager: Hardcoded credentials
   - Debug mode enabled
   - Missing security headers

7. Sensitive Data Exposure:
   - PaymentManager: Plain text passwords
   - Missing encryption
   - Logging sensitive data

8. Missing Access Control:
   - AdminManager: Missing authorization
   - Insecure direct access
   - Missing role checks

Review the code and identify these security vulnerabilities.
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
import pickle
import yaml
import base64
import marshal
import requests
import redis
import jwt
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: SQL Injection Vulnerabilities
class UserManager:
    """
    SQL Injection Vulnerabilities: Unsafe SQL queries and direct string concatenation.
    """
    def __init__(self):
        self.db = sqlite3.connect('users.db')

    def get_user(self, user_id: str) -> Dict[str, Any]:
        # Bug: SQL Injection - direct string concatenation
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        cursor = self.db.execute(query)
        user = cursor.fetchone()
        return {'user': user} if user else {'error': 'User not found'}

    def search_users(self, search_term: str) -> List[Dict[str, Any]]:
        # Bug: SQL Injection - unsafe LIKE query
        query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
        cursor = self.db.execute(query)
        return [{'user': row} for row in cursor.fetchall()]

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: SQL Injection - dynamic query construction
        set_clause = ', '.join(f"{k} = '{v}'" for k, v in data.items())
        query = f"UPDATE users SET {set_clause} WHERE id = '{user_id}'"
        self.db.execute(query)
        self.db.commit()
        return {'status': 'updated'}

# Bug: Cross-Site Scripting (XSS)
class ContentManager:
    """
    Cross-Site Scripting (XSS): Unsafe HTML rendering and missing output encoding.
    """
    def __init__(self):
        self.db = sqlite3.connect('content.db')

    def render_content(self, content_id: str) -> str:
        # Bug: XSS - direct HTML rendering
        cursor = self.db.execute(
            'SELECT content FROM pages WHERE id = ?',
            (content_id,)
        )
        content = cursor.fetchone()
        if content:
            # Bug: XSS - unsafe content rendering
            return f"""
            <html>
                <head><title>Content</title></head>
                <body>
                    <div class="content">
                        {content[0]}
                    </div>
                </body>
            </html>
            """
        return '<div>Content not found</div>'

    def save_content(self, content_id: str, content: str) -> Dict[str, Any]:
        # Bug: XSS - storing unsafe content
        self.db.execute('''
            INSERT OR REPLACE INTO pages (id, content)
            VALUES (?, ?)
        ''', (content_id, content))
        self.db.commit()
        return {'status': 'saved'}

# Bug: Cross-Site Request Forgery (CSRF)
class OrderManager:
    """
    Cross-Site Request Forgery (CSRF): Missing CSRF tokens and unsafe state changes.
    """
    def __init__(self):
        self.db = sqlite3.connect('orders.db')
        self.orders = {}

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: CSRF - missing token validation
        order_id = str(random.randint(1000, 9999))
        order = {
            'id': order_id,
            'user_id': order_data['user_id'],
            'items': order_data['items'],
            'total': sum(item['price'] * item['quantity']
                        for item in order_data['items']),
            'status': 'pending'
        }

        # Bug: CSRF - unsafe state change
        self.orders[order_id] = order
        self.db.execute('''
            INSERT INTO orders (id, user_id, items, total, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (order['id'], order['user_id'],
              json.dumps(order['items']),
              order['total'], order['status']))
        self.db.commit()

        return order

    def update_order_status(self, order_id: str,
                           status: str) -> Dict[str, Any]:
        # Bug: CSRF - missing token validation
        if order_id in self.orders:
            # Bug: CSRF - unsafe state change
            self.orders[order_id]['status'] = status
            self.db.execute('''
                UPDATE orders SET status = ? WHERE id = ?
            ''', (status, order_id))
            self.db.commit()
            return {'status': 'updated'}
        return {'error': 'Order not found'}

# Bug: Insecure Deserialization
class DataManager:
    """
    Insecure Deserialization: Unsafe object deserialization and direct eval usage.
    """
    def __init__(self):
        self.db = sqlite3.connect('data.db')

    def load_data(self, data_str: str) -> Any:
        # Bug: Insecure Deserialization - direct eval
        try:
            # Bug: Insecure Deserialization - unsafe eval
            return eval(data_str)
        except Exception as e:
            return {'error': str(e)}

    def load_pickle(self, pickle_data: bytes) -> Any:
        # Bug: Insecure Deserialization - unsafe pickle
        try:
            # Bug: Insecure Deserialization - direct pickle load
            return pickle.loads(pickle_data)
        except Exception as e:
            return {'error': str(e)}

    def load_marshal(self, marshal_data: bytes) -> Any:
        # Bug: Insecure Deserialization - unsafe marshal
        try:
            # Bug: Insecure Deserialization - direct marshal load
            return marshal.loads(marshal_data)
        except Exception as e:
            return {'error': str(e)}

# Bug: Insecure Direct Object References
class FileManager:
    """
    Insecure Direct Object References: Unsafe file access and path traversal.
    """
    def __init__(self):
        self.base_path = '/var/www/files'

    def get_file(self, filename: str) -> bytes:
        # Bug: Path Traversal - direct file access
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'rb') as f:
            return f.read()

    def save_file(self, filename: str, content: bytes) -> Dict[str, Any]:
        # Bug: Path Traversal - unsafe file path
        file_path = os.path.join(self.base_path, filename)
        with open(file_path, 'wb') as f:
            f.write(content)
        return {'status': 'saved'}

    def delete_file(self, filename: str) -> Dict[str, Any]:
        # Bug: Path Traversal - unsafe file deletion
        file_path = os.path.join(self.base_path, filename)
        os.remove(file_path)
        return {'status': 'deleted'}

# Bug: Security Misconfiguration
class ConfigManager:
    """
    Security Misconfiguration: Hardcoded credentials and debug mode.
    """
    def __init__(self):
        # Bug: Security Misconfiguration - hardcoded credentials
        self.config = {
            'database': {
                'host': 'localhost',
                'port': 5432,
                'user': 'admin',
                'password': 'admin123'
            },
            'redis': {
                'host': 'localhost',
                'port': 6379,
                'password': 'redis123'
            },
            'jwt': {
                'secret': 'your-secret-key',
                'algorithm': 'HS256'
            },
            'debug': True,  # Bug: Security Misconfiguration - debug mode
            'logging': {
                'level': 'DEBUG'  # Bug: Security Misconfiguration - debug logging
            }
        }

    def get_config(self, key: str) -> Any:
        # Bug: Security Misconfiguration - exposing sensitive config
        return self.config.get(key)

    def update_config(self, key: str, value: Any) -> Dict[str, Any]:
        # Bug: Security Misconfiguration - unsafe config update
        self.config[key] = value
        return {'status': 'updated'}

# Bug: Sensitive Data Exposure
class PaymentManager:
    """
    Sensitive Data Exposure: Plain text passwords and missing encryption.
    """
    def __init__(self):
        self.db = sqlite3.connect('payments.db')

    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Sensitive Data Exposure - logging sensitive data
        logger.info(f"Processing payment: {payment_data}")

        # Bug: Sensitive Data Exposure - storing plain text
        self.db.execute('''
            INSERT INTO payments (card_number, expiry, cvv, amount)
            VALUES (?, ?, ?, ?)
        ''', (payment_data['card_number'],
              payment_data['expiry'],
              payment_data['cvv'],
              payment_data['amount']))
        self.db.commit()

        return {'status': 'processed'}

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        # Bug: Sensitive Data Exposure - exposing sensitive data
        cursor = self.db.execute(
            'SELECT * FROM payments WHERE id = ?',
            (payment_id,)
        )
        payment = cursor.fetchone()
        if payment:
            return {
                'id': payment[0],
                'card_number': payment[1],  # Bug: Exposing card number
                'expiry': payment[2],       # Bug: Exposing expiry
                'cvv': payment[3],          # Bug: Exposing CVV
                'amount': payment[4]
            }
        return {'error': 'Payment not found'}

# Bug: Missing Access Control
class AdminManager:
    """
    Missing Access Control: Missing authorization and insecure direct access.
    """
    def __init__(self):
        self.db = sqlite3.connect('admin.db')
        self.admins = set()

    def add_admin(self, user_id: str) -> Dict[str, Any]:
        # Bug: Missing Access Control - no authorization check
        self.admins.add(user_id)
        self.db.execute('''
            INSERT INTO admins (user_id)
            VALUES (?)
        ''', (user_id,))
        self.db.commit()
        return {'status': 'added'}

    def remove_admin(self, user_id: str) -> Dict[str, Any]:
        # Bug: Missing Access Control - no authorization check
        self.admins.remove(user_id)
        self.db.execute('''
            DELETE FROM admins WHERE user_id = ?
        ''', (user_id,))
        self.db.commit()
        return {'status': 'removed'}

    def get_admin_data(self, user_id: str) -> Dict[str, Any]:
        # Bug: Missing Access Control - no role check
        cursor = self.db.execute('''
            SELECT * FROM admin_data WHERE user_id = ?
        ''', (user_id,))
        data = cursor.fetchone()
        return {'data': data} if data else {'error': 'Data not found'}

def main():
    # Test SQL Injection Vulnerabilities
    print("Testing SQL Injection Vulnerabilities:")
    user_manager = UserManager()
    try:
        # Bug: SQL Injection - malicious input
        user = user_manager.get_user("1' OR '1'='1")
        print(f"Got user: {user}")

        # Bug: SQL Injection - malicious search
        users = user_manager.search_users("' OR '1'='1")
        print(f"Found users: {users}")
    except Exception as e:
        print(f"Error in user manager: {e}")

    # Test Cross-Site Scripting (XSS)
    print("\nTesting Cross-Site Scripting (XSS):")
    content_manager = ContentManager()
    try:
        # Bug: XSS - malicious content
        content = content_manager.render_content('1')
        print(f"Rendered content: {content}")

        # Bug: XSS - storing malicious content
        content_manager.save_content('1', '<script>alert("XSS")</script>')
    except Exception as e:
        print(f"Error in content manager: {e}")

    # Test Cross-Site Request Forgery (CSRF)
    print("\nTesting Cross-Site Request Forgery (CSRF):")
    order_manager = OrderManager()
    try:
        # Bug: CSRF - missing token
        order = order_manager.create_order({
            'user_id': 'user1',
            'items': [{'price': 100, 'quantity': 1}]
        })
        print(f"Created order: {order}")
    except Exception as e:
        print(f"Error in order manager: {e}")

    # Test Insecure Deserialization
    print("\nTesting Insecure Deserialization:")
    data_manager = DataManager()
    try:
        # Bug: Insecure Deserialization - malicious eval
        result = data_manager.load_data("__import__('os').system('ls')")
        print(f"Loaded data: {result}")

        # Bug: Insecure Deserialization - malicious pickle
        malicious_pickle = pickle.dumps({'type': 'system', 'command': 'ls'})
        result = data_manager.load_pickle(malicious_pickle)
        print(f"Loaded pickle: {result}")
    except Exception as e:
        print(f"Error in data manager: {e}")

    # Test Insecure Direct Object References
    print("\nTesting Insecure Direct Object References:")
    file_manager = FileManager()
    try:
        # Bug: Path Traversal - malicious path
        content = file_manager.get_file('../../../etc/passwd')
        print(f"Got file: {content}")
    except Exception as e:
        print(f"Error in file manager: {e}")

    # Test Security Misconfiguration
    print("\nTesting Security Misconfiguration:")
    config_manager = ConfigManager()
    try:
        # Bug: Security Misconfiguration - exposing sensitive config
        config = config_manager.get_config('database')
        print(f"Got config: {config}")
    except Exception as e:
        print(f"Error in config manager: {e}")

    # Test Sensitive Data Exposure
    print("\nTesting Sensitive Data Exposure:")
    payment_manager = PaymentManager()
    try:
        # Bug: Sensitive Data Exposure - processing payment
        result = payment_manager.process_payment({
            'card_number': '4111111111111111',
            'expiry': '12/25',
            'cvv': '123',
            'amount': 100.0
        })
        print(f"Processed payment: {result}")
    except Exception as e:
        print(f"Error in payment manager: {e}")

    # Test Missing Access Control
    print("\nTesting Missing Access Control:")
    admin_manager = AdminManager()
    try:
        # Bug: Missing Access Control - adding admin
        result = admin_manager.add_admin('user1')
        print(f"Added admin: {result}")

        # Bug: Missing Access Control - accessing admin data
        data = admin_manager.get_admin_data('user1')
        print(f"Got admin data: {data}")
    except Exception as e:
        print(f"Error in admin manager: {e}")

if __name__ == "__main__":
    main()