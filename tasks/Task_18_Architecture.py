#!/usr/bin/env python3
"""
Task 18: Architectural Pattern Issues Challenge

This file contains several intentional architectural pattern issues for code review practice.
The task is to identify and fix the following issues:

1. MVC Pattern Issues:
   - UserController: Mixed model and view logic
   - OrderView: Direct database access
   - ProductModel: Contains business logic

2. Repository Pattern Issues:
   - UserRepository: Mixed persistence and business logic
   - OrderRepository: Direct SQL queries
   - ProductRepository: No abstraction

3. Service Layer Issues:
   - UserService: Mixed service and data access
   - OrderService: Direct model manipulation
   - PaymentService: Mixed concerns

4. Data Access Layer Issues:
   - DatabaseManager: Mixed connection and query logic
   - QueryBuilder: Hard-coded queries
   - TransactionManager: Mixed transaction and business logic

5. Presentation Layer Issues:
   - ViewManager: Mixed presentation and business logic
   - TemplateEngine: Direct data access
   - FormHandler: Mixed validation and presentation

6. Domain Layer Issues:
   - UserDomain: Mixed domain and persistence
   - OrderDomain: Direct service calls
   - ProductDomain: Mixed business rules

7. Application Layer Issues:
   - ApplicationController: Mixed routing and business logic
   - RequestHandler: Direct model access
   - ResponseBuilder: Mixed formatting and business logic

8. Infrastructure Layer Issues:
   - ConfigManager: Mixed configuration and business logic
   - LogManager: Direct database access
   - CacheManager: Mixed caching and business logic

Review the code and identify these architectural pattern issues.
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

# Bug: MVC Pattern Issues - Mixed model and view logic
class UserController:
    """
    Controller violating MVC pattern by mixing model and view logic.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - database, business logic, and view
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

    def create_user(self, user_data: Dict[str, Any]) -> str:
        # Bug: Mixed responsibilities - model, view, and business logic
        if not self._validate_user_data(user_data):
            return self._render_error("Invalid user data")

        user_id = str(random.randint(1000, 9999))
        user = {
            'id': user_id,
            'name': user_data['name'],
            'email': user_data['email'],
            'password': hashlib.sha256(user_data['password'].encode()).hexdigest(),
            'created_at': datetime.now().isoformat()
        }

        # Bug: Direct model manipulation in controller
        self.db.execute('''
            INSERT INTO users (id, name, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'],
              user['password'], user['created_at']))
        self.db.commit()

        # Bug: Mixed view logic in controller
        return self._render_success(user)

    def _validate_user_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Business logic in controller
        return ('name' in data and 'email' in data and
                '@' in data['email'] and
                len(data.get('password', '')) >= 8)

    def _render_success(self, data: Dict[str, Any]) -> str:
        # Bug: View logic in controller
        return f"""
        <div class="success">
            <h2>User Created Successfully</h2>
            <p>ID: {data['id']}</p>
            <p>Name: {data['name']}</p>
            <p>Email: {data['email']}</p>
        </div>
        """

    def _render_error(self, message: str) -> str:
        # Bug: View logic in controller
        return f"""
        <div class="error">
            <h2>Error</h2>
            <p>{message}</p>
        </div>
        """

# Bug: Repository Pattern Issues - Mixed persistence and business logic
class UserRepository:
    """
    Repository violating repository pattern by mixing persistence and business logic.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - database and business logic
        self.db = sqlite3.connect('users.db')
        self.validation_rules = {
            'name': {'min_length': 2, 'max_length': 50},
            'email': {'pattern': r'^[^@]+@[^@]+\.[^@]+$'},
            'password': {'min_length': 8, 'require_special': True}
        }

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities - validation, persistence, and business logic
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

        # Bug: Direct SQL in repository
        self.db.execute('''
            INSERT INTO users (id, name, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user['id'], user['name'], user['email'],
              user['password'], user['created_at']))
        self.db.commit()

        # Bug: Business logic in repository
        self._send_welcome_email(user['email'], user['name'])

        return user

    def _validate_user_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Business logic in repository
        if 'name' not in data or 'email' not in data or 'password' not in data:
            return False

        if not (self.validation_rules['name']['min_length'] <=
                len(data['name']) <=
                self.validation_rules['name']['max_length']):
            return False

        if not re.match(self.validation_rules['email']['pattern'],
                       data['email']):
            return False

        return True

    def _send_welcome_email(self, email: str, name: str) -> None:
        # Bug: Business logic in repository
        msg = MIMEText(f"Welcome {name}!")
        msg['Subject'] = 'Welcome to our service'
        msg['From'] = 'app@gmail.com'
        msg['To'] = email
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('app@gmail.com', 'password123')
        smtp.send_message(msg)
        smtp.quit()

