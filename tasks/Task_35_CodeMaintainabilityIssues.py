 #!/usr/bin/env python3
"""
Task 35: Code Maintainability Issues Challenge

This file contains several intentional maintainability issues for code review practice.
The task is to identify and fix the following maintainability problems:

1. Poor Code Organization:
   - MixedManager: mixed responsibilities
   - DataManager: unclear boundaries
   - ServiceManager: poor module structure

2. Unclear Naming:
   - Processor: vague names
   - Manager: ambiguous terms
   - Handler: unclear purpose

3. Tight Coupling:
   - ServiceManager: direct dependencies
   - DataManager: concrete implementations
   - ProcessManager: hard-coded dependencies

4. Poor Documentation:
   - UserManager: missing docstrings
   - DataProcessor: unclear parameters
   - ConfigManager: outdated comments

5. Code Duplication:
   - ValidationManager: repeated logic
   - ProcessManager: similar methods
   - DataManager: copied code

6. Complex Logic:
   - BusinessLogic: hard to follow
   - StateManager: complex state
   - WorkflowManager: unclear flow

7. Poor Error Handling:
   - DataManager: generic exceptions
   - ProcessManager: swallowed errors
   - ServiceManager: unclear error states

8. Testing Difficulties:
   - ServiceManager: untestable code
   - DataManager: hidden dependencies
   - ProcessManager: global state

Review the code and identify these maintainability issues.
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

# Bug: Poor Code Organization
class MixedManager:
    """
    Manager with mixed responsibilities and poor organization.
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

# Bug: Unclear Naming
class Processor:
    """
    Processor with unclear naming and purpose.
    """
    def __init__(self):
        # Bug: Unclear variable names
        self.x = {}  # What is x?
        self.y = []  # What is y?
        self.z = 0   # What is z?
        self.a = None  # What is a?
        self.b = False  # What is b?

    def do_something(self, thing: Any) -> Any:
        # Bug: Unclear method name
        # Bug: Unclear parameter name
        # Bug: Unclear return value
        if self.b:
            self.x[thing] = self.y
            self.z += 1
            return self.a
        return None

    def handle_stuff(self, stuff: List[Any]) -> None:
        # Bug: Unclear method name
        # Bug: Unclear parameter name
        for item in stuff:
            self.process_item(item)  # What does this do?

    def process_item(self, item: Any) -> None:
        # Bug: Unclear method name
        # Bug: Unclear parameter name
        if isinstance(item, dict):
            self.update_thing(item)  # What thing?
        elif isinstance(item, list):
            self.modify_stuff(item)  # What stuff?

# Bug: Tight Coupling
class ServiceManager:
    """
    Service manager with tight coupling.
    """
    def __init__(self):
        # Bug: Direct dependencies
        self.db = sqlite3.connect(":memory:")  # Concrete implementation
        self.cache = {}  # Concrete implementation
        self.logger = logging.getLogger(__name__)  # Concrete implementation
        self.http_client = requests.Session()  # Concrete implementation
        self.email_sender = self._create_email_sender()  # Concrete implementation
        self.file_system = self._create_file_system()  # Concrete implementation
        self.validator = self._create_validator()  # Concrete implementation
        self.transformer = self._create_transformer()  # Concrete implementation

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Tightly coupled operations
        try:
            # Validate request
            if not self.validator.validate(request):
                raise ValueError("Invalid request")

            # Transform request
            transformed = self.transformer.transform(request)

            # Save to database
            self.db.execute("INSERT INTO requests VALUES (?)", (json.dumps(transformed),))
            self.db.commit()

            # Update cache
            self.cache[request["id"]] = transformed

            # Send email
            self.email_sender.send(transformed)

            # Save to file
            self.file_system.save(transformed)

            # Log operation
            self.logger.info(f"Processed request: {transformed}")

            return transformed
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {"error": str(e)}

# Bug: Poor Documentation
class UserManager:
    """
    User manager with poor documentation.
    """
    def __init__(self):
        self.users = {}

    def add_user(self, user_data: Dict[str, Any]) -> str:
        # Bug: Missing parameter documentation
        # Bug: Missing return value documentation
        # Bug: Missing exception documentation
        user_id = str(random.randint(1, 1000000))
        self.users[user_id] = user_data
        return user_id

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        # Bug: Missing parameter documentation
        # Bug: Missing return value documentation
        # Bug: Missing exception documentation
        if user_id in self.users:
            self.users[user_id].update(updates)
            return True
        return False

    def delete_user(self, user_id: str) -> None:
        # Bug: Missing parameter documentation
        # Bug: Missing exception documentation
        # Bug: Missing side effects documentation
        if user_id in self.users:
            del self.users[user_id]

# Bug: Code Duplication
class ValidationManager:
    """
    Validation manager with code duplication.
    """
    def validate_user(self, user_data: Dict[str, Any]) -> bool:
        # Bug: Duplicate validation logic
        try:
            if not user_data:
                return False

            if "name" not in user_data:
                return False

            if "email" not in user_data:
                return False

            if "age" not in user_data:
                return False

            if not isinstance(user_data["age"], int):
                return False

            if user_data["age"] < 0:
                return False

            return True
        except Exception:
            return False

    def validate_order(self, order_data: Dict[str, Any]) -> bool:
        # Bug: Similar validation logic
        try:
            if not order_data:
                return False

            if "user_id" not in order_data:
                return False

            if "items" not in order_data:
                return False

            if "total" not in order_data:
                return False

            if not isinstance(order_data["total"], (int, float)):
                return False

            if order_data["total"] < 0:
                return False

            return True
        except Exception:
            return False

