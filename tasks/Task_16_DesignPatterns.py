#!/usr/bin/env python3
"""
Task 16: Design Pattern Misuse Challenge

This file contains several intentional design pattern misuse issues for code review practice.
The task is to identify and fix the following issues:
1. Singleton Pattern Misuse in DatabaseConnection
2. Factory Pattern Misuse in ObjectCreator
3. Observer Pattern Misuse in EventSystem
4. Strategy Pattern Misuse in PaymentProcessor
5. Decorator Pattern Misuse in Logger
6. Command Pattern Misuse in TaskManager
7. Adapter Pattern Misuse in DataConverter
8. Template Method Pattern Misuse in ReportGenerator

Review the code and identify these design pattern misuse issues.
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple, Callable
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

# Bug: Singleton Pattern Misuse - global state and improper initialization
class DatabaseConnection:
    """
    Misused Singleton pattern for database connection.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        # Bug: Improper singleton implementation - no thread safety
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Bug: Improper initialization - multiple initialization possible
        if not self._initialized:
            self.connection = None
            self._initialized = True

    def connect(self, database: str):
        # Bug: Global state - connection shared across all instances
        self.connection = sqlite3.connect(database)
        return self.connection

    def execute(self, query: str, params: tuple = ()) -> Any:
        # Bug: No connection state management
        if not self.connection:
            raise RuntimeError("Not connected to database")
        return self.connection.execute(query, params)

    def close(self):
        # Bug: Improper resource management
        if self.connection:
            self.connection.close()
            self.connection = None

