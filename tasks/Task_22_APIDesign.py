#!/usr/bin/env python3
"""
Task 22: API Design Issues Challenge

This file contains several intentional API design issues for code review practice.
The task is to identify and fix the following API design issues:

1. Inconsistent Interface Design:
   - UserAPI: Inconsistent method naming and parameter patterns
   - Mixed response formats
   - Inconsistent error handling

2. Poor Error Handling:
   - PaymentAPI: Generic error responses
   - Missing error codes
   - Inconsistent error formats

3. Versioning Issues:
   - ProductAPI: No versioning strategy
   - Breaking changes
   - Mixed API versions

4. Resource Naming Issues:
   - OrderAPI: Inconsistent resource naming
   - Poor URL structure
   - Mixed naming conventions

5. Authentication Issues:
   - SecureAPI: Inconsistent auth methods
   - Mixed security levels
   - Poor token handling

6. Response Format Issues:
   - DataAPI: Inconsistent response structures
   - Mixed data formats
   - Poor pagination

7. Documentation Issues:
   - ServiceAPI: Missing or incorrect documentation
   - Inconsistent parameter descriptions
   - Poor example usage

8. Rate Limiting Issues:
   - PublicAPI: No rate limiting
   - Inconsistent limits
   - Poor limit handling

Review the code and identify these API design issues.
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
import jwt
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: Inconsistent Interface Design
class UserAPI:
    """
    Inconsistent Interface Design: Mixed naming and response patterns.
    """
    def __init__(self):
        self.db = sqlite3.connect('users.db')
        self.cache = redis.Redis(host='localhost', port=6379, db=0)

    # Bug: Inconsistent method naming
    def get_user(self, user_id: str) -> Dict[str, Any]:
        # Bug: Inconsistent response format
        try:
            cursor = self.db.execute(
                'SELECT * FROM users WHERE id = ?',
                (user_id,)
            )
            user = cursor.fetchone()
            if user:
                return {
                    'user': {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2]
                    }
                }
            return {'error': 'User not found'}
        except Exception as e:
            return {'error': str(e)}

    # Bug: Inconsistent method naming
    def createNewUser(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Inconsistent response format
        try:
            self.db.execute('''
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            ''', (user_data['name'], user_data['email'],
                  hashlib.sha256(user_data['password'].encode()).hexdigest()))
            self.db.commit()
            return {'status': 'success', 'message': 'User created'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # Bug: Inconsistent method naming
    def update_user_info(self, user_id: str,
                        data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Inconsistent response format
        try:
            self.db.execute('''
                UPDATE users SET name = ?, email = ?
                WHERE id = ?
            ''', (data['name'], data['email'], user_id))
            self.db.commit()
            return {'result': 'updated'}
        except Exception as e:
            return {'result': 'failed', 'reason': str(e)}

    # Bug: Inconsistent method naming
    def removeUser(self, user_id: str) -> Dict[str, Any]:
        # Bug: Inconsistent response format
        try:
            self.db.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.db.commit()
            return {'deleted': True}
        except Exception as e:
            return {'deleted': False, 'error': str(e)}

# Bug: Poor Error Handling
class PaymentAPI:
    """
    Poor Error Handling: Generic errors and inconsistent formats.
    """
    def __init__(self):
        self.db = sqlite3.connect('payments.db')

    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Generic error handling
        try:
            if not self._validate_payment(payment_data):
                return {'error': 'Invalid payment data'}

            if not self._check_balance(payment_data):
                return {'error': 'Insufficient funds'}

            if not self._process_transaction(payment_data):
                return {'error': 'Transaction failed'}

            return {'status': 'success'}

        except Exception as e:
            # Bug: Generic error response
            return {'error': str(e)}

    def _validate_payment(self, data: Dict[str, Any]) -> bool:
        # Bug: No specific error codes
        if 'amount' not in data:
            raise Exception('Missing amount')
        if 'currency' not in data:
            raise Exception('Missing currency')
        if 'card_number' not in data:
            raise Exception('Missing card number')
        return True

    def _check_balance(self, data: Dict[str, Any]) -> bool:
        # Bug: No specific error codes
        if data['amount'] > 1000:
            raise Exception('Amount too high')
        return True

    def _process_transaction(self, data: Dict[str, Any]) -> bool:
        # Bug: No specific error codes
        if random.random() < 0.1:
            raise Exception('Transaction failed')
        return True

# Bug: Versioning Issues
class ProductAPI:
    """
    Versioning Issues: No versioning strategy and breaking changes.
    """
    def __init__(self):
        self.db = sqlite3.connect('products.db')
        # Bug: Mixed API versions
        self.v1_products = {}
        self.v2_products = {}

    def get_product(self, product_id: str) -> Dict[str, Any]:
        # Bug: No versioning in API
        try:
            cursor = self.db.execute(
                'SELECT * FROM products WHERE id = ?',
                (product_id,)
            )
            product = cursor.fetchone()
            if product:
                # Bug: Breaking changes in response format
                return {
                    'id': product[0],
                    'name': product[1],
                    'price': product[2],
                    'description': product[3],
                    'category': product[4],
                    'stock': product[5],
                    'created_at': product[6],
                    'updated_at': product[7],
                    'metadata': json.loads(product[8]) if product[8] else {}
                }
            return {'error': 'Product not found'}
        except Exception as e:
            return {'error': str(e)}

    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Breaking changes in parameters
        try:
            # Bug: Mixed version handling
            if 'version' in product_data and product_data['version'] == 'v2':
                return self._create_product_v2(product_data)
            return self._create_product_v1(product_data)
        except Exception as e:
            return {'error': str(e)}

    def _create_product_v1(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Old version with breaking changes
        self.db.execute('''
            INSERT INTO products (name, price, description)
            VALUES (?, ?, ?)
        ''', (data['name'], data['price'], data['description']))
        self.db.commit()
        return {'status': 'created'}

    def _create_product_v2(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: New version with different structure
        self.db.execute('''
            INSERT INTO products (name, price, description, category,
                                stock, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['price'], data['description'],
              data['category'], data['stock'],
              json.dumps(data.get('metadata', {}))))
        self.db.commit()
        return {'status': 'created', 'version': 'v2'}

# Bug: Resource Naming Issues
class OrderAPI:
    """
    Resource Naming Issues: Inconsistent naming and poor URL structure.
    """
    def __init__(self):
        self.db = sqlite3.connect('orders.db')

    # Bug: Inconsistent resource naming
    def getOrder(self, order_id: str) -> Dict[str, Any]:
        # Bug: Inconsistent method naming
        try:
            cursor = self.db.execute(
                'SELECT * FROM orders WHERE id = ?',
                (order_id,)
            )
            order = cursor.fetchone()
            if order:
                return {
                    'order_id': order[0],  # Bug: Inconsistent field naming
                    'customer': order[1],  # Bug: Inconsistent field naming
                    'items': json.loads(order[2]),
                    'total': order[3],
                    'status': order[4]
                }
            return {'error': 'Order not found'}
        except Exception as e:
            return {'error': str(e)}

    # Bug: Inconsistent resource naming
    def create_new_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Inconsistent method naming
        try:
            self.db.execute('''
                INSERT INTO orders (customer_id, items, total, status)
                VALUES (?, ?, ?, ?)
            ''', (order_data['customer_id'],
                  json.dumps(order_data['items']),
                  order_data['total'],
                  'pending'))
            self.db.commit()
            return {'order_created': True}  # Bug: Inconsistent response naming
        except Exception as e:
            return {'order_created': False, 'error': str(e)}

    # Bug: Inconsistent resource naming
    def updateOrderStatus(self, order_id: str,
                         status: str) -> Dict[str, Any]:
        # Bug: Inconsistent method naming
        try:
            self.db.execute('''
                UPDATE orders SET status = ? WHERE id = ?
            ''', (status, order_id))
            self.db.commit()
            return {'status_updated': True}  # Bug: Inconsistent response naming
        except Exception as e:
            return {'status_updated': False, 'error': str(e)}

# Bug: Authentication Issues
class SecureAPI:
    """
    Authentication Issues: Inconsistent auth methods and poor token handling.
    """
    def __init__(self):
        self.db = sqlite3.connect('auth.db')
        self.secret_key = 'your-secret-key'  # Bug: Hardcoded secret
        self.token_expiry = 3600  # Bug: Hardcoded expiry

    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed authentication methods
        try:
            if 'api_key' in credentials:
                return self._authenticate_api_key(credentials['api_key'])
            elif 'username' in credentials and 'password' in credentials:
                return self._authenticate_password(
                    credentials['username'],
                    credentials['password']
                )
            elif 'token' in credentials:
                return self._authenticate_token(credentials['token'])
            else:
                return {'error': 'Invalid credentials'}
        except Exception as e:
            return {'error': str(e)}

    def _authenticate_api_key(self, api_key: str) -> Dict[str, Any]:
        # Bug: Inconsistent auth method
        cursor = self.db.execute(
            'SELECT * FROM api_keys WHERE key = ?',
            (api_key,)
        )
        if cursor.fetchone():
            return {'authenticated': True, 'method': 'api_key'}
        return {'authenticated': False, 'error': 'Invalid API key'}

    def _authenticate_password(self, username: str,
                             password: str) -> Dict[str, Any]:
        # Bug: Inconsistent auth method
        cursor = self.db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hashlib.sha256(password.encode()).hexdigest())
        )
        if cursor.fetchone():
            token = self._generate_token(username)
            return {
                'authenticated': True,
                'method': 'password',
                'token': token
            }
        return {'authenticated': False, 'error': 'Invalid credentials'}

    def _authenticate_token(self, token: str) -> Dict[str, Any]:
        # Bug: Inconsistent auth method
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {
                'authenticated': True,
                'method': 'token',
                'user': payload['user']
            }
        except jwt.ExpiredSignatureError:
            return {'authenticated': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'authenticated': False, 'error': 'Invalid token'}

    def _generate_token(self, username: str) -> str:
        # Bug: Poor token handling
        payload = {
            'user': username,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

# Bug: Response Format Issues
class DataAPI:
    """
    Response Format Issues: Inconsistent response structures.
    """
    def __init__(self):
        self.db = sqlite3.connect('data.db')

    def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Inconsistent response format
        try:
            cursor = self.db.execute(query['sql'], query.get('params', ()))
            data = cursor.fetchall()

            # Bug: Mixed response formats
            if query.get('format') == 'detailed':
                return {
                    'data': data,
                    'metadata': {
                        'count': len(data),
                        'timestamp': datetime.now().isoformat(),
                        'query': query
                    }
                }
            elif query.get('format') == 'simple':
                return {'results': data}
            else:
                return data  # Bug: Inconsistent return type

        except Exception as e:
            # Bug: Inconsistent error format
            return {'error': str(e)}

    def get_paginated_data(self, page: int,
                          page_size: int) -> Dict[str, Any]:
        # Bug: Poor pagination
        try:
            offset = (page - 1) * page_size
            cursor = self.db.execute('''
                SELECT * FROM data LIMIT ? OFFSET ?
            ''', (page_size, offset))
            data = cursor.fetchall()

            # Bug: Inconsistent pagination format
            return {
                'data': data,
                'page': page,
                'size': page_size,
                'has_more': len(data) == page_size
            }

        except Exception as e:
            return {'error': str(e)}

# Bug: Documentation Issues
class ServiceAPI:
    """
    Documentation Issues: Missing or incorrect documentation.
    """
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Missing parameter documentation
        # Bug: Missing return value documentation
        # Bug: Missing exception documentation
        try:
            if not self._validate_request(request):
                return {'error': 'Invalid request'}

            result = self._process_data(request)
            return {'result': result}

        except Exception as e:
            return {'error': str(e)}

    def _validate_request(self, request: Dict[str, Any]) -> bool:
        # Bug: Missing documentation
        return all(key in request for key in ['type', 'data'])

    def _process_data(self, request: Dict[str, Any]) -> Any:
        # Bug: Missing documentation
        if request['type'] == 'transform':
            return self._transform_data(request['data'])
        elif request['type'] == 'filter':
            return self._filter_data(request['data'])
        else:
            raise ValueError(f"Unknown request type: {request['type']}")

    def _transform_data(self, data: Any) -> Any:
        # Bug: Missing documentation
        return str(data).upper()

    def _filter_data(self, data: Any) -> Any:
        # Bug: Missing documentation
        return [x for x in data if x > 0]

# Bug: Rate Limiting Issues
class PublicAPI:
    """
    Rate Limiting Issues: No rate limiting and inconsistent limits.
    """
    def __init__(self):
        self.db = sqlite3.connect('api.db')
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        # Bug: Inconsistent rate limits
        self.rate_limits = {
            'free': 100,  # requests per hour
            'basic': 1000,
            'premium': 10000
        }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: No rate limiting
        try:
            # Bug: Inconsistent limit checking
            if not self._check_rate_limit(request['api_key']):
                return {'error': 'Rate limit exceeded'}

            result = self._process_request(request)
            return {'result': result}

        except Exception as e:
            return {'error': str(e)}

    def _check_rate_limit(self, api_key: str) -> bool:
        # Bug: Poor rate limit implementation
        try:
            # Bug: Inconsistent limit storage
            count = self.cache.get(f"rate_limit:{api_key}")
            if count is None:
                self.cache.setex(f"rate_limit:{api_key}", 3600, 1)
                return True

            count = int(count)
            limit = self._get_rate_limit(api_key)

            if count >= limit:
                return False

            self.cache.incr(f"rate_limit:{api_key}")
            return True

        except Exception:
            return True  # Bug: Fail open

    def _get_rate_limit(self, api_key: str) -> int:
        # Bug: Inconsistent limit retrieval
        cursor = self.db.execute(
            'SELECT plan FROM api_keys WHERE key = ?',
            (api_key,)
        )
        plan = cursor.fetchone()
        return self.rate_limits.get(plan[0] if plan else 'free', 100)

def main():
    # Test Inconsistent Interface Design
    print("Testing Inconsistent Interface Design:")
    user_api = UserAPI()
    try:
        user = user_api.get_user('user1')
        print(f"Got user: {user}")

        result = user_api.createNewUser({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        })
        print(f"Created user: {result}")
    except Exception as e:
        print(f"Error in user API: {e}")

    # Test Poor Error Handling
    print("\nTesting Poor Error Handling:")
    payment_api = PaymentAPI()
    try:
        result = payment_api.process_payment({
            'amount': 100,
            'currency': 'USD',
            'card_number': '4111111111111111'
        })
        print(f"Processed payment: {result}")
    except Exception as e:
        print(f"Error in payment API: {e}")

    # Test Versioning Issues
    print("\nTesting Versioning Issues:")
    product_api = ProductAPI()
    try:
        product = product_api.get_product('product1')
        print(f"Got product: {product}")

        result = product_api.create_product({
            'version': 'v2',
            'name': 'Test Product',
            'price': 100,
            'description': 'Test Description',
            'category': 'Test Category',
            'stock': 10
        })
        print(f"Created product: {result}")
    except Exception as e:
        print(f"Error in product API: {e}")

    # Test Resource Naming Issues
    print("\nTesting Resource Naming Issues:")
    order_api = OrderAPI()
    try:
        order = order_api.getOrder('order1')
        print(f"Got order: {order}")

        result = order_api.create_new_order({
            'customer_id': 'customer1',
            'items': [{'product': 'A', 'quantity': 1}],
            'total': 100
        })
        print(f"Created order: {result}")
    except Exception as e:
        print(f"Error in order API: {e}")

    # Test Authentication Issues
    print("\nTesting Authentication Issues:")
    secure_api = SecureAPI()
    try:
        result = secure_api.authenticate({
            'username': 'john',
            'password': 'password123'
        })
        print(f"Authentication result: {result}")
    except Exception as e:
        print(f"Error in secure API: {e}")

    # Test Response Format Issues
    print("\nTesting Response Format Issues:")
    data_api = DataAPI()
    try:
        result = data_api.get_data({
            'sql': 'SELECT * FROM data',
            'format': 'detailed'
        })
        print(f"Got data: {result}")
    except Exception as e:
        print(f"Error in data API: {e}")

    # Test Documentation Issues
    print("\nTesting Documentation Issues:")
    service_api = ServiceAPI()
    try:
        result = service_api.process_request({
            'type': 'transform',
            'data': 'test'
        })
        print(f"Processed request: {result}")
    except Exception as e:
        print(f"Error in service API: {e}")

    # Test Rate Limiting Issues
    print("\nTesting Rate Limiting Issues:")
    public_api = PublicAPI()
    try:
        result = public_api.handle_request({
            'api_key': 'test_key',
            'data': 'test'
        })
        print(f"Handled request: {result}")
    except Exception as e:
        print(f"Error in public API: {e}")

if __name__ == "__main__":
    main()