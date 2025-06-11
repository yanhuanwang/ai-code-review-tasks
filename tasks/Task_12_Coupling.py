 #!/usr/bin/env python3
"""
Task 12: Code Coupling and Dependency Challenge

This file contains several intentional coupling and dependency issues for code review practice.
The task is to identify and fix the following issues:
1. Tight coupling in UserService
2. Direct database dependencies in OrderManager
3. Hard-coded dependencies in PaymentProcessor
4. Circular dependencies in NotificationSystem
5. Mixed concerns in DataProcessor
6. Direct file system dependencies in FileManager
7. Tight coupling in CacheManager
8. Improper dependency injection in ServiceLocator

Review the code and identify these coupling and dependency issues.
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
import boto3
from email.mime.text import MIMEText
import smtplib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    """
    Service for user management.
    Bug: Tight coupling with database, cache, and email service.
    """
    def __init__(self):
        # Bug: Direct database dependency
        self.db = sqlite3.connect('users.db')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                created_at TEXT
            )
        ''')

        # Bug: Direct cache dependency
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

        # Bug: Direct email service dependency
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')

    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        """Create a new user."""
        # Bug: Tight coupling with multiple services
        user_id = str(random.randint(1000, 9999))
        created_at = datetime.now().isoformat()

        # Direct database operation
        self.db.execute(
            'INSERT INTO users (id, name, email, created_at) VALUES (?, ?, ?, ?)',
            (user_id, name, email, created_at)
        )
        self.db.commit()

        # Direct cache operation
        self.cache.set(f"user:{user_id}", json.dumps({
            "id": user_id,
            "name": name,
            "email": email,
            "created_at": created_at
        }))

        # Direct email operation
        msg = MIMEText(f"Welcome {name}!")
        msg['Subject'] = 'Welcome to our service'
        msg['From'] = 'app@gmail.com'
        msg['To'] = email
        self.smtp_server.send_message(msg)

        return {"id": user_id, "name": name, "email": email, "created_at": created_at}

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information."""
        # Bug: Tight coupling with cache and database
        # Try cache first
        cached_user = self.cache.get(f"user:{user_id}")
        if cached_user:
            return json.loads(cached_user)

        # Fall back to database
        cursor = self.db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            user = {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "created_at": row[3]
            }
            # Update cache
            self.cache.set(f"user:{user_id}", json.dumps(user))
            return user
        return None

