#!/usr/bin/env python3
"""
Task 21: Design Pattern Misuse Challenge

This file contains several intentional design pattern misuses for code review practice.
The task is to identify and fix the following pattern misuses:

1. Singleton Pattern Misuse:
   - DatabaseManager: Global state, tight coupling
   - Unnecessary singleton
   - Thread safety issues

2. Factory Pattern Misuse:
   - PaymentFactory: Complex factory with too many responsibilities
   - Mixed factory and strategy
   - Violation of Single Responsibility

3. Observer Pattern Misuse:
   - EventManager: Tight coupling between subject and observers
   - No unsubscribe mechanism
   - Memory leaks

4. Strategy Pattern Misuse:
   - SortingStrategy: Mixed strategy and state
   - Unnecessary abstraction
   - Violation of Interface Segregation

5. Decorator Pattern Misuse:
   - LoggingDecorator: Violation of Liskov Substitution
   - Mixed concerns
   - Unnecessary decoration

6. Command Pattern Misuse:
   - CommandProcessor: Mixed command and state
   - No undo mechanism
   - Violation of Single Responsibility

7. Template Method Misuse:
   - DataProcessor: Violation of Open/Closed
   - Mixed template and strategy
   - Unnecessary inheritance

8. Adapter Pattern Misuse:
   - PaymentAdapter: Violation of Interface Segregation
   - Mixed adapter and facade
   - Unnecessary adaptation

Review the code and identify these pattern misuses.
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple, Protocol
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

# Bug: Singleton Pattern Misuse - Unnecessary global state
class DatabaseManager:
    """
    Singleton Pattern Misuse: Unnecessary global state and tight coupling.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        # Bug: Thread-unsafe singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Bug: Multiple initialization possible
        if not self._initialized:
            self.connection = sqlite3.connect('app.db')
            self.cursor = self.connection.cursor()
            self._initialized = True

    def execute_query(self, query: str, params: tuple = ()) -> List[Any]:
        # Bug: Global state access
        return self.cursor.execute(query, params).fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> None:
        # Bug: Global state modification
        self.cursor.execute(query, params)
        self.connection.commit()

