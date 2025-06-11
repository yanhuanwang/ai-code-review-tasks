#!/usr/bin/env python3
"""
Task 14: Code Organization and Structure Challenge

This file contains several intentional organization and structure issues for code review practice.
The task is to identify and fix the following issues:
1. Mixed concerns in UserSystem
2. Improper class hierarchy in AnimalSystem
3. Unclear module boundaries in DataSystem
4. Poor separation of concerns in PaymentSystem
5. Inconsistent abstraction levels in FileSystem
6. Mixed responsibilities in NotificationSystem
7. Unclear component relationships in CacheSystem
8. Poor module organization in ServiceSystem

Review the code and identify these organization and structure issues.
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

# Bug: Mixed concerns - database, validation, and business logic in one class
class UserSystem:
    """
    System for managing users, including database operations, validation,
    and business logic.
    """
    def __init__(self):
        # Bug: Mixed concerns - database initialization
        self.db = sqlite3.connect('users.db')
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                created_at TEXT
            )
        ''')

        # Bug: Mixed concerns - email configuration
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')

        # Bug: Mixed concerns - validation rules
        self.validation_rules = {
            'name': {'min_length': 2, 'max_length': 50},
            'email': {'pattern': r'^[^@]+@[^@]+\.[^@]+$'},
            'password': {'min_length': 8, 'require_special': True}
        }

    def create_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user."""
        # Bug: Mixed concerns - validation, database, and email
        if not self._validate_name(name):
            raise ValueError("Invalid name")
        if not self._validate_email(email):
            raise ValueError("Invalid email")
        if not self._validate_password(password):
            raise ValueError("Invalid password")

        user_id = str(random.randint(1000, 9999))
        created_at = datetime.now().isoformat()

        self.db.execute(
            'INSERT INTO users (id, name, email, created_at) VALUES (?, ?, ?, ?)',
            (user_id, name, email, created_at)
        )
        self.db.commit()

        self._send_welcome_email(email, name)

        return {"id": user_id, "name": name, "email": email, "created_at": created_at}

    def _validate_name(self, name: str) -> bool:
        """Validate user name."""
        rules = self.validation_rules['name']
        return (len(name) >= rules['min_length'] and
                len(name) <= rules['max_length'])

    def _validate_email(self, email: str) -> bool:
        """Validate email address."""
        return bool(re.match(self.validation_rules['email']['pattern'], email))

    def _validate_password(self, password: str) -> bool:
        """Validate password."""
        rules = self.validation_rules['password']
        return (len(password) >= rules['min_length'] and
                bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)))

    def _send_welcome_email(self, email: str, name: str) -> None:
        """Send welcome email."""
        msg = MIMEText(f"Welcome {name}!")
        msg['Subject'] = 'Welcome to our service'
        msg['From'] = 'app@gmail.com'
        msg['To'] = email
        self.smtp_server.send_message(msg)

# Bug: Improper class hierarchy - mixed inheritance and composition
class Animal:
    """Base class for animals."""
    def __init__(self, name: str):
        self.name = name

    def make_sound(self) -> str:
        """Make animal sound."""
        return "Some sound"

class Dog(Animal):
    """Dog class."""
    def __init__(self, name: str, breed: str):
        # Bug: Improper inheritance - calling parent after own initialization
        self.breed = breed
        super().__init__(name)

    def make_sound(self) -> str:
        """Make dog sound."""
        return "Woof!"

class Cat(Animal):
    """Cat class."""
    def __init__(self, name: str, color: str):
        # Bug: Improper inheritance - duplicate parent initialization
        super().__init__(name)
        self.color = color
        super().__init__(name)  # Duplicate initialization

    def make_sound(self) -> str:
        """Make cat sound."""
        return "Meow!"

class PetShop:
    """Pet shop class."""
    def __init__(self):
        # Bug: Improper composition - direct animal creation
        self.animals = [
            Dog("Rex", "German Shepherd"),
            Cat("Whiskers", "Orange")
        ]

    def add_animal(self, animal: Animal) -> None:
        """Add animal to shop."""
        # Bug: Improper type checking
        if isinstance(animal, (Dog, Cat)):
            self.animals.append(animal)

