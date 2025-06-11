#!/usr/bin/env python3
"""
Task 20: Code Smells Challenge

This file contains several intentional code smells for code review practice.
The task is to identify and fix the following code smells:

1. Long Method Smell:
   - OrderProcessor: Methods that are too long and do too many things
   - Complex control flow
   - Multiple levels of nesting

2. Large Class Smell:
   - UserManager: Class with too many responsibilities
   - Too many instance variables
   - Too many methods

3. Primitive Obsession Smell:
   - AddressHandler: Using primitives instead of objects
   - String manipulation for complex data
   - Lack of encapsulation

4. Data Class Smell:
   - UserData: Class that only holds data
   - No behavior
   - Public attributes

5. Feature Envy Smell:
   - OrderValidator: Method that uses another class's data more than its own
   - Inappropriate method placement
   - Violation of encapsulation

6. Inappropriate Intimacy Smell:
   - OrderProcessor and OrderValidator: Classes that know too much about each other
   - Tight coupling
   - Violation of encapsulation

7. Refused Bequest Smell:
   - SpecializedUser: Subclass that doesn't use parent class behavior
   - Inheritance misuse
   - Liskov Substitution Principle violation

8. Temporary Field Smell:
   - DataProcessor: Fields that are only used in certain situations
   - Inconsistent state
   - Poor encapsulation

Review the code and identify these code smells.
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
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: Long Method Smell - Method that is too long and does too many things
class OrderProcessor:
    """
    Long Method Smell: Methods that are too long and do too many things.
    """
    def __init__(self):
        self.db = sqlite3.connect('orders.db')
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Long Method - too many responsibilities and complex control flow
        try:
            # Validation
            if not self._validate_order_data(order_data):
                raise ValueError("Invalid order data")

            # Generate order ID
            order_id = f"ORD-{random.randint(100000, 999999)}"

            # Create order object
            order = {
                'id': order_id,
                'user_id': order_data['user_id'],
                'items': order_data['items'],
                'total': sum(item['price'] * item['quantity']
                           for item in order_data['items']),
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            }

            # Save to database
            self.db.execute('''
                INSERT INTO orders (id, user_id, items, total, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order['id'], order['user_id'], json.dumps(order['items']),
                  order['total'], order['status'], order['created_at']))
            self.db.commit()

            # Update cache
            self.cache.set(f"order:{order_id}", json.dumps(order),
                          ex=3600)

            # Process payment
            payment_result = self._process_payment(order)
            if not payment_result['success']:
                raise ValueError(f"Payment failed: {payment_result['error']}")

            # Update inventory
            inventory_result = self._update_inventory(order)
            if not inventory_result['success']:
                raise ValueError(f"Inventory update failed: {inventory_result['error']}")

            # Send notifications
            self._send_order_confirmation(order)
            self._send_inventory_notification(order)
            self._send_payment_notification(order)

            # Update order status
            order['status'] = 'completed'
            self.db.execute('''
                UPDATE orders SET status = ? WHERE id = ?
            ''', (order['status'], order['id']))
            self.db.commit()

            # Update cache
            self.cache.set(f"order:{order_id}", json.dumps(order),
                          ex=3600)

            # Log success
            logger.info(f"Order {order_id} processed successfully")

            return order

        except Exception as e:
            # Error handling
            logger.error(f"Error processing order: {str(e)}")
            if 'order' in locals():
                self._handle_failed_order(order, str(e))
            raise

    def _validate_order_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Long Method - complex validation logic
        if not isinstance(data, dict):
            return False

        if 'user_id' not in data or not isinstance(data['user_id'], str):
            return False

        if 'items' not in data or not isinstance(data['items'], list):
            return False

        for item in data['items']:
            if not isinstance(item, dict):
                return False

            if 'product_id' not in item or not isinstance(item['product_id'], str):
                return False

            if 'price' not in item or not isinstance(item['price'], (int, float)):
                return False

            if 'quantity' not in item or not isinstance(item['quantity'], int):
                return False

            if item['price'] < 0 or item['quantity'] < 0:
                return False

        return True

    def _process_payment(self, order: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Long Method - complex payment processing
        try:
            # Validate payment data
            if not self._validate_payment_data(order):
                return {'success': False, 'error': 'Invalid payment data'}

            # Check payment method
            payment_method = self._get_payment_method(order['user_id'])
            if not payment_method:
                return {'success': False, 'error': 'No payment method found'}

            # Process payment based on method
            if payment_method == 'credit_card':
                result = self._process_credit_card_payment(order)
            elif payment_method == 'paypal':
                result = self._process_paypal_payment(order)
            else:
                return {'success': False, 'error': 'Unsupported payment method'}

            # Update payment status
            if result['success']:
                self._update_payment_status(order['id'], 'completed')

            return result

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _update_inventory(self, order: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Long Method - complex inventory update
        try:
            # Validate inventory data
            if not self._validate_inventory_data(order):
                return {'success': False, 'error': 'Invalid inventory data'}

            # Check inventory availability
            for item in order['items']:
                if not self._check_item_availability(item):
                    return {'success': False, 'error': 'Item not available'}

            # Update inventory levels
            for item in order['items']:
                self._update_item_quantity(item)

            # Log inventory changes
            self._log_inventory_changes(order)

            return {'success': True}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _handle_failed_order(self, order: Dict[str, Any], error: str) -> None:
        # Bug: Long Method - complex error handling
        try:
            # Update order status
            order['status'] = 'failed'
            order['error'] = error

            # Save to database
            self.db.execute('''
                UPDATE orders SET status = ?, error = ? WHERE id = ?
            ''', (order['status'], error, order['id']))
            self.db.commit()

            # Update cache
            self.cache.set(f"order:{order['id']}", json.dumps(order),
                          ex=3600)

            # Send failure notification
            self._send_failure_notification(order)

            # Log failure
            logger.error(f"Order {order['id']} failed: {error}")

        except Exception as e:
            logger.error(f"Error handling failed order: {str(e)}")

# Bug: Large Class Smell - Class with too many responsibilities
class UserManager:
    """
    Large Class Smell: Class with too many responsibilities and methods.
    """
    def __init__(self):
        # Bug: Too many instance variables
        self.db = sqlite3.connect('users.db')
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp_server.starttls()
        self.smtp_server.login('app@gmail.com', 'password123')
        self.password_salt = "random_salt"
        self.session_timeout = 3600
        self.max_login_attempts = 3
        self.password_min_length = 8
        self.password_require_special = True
        self.password_require_numbers = True
        self.password_require_uppercase = True
        self.email_verification_required = True
        self.phone_verification_required = True
        self.two_factor_required = True
        self.notification_preferences = {}
        self.user_roles = {}
        self.permissions = {}
        self.audit_log = []
        self.failed_logins = {}
        self.locked_accounts = set()
        self.verification_tokens = {}
        self.password_reset_tokens = {}
        self.session_tokens = {}
        self.api_keys = {}
        self.oauth_tokens = {}
        self.user_preferences = {}
        self.user_statistics = {}
        self.user_activity_log = []
        self.user_devices = {}
        self.user_sessions = {}
        self.user_notifications = {}
        self.user_messages = {}
        self.user_files = {}
        self.user_settings = {}
        self.user_metadata = {}

    # Bug: Too many methods with mixed responsibilities
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # User creation logic
        pass

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # User update logic
        pass

    def delete_user(self, user_id: str) -> bool:
        # User deletion logic
        pass

    def authenticate_user(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        # Authentication logic
        pass

    def verify_email(self, token: str) -> bool:
        # Email verification logic
        pass

    def verify_phone(self, token: str) -> bool:
        # Phone verification logic
        pass

    def reset_password(self, token: str, new_password: str) -> bool:
        # Password reset logic
        pass

    def change_password(self, user_id: str, old_password: str,
                       new_password: str) -> bool:
        # Password change logic
        pass

    def enable_2fa(self, user_id: str) -> Dict[str, Any]:
        # 2FA enablement logic
        pass

    def disable_2fa(self, user_id: str) -> bool:
        # 2FA disablement logic
        pass

    def generate_api_key(self, user_id: str) -> str:
        # API key generation logic
        pass

    def revoke_api_key(self, user_id: str, api_key: str) -> bool:
        # API key revocation logic
        pass

    def update_preferences(self, user_id: str,
                          preferences: Dict[str, Any]) -> bool:
        # Preferences update logic
        pass

    def update_role(self, user_id: str, role: str) -> bool:
        # Role update logic
        pass

    def update_permissions(self, user_id: str,
                          permissions: List[str]) -> bool:
        # Permissions update logic
        pass

    def log_activity(self, user_id: str, activity: str) -> None:
        # Activity logging logic
        pass

    def get_statistics(self, user_id: str) -> Dict[str, Any]:
        # Statistics retrieval logic
        pass

    def manage_devices(self, user_id: str, device_data: Dict[str, Any]) -> bool:
        # Device management logic
        pass

    def manage_sessions(self, user_id: str,
                       session_data: Dict[str, Any]) -> bool:
        # Session management logic
        pass

    def send_notification(self, user_id: str,
                         notification: Dict[str, Any]) -> bool:
        # Notification sending logic
        pass

    def send_message(self, user_id: str, message: Dict[str, Any]) -> bool:
        # Message sending logic
        pass

    def manage_files(self, user_id: str, file_data: Dict[str, Any]) -> bool:
        # File management logic
        pass

    def update_settings(self, user_id: str,
                       settings: Dict[str, Any]) -> bool:
        # Settings update logic
        pass

    def update_metadata(self, user_id: str,
                       metadata: Dict[str, Any]) -> bool:
        # Metadata update logic
        pass

# Bug: Primitive Obsession Smell - Using primitives instead of objects
class AddressHandler:
    """
    Primitive Obsession Smell: Using primitives instead of proper objects.
    """
    def __init__(self):
        # Bug: Using primitive types for complex data
        self.addresses = {}  # Dict[str, Dict[str, str]]

    def add_address(self, user_id: str, address_data: Dict[str, str]) -> bool:
        # Bug: String manipulation for complex data
        try:
            # Validate address components
            if not all(key in address_data for key in
                      ['street', 'city', 'state', 'zip', 'country']):
                return False

            # Format address
            formatted_address = (
                f"{address_data['street']}\n"
                f"{address_data['city']}, {address_data['state']} "
                f"{address_data['zip']}\n"
                f"{address_data['country']}"
            )

            # Store address
            self.addresses[user_id] = {
                'raw': address_data,
                'formatted': formatted_address,
                'validation': self._validate_address(address_data)
            }

            return True

        except Exception:
            return False

    def _validate_address(self, address: Dict[str, str]) -> Dict[str, Any]:
        # Bug: Complex validation using primitives
        validation = {
            'is_valid': True,
            'errors': []
        }

        # Validate street
        if not address['street'] or len(address['street']) < 5:
            validation['is_valid'] = False
            validation['errors'].append('Invalid street address')

        # Validate city
        if not address['city'] or not address['city'].replace(' ', '').isalpha():
            validation['is_valid'] = False
            validation['errors'].append('Invalid city')

        # Validate state
        if not address['state'] or len(address['state']) != 2:
            validation['is_valid'] = False
            validation['errors'].append('Invalid state')

        # Validate zip
        if not address['zip'] or not address['zip'].isdigit():
            validation['is_valid'] = False
            validation['errors'].append('Invalid zip code')

        # Validate country
        if not address['country'] or len(address['country']) != 2:
            validation['is_valid'] = False
            validation['errors'].append('Invalid country')

        return validation

# Bug: Data Class Smell - Class that only holds data
@dataclass
class UserData:
    """
    Data Class Smell: Class that only holds data with no behavior.
    """
    # Bug: Public attributes with no encapsulation
    user_id: str
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str
    address: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    last_login: datetime
    is_active: bool
    is_verified: bool
    role: str
    permissions: List[str]
    preferences: Dict[str, Any]
    metadata: Dict[str, Any]

# Bug: Feature Envy Smell - Method that uses another class's data more than its own
class OrderValidator:
    """
    Feature Envy Smell: Method that uses another class's data more than its own.
    """
    def __init__(self):
        # Bug: Minimal own data
        self.validation_rules = {
            'min_order_amount': 10.0,
            'max_order_amount': 1000.0
        }

    def validate_order(self, order: Dict[str, Any],
                      user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Uses user_data more than its own data
        validation = {
            'is_valid': True,
            'errors': []
        }

        # Validate user data
        if not user_data['is_active']:
            validation['is_valid'] = False
            validation['errors'].append('User account is inactive')

        if not user_data['is_verified']:
            validation['is_valid'] = False
            validation['errors'].append('User email is not verified')

        if not user_data['address']:
            validation['is_valid'] = False
            validation['errors'].append('User has no shipping address')

        # Validate order against user data
        if order['total'] > user_data.get('credit_limit', 0):
            validation['is_valid'] = False
            validation['errors'].append('Order exceeds credit limit')

        if not any(role in user_data['permissions']
                  for role in ['can_order', 'can_purchase']):
            validation['is_valid'] = False
            validation['errors'].append('User lacks order permissions')

        return validation

# Bug: Inappropriate Intimacy Smell - Classes that know too much about each other
class OrderProcessor:
    """
    Inappropriate Intimacy Smell: Class that knows too much about another class.
    """
    def __init__(self, validator: 'OrderValidator'):
        # Bug: Direct dependency on another class
        self.validator = validator
        self.db = sqlite3.connect('orders.db')

    def process_order(self, order: Dict[str, Any],
                     user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Direct access to another class's internals
        validation = self.validator.validate_order(order, user_data)
        if not validation['is_valid']:
            raise ValueError(validation['errors'])

        # Process order using user data directly
        order['user_email'] = user_data['email']
        order['user_address'] = user_data['address']
        order['user_permissions'] = user_data['permissions']

        # Save order with user data
        self.db.execute('''
            INSERT INTO orders (id, user_id, user_email, user_address,
                              user_permissions, items, total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order['id'], user_data['user_id'], user_data['email'],
              json.dumps(user_data['address']),
              json.dumps(user_data['permissions']),
              json.dumps(order['items']), order['total'],
              'pending'))
        self.db.commit()

        return order

# Bug: Refused Bequest Smell - Subclass that doesn't use parent class behavior
class User:
    """
    Base class for user functionality.
    """
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = True
        self.created_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def update_email(self, new_email: str) -> None:
        self.email = new_email

    def get_info(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class SpecializedUser(User):
    """
    Refused Bequest Smell: Subclass that doesn't use parent class behavior.
    """
    def __init__(self, user_id: str, username: str, email: str):
        # Bug: Doesn't call parent's __init__
        self.id = user_id  # Different attribute name
        self.name = username  # Different attribute name
        self.contact = email  # Different attribute name
        self.status = True  # Different attribute name
        self.registration_date = datetime.now()  # Different attribute name

    # Bug: Doesn't use parent's methods
    def enable(self) -> None:
        self.status = True

    def disable(self) -> None:
        self.status = False

    def change_contact(self, new_contact: str) -> None:
        self.contact = new_contact

    def get_details(self) -> Dict[str, Any]:  # Different method name
        return {
            'id': self.id,
            'name': self.name,
            'contact': self.contact,
            'status': self.status,
            'registration_date': self.registration_date.isoformat()
        }

# Bug: Temporary Field Smell - Fields that are only used in certain situations
class DataProcessor:
    """
    Temporary Field Smell: Fields that are only used in certain situations.
    """
    def __init__(self):
        # Bug: Temporary fields that are only used in specific methods
        self.temp_data = None
        self.processing_status = None
        self.validation_result = None
        self.transformation_cache = {}
        self.error_context = None
        self.retry_count = 0
        self.last_operation = None
        self.operation_timestamp = None

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Setting temporary fields
        self.temp_data = data
        self.processing_status = 'started'
        self.operation_timestamp = datetime.now()

        try:
            # Process data
            result = self._transform_data(data)
            self.processing_status = 'completed'
            return result

        except Exception as e:
            # Bug: Using temporary fields for error handling
            self.error_context = str(e)
            self.processing_status = 'failed'
            raise

        finally:
            # Bug: Cleaning up temporary fields
            self.temp_data = None
            self.processing_status = None
            self.error_context = None

    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Using temporary fields for transformation
        if data in self.transformation_cache:
            return self.transformation_cache[data]

        self.last_operation = 'transform'
        result = {k: str(v).upper() for k, v in data.items()}
        self.transformation_cache[data] = result

        return result

def main():
    # Test Long Method smell
    print("Testing Long Method smell:")
    order_processor = OrderProcessor()
    try:
        result = order_processor.process_order({
            'user_id': 'user1',
            'items': [
                {'product_id': 'A', 'price': 100, 'quantity': 1}
            ]
        })
        print(f"Processed order: {result}")
    except Exception as e:
        print(f"Error in order processor: {e}")

    # Test Large Class smell
    print("\nTesting Large Class smell:")
    user_manager = UserManager()
    try:
        user = user_manager.create_user({
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'Password123!'
        })
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error in user manager: {e}")

    # Test Primitive Obsession smell
    print("\nTesting Primitive Obsession smell:")
    address_handler = AddressHandler()
    try:
        result = address_handler.add_address('user1', {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
            'country': 'US'
        })
        print(f"Added address: {result}")
    except Exception as e:
        print(f"Error in address handler: {e}")

    # Test Data Class smell
    print("\nTesting Data Class smell:")
    user_data = UserData(
        user_id='user1',
        username='john_doe',
        email='john@example.com',
        password='hashed_password',
        first_name='John',
        last_name='Doe',
        phone='1234567890',
        address={'street': '123 Main St'},
        created_at=datetime.now(),
        updated_at=datetime.now(),
        last_login=datetime.now(),
        is_active=True,
        is_verified=True,
        role='user',
        permissions=['read'],
        preferences={},
        metadata={}
    )
    print(f"Created user data: {user_data}")

    # Test Feature Envy smell
    print("\nTesting Feature Envy smell:")
    order_validator = OrderValidator()
    try:
        result = order_validator.validate_order(
            {'total': 100},
            {
                'is_active': True,
                'is_verified': True,
                'address': {'street': '123 Main St'},
                'credit_limit': 1000,
                'permissions': ['can_order']
            }
        )
        print(f"Validated order: {result}")
    except Exception as e:
        print(f"Error in order validator: {e}")

    # Test Inappropriate Intimacy smell
    print("\nTesting Inappropriate Intimacy smell:")
    order_processor = OrderProcessor(order_validator)
    try:
        result = order_processor.process_order(
            {'id': 'order1', 'items': [], 'total': 100},
            {
                'user_id': 'user1',
                'email': 'john@example.com',
                'address': {'street': '123 Main St'},
                'permissions': ['can_order']
            }
        )
        print(f"Processed order: {result}")
    except Exception as e:
        print(f"Error in order processor: {e}")

    # Test Refused Bequest smell
    print("\nTesting Refused Bequest smell:")
    specialized_user = SpecializedUser('user1', 'john_doe', 'john@example.com')
    print(f"Created specialized user: {specialized_user.get_details()}")

    # Test Temporary Field smell
    print("\nTesting Temporary Field smell:")
    data_processor = DataProcessor()
    try:
        result = data_processor.process_data({'key': 'value'})
        print(f"Processed data: {result}")
    except Exception as e:
        print(f"Error in data processor: {e}")

if __name__ == "__main__":
    main()