# Bug: Factory Pattern Misuse - Complex factory with mixed responsibilities
class PaymentFactory:
    """
    Factory Pattern Misuse: Complex factory with mixed responsibilities.
    """
    def __init__(self):
        # Bug: Factory with too many responsibilities
        self.payment_methods = {
            'credit_card': self._create_credit_card_payment,
            'paypal': self._create_paypal_payment,
            'bank_transfer': self._create_bank_transfer_payment
        }
        self.validation_rules = {
            'credit_card': self._validate_credit_card,
            'paypal': self._validate_paypal,
            'bank_transfer': self._validate_bank_transfer
        }
        self.processing_rules = {
            'credit_card': self._process_credit_card,
            'paypal': self._process_paypal,
            'bank_transfer': self._process_bank_transfer
        }

    def create_payment(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed factory and strategy
        if method not in self.payment_methods:
            raise ValueError(f"Unsupported payment method: {method}")

        # Validate payment data
        if not self.validation_rules[method](data):
            raise ValueError(f"Invalid payment data for {method}")

        # Create payment object
        payment = self.payment_methods[method](data)

        # Process payment
        result = self.processing_rules[method](payment)

        # Update payment status
        payment['status'] = 'completed' if result else 'failed'

        return payment

    def _create_credit_card_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed creation and validation
        return {
            'type': 'credit_card',
            'card_number': data['card_number'],
            'expiry': data['expiry'],
            'cvv': data['cvv'],
            'amount': data['amount'],
            'currency': data['currency'],
            'status': 'pending'
        }

    def _create_paypal_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed creation and validation
        return {
            'type': 'paypal',
            'email': data['email'],
            'amount': data['amount'],
            'currency': data['currency'],
            'status': 'pending'
        }

    def _create_bank_transfer_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Mixed creation and validation
        return {
            'type': 'bank_transfer',
            'account_number': data['account_number'],
            'routing_number': data['routing_number'],
            'amount': data['amount'],
            'currency': data['currency'],
            'status': 'pending'
        }

    def _validate_credit_card(self, data: Dict[str, Any]) -> bool:
        # Bug: Validation in factory
        return all(key in data for key in
                  ['card_number', 'expiry', 'cvv', 'amount', 'currency'])

    def _validate_paypal(self, data: Dict[str, Any]) -> bool:
        # Bug: Validation in factory
        return all(key in data for key in ['email', 'amount', 'currency'])

    def _validate_bank_transfer(self, data: Dict[str, Any]) -> bool:
        # Bug: Validation in factory
        return all(key in data for key in
                  ['account_number', 'routing_number', 'amount', 'currency'])

    def _process_credit_card(self, payment: Dict[str, Any]) -> bool:
        # Bug: Processing in factory
        return random.random() > 0.1

    def _process_paypal(self, payment: Dict[str, Any]) -> bool:
        # Bug: Processing in factory
        return random.random() > 0.1

    def _process_bank_transfer(self, payment: Dict[str, Any]) -> bool:
        # Bug: Processing in factory
        return random.random() > 0.1

# Bug: Observer Pattern Misuse - Tight coupling and memory leaks
class EventManager:
    """
    Observer Pattern Misuse: Tight coupling and memory leaks.
    """
    def __init__(self):
        # Bug: No unsubscribe mechanism
        self.observers = []
        self.events = []

    def add_observer(self, observer: Any) -> None:
        # Bug: Direct observer reference
        self.observers.append(observer)

    def notify_observers(self, event: Dict[str, Any]) -> None:
        # Bug: Direct observer calls
        self.events.append(event)
        for observer in self.observers:
            observer.update(event)

    def process_event(self, event: Dict[str, Any]) -> None:
        # Bug: Mixed event processing and notification
        # Process event
        event['processed_at'] = datetime.now().isoformat()
        event['status'] = 'processed'

        # Notify observers
        self.notify_observers(event)

        # Store event
        self.events.append(event)

# Bug: Strategy Pattern Misuse - Mixed strategy and state
class SortingStrategy:
    """
    Strategy Pattern Misuse: Mixed strategy and state.
    """
    def __init__(self):
        # Bug: Mixed strategy and state
        self.current_strategy = None
        self.data = []
        self.sorted_data = []
        self.comparison_count = 0
        self.swap_count = 0

    def set_strategy(self, strategy: str) -> None:
        # Bug: Strategy selection mixed with state
        if strategy == 'bubble':
            self.current_strategy = self._bubble_sort
        elif strategy == 'quick':
            self.current_strategy = self._quick_sort
        elif strategy == 'merge':
            self.current_strategy = self._merge_sort
        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

    def sort(self, data: List[Any]) -> List[Any]:
        # Bug: Mixed strategy execution and state
        self.data = data.copy()
        self.sorted_data = []
        self.comparison_count = 0
        self.swap_count = 0

        if not self.current_strategy:
            raise ValueError("No strategy set")

        self.sorted_data = self.current_strategy()
        return self.sorted_data

    def _bubble_sort(self) -> List[Any]:
        # Bug: Strategy implementation mixed with state
        data = self.data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparison_count += 1
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.swap_count += 1
        return data

    def _quick_sort(self) -> List[Any]:
        # Bug: Strategy implementation mixed with state
        data = self.data.copy()
        if len(data) <= 1:
            return data

        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]

        self.comparison_count += len(data)
        return (self._quick_sort(left) + middle +
                self._quick_sort(right))

    def _merge_sort(self) -> List[Any]:
        # Bug: Strategy implementation mixed with state
        data = self.data.copy()
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = self._merge_sort(data[:mid])
        right = self._merge_sort(data[mid:])

        self.comparison_count += len(data)
        return self._merge(left, right)

    def _merge(self, left: List[Any], right: List[Any]) -> List[Any]:
        # Bug: Helper method mixed with state
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            self.comparison_count += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

# Bug: Decorator Pattern Misuse - Violation of Liskov Substitution
class LoggingDecorator:
    """
    Decorator Pattern Misuse: Violation of Liskov Substitution.
    """
    def __init__(self, component: Any):
        # Bug: Direct component reference
        self.component = component
        self.logs = []

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Changed behavior of decorated component
        try:
            # Log before processing
            self.logs.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'start',
                'data': data
            })

            # Process data
            result = self.component.process(data)

            # Log after processing
            self.logs.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'end',
                'data': result
            })

            # Bug: Additional behavior not in original component
            result['processed_at'] = datetime.now().isoformat()
            result['processing_time'] = time.time()

            return result

        except Exception as e:
            # Bug: Changed error handling
            self.logs.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'error',
                'error': str(e)
            })
            raise ValueError(f"Processing failed: {str(e)}")