# Bug: Service Layer Issues - Mixed service and data access
class OrderService:
    """
    Service violating service layer pattern by mixing service and data access.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - database, business logic, and external services
        self.db = sqlite3.connect('orders.db')
        self.payment_processor = PaymentProcessor()
        self.inventory_manager = InventoryManager()
        self.notification_service = NotificationService()

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities - validation, persistence, and business logic
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

        # Bug: Direct data access in service
        self.db.execute('''
            INSERT INTO orders (id, user_id, items, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order['id'], order['user_id'], json.dumps(order['items']),
              order['total'], order['status'], order['created_at']))
        self.db.commit()

        # Bug: Mixed business logic in service
        payment_result = self.payment_processor.process_payment(
            order['total'],
            'USD',
            'credit_card'
        )

        self.inventory_manager.update_inventory(order['items'])

        self.notification_service.send_notification(
            order['user_id'],
            'order_confirmation',
            {'order_id': order['id'], 'total': order['total']}
        )

        return order

    def _validate_order_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Business logic in service
        return ('user_id' in data and 'items' in data and
                len(data['items']) > 0)

class PaymentProcessor:
    """Payment processor for OrderService."""
    def process_payment(self, amount: float, currency: str,
                       method: str) -> Dict[str, Any]:
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': method,
            'transaction_id': f"TXN-{random.randint(100000, 999999)}"
        }

class InventoryManager:
    """Inventory manager for OrderService."""
    def update_inventory(self, items: List[Dict[str, Any]]) -> None:
        print(f"Updating inventory for items: {items}")

class NotificationService:
    """Notification service for OrderService."""
    def send_notification(self, user_id: str, template: str,
                         data: Dict[str, Any]) -> None:
        print(f"Sending {template} notification to {user_id}: {data}")

# Bug: Data Access Layer Issues - Mixed connection and query logic
class DatabaseManager:
    """
    Database manager violating data access layer pattern.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - connection and query management
        self.connections = {}
        self.query_cache = {}
        self.transaction_stack = []

    def connect(self, database: str) -> sqlite3.Connection:
        # Bug: Mixed responsibilities - connection and caching
        if database not in self.connections:
            self.connections[database] = sqlite3.connect(database)
        return self.connections[database]

    def execute_query(self, database: str, query: str,
                     params: tuple = ()) -> Any:
        # Bug: Mixed responsibilities - query execution and caching
        cache_key = f"{database}:{query}:{str(params)}"
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]

        conn = self.connect(database)
        cursor = conn.execute(query, params)
        result = cursor.fetchall()

        self.query_cache[cache_key] = result
        return result

    def begin_transaction(self, database: str) -> None:
        # Bug: Mixed responsibilities - transaction and connection management
        conn = self.connect(database)
        conn.execute('BEGIN TRANSACTION')
        self.transaction_stack.append(database)

    def commit_transaction(self) -> None:
        # Bug: Mixed responsibilities - transaction and connection management
        if not self.transaction_stack:
            raise RuntimeError("No active transaction")

        database = self.transaction_stack.pop()
        conn = self.connect(database)
        conn.commit()

    def rollback_transaction(self) -> None:
        # Bug: Mixed responsibilities - transaction and connection management
        if not self.transaction_stack:
            raise RuntimeError("No active transaction")

        database = self.transaction_stack.pop()
        conn = self.connect(database)
        conn.rollback()

# Bug: Presentation Layer Issues - Mixed presentation and business logic
class ViewManager:
    """
    View manager violating presentation layer pattern.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - template engine and business logic
        self.templates = {
            'user': self._render_user_template,
            'order': self._render_order_template,
            'product': self._render_product_template
        }
        self.db = sqlite3.connect('views.db')

    def render_view(self, view_type: str, data: Dict[str, Any]) -> str:
        # Bug: Mixed responsibilities - rendering and business logic
        if view_type not in self.templates:
            raise ValueError(f"Unknown view type: {view_type}")

        # Bug: Direct data access in presentation layer
        if view_type == 'user':
            user_data = self.db.execute(
                'SELECT * FROM users WHERE id = ?',
                (data['user_id'],)
            ).fetchone()
            data.update(dict(user_data))

        template = self.templates[view_type]
        return template(data)

    def _render_user_template(self, data: Dict[str, Any]) -> str:
        # Bug: Mixed responsibilities - template and business logic
        return f"""
        <div class="user-profile">
            <h2>{data['name']}</h2>
            <p>Email: {data['email']}</p>
            <p>Member since: {data['created_at']}</p>
            <div class="user-stats">
                <p>Total orders: {self._get_user_order_count(data['id'])}</p>
                <p>Total spent: ${self._get_user_total_spent(data['id'])}</p>
            </div>
        </div>
        """

    def _get_user_order_count(self, user_id: str) -> int:
        # Bug: Business logic in presentation layer
        return self.db.execute(
            'SELECT COUNT(*) FROM orders WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0]

    def _get_user_total_spent(self, user_id: str) -> float:
        # Bug: Business logic in presentation layer
        return self.db.execute(
            'SELECT SUM(total) FROM orders WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0] or 0.0

def main():
    # Test MVC pattern issues
    print("Testing MVC pattern issues:")
    user_controller = UserController()
    try:
        result = user_controller.create_user({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'Password123!'
        })
        print(f"Controller result: {result}")
    except Exception as e:
        print(f"Error in controller: {e}")

    # Test Repository pattern issues
    print("\nTesting Repository pattern issues:")
    user_repository = UserRepository()
    try:
        user = user_repository.create({
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'password': 'Password123!'
        })
        print(f"Repository result: {user}")
    except Exception as e:
        print(f"Error in repository: {e}")

    # Test Service layer issues
    print("\nTesting Service layer issues:")
    order_service = OrderService()
    try:
        order = order_service.create_order({
            'user_id': 'user1',
            'items': [
                {'product': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Service result: {order}")
    except Exception as e:
        print(f"Error in service: {e}")

    # Test Data Access layer issues
    print("\nTesting Data Access layer issues:")
    db_manager = DatabaseManager()
    try:
        db_manager.begin_transaction('test.db')
        result = db_manager.execute_query(
            'test.db',
            'SELECT * FROM users WHERE id = ?',
            ('user1',)
        )
        db_manager.commit_transaction()
        print(f"Database result: {result}")
    except Exception as e:
        print(f"Error in database manager: {e}")

    # Test Presentation layer issues
    print("\nTesting Presentation layer issues:")
    view_manager = ViewManager()
    try:
        view = view_manager.render_view('user', {'user_id': 'user1'})
        print(f"View result: {view}")
    except Exception as e:
        print(f"Error in view manager: {e}")

if __name__ == "__main__":
    main()