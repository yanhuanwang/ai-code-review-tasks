#!/usr/bin/env python3
"""
Task 27: Error Handling Issues Challenge

This file contains several intentional error handling issues for code review practice.
The task is to identify and fix the following error handling problems:

1. Swallowed Exceptions:
   - DataProcessor: Bare except clauses
   - FileManager: Ignored exceptions
   - NetworkManager: Hidden errors

2. Generic Error Handling:
   - UserManager: Catching all exceptions
   - OrderManager: Generic error messages
   - CacheManager: Non-specific error types

3. Missing Error Recovery:
   - DatabaseManager: No retry logic
   - ServiceManager: No fallback
   - ResourceManager: No cleanup

4. Improper Error Propagation:
   - ValidationManager: Lost error context
   - ProcessManager: Changed error types
   - StateManager: Masked errors

5. Inadequate Error Information:
   - LogManager: Missing error details
   - ErrorManager: Generic error codes
   - APIManager: Lost stack traces

6. Error Handling Anti-patterns:
   - SecurityManager: Error-based flow control
   - AuthManager: Exception-based validation
   - ConfigManager: Error-based configuration

7. Resource Leaks:
   - FileHandler: Unclosed resources
   - ConnectionManager: Leaked connections
   - ThreadManager: Unjoined threads

8. Error State Management:
   - StateManager: Inconsistent state
   - TransactionManager: Partial updates
   - CacheManager: Corrupted cache

Review the code and identify these error handling issues.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import psycopg2
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: Swallowed Exceptions
class DataProcessor:
    """
    Data processor with swallowed exceptions.
    """
    def process_data(self, data: str) -> Dict[str, Any]:
        try:
            # Bug: Swallowed exception - bare except
            return json.loads(data)
        except:
            # Bug: Swallowed exception - no error handling
            return {}

    def validate_data(self, data: Dict[str, Any]) -> bool:
        try:
            # Bug: Swallowed exception - ignored error
            required_fields = ["id", "name", "value"]
            for field in required_fields:
                if field not in data:
                    return False
            return True
        except:
            # Bug: Swallowed exception - no error details
            return False

# Bug: Generic Error Handling
class UserManager:
    """
    User manager with generic error handling.
    """
    def __init__(self):
        self.users = {}

    def add_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Bug: Generic exception handling
            user_id = user_data["id"]
            self.users[user_id] = user_data
            return {"status": "success", "user_id": user_id}
        except Exception as e:
            # Bug: Generic error message
            return {"status": "error", "message": "An error occurred"}

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Bug: Generic exception handling
            if user_id not in self.users:
                raise Exception("User not found")
            self.users[user_id].update(updates)
            return {"status": "success"}
        except Exception as e:
            # Bug: Generic error handling
            return {"status": "error", "message": str(e)}

# Bug: Missing Error Recovery
class DatabaseManager:
    """
    Database manager with missing error recovery.
    """
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self) -> None:
        try:
            # Bug: No retry logic
            self.connection = sqlite3.connect("database.db")
        except sqlite3.Error as e:
            # Bug: No recovery mechanism
            logger.error(f"Database connection failed: {e}")
            raise

    def execute_query(self, query: str) -> List[Any]:
        try:
            # Bug: No connection recovery
            cursor = self.connection.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            # Bug: No retry or fallback
            logger.error(f"Query execution failed: {e}")
            raise

# Bug: Improper Error Propagation
class ValidationManager:
    """
    Validation manager with improper error propagation.
    """
    def validate_input(self, data: Dict[str, Any]) -> bool:
        try:
            # Bug: Lost error context
            if not self._validate_required_fields(data):
                raise ValueError("Missing required fields")
            if not self._validate_data_types(data):
                raise TypeError("Invalid data types")
            return True
        except (ValueError, TypeError) as e:
            # Bug: Changed error type
            raise Exception(f"Validation failed: {str(e)}")

    def _validate_required_fields(self, data: Dict[str, Any]) -> bool:
        # Bug: Masked validation error
        try:
            required = ["id", "name", "email"]
            return all(field in data for field in required)
        except:
            return False

# Bug: Inadequate Error Information
class LogManager:
    """
    Log manager with inadequate error information.
    """
    def log_error(self, error: Exception) -> None:
        # Bug: Missing error details
        logger.error(f"An error occurred: {str(error)}")

    def log_database_error(self, error: sqlite3.Error) -> None:
        # Bug: Generic error code
        logger.error("Database error occurred")

    def log_network_error(self, error: requests.RequestException) -> None:
        # Bug: Lost stack trace
        logger.error(f"Network error: {error}")

# Bug: Error Handling Anti-patterns
class SecurityManager:
    """
    Security manager with error handling anti-patterns.
    """
    def validate_token(self, token: str) -> bool:
        try:
            # Bug: Error-based flow control
            if not token:
                raise ValueError("Invalid token")
            # Bug: Exception-based validation
            if not self._check_token_format(token):
                raise ValueError("Invalid token format")
            return True
        except ValueError:
            return False

    def _check_token_format(self, token: str) -> bool:
        # Bug: Exception-based validation
        try:
            return len(token) > 10
        except:
            return False

# Bug: Resource Leaks
class FileHandler:
    """
    File handler with resource leaks.
    """
    def __init__(self):
        self.files = []

    def open_file(self, filename: str) -> None:
        # Bug: Unclosed file handle
        file = open(filename, "r")
        self.files.append(file)

    def read_file(self, filename: str) -> str:
        # Bug: Resource leak
        file = open(filename, "r")
        try:
            return file.read()
        except:
            # Bug: Unclosed file on error
            return ""

    def close_all(self) -> None:
        # Bug: Incomplete cleanup
        for file in self.files:
            try:
                file.close()
            except:
                pass

# Bug: Error State Management
class TransactionManager:
    """
    Transaction manager with error state issues.
    """
    def __init__(self):
        self.transactions = {}
        self.lock = threading.Lock()

    def begin_transaction(self, transaction_id: str) -> None:
        # Bug: Inconsistent state
        with self.lock:
            self.transactions[transaction_id] = {
                "status": "started",
                "start_time": time.time()
            }

    def commit_transaction(self, transaction_id: str) -> None:
        try:
            # Bug: Partial update
            with self.lock:
                if transaction_id in self.transactions:
                    self.transactions[transaction_id]["status"] = "committed"
                    # Bug: Incomplete state update
                    self.transactions[transaction_id]["end_time"] = time.time()
        except:
            # Bug: Inconsistent state on error
            pass

    def rollback_transaction(self, transaction_id: str) -> None:
        # Bug: Incomplete rollback
        with self.lock:
            if transaction_id in self.transactions:
                self.transactions[transaction_id]["status"] = "rolled_back"

# Bug: Error Recovery Anti-patterns
class ServiceManager:
    """
    Service manager with error recovery anti-patterns.
    """
    def __init__(self):
        self.services = {}
        self.retry_count = 0

    def call_service(self, service_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Infinite retry
        while True:
            try:
                # Bug: No retry limit
                return self._make_service_call(service_name, data)
            except Exception as e:
                # Bug: No backoff
                time.sleep(1)
                continue

    def _make_service_call(self, service_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: No service fallback
        if service_name not in self.services:
            raise ValueError("Service not found")
        return self.services[service_name](data)

# Bug: Error Handling in Async Code
class AsyncManager:
    """
    Async manager with error handling issues.
    """
    def __init__(self):
        self.tasks = []

    async def process_data(self, data: List[Any]) -> List[Any]:
        # Bug: Unhandled async exceptions
        results = []
        for item in data:
            # Bug: No error handling in async
            result = await self._process_item(item)
            results.append(result)
        return results

    async def _process_item(self, item: Any) -> Any:
        # Bug: Swallowed async exception
        try:
            return await self._async_operation(item)
        except:
            return None

def main():
    """
    Main function to demonstrate error handling issues.
    """
    print("Error Handling Issues Demonstration:")
    print("===================================")

    try:
        # Test DataProcessor
        data_processor = DataProcessor()
        result = data_processor.process_data("invalid json")
        print(f"DataProcessor result: {result}")

        # Test UserManager
        user_manager = UserManager()
        result = user_manager.add_user({"id": "user1"})
        print(f"UserManager result: {result}")

        # Test DatabaseManager
        db_manager = DatabaseManager()
        try:
            result = db_manager.execute_query("SELECT * FROM nonexistent")
            print(f"DatabaseManager result: {result}")
        except Exception as e:
            print(f"DatabaseManager error: {e}")

        # Test ValidationManager
        validation_manager = ValidationManager()
        try:
            result = validation_manager.validate_input({"id": 1})
            print(f"ValidationManager result: {result}")
        except Exception as e:
            print(f"ValidationManager error: {e}")

        # Test LogManager
        log_manager = LogManager()
        try:
            raise ValueError("Test error")
        except Exception as e:
            log_manager.log_error(e)

        # Test SecurityManager
        security_manager = SecurityManager()
        result = security_manager.validate_token("")
        print(f"SecurityManager result: {result}")

        # Test FileHandler
        file_handler = FileHandler()
        try:
            file_handler.read_file("nonexistent.txt")
        except Exception as e:
            print(f"FileHandler error: {e}")

        # Test TransactionManager
        transaction_manager = TransactionManager()
        transaction_manager.begin_transaction("tx1")
        transaction_manager.commit_transaction("tx1")
        print(f"TransactionManager state: {transaction_manager.transactions}")

        # Test ServiceManager
        service_manager = ServiceManager()
        try:
            result = service_manager.call_service("nonexistent", {})
            print(f"ServiceManager result: {result}")
        except Exception as e:
            print(f"ServiceManager error: {e}")

    except Exception as e:
        print(f"Main error: {e}")
        # Bug: Generic error handling in main
        pass

if __name__ == "__main__":
    main()