# Bug: Complex Logic
class BusinessLogic:
    """
    Business logic with complex, hard-to-follow code.
    """
    def __init__(self):
        self.state = {}
        self.history = []
        self.rules = {}
        self.exceptions = {}
        self.overrides = {}
        self.dependencies = {}
        self.calculations = {}
        self.validations = {}
        self.transformations = {}

    def process_business_logic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Complex, hard-to-follow logic
        try:
            # Update state
            self._update_state(data)

            # Apply rules
            if self._should_apply_rules(data):
                data = self._apply_rules(data)

            # Handle exceptions
            if self._has_exceptions(data):
                data = self._handle_exceptions(data)

            # Apply overrides
            if self._has_overrides(data):
                data = self._apply_overrides(data)

            # Check dependencies
            if self._check_dependencies(data):
                data = self._process_dependencies(data)

            # Perform calculations
            if self._needs_calculation(data):
                data = self._perform_calculations(data)

            # Validate results
            if self._needs_validation(data):
                data = self._validate_results(data)

            # Transform data
            if self._needs_transformation(data):
                data = self._transform_data(data)

            # Update history
            self._update_history(data)

            return data
        except Exception as e:
            return self._handle_error(e)

# Bug: Poor Error Handling
class DataManager:
    """
    Data manager with poor error handling.
    """
    def __init__(self):
        self.data = {}

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Generic exception handling
        try:
            # Bug: Swallowed exceptions
            try:
                self._validate_data(data)
            except:
                pass

            # Bug: Generic exception
            try:
                self._transform_data(data)
            except Exception as e:
                print(f"Error: {e}")

            # Bug: Unclear error state
            try:
                self._save_data(data)
            except:
                return {"status": "error"}

            return data
        except:
            return {"status": "error"}

    def _validate_data(self, data: Dict[str, Any]) -> None:
        # Bug: Generic exception
        if not data:
            raise Exception("Invalid data")

    def _transform_data(self, data: Dict[str, Any]) -> None:
        # Bug: Generic exception
        if "value" not in data:
            raise Exception("Missing value")

    def _save_data(self, data: Dict[str, Any]) -> None:
        # Bug: Generic exception
        if "id" not in data:
            raise Exception("Missing id")

# Bug: Testing Difficulties
class ProcessManager:
    """
    Process manager with testing difficulties.
    """
    def __init__(self):
        # Bug: Global state
        global PROCESS_STATE
        PROCESS_STATE = {}

        # Bug: Hidden dependencies
        self.db = self._get_database()
        self.cache = self._get_cache()
        self.logger = self._get_logger()

        # Bug: Hard-coded values
        self.timeout = 30
        self.max_retries = 3
        self.batch_size = 100

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Untestable code
        # Bug: Global state usage
        # Bug: Hidden dependencies
        try:
            # Update global state
            PROCESS_STATE["processing"] = True

            # Use hidden dependencies
            self.db.execute("INSERT INTO data VALUES (?)", (json.dumps(data),))
            self.cache[data["id"]] = data
            self.logger.info(f"Processing data: {data}")

            # Use hard-coded values
            time.sleep(self.timeout)

            # Update global state
            PROCESS_STATE["processed"] = True

            return data
        except Exception as e:
            # Bug: Global state in error handling
            PROCESS_STATE["error"] = str(e)
            raise

def main():
    """
    Main function to demonstrate maintainability issues.
    """
    print("Code Maintainability Issues Demonstration:")
    print("========================================")

    try:
        # Test MixedManager
        mixed_manager = MixedManager()
        result = mixed_manager.process_data({"id": 1, "value": "test"})
        print(f"MixedManager result: {result}")

        # Test Processor
        processor = Processor()
        result = processor.do_something({"key": "value"})
        print(f"Processor result: {result}")

        # Test ServiceManager
        service_manager = ServiceManager()
        result = service_manager.process_request({"id": 1, "data": "test"})
        print(f"ServiceManager result: {result}")

        # Test UserManager
        user_manager = UserManager()
        result = user_manager.add_user({"name": "John", "email": "john@example.com"})
        print(f"UserManager result: {result}")

        # Test ValidationManager
        validation_manager = ValidationManager()
        result = validation_manager.validate_user({"name": "John", "email": "john@example.com", "age": 30})
        print(f"ValidationManager result: {result}")

        # Test BusinessLogic
        business_logic = BusinessLogic()
        result = business_logic.process_business_logic({"id": 1, "value": 100})
        print(f"BusinessLogic result: {result}")

        # Test DataManager
        data_manager = DataManager()
        result = data_manager.process_data({"id": 1, "value": "test"})
        print(f"DataManager result: {result}")

        # Test ProcessManager
        process_manager = ProcessManager()
        result = process_manager.process_data({"id": 1, "value": "test"})
        print(f"ProcessManager result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()