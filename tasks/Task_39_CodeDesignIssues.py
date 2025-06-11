#!/usr/bin/env python3
"""
Task 39: Code Design Issues Challenge

This file contains several intentional design issues for code review practice.
The task is to identify and fix the following design problems:

1. Poor Separation of Concerns:
   - MixedManager: mixed responsibilities
   - DataManager: unclear boundaries
   - ServiceManager: multiple concerns

2. Tight Coupling:
   - OrderManager: direct dependencies
   - UserManager: concrete implementations
   - ProcessManager: hard-coded dependencies

3. Violation of SOLID Principles:
   - Single Responsibility: Manager class
   - Open/Closed: PaymentProcessor
   - Liskov Substitution: User hierarchy
   - Interface Segregation: DataProcessor
   - Dependency Inversion: ServiceManager

4. Poor Abstraction:
   - FileManager: leaky abstractions
   - DatabaseManager: implementation details
   - NetworkManager: low-level details

5. God Classes:
   - SystemManager: too many responsibilities
   - ProcessManager: too many methods
   - DataManager: too many features

6. Poor Encapsulation:
   - UserManager: exposed internals
   - CacheManager: public state
   - ConfigManager: global state

7. Inappropriate Inheritance:
   - User hierarchy: wrong abstraction
   - Processor hierarchy: deep inheritance
   - Manager hierarchy: mixed concerns

8. Poor Interface Design:
   - DataProcessor: unclear contracts
   - ServiceManager: inconsistent methods
   - ValidationManager: mixed interfaces

Review the code and identify these design issues.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
from typing import List, Dict, Any, Optional, Union, Tuple, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import psycopg2
from abc import ABC, abstractmethod
from enum import Enum
from collections import defaultdict

# Bug: Poor Separation of Concerns
class MixedManager:
    """
    Manager with mixed responsibilities and poor separation of concerns.
    """
    def __init__(self):
        # Bug: Mixed concerns
        self.db = sqlite3.connect(":memory:")  # Database
        self.cache = {}  # Caching
        self.logger = logging.getLogger(__name__)  # Logging
        self.config = {}  # Configuration
        self.users = {}  # User management
        self.orders = {}  # Order management
        self.products = {}  # Product management
        self.notifications = []  # Notifications
        self.metrics = defaultdict(int)  # Metrics
        self.locks = {}  # Threading
        self.timers = {}  # Timing
        self.validators = {}  # Validation
        self.transformers = {}  # Data transformation

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities
        try:
            # Validate data
            if not self._validate_data(data):
                raise ValueError("Invalid data")

            # Transform data
            transformed = self._transform_data(data)

            # Save to database
            self._save_to_db(transformed)

            # Update cache
            self._update_cache(transformed)

            # Send notification
            self._send_notification(transformed)

            # Update metrics
            self._update_metrics(transformed)

            # Log operation
            self._log_operation(transformed)

            return transformed
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            return {"error": str(e)}

# Bug: Tight Coupling
class OrderManager:
    """
    Order manager with tight coupling to concrete implementations.
    """
    def __init__(self):
        # Bug: Direct dependencies
        # Bug: Concrete implementations
        # Bug: Hard-coded dependencies
        self.db = sqlite3.connect(":memory:")
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        self.email_sender = self._create_email_sender()
        self.payment_processor = self._create_payment_processor()
        self.shipping_service = self._create_shipping_service()
        self.notification_service = self._create_notification_service()

    def process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Tightly coupled operations
        try:
            # Process payment
            payment_result = self.payment_processor.process_payment(order)

            # Update database
            self.db.execute("INSERT INTO orders VALUES (?)", (json.dumps(order),))
            self.db.commit()

            # Update cache
            self.cache[order["id"]] = order

            # Send email
            self.email_sender.send_order_confirmation(order)

            # Process shipping
            shipping_result = self.shipping_service.create_shipment(order)

            # Send notification
            self.notification_service.notify_order_processed(order)

            # Log operation
            self.logger.info(f"Order processed: {order}")

            return {
                "order": order,
                "payment": payment_result,
                "shipping": shipping_result
            }
        except Exception as e:
            self.logger.error(f"Error processing order: {e}")
            return {"error": str(e)}

# Bug: Violation of SOLID Principles
class Manager(ABC):
    """
    Base manager class violating Single Responsibility Principle.
    """
    def __init__(self):
        # Bug: Multiple responsibilities
        self.db = self._setup_database()
        self.cache = self._setup_cache()
        self.logger = self._setup_logger()
        self.validator = self._setup_validator()
        self.transformer = self._setup_transformer()
        self.notifier = self._setup_notifier()
        self.metrics = self._setup_metrics()

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Multiple responsibilities
        try:
            # Validate
            if not self.validator.validate(data):
                raise ValueError("Invalid data")

            # Transform
            transformed = self.transformer.transform(data)

            # Save to database
            self._save_to_db(transformed)

            # Update cache
            self._update_cache(transformed)

            # Send notification
            self._send_notification(transformed)

            # Update metrics
            self._update_metrics(transformed)

            return transformed
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {"error": str(e)}

# Bug: Poor Abstraction
class FileManager:
    """
    File manager with leaky abstractions.
    """
    def __init__(self):
        # Bug: Exposed implementation details
        self.file_handle = None
        self.buffer_size = 8192
        self.encoding = 'utf-8'
        self.mode = 'r'
        self.errors = 'strict'
        self.newline = None
        self.closefd = True
        self.opener = None

    def read_file(self, path: str) -> str:
        # Bug: Leaky abstraction
        # Bug: Exposed implementation details
        try:
            with open(path, mode=self.mode, encoding=self.encoding,
                     errors=self.errors, newline=self.newline,
                     closefd=self.closefd, opener=self.opener) as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading file: {e}")

# Bug: God Class
class SystemManager:
    """
    System manager with too many responsibilities (God Class).
    """
    def __init__(self):
        # Bug: Too many responsibilities
        # Bug: Too many features
        # Bug: Too many methods
        self.db = self._setup_database()
        self.cache = self._setup_cache()
        self.logger = self._setup_logger()
        self.validator = self._setup_validator()
        self.transformer = self._setup_transformer()
        self.notifier = self._setup_notifier()
        self.metrics = self._setup_metrics()
        self.scheduler = self._setup_scheduler()
        self.security = self._setup_security()
        self.backup = self._setup_backup()
        self.monitoring = self._setup_monitoring()
        self.reporting = self._setup_reporting()
        self.auditing = self._setup_auditing()
        self.config = self._setup_config()
        self.users = self._setup_users()
        self.orders = self._setup_orders()
        self.products = self._setup_products()
        self.payments = self._setup_payments()
        self.shipping = self._setup_shipping()
        self.notifications = self._setup_notifications()
        self.analytics = self._setup_analytics()
        self.workflow = self._setup_workflow()
        self.tasks = self._setup_tasks()
        self.jobs = self._setup_jobs()
        self.events = self._setup_events()
        self.messages = self._setup_messages()
        self.files = self._setup_files()
        self.network = self._setup_network()
        self.storage = self._setup_storage()
        self.compute = self._setup_compute()
        self.queue = self._setup_queue()
        self.lock = self._setup_lock()
        self.timer = self._setup_timer()
        self.state = self._setup_state()

# Bug: Poor Encapsulation
class UserManager:
    """
    User manager with poor encapsulation.
    """
    def __init__(self):
        # Bug: Exposed internals
        # Bug: Public state
        # Bug: Global state
        self.users = {}  # Public state
        self.active_users = set()  # Public state
        self.user_sessions = {}  # Public state
        self.user_preferences = {}  # Public state
        self.user_roles = {}  # Public state
        self.user_permissions = {}  # Public state
        self.user_activity = []  # Public state
        self.user_metrics = defaultdict(int)  # Public state

    def add_user(self, user_data: Dict[str, Any]) -> str:
        # Bug: Exposed internals
        # Bug: Direct state manipulation
        user_id = str(random.randint(1, 1000000))
        self.users[user_id] = user_data
        self.active_users.add(user_id)
        self.user_sessions[user_id] = []
        self.user_preferences[user_id] = {}
        self.user_roles[user_id] = []
        self.user_permissions[user_id] = set()
        self.user_activity.append({"user_id": user_id, "action": "create", "time": time.time()})
        self.user_metrics["users_created"] += 1
        return user_id

# Bug: Inappropriate Inheritance
class User:
    """
    Base user class with inappropriate inheritance.
    """
    def __init__(self):
        # Bug: Wrong abstraction
        # Bug: Mixed concerns
        self.id = None
        self.name = None
        self.email = None
        self.password = None
        self.role = None
        self.permissions = set()
        self.preferences = {}
        self.sessions = []
        self.activity = []
        self.metrics = defaultdict(int)
        self.notifications = []
        self.orders = []
        self.payments = []
        self.shipping = []
        self.files = []
        self.messages = []
        self.tasks = []
        self.jobs = []
        self.events = []
        self.state = {}

class AdminUser(User):
    """
    Admin user with inappropriate inheritance.
    """
    def __init__(self):
        # Bug: Wrong abstraction
        # Bug: Mixed concerns
        super().__init__()
        self.admin_level = None
        self.admin_permissions = set()
        self.admin_actions = []
        self.admin_audit_log = []
        self.admin_reports = []
        self.admin_tasks = []
        self.admin_jobs = []
        self.admin_events = []
        self.admin_state = {}

# Bug: Poor Interface Design
class DataProcessor:
    """
    Data processor with poor interface design.
    """
    def __init__(self):
        # Bug: Unclear contracts
        # Bug: Mixed interfaces
        # Bug: Inconsistent methods
        self.processors = {}
        self.validators = {}
        self.transformers = {}
        self.storage = {}
        self.cache = {}
        self.state = {}

    def process(self, data: Any, options: Optional[Dict[str, Any]] = None) -> Any:
        # Bug: Unclear contract
        # Bug: Mixed interface
        # Bug: Inconsistent method
        try:
            # Process data
            if isinstance(data, dict):
                return self._process_dict(data, options)
            elif isinstance(data, list):
                return self._process_list(data, options)
            elif isinstance(data, str):
                return self._process_string(data, options)
            elif isinstance(data, (int, float)):
                return self._process_number(data, options)
            else:
                return self._process_other(data, options)
        except Exception as e:
            return {"error": str(e)}

def main():
    """
    Main function to demonstrate design issues.
    """
    print("Code Design Issues Demonstration:")
    print("===============================")

    try:
        # Test MixedManager
        mixed_manager = MixedManager()
        result = mixed_manager.process_data({"id": 1, "value": "test"})
        print(f"MixedManager result: {result}")

        # Test OrderManager
        order_manager = OrderManager()
        result = order_manager.process_order({
            "id": 1,
            "items": ["item1", "item2"],
            "total": 100.0
        })
        print(f"OrderManager result: {result}")

        # Test FileManager
        file_manager = FileManager()
        file_manager.write_file("test.txt", "test content")
        result = file_manager.read_file("test.txt")
        print(f"FileManager result: {result}")

        # Test SystemManager
        system_manager = SystemManager()
        result = system_manager.process_data({"id": 1, "value": "test"})
        print(f"SystemManager result: {result}")

        # Test UserManager
        user_manager = UserManager()
        result = user_manager.add_user({
            "name": "John",
            "email": "john@example.com"
        })
        print(f"UserManager result: {result}")

        # Test User hierarchy
        admin_user = AdminUser()
        admin_user.name = "Admin"
        admin_user.email = "admin@example.com"
        print(f"AdminUser: {admin_user.name}, {admin_user.email}")

        # Test DataProcessor
        data_processor = DataProcessor()
        result = data_processor.process({"id": 1, "value": "test"})
        print(f"DataProcessor result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()