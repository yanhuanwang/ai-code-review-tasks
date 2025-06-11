#!/usr/bin/env python3
"""
Task 10: API Design and Interface Challenge

This file contains several intentional API design and interface issues for code review practice.
The task is to identify and fix the following issues:
1. Inconsistent method signatures in UserAPI
2. Poor error handling in PaymentAPI
3. Inconsistent return types in DataAPI
4. Mixed abstraction levels in FileAPI
5. Poor parameter validation in SearchAPI
6. Inconsistent naming conventions in CacheAPI
7. Poor interface design in NotificationAPI
8. Improper abstraction in DatabaseAPI

Review the code and identify these API design and interface issues.
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
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserAPI:
    """
    API for user management operations.
    Bug: Inconsistent method signatures and parameter handling.
    """
    def __init__(self):
        self.users = {}

    # Bug: Inconsistent method signatures
    def create_user(self, name: str, email: str, age: int) -> Dict[str, Any]:
        """Create a new user."""
        user_id = str(random.randint(1000, 9999))
        self.users[user_id] = {
            "name": name,
            "email": email,
            "age": age
        }
        return {"id": user_id, "name": name, "email": email, "age": age}

    # Bug: Different parameter order and naming
    def update_user(self, user_id: str, data: Dict[str, Any]) -> None:
        """Update user information."""
        if user_id in self.users:
            self.users[user_id].update(data)

    # Bug: Inconsistent return type
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information."""
        return self.users.get(user_id)

    # Bug: Different parameter style
    def delete_user(self, *args, **kwargs) -> bool:
        """Delete a user."""
        user_id = args[0] if args else kwargs.get("user_id")
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    # Bug: Inconsistent method naming
    def findUsersByEmail(self, email: str) -> List[Dict[str, Any]]:
        """Find users by email."""
        return [user for user in self.users.values() if user["email"] == email]

    # Bug: Different parameter validation
    def search_users(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search users."""
        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        return list(self.users.values())[:limit]

class PaymentAPI:
    """
    API for payment processing.
    Bug: Poor error handling and inconsistent error responses.
    """
    def __init__(self):
        self.payments = {}
        self.balance = 1000.0

    # Bug: Inconsistent error handling
    def process_payment(self, amount: float, user_id: str) -> Dict[str, Any]:
        """Process a payment."""
        try:
            if amount <= 0:
                return {"status": "error", "message": "Invalid amount"}

            if amount > self.balance:
                return {"status": "error", "message": "Insufficient funds"}

            payment_id = str(random.randint(1000, 9999))
            self.payments[payment_id] = {
                "amount": amount,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
            self.balance -= amount

            return {
                "status": "success",
                "payment_id": payment_id,
                "amount": amount
            }
        except Exception as e:
            # Bug: Generic exception handling
            return {"status": "error", "message": str(e)}

    # Bug: Inconsistent error response format
    def refund_payment(self, payment_id: str) -> Tuple[bool, str]:
        """Refund a payment."""
        if payment_id not in self.payments:
            return False, "Payment not found"

        payment = self.payments[payment_id]
        self.balance += payment["amount"]
        del self.payments[payment_id]
        return True, "Refund successful"

    # Bug: Silent error handling
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status."""
        payment = self.payments.get(payment_id)
        if not payment:
            return {"status": "unknown"}
        return {"status": "completed", "details": payment}

    # Bug: Inconsistent error propagation
    def cancel_payment(self, payment_id: str) -> None:
        """Cancel a payment."""
        if payment_id in self.payments:
            payment = self.payments[payment_id]
            self.balance += payment["amount"]
            del self.payments[payment_id]

class DataAPI:
    """
    API for data operations.
    Bug: Inconsistent return types and mixed abstraction levels.
    """
    def __init__(self):
        self.data = {}

    # Bug: Inconsistent return types
    def get_data(self, key: str) -> Union[Dict[str, Any], List[Any], str, None]:
        """Get data by key."""
        return self.data.get(key)

    # Bug: Mixed abstraction levels
    def store_data(self, key: str, value: Any) -> bool:
        """Store data."""
        try:
            if isinstance(value, (dict, list)):
                self.data[key] = value
            elif isinstance(value, str):
                self.data[key] = json.loads(value)
            else:
                self.data[key] = str(value)
            return True
        except Exception:
            return False

    # Bug: Inconsistent return format
    def update_data(self, key: str, value: Any) -> Dict[str, Any]:
        """Update data."""
        if key in self.data:
            self.data[key] = value
            return {"status": "success", "key": key, "value": value}
        return {"status": "error", "message": "Key not found"}

    # Bug: Mixed return types
    def delete_data(self, key: str) -> Union[bool, Dict[str, Any]]:
        """Delete data."""
        if key in self.data:
            del self.data[key]
            return True
        return {"status": "error", "message": "Key not found"}

    # Bug: Inconsistent method behavior
    def list_data(self, prefix: str = "") -> List[str]:
        """List data keys."""
        if prefix:
            return [k for k in self.data.keys() if k.startswith(prefix)]
        return list(self.data.keys())

class FileAPI:
    """
    API for file operations.
    Bug: Mixed abstraction levels and inconsistent interface.
    """
    def __init__(self):
        self.files = {}

    # Bug: Mixed abstraction levels
    def save_file(self, filename: str, content: Union[str, bytes]) -> bool:
        """Save file content."""
        try:
            if isinstance(content, str):
                self.files[filename] = content.encode()
            else:
                self.files[filename] = content
            return True
        except Exception:
            return False

    # Bug: Inconsistent interface
    def read_file(self, filename: str, as_text: bool = True) -> Union[str, bytes, None]:
        """Read file content."""
        if filename in self.files:
            content = self.files[filename]
            return content.decode() if as_text else content
        return None

    # Bug: Mixed abstraction levels
    def delete_file(self, filename: str) -> Dict[str, Any]:
        """Delete a file."""
        if filename in self.files:
            del self.files[filename]
            return {"status": "success", "filename": filename}
        return {"status": "error", "message": "File not found"}

    # Bug: Inconsistent method behavior
    def list_files(self, pattern: str = "*") -> List[str]:
        """List files."""
        if pattern == "*":
            return list(self.files.keys())
        return [f for f in self.files.keys() if re.match(pattern, f)]

    # Bug: Mixed abstraction levels
    def copy_file(self, source: str, destination: str) -> bool:
        """Copy a file."""
        if source in self.files:
            self.files[destination] = self.files[source]
            return True
        return False

class SearchAPI:
    """
    API for search operations.
    Bug: Poor parameter validation and inconsistent search behavior.
    """
    def __init__(self):
        self.items = []

    # Bug: Poor parameter validation
    def search(self, query: Any, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search items."""
        results = []
        for item in self.items:
            if self._matches_query(item, query) and self._matches_filters(item, filters):
                results.append(item)
        return results

    # Bug: Inconsistent search behavior
    def advanced_search(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Advanced search with multiple criteria."""
        results = self.items
        for field, value in criteria.items():
            results = [item for item in results if self._matches_field(item, field, value)]
        return results

    # Bug: Poor parameter validation
    def _matches_query(self, item: Dict[str, Any], query: Any) -> bool:
        """Check if item matches query."""
        if isinstance(query, str):
            return any(query.lower() in str(v).lower() for v in item.values())
        return query in item.values()

    # Bug: Inconsistent filter handling
    def _matches_filters(self, item: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        """Check if item matches filters."""
        if not filters:
            return True
        return all(self._matches_field(item, field, value) for field, value in filters.items())

    # Bug: Poor parameter validation
    def _matches_field(self, item: Dict[str, Any], field: str, value: Any) -> bool:
        """Check if item field matches value."""
        if field not in item:
            return False
        if isinstance(value, (int, float)):
            return item[field] == value
        if isinstance(value, str):
            return value.lower() in str(item[field]).lower()
        return item[field] == value

class CacheAPI:
    """
    API for caching operations.
    Bug: Inconsistent naming conventions and mixed abstraction levels.
    """
    def __init__(self):
        self.cache = {}
        self.ttl = {}

    # Bug: Inconsistent naming
    def setCache(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set cache value."""
        self.cache[key] = value
        self.ttl[key] = time.time() + ttl

    # Bug: Inconsistent naming
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cache value."""
        if key in self.cache and time.time() < self.ttl.get(key, 0):
            return self.cache[key]
        return None

    # Bug: Mixed abstraction levels
    def deleteCache(self, key: str) -> bool:
        """Delete cache value."""
        if key in self.cache:
            del self.cache[key]
            del self.ttl[key]
            return True
        return False

    # Bug: Inconsistent naming
    def clear_cache(self) -> None:
        """Clear all cache values."""
        self.cache.clear()
        self.ttl.clear()

    # Bug: Mixed abstraction levels
    def getCacheStats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "keys": list(self.cache.keys()),
            "ttl": {k: v - time.time() for k, v in self.ttl.items()}
        }

class NotificationAPI:
    """
    API for notification operations.
    Bug: Poor interface design and inconsistent notification handling.
    """
    def __init__(self):
        self.notifications = []

    # Bug: Poor interface design
    def send_notification(self, user_id: str, message: str,
                         notification_type: str = "info",
                         priority: int = 1,
                         channel: str = "email") -> Dict[str, Any]:
        """Send a notification."""
        notification = {
            "id": str(random.randint(1000, 9999)),
            "user_id": user_id,
            "message": message,
            "type": notification_type,
            "priority": priority,
            "channel": channel,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }
        self.notifications.append(notification)
        return notification

    # Bug: Inconsistent notification handling
    def get_notifications(self, user_id: Optional[str] = None,
                         notification_type: Optional[str] = None,
                         status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get notifications."""
        results = self.notifications
        if user_id:
            results = [n for n in results if n["user_id"] == user_id]
        if notification_type:
            results = [n for n in results if n["type"] == notification_type]
        if status:
            results = [n for n in results if n["status"] == status]
        return results

    # Bug: Poor interface design
    def mark_as_read(self, notification_id: str) -> bool:
        """Mark notification as read."""
        for notification in self.notifications:
            if notification["id"] == notification_id:
                notification["status"] = "read"
                return True
        return False

    # Bug: Inconsistent notification handling
    def delete_notification(self, notification_id: str) -> Dict[str, Any]:
        """Delete a notification."""
        for i, notification in enumerate(self.notifications):
            if notification["id"] == notification_id:
                del self.notifications[i]
                return {"status": "success", "id": notification_id}
        return {"status": "error", "message": "Notification not found"}

class DatabaseAPI:
    """
    API for database operations.
    Bug: Improper abstraction and mixed concerns.
    """
    def __init__(self):
        self.tables = {}

    # Bug: Improper abstraction
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a database query."""
        # Bug: Mixed concerns (query parsing and execution)
        if query.lower().startswith("select"):
            table = query.split("from")[1].split()[0]
            if table in self.tables:
                return self.tables[table]
        elif query.lower().startswith("insert"):
            table = query.split("into")[1].split()[0]
            if table not in self.tables:
                self.tables[table] = []
            self.tables[table].append(params or {})
        elif query.lower().startswith("update"):
            table = query.split("update")[1].split()[0]
            if table in self.tables:
                for row in self.tables[table]:
                    row.update(params or {})
        elif query.lower().startswith("delete"):
            table = query.split("from")[1].split()[0]
            if table in self.tables:
                self.tables[table] = []
        return []

    # Bug: Mixed concerns
    def create_table(self, table_name: str, columns: List[str]) -> bool:
        """Create a new table."""
        if table_name not in self.tables:
            self.tables[table_name] = []
            return True
        return False

    # Bug: Improper abstraction
    def insert_row(self, table: str, data: Dict[str, Any]) -> bool:
        """Insert a row into a table."""
        if table in self.tables:
            self.tables[table].append(data)
            return True
        return False

    # Bug: Mixed concerns
    def update_row(self, table: str, where: Dict[str, Any], data: Dict[str, Any]) -> int:
        """Update rows in a table."""
        if table not in self.tables:
            return 0
        count = 0
        for row in self.tables[table]:
            if all(row.get(k) == v for k, v in where.items()):
                row.update(data)
                count += 1
        return count

    # Bug: Improper abstraction
    def delete_rows(self, table: str, where: Dict[str, Any]) -> int:
        """Delete rows from a table."""
        if table not in self.tables:
            return 0
        initial_count = len(self.tables[table])
        self.tables[table] = [
            row for row in self.tables[table]
            if not all(row.get(k) == v for k, v in where.items())
        ]
        return initial_count - len(self.tables[table])

def main():
    # Test UserAPI inconsistent method signatures
    print("Testing UserAPI inconsistent method signatures:")
    user_api = UserAPI()
    user = user_api.create_user("John Doe", "john@example.com", 30)
    print(f"Created user: {user}")
    user_api.update_user(user["id"], {"age": 31})
    print(f"Updated user: {user_api.get_user(user['id'])}")
    print(f"Found users: {user_api.findUsersByEmail('john@example.com')}")
    print(f"Deleted user: {user_api.delete_user(user_id=user['id'])}")

    # Test PaymentAPI poor error handling
    print("\nTesting PaymentAPI poor error handling:")
    payment_api = PaymentAPI()
    result = payment_api.process_payment(100.0, "user1")
    print(f"Payment result: {result}")
    status, message = payment_api.refund_payment(result["payment_id"])
    print(f"Refund result: {status}, {message}")
    print(f"Payment status: {payment_api.get_payment_status(result['payment_id'])}")

    # Test DataAPI inconsistent return types
    print("\nTesting DataAPI inconsistent return types:")
    data_api = DataAPI()
    data_api.store_data("key1", {"name": "John"})
    print(f"Stored data: {data_api.get_data('key1')}")
    print(f"Updated data: {data_api.update_data('key1', {'name': 'Jane'})}")
    print(f"Deleted data: {data_api.delete_data('key1')}")

    # Test FileAPI mixed abstraction levels
    print("\nTesting FileAPI mixed abstraction levels:")
    file_api = FileAPI()
    file_api.save_file("test.txt", "Hello, World!")
    print(f"File content: {file_api.read_file('test.txt')}")
    print(f"Deleted file: {file_api.delete_file('test.txt')}")

    # Test SearchAPI poor parameter validation
    print("\nTesting SearchAPI poor parameter validation:")
    search_api = SearchAPI()
    search_api.items = [
        {"name": "John", "age": 30},
        {"name": "Jane", "age": 25}
    ]
    print(f"Search results: {search_api.search('John')}")
    print(f"Advanced search: {search_api.advanced_search({'age': 30})}")

    # Test CacheAPI inconsistent naming
    print("\nTesting CacheAPI inconsistent naming:")
    cache_api = CacheAPI()
    cache_api.setCache("key1", "value1")
    print(f"Cached value: {cache_api.get_cache('key1')}")
    print(f"Cache stats: {cache_api.getCacheStats()}")

    # Test NotificationAPI poor interface design
    print("\nTesting NotificationAPI poor interface design:")
    notification_api = NotificationAPI()
    notification = notification_api.send_notification(
        "user1",
        "Hello!",
        notification_type="info",
        priority=1,
        channel="email"
    )
    print(f"Sent notification: {notification}")
    print(f"User notifications: {notification_api.get_notifications(user_id='user1')}")

    # Test DatabaseAPI improper abstraction
    print("\nTesting DatabaseAPI improper abstraction:")
    db_api = DatabaseAPI()
    db_api.create_table("users", ["id", "name", "email"])
    db_api.insert_row("users", {"id": 1, "name": "John", "email": "john@example.com"})
    print(f"Query results: {db_api.execute_query('SELECT * FROM users')}")
    print(f"Updated rows: {db_api.update_row('users', {'id': 1}, {'name': 'Jane'})}")

if __name__ == "__main__":
    main()