# Bug: Command Pattern Misuse - Mixed command and state
class CommandProcessor:
    """
    Command Pattern Misuse: Mixed command and state.
    """
    def __init__(self):
        # Bug: Mixed command and state
        self.commands = []
        self.current_state = {}
        self.history = []
        self.undo_stack = []

    def execute_command(self, command: Dict[str, Any]) -> None:
        # Bug: Mixed command execution and state management
        if command['type'] == 'create':
            self._execute_create(command)
        elif command['type'] == 'update':
            self._execute_update(command)
        elif command['type'] == 'delete':
            self._execute_delete(command)
        else:
            raise ValueError(f"Unsupported command type: {command['type']}")

        # Update state
        self.current_state = self._compute_state()

        # Update history
        self.history.append({
            'command': command,
            'state': self.current_state.copy(),
            'timestamp': datetime.now().isoformat()
        })

    def _execute_create(self, command: Dict[str, Any]) -> None:
        # Bug: Command implementation mixed with state
        if command['id'] in self.current_state:
            raise ValueError(f"Item {command['id']} already exists")

        self.commands.append({
            'type': 'create',
            'id': command['id'],
            'data': command['data']
        })

    def _execute_update(self, command: Dict[str, Any]) -> None:
        # Bug: Command implementation mixed with state
        if command['id'] not in self.current_state:
            raise ValueError(f"Item {command['id']} does not exist")

        self.commands.append({
            'type': 'update',
            'id': command['id'],
            'data': command['data']
        })

    def _execute_delete(self, command: Dict[str, Any]) -> None:
        # Bug: Command implementation mixed with state
        if command['id'] not in self.current_state:
            raise ValueError(f"Item {command['id']} does not exist")

        self.commands.append({
            'type': 'delete',
            'id': command['id']
        })

    def _compute_state(self) -> Dict[str, Any]:
        # Bug: State computation mixed with commands
        state = {}
        for cmd in self.commands:
            if cmd['type'] == 'create':
                state[cmd['id']] = cmd['data']
            elif cmd['type'] == 'update':
                state[cmd['id']].update(cmd['data'])
            elif cmd['type'] == 'delete':
                del state[cmd['id']]
        return state

def main():
    # Test Singleton Pattern misuse
    print("Testing Singleton Pattern misuse:")
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    print(f"Same instance: {db1 is db2}")

    # Test Factory Pattern misuse
    print("\nTesting Factory Pattern misuse:")
    payment_factory = PaymentFactory()
    try:
        payment = payment_factory.create_payment('credit_card', {
            'card_number': '4111111111111111',
            'expiry': '12/25',
            'cvv': '123',
            'amount': 100.0,
            'currency': 'USD'
        })
        print(f"Created payment: {payment}")
    except Exception as e:
        print(f"Error in payment factory: {e}")

    # Test Observer Pattern misuse
    print("\nTesting Observer Pattern misuse:")
    event_manager = EventManager()
    class TestObserver:
        def update(self, event):
            print(f"Received event: {event}")

    observer = TestObserver()
    event_manager.add_observer(observer)
    event_manager.process_event({'type': 'test', 'data': 'test'})

    # Test Strategy Pattern misuse
    print("\nTesting Strategy Pattern misuse:")
    sorter = SortingStrategy()
    sorter.set_strategy('bubble')
    result = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"Sorted data: {result}")
    print(f"Comparisons: {sorter.comparison_count}")
    print(f"Swaps: {sorter.swap_count}")

    # Test Decorator Pattern misuse
    print("\nTesting Decorator Pattern misuse:")
    class TestComponent:
        def process(self, data):
            return {'result': 'processed'}

    decorated = LoggingDecorator(TestComponent())
    try:
        result = decorated.process({'input': 'test'})
        print(f"Decorated result: {result}")
        print(f"Logs: {decorated.logs}")
    except Exception as e:
        print(f"Error in decorator: {e}")

    # Test Command Pattern misuse
    print("\nTesting Command Pattern misuse:")
    processor = CommandProcessor()
    try:
        processor.execute_command({
            'type': 'create',
            'id': 'item1',
            'data': {'value': 100}
        })
        processor.execute_command({
            'type': 'update',
            'id': 'item1',
            'data': {'value': 200}
        })
        print(f"Current state: {processor.current_state}")
        print(f"History: {processor.history}")
    except Exception as e:
        print(f"Error in command processor: {e}")

if __name__ == "__main__":
    main()