# Bug: Factory Pattern Misuse - mixed responsibilities and poor abstraction
class ObjectCreator:
    """
    Misused Factory pattern for object creation.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - factory knows too much
        self.creators = {
            'user': self._create_user,
            'order': self._create_order,
            'product': self._create_product,
            'payment': self._create_payment
        }
        self.validators = {
            'user': self._validate_user,
            'order': self._validate_order,
            'product': self._validate_product,
            'payment': self._validate_payment
        }
        self.db = DatabaseConnection()

    def create_object(self, object_type: str, data: Dict[str, Any]) -> Any:
        # Bug: Mixed responsibilities - validation, creation, and persistence
        if object_type not in self.creators:
            raise ValueError(f"Unknown object type: {object_type}")

        if not self.validators[object_type](data):
            raise ValueError(f"Invalid {object_type} data")

        obj = self.creators[object_type](data)
        self._save_object(object_type, obj)
        return obj

    def _create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed creation and business logic
        return {
            'id': str(random.randint(1000, 9999)),
            'name': data['name'],
            'email': data['email'],
            'created_at': datetime.now().isoformat()
        }

    def _create_order(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed creation and business logic
        return {
            'id': f"ORD-{random.randint(100000, 999999)}",
            'user_id': data['user_id'],
            'items': data['items'],
            'total': sum(item['price'] * item['quantity']
                        for item in data['items']),
            'created_at': datetime.now().isoformat()
        }

    def _validate_user(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed validation and business rules
        return ('name' in data and 'email' in data and
                '@' in data['email'])

    def _validate_order(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed validation and business rules
        return ('user_id' in data and 'items' in data and
                len(data['items']) > 0)

    def _save_object(self, object_type: str, obj: Dict[str, Any]) -> None:
        # Bug: Mixed persistence and business logic
        table = f"{object_type}s"
        columns = ', '.join(obj.keys())
        placeholders = ', '.join(['?' for _ in obj])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.db.execute(query, tuple(obj.values()))

# Bug: Observer Pattern Misuse - tight coupling and improper event handling
class EventSystem:
    """
    Misused Observer pattern for event handling.
    """
    def __init__(self):
        # Bug: Tight coupling - direct references to observers
        self.observers = {
            'user_created': [],
            'order_placed': [],
            'payment_received': []
        }
        self.db = DatabaseConnection()
        self.notification_system = NotificationSystem()

    def subscribe(self, event_type: str, observer: Callable) -> None:
        # Bug: No observer management - can't unsubscribe
        if event_type not in self.observers:
            raise ValueError(f"Unknown event type: {event_type}")
        self.observers[event_type].append(observer)

    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        # Bug: Mixed event handling and business logic
        if event_type not in self.observers:
            raise ValueError(f"Unknown event type: {event_type}")

        # Bug: Synchronous notification - blocks event processing
        for observer in self.observers[event_type]:
            try:
                observer(data)
            except Exception as e:
                logger.error(f"Error in observer: {e}")

        # Bug: Mixed event handling and persistence
        self._save_event(event_type, data)

        # Bug: Mixed event handling and notifications
        if event_type == 'order_placed':
            self.notification_system.send_notification(
                data['user_id'],
                'order_confirmation',
                {'order_id': data['order_id']},
                ['email']
            )

    def _save_event(self, event_type: str, data: Dict[str, Any]) -> None:
        # Bug: Mixed event handling and persistence
        event = {
            'type': event_type,
            'data': json.dumps(data),
            'timestamp': datetime.now().isoformat()
        }
        self.db.execute(
            'INSERT INTO events (type, data, timestamp) VALUES (?, ?, ?)',
            (event['type'], event['data'], event['timestamp'])
        )

# Bug: Strategy Pattern Misuse - mixed strategies and poor abstraction
class PaymentProcessor:
    """
    Misused Strategy pattern for payment processing.
    """
    def __init__(self):
        # Bug: Mixed strategies - payment methods know too much
        self.strategies = {
            'credit_card': self._process_credit_card,
            'paypal': self._process_paypal,
            'bank_transfer': self._process_bank_transfer
        }
        self.db = DatabaseConnection()
        self.notification_system = NotificationSystem()

    def process_payment(self, amount: float, currency: str,
                       method: str) -> Dict[str, Any]:
        # Bug: Mixed strategy selection and business logic
        if method not in self.strategies:
            raise ValueError(f"Unknown payment method: {method}")

        strategy = self.strategies[method]
        result = strategy(amount, currency)

        # Bug: Mixed strategy and persistence
        self._save_payment(result)

        # Bug: Mixed strategy and notification
        if result['status'] == 'completed':
            self.notification_system.send_notification(
                result['user_id'],
                'payment_received',
                {'amount': amount, 'currency': currency},
                ['email']
            )

        return result

    def _process_credit_card(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Mixed strategy and business logic
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'credit_card',
            'transaction_id': f"CC-{random.randint(100000, 999999)}",
            'timestamp': datetime.now().isoformat()
        }

    def _process_paypal(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Mixed strategy and business logic
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'paypal',
            'transaction_id': f"PP-{random.randint(100000, 999999)}",
            'timestamp': datetime.now().isoformat()
        }

    def _process_bank_transfer(self, amount: float, currency: str) -> Dict[str, Any]:
        # Bug: Mixed strategy and business logic
        return {
            'status': 'completed',
            'amount': amount,
            'currency': currency,
            'method': 'bank_transfer',
            'transaction_id': f"BT-{random.randint(100000, 999999)}",
            'timestamp': datetime.now().isoformat()
        }

    def _save_payment(self, payment: Dict[str, Any]) -> None:
        # Bug: Mixed strategy and persistence
        self.db.execute(
            'INSERT INTO payments (transaction_id, amount, currency, method, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
            (payment['transaction_id'], payment['amount'],
             payment['currency'], payment['method'],
             payment['status'], payment['timestamp'])
        )

# Bug: Decorator Pattern Misuse - mixed responsibilities and poor composition
class Logger:
    """
    Misused Decorator pattern for logging.
    """
    def __init__(self):
        # Bug: Mixed responsibilities - logging and business logic
        self.loggers = {
            'file': self._log_to_file,
            'database': self._log_to_database,
            'email': self._log_to_email
        }
        self.db = DatabaseConnection()

    def log(self, level: str, message: str,
            destinations: List[str]) -> None:
        # Bug: Mixed logging and business logic
        for destination in destinations:
            if destination not in self.loggers:
                raise ValueError(f"Unknown destination: {destination}")

            logger = self.loggers[destination]
            try:
                logger(level, message)
            except Exception as e:
                print(f"Error logging to {destination}: {e}")

        # Bug: Mixed logging and persistence
        self._save_log(level, message)

    def _log_to_file(self, level: str, message: str) -> None:
        # Bug: Mixed logging and file handling
        with open('app.log', 'a') as f:
            f.write(f"{datetime.now()} [{level}] {message}\n")

    def _log_to_database(self, level: str, message: str) -> None:
        # Bug: Mixed logging and database operations
        self.db.execute(
            'INSERT INTO logs (level, message, timestamp) VALUES (?, ?, ?)',
            (level, message, datetime.now().isoformat())
        )

    def _log_to_email(self, level: str, message: str) -> None:
        # Bug: Mixed logging and email sending
        if level == 'ERROR':
            # Simulate email sending
            print(f"Sending error email: {message}")

    def _save_log(self, level: str, message: str) -> None:
        # Bug: Mixed logging and persistence
        self.db.execute(
            'INSERT INTO log_history (level, message, timestamp) VALUES (?, ?, ?)',
            (level, message, datetime.now().isoformat())
        )

# Bug: Command Pattern Misuse - mixed commands and poor encapsulation
class TaskManager:
    """
    Misused Command pattern for task management.
    """
    def __init__(self):
        # Bug: Mixed commands - commands know too much
        self.commands = {
            'create_user': self._create_user_command,
            'update_order': self._update_order_command,
            'process_payment': self._process_payment_command
        }
        self.db = DatabaseConnection()
        self.notification_system = NotificationSystem()

    def execute_command(self, command: str, data: Dict[str, Any]) -> Any:
        # Bug: Mixed command execution and business logic
        if command not in self.commands:
            raise ValueError(f"Unknown command: {command}")

        cmd = self.commands[command]
        result = cmd(data)

        # Bug: Mixed command and persistence
        self._save_command(command, data, result)

        # Bug: Mixed command and notification
        if command == 'create_user':
            self.notification_system.send_notification(
                result['id'],
                'welcome',
                {'name': result['name']},
                ['email']
            )

        return result

    def _create_user_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed command and business logic
        user = {
            'id': str(random.randint(1000, 9999)),
            'name': data['name'],
            'email': data['email'],
            'created_at': datetime.now().isoformat()
        }
        self.db.execute(
            'INSERT INTO users (id, name, email, created_at) VALUES (?, ?, ?, ?)',
            (user['id'], user['name'], user['email'], user['created_at'])
        )
        return user

    def _update_order_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed command and business logic
        # Implementation needed
        raise NotImplementedError("Command not implemented")

    def _process_payment_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed command and business logic
        # Implementation needed
        raise NotImplementedError("Command not implemented")

    def _save_command(self, command: str, data: Dict[str, Any],
                     result: Any) -> None:
        # Bug: Mixed command and persistence
        self.db.execute(
            'INSERT INTO command_history (command, data, result, timestamp) VALUES (?, ?, ?, ?)',
            (command, json.dumps(data), json.dumps(result),
             datetime.now().isoformat())
        )

# Bug: Adapter Pattern Misuse - mixed adapters and poor abstraction
class DataConverter:
    """
    Misused Adapter pattern for data conversion.
    """
    def __init__(self):
        # Bug: Mixed adapters - adapters know too much
        self.adapters = {
            'json_to_xml': self._json_to_xml,
            'xml_to_json': self._xml_to_json,
            'csv_to_json': self._csv_to_json
        }
        self.db = DatabaseConnection()

    def convert(self, source_format: str, target_format: str,
                data: Any) -> Any:
        # Bug: Mixed conversion and business logic
        adapter_key = f"{source_format}_to_{target_format}"
        if adapter_key not in self.adapters:
            raise ValueError(f"Unsupported conversion: {adapter_key}")

        adapter = self.adapters[adapter_key]
        result = adapter(data)

        # Bug: Mixed conversion and persistence
        self._save_conversion(source_format, target_format, data, result)

        return result

    def _json_to_xml(self, data: Dict[str, Any]) -> str:
        # Bug: Mixed conversion and business logic
        # Simulate JSON to XML conversion
        return f"<root>{json.dumps(data)}</root>"

    def _xml_to_json(self, data: str) -> Dict[str, Any]:
        # Bug: Mixed conversion and business logic
        # Simulate XML to JSON conversion
        return {'data': data.strip('<root>').strip('</root>')}

    def _csv_to_json(self, data: str) -> Dict[str, Any]:
        # Bug: Mixed conversion and business logic
        # Simulate CSV to JSON conversion
        return {'data': data.split(',')}

    def _save_conversion(self, source_format: str, target_format: str,
                        source_data: Any, target_data: Any) -> None:
        # Bug: Mixed conversion and persistence
        self.db.execute(
            'INSERT INTO conversions (source_format, target_format, source_data, target_data, timestamp) VALUES (?, ?, ?, ?, ?)',
            (source_format, target_format, str(source_data),
             str(target_data), datetime.now().isoformat())
        )

# Bug: Template Method Pattern Misuse - mixed templates and poor inheritance
class ReportGenerator(ABC):
    """
    Misused Template Method pattern for report generation.
    """
    def __init__(self):
        # Bug: Mixed templates - base class knows too much
        self.db = DatabaseConnection()
        self.notification_system = NotificationSystem()

    def generate_report(self, data: Dict[str, Any]) -> str:
        # Bug: Mixed template and business logic
        if not self._validate_data(data):
            raise ValueError("Invalid report data")

        report = self._generate_report_content(data)
        formatted_report = self._format_report(report)

        # Bug: Mixed template and persistence
        self._save_report(formatted_report)

        # Bug: Mixed template and notification
        if self._should_notify():
            self._send_notification(formatted_report)

        return formatted_report

    @abstractmethod
    def _generate_report_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed template and business logic
        pass

    def _validate_data(self, data: Dict[str, Any]) -> bool:
        # Bug: Mixed template and validation
        return True

    def _format_report(self, report: Dict[str, Any]) -> str:
        # Bug: Mixed template and formatting
        return json.dumps(report, indent=2)

    def _save_report(self, report: str) -> None:
        # Bug: Mixed template and persistence
        self.db.execute(
            'INSERT INTO reports (content, timestamp) VALUES (?, ?)',
            (report, datetime.now().isoformat())
        )

    def _should_notify(self) -> bool:
        # Bug: Mixed template and business logic
        return True

    def _send_notification(self, report: str) -> None:
        # Bug: Mixed template and notification
        self.notification_system.send_notification(
            'admin',
            'report_generated',
            {'report': report},
            ['email']
        )

class SalesReportGenerator(ReportGenerator):
    """
    Misused concrete implementation of ReportGenerator.
    """
    def _generate_report_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed template and business logic
        return {
            'total_sales': sum(item['amount'] for item in data['sales']),
            'total_orders': len(data['sales']),
            'sales_by_product': {
                item['product']: sum(s['amount'] for s in data['sales']
                                   if s['product'] == item['product'])
                for item in data['sales']
            }
        }

def main():
    # Test DatabaseConnection singleton misuse
    print("Testing DatabaseConnection singleton misuse:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")

    # Test ObjectCreator factory misuse
    print("\nTesting ObjectCreator factory misuse:")
    creator = ObjectCreator()
    try:
        user = creator.create_object('user', {
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        print(f"Created user: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Test EventSystem observer misuse
    print("\nTesting EventSystem observer misuse:")
    event_system = EventSystem()
    event_system.subscribe('user_created', lambda data: print(f"User created: {data}"))
    event_system.notify('user_created', {'user_id': 'user1', 'name': 'John'})

    # Test PaymentProcessor strategy misuse
    print("\nTesting PaymentProcessor strategy misuse:")
    payment_processor = PaymentProcessor()
    result = payment_processor.process_payment(100.0, "USD", "credit_card")
    print(f"Payment result: {result}")

    # Test Logger decorator misuse
    print("\nTesting Logger decorator misuse:")
    logger = Logger()
    logger.log('INFO', 'Test message', ['file', 'database'])

    # Test TaskManager command misuse
    print("\nTesting TaskManager command misuse:")
    task_manager = TaskManager()
    result = task_manager.execute_command('create_user', {
        'name': 'John Doe',
        'email': 'john@example.com'
    })
    print(f"Command result: {result}")

    # Test DataConverter adapter misuse
    print("\nTesting DataConverter adapter misuse:")
    converter = DataConverter()
    result = converter.convert('json', 'xml', {'name': 'John'})
    print(f"Conversion result: {result}")

    # Test ReportGenerator template method misuse
    print("\nTesting ReportGenerator template method misuse:")
    report_generator = SalesReportGenerator()
    report = report_generator.generate_report({
        'sales': [
            {'product': 'A', 'amount': 100},
            {'product': 'B', 'amount': 200}
        ]
    })
    print(f"Generated report: {report}")

if __name__ == "__main__":
    main()