# Bug: Unclear module boundaries - mixed data handling and business logic
class DataSystem:
    """
    System for handling data operations.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - data storage and processing
        self.data = {}
        self.processors = {
            'user': self._process_user_data,
            'order': self._process_order_data,
            'product': self._process_product_data
        }
        self.validators = {
            'user': self._validate_user_data,
            'order': self._validate_order_data,
            'product': self._validate_product_data
        }

    def process_data(self, data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data of specified type."""
        # Bug: Mixed concerns - validation, processing, and storage
        if data_type not in self.processors:
            raise ValueError(f"Unknown data type: {data_type}")

        if not self.validators[data_type](data):
            raise ValueError(f"Invalid {data_type} data")

        processed_data = self.processors[data_type](data)
        self.data[f"{data_type}:{hash(str(data))}"] = processed_data
        return processed_data

    def _process_user_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user data."""
        return {k: str(v).lower() for k, v in data.items()}

    def _process_order_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process order data."""
        return {k: float(v) if isinstance(v, (int, float)) else v
                for k, v in data.items()}

    def _process_product_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process product data."""
        return {k: str(v).upper() for k, v in data.items()}

    def _validate_user_data(self, data: Dict[str, Any]) -> bool:
        """Validate user data."""
        return all(isinstance(v, str) for v in data.values())

    def _validate_order_data(self, data: Dict[str, Any]) -> bool:
        """Validate order data."""
        return all(isinstance(v, (int, float)) for v in data.values())

    def _validate_product_data(self, data: Dict[str, Any]) -> bool:
        """Validate product data."""
        return all(isinstance(v, str) for v in data.values())

# Bug: Poor separation of concerns - mixed payment processing and business logic
class PaymentSystem:
    """
    System for handling payments.
    """
    def __init__(self):
        # Bug: Mixed concerns - payment processing and business rules
        self.payments = {}
        self.business_rules = {
            'min_amount': 1.0,
            'max_amount': 10000.0,
            'allowed_currencies': ['USD', 'EUR', 'GBP'],
            'processing_fee': 0.02
        }

    def process_payment(self, amount: float, currency: str,
                       payment_method: str) -> Dict[str, Any]:
        """Process a payment."""
        # Bug: Mixed concerns - validation, processing, and business rules
        if not self._validate_payment(amount, currency):
            raise ValueError("Invalid payment details")

        if not self._check_business_rules(amount, currency):
            raise ValueError("Payment violates business rules")

        payment_id = str(random.randint(1000, 9999))
        processing_fee = amount * self.business_rules['processing_fee']

        payment = {
            'id': payment_id,
            'amount': amount,
            'currency': currency,
            'method': payment_method,
            'fee': processing_fee,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }

        self.payments[payment_id] = payment
        self._update_business_metrics(payment)

        return payment

    def _validate_payment(self, amount: float, currency: str) -> bool:
        """Validate payment details."""
        return (isinstance(amount, (int, float)) and
                amount > 0 and
                currency in self.business_rules['allowed_currencies'])

    def _check_business_rules(self, amount: float, currency: str) -> bool:
        """Check business rules."""
        return (amount >= self.business_rules['min_amount'] and
                amount <= self.business_rules['max_amount'])

    def _update_business_metrics(self, payment: Dict[str, Any]) -> None:
        """Update business metrics."""
        # Bug: Mixed concerns - business metrics and payment processing
        pass

# Bug: Inconsistent abstraction levels - mixed high and low level operations
class FileSystem:
    """
    System for file operations.
    """
    def __init__(self):
        # Bug: Mixed abstraction levels - file system and business logic
        self.base_dir = Path('files')
        self.base_dir.mkdir(exist_ok=True)
        self.file_types = {
            'text': ['.txt', '.md', '.log'],
            'image': ['.jpg', '.png', '.gif'],
            'document': ['.pdf', '.doc', '.docx']
        }

    def save_file(self, filename: str, content: Union[str, bytes],
                 file_type: str) -> bool:
        """Save file."""
        # Bug: Mixed abstraction levels - file system and business logic
        if not self._validate_file_type(filename, file_type):
            raise ValueError(f"Invalid file type for {filename}")

        try:
            file_path = self.base_dir / filename
            mode = 'wb' if isinstance(content, bytes) else 'w'
            with open(file_path, mode) as f:
                f.write(content)

            self._update_file_metadata(file_path, file_type)
            self._cleanup_old_files()
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False

    def _validate_file_type(self, filename: str, file_type: str) -> bool:
        """Validate file type."""
        if file_type not in self.file_types:
            return False
        return any(filename.endswith(ext) for ext in self.file_types[file_type])

    def _update_file_metadata(self, file_path: Path, file_type: str) -> None:
        """Update file metadata."""
        # Bug: Mixed abstraction levels - file system and metadata
        pass

    def _cleanup_old_files(self) -> None:
        """Clean up old files."""
        # Bug: Mixed abstraction levels - file system and cleanup
        pass

# Bug: Mixed responsibilities - notification and business logic
class NotificationSystem:
    """
    System for handling notifications.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - notification and business logic
        self.notifications = []
        self.templates = {
            'welcome': 'Welcome {name}!',
            'order': 'Order {order_id} has been {status}',
            'payment': 'Payment of {amount} {currency} has been {status}'
        }
        self.channels = {
            'email': self._send_email,
            'sms': self._send_sms,
            'push': self._send_push
        }

    def send_notification(self, user_id: str, template: str,
                         data: Dict[str, Any], channels: List[str]) -> bool:
        """Send notification."""
        # Bug: Mixed responsibilities - notification and business logic
        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}")

        message = self.templates[template].format(**data)
        notification = {
            'id': str(random.randint(1000, 9999)),
            'user_id': user_id,
            'template': template,
            'message': message,
            'data': data,
            'channels': channels,
            'status': 'sent',
            'timestamp': datetime.now().isoformat()
        }

        for channel in channels:
            if channel in self.channels:
                self.channels[channel](user_id, message)

        self.notifications.append(notification)
        self._update_notification_metrics(notification)
        return True

    def _send_email(self, user_id: str, message: str) -> None:
        """Send email notification."""
        # Bug: Mixed responsibilities - notification and email
        pass

    def _send_sms(self, user_id: str, message: str) -> None:
        """Send SMS notification."""
        # Bug: Mixed responsibilities - notification and SMS
        pass

    def _send_push(self, user_id: str, message: str) -> None:
        """Send push notification."""
        # Bug: Mixed responsibilities - notification and push
        pass

    def _update_notification_metrics(self, notification: Dict[str, Any]) -> None:
        """Update notification metrics."""
        # Bug: Mixed responsibilities - notification and metrics
        pass

