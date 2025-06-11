#!/usr/bin/env python3
"""
Task 40: Code Architecture Issues Challenge

This file contains several intentional architectural issues for code review practice.
The task is to identify and fix the following architectural problems:

1. Monolithic Design:
   - System: tightly coupled components
   - Database: shared database
   - Services: no service boundaries

2. Improper Layering:
   - BusinessLogic: mixed with data access
   - Presentation: mixed with business logic
   - DataAccess: mixed with business rules

3. Poor System Organization:
   - Circular dependencies
   - Unclear module boundaries
   - Mixed responsibilities

4. Inappropriate Coupling:
   - Direct database access
   - Hard-coded dependencies
   - Global state usage

5. Poor Service Design:
   - No service boundaries
   - Mixed service responsibilities
   - No service isolation

6. Inefficient Data Flow:
   - Unnecessary data transformations
   - Redundant data passing
   - Poor data locality

7. Poor Component Design:
   - No clear interfaces
   - Mixed component responsibilities
   - No component isolation

8. Architectural Violations:
   - Cross-layer dependencies
   - Bypassed abstractions
   - Violated design patterns

Review the code and identify these architectural issues.
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

# Global state (Bug: Poor System Organization)
DATABASE = sqlite3.connect(":memory:")  # Bug: Shared database
CACHE = {}  # Bug: Global cache
LOGGER = logging.getLogger(__name__)  # Bug: Global logger
CONFIG = {}  # Bug: Global config
USERS = {}  # Bug: Global users
ORDERS = {}  # Bug: Global orders
PRODUCTS = {}  # Bug: Global products

# Bug: Monolithic Design
class MonolithicSystem:
    """
    Monolithic system with tightly coupled components.
    """
    def __init__(self):
        # Bug: Tight coupling
        # Bug: No service boundaries
        # Bug: Mixed responsibilities
        self.db = DATABASE  # Bug: Direct database access
        self.cache = CACHE  # Bug: Global state
        self.logger = LOGGER  # Bug: Global logger
        self.config = CONFIG  # Bug: Global config
        self.users = USERS  # Bug: Global state
        self.orders = ORDERS  # Bug: Global state
        self.products = PRODUCTS  # Bug: Global state

        # Bug: Mixed service responsibilities
        self.auth_service = self._setup_auth_service()
        self.order_service = self._setup_order_service()
        self.payment_service = self._setup_payment_service()
        self.shipping_service = self._setup_shipping_service()
        self.notification_service = self._setup_notification_service()
        self.reporting_service = self._setup_reporting_service()
        self.analytics_service = self._setup_analytics_service()

    def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed responsibilities
        # Bug: No service boundaries
        # Bug: Direct database access
        try:
            # Validate user
            user = self.auth_service.validate_user(order_data["user_id"])
            if not user:
                raise ValueError("Invalid user")

            # Process order
            order = self.order_service.create_order(order_data)

            # Process payment
            payment = self.payment_service.process_payment(order)

            # Create shipment
            shipment = self.shipping_service.create_shipment(order)

            # Send notification
            self.notification_service.send_order_confirmation(order)

            # Generate report
            report = self.reporting_service.generate_order_report(order)

            # Update analytics
            self.analytics_service.track_order(order)

            # Update database directly
            self.db.execute("INSERT INTO orders VALUES (?)", (json.dumps(order),))
            self.db.commit()

            return {
                "order": order,
                "payment": payment,
                "shipment": shipment,
                "report": report
            }
        except Exception as e:
            self.logger.error(f"Error processing order: {e}")
            return {"error": str(e)}

# Bug: Improper Layering
class BusinessLogic:
    """
    Business logic with improper layering.
    """
    def __init__(self):
        # Bug: Mixed with data access
        # Bug: Mixed with presentation
        # Bug: Direct database access
        self.db = DATABASE  # Bug: Direct database access
        self.cache = CACHE  # Bug: Global state
        self.logger = LOGGER  # Bug: Global logger

    def calculate_order_total(self, order_id: str) -> float:
        # Bug: Mixed responsibilities
        # Bug: Direct database access
        # Bug: Business logic mixed with data access
        try:
            # Direct database query
            cursor = self.db.execute(
                "SELECT * FROM orders WHERE id = ?",
                (order_id,)
            )
            order = cursor.fetchone()

            if not order:
                raise ValueError("Order not found")

            # Business logic mixed with data access
            total = 0.0
            for item in json.loads(order[0])["items"]:
                # Direct database query in business logic
                cursor = self.db.execute(
                    "SELECT price FROM products WHERE id = ?",
                    (item["product_id"],)
                )
                product = cursor.fetchone()
                if product:
                    total += product[0] * item["quantity"]

            # Business logic mixed with presentation
            if total > 1000:
                print("Large order detected!")  # Bug: Presentation in business logic

            return total
        except Exception as e:
            self.logger.error(f"Error calculating total: {e}")
            return 0.0

# Bug: Poor Service Design
class ServiceManager:
    """
    Service manager with poor service design.
    """
    def __init__(self):
        # Bug: No service boundaries
        # Bug: Mixed service responsibilities
        # Bug: No service isolation
        self.services = {}
        self.state = {}
        self.dependencies = {}
        self.config = {}
        self.logger = LOGGER  # Bug: Global logger

    def register_service(self, name: str, service: Any) -> None:
        # Bug: No service boundaries
        # Bug: Mixed service responsibilities
        self.services[name] = service
        self.state[name] = {}
        self.dependencies[name] = set()
        self.config[name] = {}

    def process_request(self, service_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: No service isolation
        # Bug: Mixed service responsibilities
        try:
            service = self.services.get(service_name)
            if not service:
                raise ValueError(f"Service {service_name} not found")

            # No service boundaries
            # Direct service communication
            result = service.process(request)

            # Update service state
            self.state[service_name].update(result)

            # Update dependencies
            for dep in self.dependencies[service_name]:
                dep_service = self.services.get(dep)
                if dep_service:
                    dep_service.update(result)

            return result
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {"error": str(e)}

# Bug: Inefficient Data Flow
class DataFlowManager:
    """
    Data flow manager with inefficient data flow.
    """
    def __init__(self):
        # Bug: Unnecessary transformations
        # Bug: Redundant data passing
        # Bug: Poor data locality
        self.transformers = {}
        self.validators = {}
        self.storage = {}
        self.cache = CACHE  # Bug: Global state
        self.logger = LOGGER  # Bug: Global logger

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Inefficient data flow
        try:
            # Unnecessary transformations
            transformed = self._transform_data(data)
            validated = self._validate_data(transformed)
            normalized = self._normalize_data(validated)
            enriched = self._enrich_data(normalized)
            formatted = self._format_data(enriched)

            # Redundant data passing
            self._store_data(formatted)
            self._cache_data(formatted)
            self._log_data(formatted)
            self._notify_data(formatted)

            # Poor data locality
            return {
                "original": data,
                "transformed": transformed,
                "validated": validated,
                "normalized": normalized,
                "enriched": enriched,
                "formatted": formatted
            }
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            return {"error": str(e)}

# Bug: Poor Component Design
class ComponentManager:
    """
    Component manager with poor component design.
    """
    def __init__(self):
        # Bug: No clear interfaces
        # Bug: Mixed component responsibilities
        # Bug: No component isolation
        self.components = {}
        self.dependencies = {}
        self.state = {}
        self.config = {}
        self.logger = LOGGER  # Bug: Global logger

    def register_component(self, name: str, component: Any) -> None:
        # Bug: No component isolation
        # Bug: Mixed component responsibilities
        self.components[name] = component
        self.dependencies[name] = set()
        self.state[name] = {}
        self.config[name] = {}

    def process_component(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: No clear interfaces
        # Bug: Mixed component responsibilities
        try:
            component = self.components.get(name)
            if not component:
                raise ValueError(f"Component {name} not found")

            # Direct component communication
            # No component isolation
            result = component.process(data)

            # Update component state
            self.state[name].update(result)

            # Update dependencies
            for dep in self.dependencies[name]:
                dep_component = self.components.get(dep)
                if dep_component:
                    dep_component.update(result)

            return result
        except Exception as e:
            self.logger.error(f"Error processing component: {e}")
            return {"error": str(e)}

# Bug: Architectural Violations
class SystemArchitecture:
    """
    System architecture with architectural violations.
    """
    def __init__(self):
        # Bug: Cross-layer dependencies
        # Bug: Bypassed abstractions
        # Bug: Violated design patterns
        self.presentation = self._setup_presentation()
        self.business = self._setup_business()
        self.data = self._setup_data()
        self.logger = LOGGER  # Bug: Global logger

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Architectural violations
        try:
            # Cross-layer dependencies
            # Presentation directly accessing data layer
            data = self.data.get_data(request["id"])

            # Business logic in presentation layer
            if data["status"] == "error":
                print("Error detected!")  # Bug: Presentation in business logic

            # Bypassed abstractions
            # Direct database access in presentation layer
            self.data.db.execute(
                "UPDATE requests SET status = ? WHERE id = ?",
                ("processed", request["id"])
            )

            # Violated design patterns
            # Singleton pattern violation
            global DATABASE
            DATABASE.execute(
                "INSERT INTO logs VALUES (?)",
                (json.dumps(request),)
            )

            return {
                "request": request,
                "data": data,
                "status": "processed"
            }
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {"error": str(e)}

def main():
    """
    Main function to demonstrate architectural issues.
    """
    print("Code Architecture Issues Demonstration:")
    print("=====================================")

    try:
        # Test MonolithicSystem
        system = MonolithicSystem()
        result = system.process_order({
            "user_id": "user1",
            "items": [{"product_id": "prod1", "quantity": 2}]
        })
        print(f"MonolithicSystem result: {result}")

        # Test BusinessLogic
        business = BusinessLogic()
        result = business.calculate_order_total("order1")
        print(f"BusinessLogic result: {result}")

        # Test ServiceManager
        service_manager = ServiceManager()
        service_manager.register_service("test", lambda x: {"processed": x})
        result = service_manager.process_request("test", {"data": "test"})
        print(f"ServiceManager result: {result}")

        # Test DataFlowManager
        data_flow = DataFlowManager()
        result = data_flow.process_data({"id": 1, "value": "test"})
        print(f"DataFlowManager result: {result}")

        # Test ComponentManager
        component_manager = ComponentManager()
        component_manager.register_component("test", lambda x: {"processed": x})
        result = component_manager.process_component("test", {"data": "test"})
        print(f"ComponentManager result: {result}")

        # Test SystemArchitecture
        architecture = SystemArchitecture()
        result = architecture.process_request({"id": "req1", "data": "test"})
        print(f"SystemArchitecture result: {result}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()