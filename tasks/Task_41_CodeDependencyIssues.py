#!/usr/bin/env python3
"""
Task 41: Code Dependency Issues Challenge

This file contains several intentional dependency issues for code review practice.
The task is to identify and fix the following dependency problems:

1. Circular Dependencies:
   - ServiceA depends on ServiceB, which depends on ServiceA
   - ManagerA depends on ManagerB, which depends on ManagerA
   - ModuleA imports ModuleB, which imports ModuleA

2. Tight Coupling:
   - Direct class dependencies
   - Concrete implementation dependencies
   - Hard-coded dependencies

3. Improper Dependency Management:
   - Missing dependency injection
   - Global state dependencies
   - Static dependencies

4. Hidden Dependencies:
   - Implicit dependencies
   - Side-effect dependencies
   - Runtime dependencies

5. Unnecessary Dependencies:
   - Unused imports
   - Over-importing
   - Redundant dependencies

6. Version Conflicts:
   - Incompatible versions
   - Version mismatches
   - Outdated dependencies

7. Dependency Cycles:
   - Complex dependency graphs
   - Long dependency chains
   - Circular import chains

8. Poor Dependency Design:
   - No dependency interfaces
   - Mixed dependency concerns
   - Unclear dependency boundaries

Review the code and identify these dependency issues.
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

# Bug: Global State Dependencies
DATABASE = sqlite3.connect(":memory:")  # Bug: Global database
CACHE = {}  # Bug: Global cache
LOGGER = logging.getLogger(__name__)  # Bug: Global logger
CONFIG = {}  # Bug: Global config

# Bug: Circular Dependencies
class ServiceA:
    """
    Service A with circular dependency on ServiceB.
    """
    def __init__(self):
        # Bug: Circular dependency
        from .service_b import ServiceB  # Bug: Circular import
        self.service_b = ServiceB()  # Bug: Direct dependency
        self.logger = LOGGER  # Bug: Global dependency

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Circular dependency usage
        try:
            # Process data
            result = self.service_b.process(data)  # Bug: Circular call
            return {"service_a": "processed", "service_b_result": result}
        except Exception as e:
            self.logger.error(f"ServiceA error: {e}")
            return {"error": str(e)}

class ServiceB:
    """
    Service B with circular dependency on ServiceA.
    """
    def __init__(self):
        # Bug: Circular dependency
        from .service_a import ServiceA  # Bug: Circular import
        self.service_a = ServiceA()  # Bug: Direct dependency
        self.logger = LOGGER  # Bug: Global dependency

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Circular dependency usage
        try:
            # Process data
            result = self.service_a.process(data)  # Bug: Circular call
            return {"service_b": "processed", "service_a_result": result}
        except Exception as e:
            self.logger.error(f"ServiceB error: {e}")
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
        self.db = DATABASE  # Bug: Direct database dependency
        self.cache = CACHE  # Bug: Direct cache dependency
        self.logger = LOGGER  # Bug: Direct logger dependency
        self.payment_processor = self._create_payment_processor()  # Bug: Concrete dependency
        self.shipping_service = self._create_shipping_service()  # Bug: Concrete dependency
        self.notification_service = self._create_notification_service()  # Bug: Concrete dependency

    def process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Tight coupling to implementations
        try:
            # Process payment
            payment_result = self.payment_processor.process_payment(order)  # Bug: Direct call

            # Create shipment
            shipping_result = self.shipping_service.create_shipment(order)  # Bug: Direct call

            # Send notification
            self.notification_service.send_notification(order)  # Bug: Direct call

            # Update database
            self.db.execute("INSERT INTO orders VALUES (?)", (json.dumps(order),))  # Bug: Direct call
            self.db.commit()

            return {
                "order": order,
                "payment": payment_result,
                "shipping": shipping_result
            }
        except Exception as e:
            self.logger.error(f"Order processing error: {e}")
            return {"error": str(e)}

# Bug: Improper Dependency Management
class UserManager:
    """
    User manager with improper dependency management.
    """
    def __init__(self):
        # Bug: Missing dependency injection
        # Bug: Global state dependencies
        # Bug: Static dependencies
        self.db = DATABASE  # Bug: Global dependency
        self.cache = CACHE  # Bug: Global dependency
        self.logger = LOGGER  # Bug: Global dependency
        self.config = CONFIG  # Bug: Global dependency
        self.validator = self._create_validator()  # Bug: Static dependency
        self.authenticator = self._create_authenticator()  # Bug: Static dependency
        self.notifier = self._create_notifier()  # Bug: Static dependency

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Improper dependency usage
        try:
            # Validate user data
            if not self.validator.validate(user_data):  # Bug: Direct dependency
                raise ValueError("Invalid user data")

            # Authenticate user
            auth_result = self.authenticator.authenticate(user_data)  # Bug: Direct dependency

            # Create user
            user_id = str(random.randint(1, 1000000))
            self.db.execute("INSERT INTO users VALUES (?, ?)", (user_id, json.dumps(user_data)))  # Bug: Direct dependency
            self.db.commit()

            # Cache user
            self.cache[user_id] = user_data  # Bug: Direct dependency

            # Notify
            self.notifier.notify_user_created(user_id)  # Bug: Direct dependency

            return {"user_id": user_id, "auth": auth_result}
        except Exception as e:
            self.logger.error(f"User creation error: {e}")  # Bug: Direct dependency
            return {"error": str(e)}

# Bug: Hidden Dependencies
class ProcessManager:
    """
    Process manager with hidden dependencies.
    """
    def __init__(self):
        # Bug: Implicit dependencies
        # Bug: Side-effect dependencies
        # Bug: Runtime dependencies
        self.processes = {}
        self.state = {}
        self.logger = LOGGER  # Bug: Hidden dependency

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Hidden dependencies
        try:
            # Implicit dependency on global state
            if data.get("use_cache", False):
                cached = CACHE.get(data["id"])  # Bug: Hidden dependency
                if cached:
                    return cached

            # Side-effect dependency
            self._update_metrics(data)  # Bug: Hidden dependency on metrics

            # Runtime dependency
            if hasattr(data, "process"):  # Bug: Runtime dependency
                return data.process()

            # Process data
            result = self._process(data)

            # Hidden dependency on global state
            CACHE[data["id"]] = result  # Bug: Hidden dependency

            return result
        except Exception as e:
            self.logger.error(f"Processing error: {e}")  # Bug: Hidden dependency
            return {"error": str(e)}

# Bug: Unnecessary Dependencies
class DataManager:
    """
    Data manager with unnecessary dependencies.
    """
    def __init__(self):
        # Bug: Unused imports
        # Bug: Over-importing
        # Bug: Redundant dependencies
        import psycopg2  # Bug: Unused import
        import requests  # Bug: Unused import
        import threading  # Bug: Unused import
        import traceback  # Bug: Unused import
        from datetime import datetime, timedelta  # Bug: Over-importing
        from collections import defaultdict, OrderedDict  # Bug: Over-importing

        self.db = DATABASE  # Bug: Redundant dependency
        self.cache = CACHE  # Bug: Redundant dependency
        self.logger = LOGGER  # Bug: Redundant dependency

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Unnecessary dependency usage
        try:
            # Process data
            result = self._process(data)

            # Unnecessary database access
            self.db.execute("SELECT 1")  # Bug: Unnecessary dependency

            # Unnecessary cache access
            self.cache.get("unused")  # Bug: Unnecessary dependency

            return result
        except Exception as e:
            self.logger.error(f"Data processing error: {e}")  # Bug: Unnecessary dependency
            return {"error": str(e)}

# Bug: Dependency Cycles
class ManagerA:
    """
    Manager A with dependency cycle.
    """
    def __init__(self):
        # Bug: Complex dependency graph
        # Bug: Long dependency chain
        # Bug: Circular import chain
        from .manager_b import ManagerB  # Bug: Circular import
        from .manager_c import ManagerC  # Bug: Circular import
        from .manager_d import ManagerD  # Bug: Circular import

        self.manager_b = ManagerB()  # Bug: Dependency chain
        self.manager_c = ManagerC()  # Bug: Dependency chain
        self.manager_d = ManagerD()  # Bug: Dependency chain
        self.logger = LOGGER  # Bug: Global dependency

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Dependency cycle usage
        try:
            # Process through dependency chain
            result_b = self.manager_b.process(data)  # Bug: Chain dependency
            result_c = self.manager_c.process(result_b)  # Bug: Chain dependency
            result_d = self.manager_d.process(result_c)  # Bug: Chain dependency

            return {
                "manager_a": "processed",
                "manager_b_result": result_b,
                "manager_c_result": result_c,
                "manager_d_result": result_d
            }
        except Exception as e:
            self.logger.error(f"ManagerA error: {e}")
            return {"error": str(e)}

# Bug: Poor Dependency Design
class ServiceManager:
    """
    Service manager with poor dependency design.
    """
    def __init__(self):
        # Bug: No dependency interfaces
        # Bug: Mixed dependency concerns
        # Bug: Unclear dependency boundaries
        self.services = {}
        self.dependencies = {}
        self.state = {}
        self.logger = LOGGER  # Bug: Global dependency

    def register_service(self, name: str, service: Any) -> None:
        # Bug: Poor dependency design
        # No interface enforcement
        # Mixed concerns
        # Unclear boundaries
        self.services[name] = service
        self.dependencies[name] = set()
        self.state[name] = {}

    def process_request(self, service_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Poor dependency usage
        try:
            service = self.services.get(service_name)
            if not service:
                raise ValueError(f"Service {service_name} not found")

            # Direct service calls
            # No interface enforcement
            # Mixed concerns
            result = service.process(request)

            # Update dependencies
            for dep in self.dependencies[service_name]:
                dep_service = self.services.get(dep)
                if dep_service:
                    dep_service.update(result)

            return result
        except Exception as e:
            self.logger.error(f"Service processing error: {e}")
            return {"error": str(e)}

def main():
    """
    Main function to demonstrate dependency issues.
    """
    print("Code Dependency Issues Demonstration:")
    print("===================================")

    try:
        # Test ServiceA/ServiceB circular dependency
        service_a = ServiceA()
        result = service_a.process({"id": 1, "value": "test"})
        print(f"ServiceA result: {result}")

        # Test OrderManager tight coupling
        order_manager = OrderManager()
        result = order_manager.process_order({
            "id": 1,
            "items": ["item1", "item2"],
            "total": 100.0
        })
        print(f"OrderManager result: {result}")

        # Test UserManager improper dependency management
        user_manager = UserManager()
        result = user_manager.create_user({
            "name": "John",
            "email": "john@example.com"
        })
        print(f"UserManager result: {result}")

        # Test ProcessManager hidden dependencies
        process_manager = ProcessManager()
        result = process_manager.process_data({
            "id": 1,
            "value": "test",
            "use_cache": True
        })
        print(f"ProcessManager result: {result}")

        # Test DataManager unnecessary dependencies
        data_manager = DataManager()
        result = data_manager.process_data({"id": 1, "value": "test"})
        print(f"DataManager result: {result}")

        # Test ManagerA dependency cycles
        manager_a = ManagerA()
        result = manager_a.process({"id": 1, "value": "test"})
        print(f"ManagerA result: {result}")

        # Test ServiceManager poor dependency design
        service_manager = ServiceManager()
        service_manager.register_service("test", lambda x: {"processed": x})
        result = service_manager.process_request("test", {"data": "test"})
        print(f"ServiceManager result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()