# Bug: Unclear component relationships - mixed cache and business logic
class CacheSystem:
    """
    System for caching operations.
    """
    def __init__(self):
        # Bug: Unclear component relationships - cache and business logic
        self.cache = {}
        self.metrics = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        self.policies = {
            'max_size': 1000,
            'ttl': 3600,
            'eviction_policy': 'lru'
        }

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Bug: Unclear component relationships - cache and metrics
        if key in self.cache:
            self.metrics['hits'] += 1
            return self.cache[key]

        self.metrics['misses'] += 1
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        # Bug: Unclear component relationships - cache and policies
        if len(self.cache) >= self.policies['max_size']:
            self._evict_entries()

        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }

    def _evict_entries(self) -> None:
        """Evict entries from cache."""
        # Bug: Unclear component relationships - cache and eviction
        if self.policies['eviction_policy'] == 'lru':
            self._evict_lru()
        else:
            self._evict_random()

    def _evict_lru(self) -> None:
        """Evict least recently used entries."""
        # Bug: Unclear component relationships - cache and LRU
        pass

    def _evict_random(self) -> None:
        """Evict random entries."""
        # Bug: Unclear component relationships - cache and random
        pass

# Bug: Poor module organization - mixed service and business logic
class ServiceSystem:
    """
    System for managing services.
    """
    def __init__(self):
        # Bug: Poor module organization - mixed services
        self.services = {}
        self.dependencies = {}
        self.metrics = {}

    def register_service(self, name: str, service: Any,
                        dependencies: List[str]) -> None:
        """Register a service."""
        # Bug: Poor module organization - mixed service registration
        if name in self.services:
            raise ValueError(f"Service {name} already registered")

        self.services[name] = service
        self.dependencies[name] = dependencies
        self.metrics[name] = {
            'calls': 0,
            'errors': 0,
            'latency': []
        }

    def get_service(self, name: str) -> Any:
        """Get a service."""
        # Bug: Poor module organization - mixed service access
        if name not in self.services:
            raise ValueError(f"Service {name} not found")

        self.metrics[name]['calls'] += 1
        return self.services[name]

    def call_service(self, name: str, method: str,
                    *args, **kwargs) -> Any:
        """Call a service method."""
        # Bug: Poor module organization - mixed service calls
        service = self.get_service(name)
        if not hasattr(service, method):
            raise ValueError(f"Method {method} not found in service {name}")

        start_time = time.time()
        try:
            result = getattr(service, method)(*args, **kwargs)
            self._update_metrics(name, time.time() - start_time)
            return result
        except Exception as e:
            self.metrics[name]['errors'] += 1
            raise

    def _update_metrics(self, name: str, latency: float) -> None:
        """Update service metrics."""
        # Bug: Poor module organization - mixed metrics
        self.metrics[name]['latency'].append(latency)
        if len(self.metrics[name]['latency']) > 100:
            self.metrics[name]['latency'] = self.metrics[name]['latency'][-100:]