class OrderManager:
    """
    Manages order operations.
    Bug: Direct database and external service dependencies.
    """
    def __init__(self):
        # Bug: Direct database dependency
        self.db = sqlite3.connect('orders.db')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                total REAL,
                status TEXT,
                created_at TEXT
            )
        ''')

        # Bug: Direct external service dependency
        self.s3 = boto3.client('s3',
            aws_access_key_id='AKIAXXXXXXXXXXXXXXXX',
            aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )

    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new order."""
        # Bug: Direct database and external service operations
        order_id = str(random.randint(1000, 9999))
        total = sum(item['price'] * item['quantity'] for item in items)
        created_at = datetime.now().isoformat()

        # Direct database operation
        self.db.execute(
            'INSERT INTO orders (id, user_id, total, status, created_at) VALUES (?, ?, ?, ?, ?)',
            (order_id, user_id, total, 'pending', created_at)
        )
        self.db.commit()

        # Direct S3 operation
        self.s3.put_object(
            Bucket='orders-bucket',
            Key=f'orders/{order_id}.json',
            Body=json.dumps({
                "id": order_id,
                "user_id": user_id,
                "items": items,
                "total": total,
                "created_at": created_at
            })
        )

        return {
            "id": order_id,
            "user_id": user_id,
            "total": total,
            "status": "pending",
            "created_at": created_at
        }

class PaymentProcessor:
    """
    Processes payments.
    Bug: Hard-coded dependencies and direct external service calls.
    """
    def __init__(self):
        # Bug: Hard-coded API keys and endpoints
        self.stripe_api_key = 'sk_test_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        self.paypal_client_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        self.paypal_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

        # Bug: Direct external service dependencies
        self.stripe = requests.Session()
        self.stripe.headers.update({
            'Authorization': f'Bearer {self.stripe_api_key}',
            'Content-Type': 'application/json'
        })

        self.paypal = requests.Session()
        self.paypal.headers.update({
            'Authorization': f'Basic {self.paypal_client_id}:{self.paypal_secret}',
            'Content-Type': 'application/json'
        })

    def process_payment(self, amount: float, currency: str, method: str) -> Dict[str, Any]:
        """Process a payment."""
        # Bug: Direct external service calls
        if method == 'stripe':
            response = self.stripe.post(
                'https://api.stripe.com/v1/charges',
                json={
                    'amount': int(amount * 100),
                    'currency': currency,
                    'source': 'tok_visa'
                }
            )
            return response.json()
        elif method == 'paypal':
            response = self.paypal.post(
                'https://api.paypal.com/v1/payments/payment',
                json={
                    'intent': 'sale',
                    'amount': {
                        'total': str(amount),
                        'currency': currency
                    }
                }
            )
            return response.json()
        else:
            raise ValueError(f"Unsupported payment method: {method}")

class NotificationSystem:
    """
    Handles notifications.
    Bug: Circular dependencies and mixed concerns.
    """
    def __init__(self):
        # Bug: Circular dependency with UserService
        self.user_service = UserService()

        # Bug: Direct external service dependencies
        self.sns = boto3.client('sns',
            aws_access_key_id='AKIAXXXXXXXXXXXXXXXX',
            aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )

        self.firebase = requests.Session()
        self.firebase.headers.update({
            'Authorization': 'key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'Content-Type': 'application/json'
        })

    def send_notification(self, user_id: str, message: str, channels: List[str]) -> bool:
        """Send notification to user."""
        # Bug: Circular dependency usage
        user = self.user_service.get_user(user_id)
        if not user:
            return False

        # Bug: Mixed concerns (notification routing and sending)
        for channel in channels:
            if channel == 'email':
                msg = MIMEText(message)
                msg['Subject'] = 'Notification'
                msg['From'] = 'app@gmail.com'
                msg['To'] = user['email']
                self.user_service.smtp_server.send_message(msg)

            elif channel == 'sms':
                self.sns.publish(
                    PhoneNumber=user.get('phone', ''),
                    Message=message
                )

            elif channel == 'push':
                self.firebase.post(
                    'https://fcm.googleapis.com/fcm/send',
                    json={
                        'to': user.get('fcm_token', ''),
                        'notification': {
                            'title': 'Notification',
                            'body': message
                        }
                    }
                )

        return True

class DataProcessor:
    """
    Processes data.
    Bug: Mixed concerns and direct dependencies.
    """
    def __init__(self):
        # Bug: Direct database dependency
        self.db = sqlite3.connect('data.db')

        # Bug: Direct cache dependency
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

        # Bug: Direct file system dependency
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data."""
        # Bug: Mixed concerns (processing, storage, and caching)
        processed_data = self._transform_data(data)

        # Direct database operation
        self.db.execute(
            'INSERT INTO processed_data (id, data, created_at) VALUES (?, ?, ?)',
            (str(random.randint(1000, 9999)), json.dumps(processed_data), datetime.now().isoformat())
        )
        self.db.commit()

        # Direct cache operation
        self.cache.set(f"data:{hash(str(processed_data))}", json.dumps(processed_data))

        # Direct file system operation
        with open(self.data_dir / f"{hash(str(processed_data))}.json", 'w') as f:
            json.dump(processed_data, f)

        return processed_data

    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data."""
        # Bug: Mixed transformation logic
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

class FileManager:
    """
    Manages file operations.
    Bug: Direct file system and external service dependencies.
    """
    def __init__(self):
        # Bug: Direct file system dependency
        self.base_dir = Path('files')
        self.base_dir.mkdir(exist_ok=True)

        # Bug: Direct external service dependency
        self.s3 = boto3.client('s3',
            aws_access_key_id='AKIAXXXXXXXXXXXXXXXX',
            aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )

    def save_file(self, filename: str, content: Union[str, bytes], backup: bool = True) -> bool:
        """Save file."""
        # Bug: Mixed concerns (local storage and cloud backup)
        try:
            # Direct file system operation
            file_path = self.base_dir / filename
            with open(file_path, 'wb' if isinstance(content, bytes) else 'w') as f:
                f.write(content)

            # Direct S3 operation
            if backup:
                self.s3.upload_file(
                    str(file_path),
                    'backup-bucket',
                    f'files/{filename}'
                )

            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False

class CacheManager:
    """
    Manages caching operations.
    Bug: Tight coupling with specific cache implementation.
    """
    def __init__(self):
        # Bug: Direct Redis dependency
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

        # Bug: Direct Memcached dependency
        self.memcached = boto3.client('elasticache',
            aws_access_key_id='AKIAXXXXXXXXXXXXXXXX',
            aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        )

    def get(self, key: str, use_memcached: bool = False) -> Optional[Any]:
        """Get value from cache."""
        # Bug: Tight coupling with specific cache implementations
        try:
            if use_memcached:
                response = self.memcached.get_item(
                    TableName='cache',
                    Key={'key': {'S': key}}
                )
                return response.get('Item', {}).get('value', {}).get('S')
            else:
                value = self.redis.get(key)
                return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300, use_memcached: bool = False) -> bool:
        """Set value in cache."""
        # Bug: Tight coupling with specific cache implementations
        try:
            if use_memcached:
                self.memcached.put_item(
                    TableName='cache',
                    Item={
                        'key': {'S': key},
                        'value': {'S': json.dumps(value)},
                        'ttl': {'N': str(int(time.time() + ttl))}
                    }
                )
            else:
                self.redis.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False

class ServiceLocator:
    """
    Service locator for dependency management.
    Bug: Improper dependency injection and service management.
    """
    def __init__(self):
        # Bug: Direct service instantiation
        self.services = {
            'user': UserService(),
            'order': OrderManager(),
            'payment': PaymentProcessor(),
            'notification': NotificationSystem(),
            'data': DataProcessor(),
            'file': FileManager(),
            'cache': CacheManager()
        }

    def get_service(self, service_name: str) -> Any:
        """Get service instance."""
        # Bug: Direct service access without proper dependency management
        if service_name not in self.services:
            raise ValueError(f"Service not found: {service_name}")
        return self.services[service_name]

    def register_service(self, service_name: str, service_instance: Any) -> None:
        """Register a service instance."""
        # Bug: Direct service registration without validation
        self.services[service_name] = service_instance

def main():
    # Test UserService tight coupling
    print("Testing UserService tight coupling:")
    user_service = UserService()
    user = user_service.create_user("John Doe", "john@example.com")
    print(f"Created user: {user}")
    print(f"Retrieved user: {user_service.get_user(user['id'])}")

    # Test OrderManager direct dependencies
    print("\nTesting OrderManager direct dependencies:")
    order_manager = OrderManager()
    order = order_manager.create_order("user1", [
        {"price": 10.0, "quantity": 2},
        {"price": 20.0, "quantity": 1}
    ])
    print(f"Created order: {order}")

    # Test PaymentProcessor hard-coded dependencies
    print("\nTesting PaymentProcessor hard-coded dependencies:")
    payment_processor = PaymentProcessor()
    try:
        result = payment_processor.process_payment(100.0, "USD", "stripe")
        print(f"Payment result: {result}")
    except Exception as e:
        print(f"Payment error: {e}")

    # Test NotificationSystem circular dependencies
    print("\nTesting NotificationSystem circular dependencies:")
    notification_system = NotificationSystem()
    result = notification_system.send_notification(
        "user1",
        "Test notification",
        ["email", "sms", "push"]
    )
    print(f"Notification result: {result}")

    # Test DataProcessor mixed concerns
    print("\nTesting DataProcessor mixed concerns:")
    data_processor = DataProcessor()
    result = data_processor.process_data({
        "name": " John ",
        "age": 30,
        "scores": [85, 90, 95]
    })
    print(f"Processed data: {result}")

    # Test FileManager direct dependencies
    print("\nTesting FileManager direct dependencies:")
    file_manager = FileManager()
    result = file_manager.save_file(
        "test.txt",
        "Hello, World!",
        backup=True
    )
    print(f"File save result: {result}")

    # Test CacheManager tight coupling
    print("\nTesting CacheManager tight coupling:")
    cache_manager = CacheManager()
    cache_manager.set("test_key", {"name": "John", "age": 30})
    print(f"Cached value: {cache_manager.get('test_key')}")

    # Test ServiceLocator improper dependency injection
    print("\nTesting ServiceLocator improper dependency injection:")
    service_locator = ServiceLocator()
    user_service = service_locator.get_service('user')
    print(f"Retrieved user service: {user_service}")

if __name__ == "__main__":
    main()