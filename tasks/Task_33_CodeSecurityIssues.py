#!/usr/bin/env python3
"""
Task 33: Code Security Issues Challenge

This file contains several intentional security issues for code review practice.
The task is to identify and fix the following security problems:

1. SQL Injection:
   - UserManager: unsafe SQL queries
   - OrderManager: string concatenation in queries
   - DataManager: unescaped user input

2. Hardcoded Credentials:
   - DatabaseManager: hardcoded passwords
   - APIManager: embedded API keys
   - ConfigManager: sensitive data in code

3. Unsafe Deserialization:
   - DataProcessor: unsafe pickle usage
   - CacheManager: unsafe JSON deserialization
   - MessageProcessor: unsafe YAML loading

4. Insecure File Operations:
   - FileManager: unsafe file paths
   - LogManager: path traversal
   - BackupManager: unsafe file permissions

5. Insecure Communication:
   - NetworkManager: unencrypted data
   - APIManager: missing SSL verification
   - MessageManager: plain text passwords

6. Access Control Issues:
   - UserManager: missing authorization
   - ResourceManager: improper access checks
   - AdminManager: weak permission model

7. Input Validation:
   - ValidationManager: insufficient validation
   - DataProcessor: missing input sanitization
   - UserManager: unsafe user input

8. Security Misconfiguration:
   - ConfigManager: weak security settings
   - SecurityManager: improper encryption
   - SessionManager: weak session handling

Review the code and identify these security issues.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
import pickle
import yaml
import base64
import hashlib
import hmac
import ssl
import socket
import subprocess
import tempfile
import shutil
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import psycopg2
from abc import ABC, abstractmethod
from enum import Enum
import jwt
import bcrypt
import cryptography
from cryptography.fernet import Fernet

# Bug: SQL Injection
class UserManager:
    """
    User manager with SQL injection vulnerabilities.
    """
    def __init__(self):
        # Bug: Hardcoded database credentials
        self.db = sqlite3.connect("users.db")
        self.cursor = self.db.cursor()

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        # Bug: SQL injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        # Bug: SQL injection vulnerability
        set_clause = ", ".join([f"{k} = '{v}'" for k, v in updates.items()])
        query = f"UPDATE users SET {set_clause} WHERE username = '{username}'"
        self.cursor.execute(query)
        self.db.commit()
        return True

    def delete_user(self, username: str) -> bool:
        # Bug: SQL injection vulnerability
        query = f"DELETE FROM users WHERE username = '{username}' OR email = '{username}'"
        self.cursor.execute(query)
        self.db.commit()
        return True

# Bug: Hardcoded Credentials
class DatabaseManager:
    """
    Database manager with hardcoded credentials.
    """
    def __init__(self):
        # Bug: Hardcoded database credentials
        self.db_config = {
            "host": "localhost",
            "port": 5432,
            "database": "myapp",
            "user": "admin",
            "password": "super_secret_password_123",  # Bug: Hardcoded password
            "sslmode": "disable"  # Bug: Disabled SSL
        }

        # Bug: Hardcoded API keys
        self.api_keys = {
            "stripe": "sk_live_51HxXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "aws": "AKIAXXXXXXXXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "google": "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        }

        # Bug: Hardcoded encryption key
        self.encryption_key = "my_secret_key_123"  # Bug: Weak encryption key

    def connect(self) -> None:
        # Bug: Using hardcoded credentials
        self.connection = psycopg2.connect(**self.db_config)

# Bug: Unsafe Deserialization
class DataProcessor:
    """
    Data processor with unsafe deserialization.
    """
    def process_data(self, data: bytes) -> Dict[str, Any]:
        # Bug: Unsafe pickle deserialization
        return pickle.loads(data)  # Bug: Arbitrary code execution risk

    def load_config(self, config_data: str) -> Dict[str, Any]:
        # Bug: Unsafe YAML loading
        return yaml.load(config_data, Loader=yaml.Loader)  # Bug: Arbitrary code execution risk

    def parse_message(self, message: str) -> Dict[str, Any]:
        # Bug: Unsafe JSON deserialization with custom object hook
        return json.loads(message, object_hook=self._custom_hook)  # Bug: Arbitrary code execution risk

    def _custom_hook(self, obj: Dict[str, Any]) -> Any:
        # Bug: Unsafe object construction
        if "__class__" in obj:
            class_name = obj["__class__"]
            if class_name in globals():
                return globals()[class_name](**obj)
        return obj

# Bug: Insecure File Operations
class FileManager:
    """
    File manager with insecure file operations.
    """
    def read_file(self, filename: str) -> str:
        # Bug: Path traversal vulnerability
        with open(filename, "r") as f:  # Bug: Unsafe file path
            return f.read()

    def write_file(self, filename: str, content: str) -> None:
        # Bug: Unsafe file permissions
        with open(filename, "w") as f:  # Bug: Unsafe file path
            f.write(content)
        os.chmod(filename, 0o777)  # Bug: Overly permissive file permissions

    def delete_file(self, filename: str) -> None:
        # Bug: Unsafe file deletion
        os.remove(filename)  # Bug: Unsafe file path

    def create_temp_file(self, content: str) -> str:
        # Bug: Unsafe temporary file creation
        fd, path = tempfile.mkstemp()  # Bug: Predictable temporary file
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

# Bug: Insecure Communication
class NetworkManager:
    """
    Network manager with insecure communication.
    """
    def __init__(self):
        # Bug: Disabled SSL verification
        self.session = requests.Session()
        self.session.verify = False  # Bug: Disabled SSL verification

    def send_data(self, url: str, data: Dict[str, Any]) -> None:
        # Bug: Unencrypted sensitive data
        response = self.session.post(url, json=data)  # Bug: Plain text transmission
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")  # Bug: Logging sensitive data

    def download_file(self, url: str, filename: str) -> None:
        # Bug: Unsafe file download
        response = self.session.get(url, stream=True)
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

# Bug: Access Control Issues
class ResourceManager:
    """
    Resource manager with access control issues.
    """
    def __init__(self):
        self.resources = {}
        self.permissions = defaultdict(set)

    def check_access(self, user_id: str, resource_id: str, action: str) -> bool:
        # Bug: Insufficient access control
        if user_id in self.permissions:
            return True  # Bug: Overly permissive access

    def grant_access(self, user_id: str, resource_id: str, action: str) -> None:
        # Bug: Missing access control
        self.permissions[user_id].add(action)  # Bug: No validation

    def revoke_access(self, user_id: str, resource_id: str, action: str) -> None:
        # Bug: Missing access control
        if action in self.permissions[user_id]:
            self.permissions[user_id].remove(action)  # Bug: No validation

# Bug: Input Validation
class ValidationManager:
    """
    Validation manager with insufficient input validation.
    """
    def validate_input(self, data: Dict[str, Any]) -> bool:
        # Bug: Insufficient input validation
        if not data:
            return False

        # Bug: Missing type checking
        if "username" in data:
            return True  # Bug: No validation

        # Bug: Missing length validation
        if "password" in data:
            return True  # Bug: No validation

        # Bug: Missing format validation
        if "email" in data:
            return True  # Bug: No validation

        return True  # Bug: Default to True

    def sanitize_input(self, data: str) -> str:
        # Bug: Insufficient input sanitization
        return data.replace("<script>", "")  # Bug: Weak sanitization

# Bug: Security Misconfiguration
class SecurityManager:
    """
    Security manager with security misconfigurations.
    """
    def __init__(self):
        # Bug: Weak encryption settings
        self.encryption_key = "weak_key_123"  # Bug: Weak key
        self.algorithm = "DES"  # Bug: Weak algorithm
        self.iterations = 1000  # Bug: Too few iterations

        # Bug: Weak password hashing
        self.salt = "static_salt"  # Bug: Static salt

    def hash_password(self, password: str) -> str:
        # Bug: Weak password hashing
        return hashlib.md5((password + self.salt).encode()).hexdigest()  # Bug: MD5 with static salt

    def verify_password(self, password: str, hashed: str) -> bool:
        # Bug: Weak password verification
        return self.hash_password(password) == hashed

    def encrypt_data(self, data: str) -> str:
        # Bug: Weak encryption
        return base64.b64encode(data.encode()).decode()  # Bug: Base64 is not encryption

    def decrypt_data(self, encrypted: str) -> str:
        # Bug: Weak decryption
        return base64.b64decode(encrypted.encode()).decode()  # Bug: Base64 is not encryption

# Bug: Session Management
class SessionManager:
    """
    Session manager with weak session handling.
    """
    def __init__(self):
        # Bug: Insecure session storage
        self.sessions = {}  # Bug: In-memory storage
        self.session_timeout = 3600  # Bug: Long timeout

    def create_session(self, user_id: str) -> str:
        # Bug: Weak session ID generation
        session_id = str(random.randint(1, 1000000))  # Bug: Predictable session ID
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": time.time(),
            "last_activity": time.time()
        }
        return session_id

    def validate_session(self, session_id: str) -> bool:
        # Bug: Insufficient session validation
        if session_id in self.sessions:
            return True  # Bug: No timeout check
        return False

    def update_session(self, session_id: str) -> None:
        # Bug: Missing session security
        if session_id in self.sessions:
            self.sessions[session_id]["last_activity"] = time.time()  # Bug: No validation

def main():
    """
    Main function to demonstrate security issues.
    """
    print("Code Security Issues Demonstration:")
    print("=================================")

    try:
        # Test UserManager
        user_manager = UserManager()
        result = user_manager.get_user("admin' OR '1'='1")  # SQL injection attempt
        print(f"UserManager result: {result}")

        # Test DatabaseManager
        db_manager = DatabaseManager()
        db_manager.connect()  # Using hardcoded credentials
        print("DatabaseManager: Connected to database")

        # Test DataProcessor
        data_processor = DataProcessor()
        result = data_processor.process_data(pickle.dumps({"__class__": "subprocess.Popen", "args": ["ls"]}))
        print(f"DataProcessor result: {result}")

        # Test FileManager
        file_manager = FileManager()
        file_manager.write_file("/tmp/test.txt", "test")  # Unsafe file operation
        print("FileManager: File written")

        # Test NetworkManager
        network_manager = NetworkManager()
        network_manager.send_data("http://example.com", {"password": "secret"})  # Unencrypted data
        print("NetworkManager: Data sent")

        # Test ResourceManager
        resource_manager = ResourceManager()
        result = resource_manager.check_access("user1", "resource1", "read")  # Insufficient access control
        print(f"ResourceManager result: {result}")

        # Test ValidationManager
        validation_manager = ValidationManager()
        result = validation_manager.validate_input({"username": "<script>alert('xss')</script>"})  # Insufficient validation
        print(f"ValidationManager result: {result}")

        # Test SecurityManager
        security_manager = SecurityManager()
        hashed = security_manager.hash_password("password123")  # Weak password hashing
        print(f"SecurityManager hash: {hashed}")

        # Test SessionManager
        session_manager = SessionManager()
        session_id = session_manager.create_session("user1")  # Weak session handling
        print(f"SessionManager session: {session_id}")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()