def main():
    # Test UserSystem mixed concerns
    print("Testing UserSystem mixed concerns:")
    user_system = UserSystem()
    try:
        user = user_system.create_user("John Doe", "john@example.com", "Password123!")
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Test AnimalSystem improper class hierarchy
    print("\nTesting AnimalSystem improper class hierarchy:")
    pet_shop = PetShop()
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Luna", "Black")
    pet_shop.add_animal(dog)
    pet_shop.add_animal(cat)
    print(f"Dog sound: {dog.make_sound()}")
    print(f"Cat sound: {cat.make_sound()}")

    # Test DataSystem unclear module boundaries
    print("\nTesting DataSystem unclear module boundaries:")
    data_system = DataSystem()
    try:
        result = data_system.process_data('user', {
            'name': 'John',
            'email': 'john@example.com'
        })
        print(f"Processed data: {result}")
    except Exception as e:
        print(f"Error processing data: {e}")

    # Test PaymentSystem poor separation of concerns
    print("\nTesting PaymentSystem poor separation of concerns:")
    payment_system = PaymentSystem()
    try:
        result = payment_system.process_payment(100.0, "USD", "credit_card")
        print(f"Payment result: {result}")
    except Exception as e:
        print(f"Error processing payment: {e}")

    # Test FileSystem inconsistent abstraction levels
    print("\nTesting FileSystem inconsistent abstraction levels:")
    file_system = FileSystem()
    try:
        result = file_system.save_file("test.txt", "Hello, World!", "text")
        print(f"File save result: {result}")
    except Exception as e:
        print(f"Error saving file: {e}")

    # Test NotificationSystem mixed responsibilities
    print("\nTesting NotificationSystem mixed responsibilities:")
    notification_system = NotificationSystem()
    try:
        result = notification_system.send_notification(
            "user1",
            "welcome",
            {"name": "John"},
            ["email", "sms"]
        )
        print(f"Notification result: {result}")
    except Exception as e:
        print(f"Error sending notification: {e}")

    # Test CacheSystem unclear component relationships
    print("\nTesting CacheSystem unclear component relationships:")
    cache_system = CacheSystem()
    cache_system.set("test_key", "test_value")
    print(f"Cached value: {cache_system.get('test_key')}")

    # Test ServiceSystem poor module organization
    print("\nTesting ServiceSystem poor module organization:")
    service_system = ServiceSystem()
    service_system.register_service("test", {"method": lambda x: x * 2}, [])
    try:
        result = service_system.call_service("test", "method", 5)
        print(f"Service call result: {result}")
    except Exception as e:
        print(f"Error calling service: {e}")

if __name__ == "__main__":
    main()