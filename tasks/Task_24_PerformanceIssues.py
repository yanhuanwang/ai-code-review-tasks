#!/usr/bin/env python3
"""
Task 24: Performance Issues Challenge

This file contains several intentional performance issues for code review practice.
The task is to identify and fix the following performance problems:

1. Inefficient Algorithms:
   - SearchManager: O(n) search in sorted data
   - SortManager: Bubble sort for large datasets
   - CacheManager: Linear cache lookup

2. Memory Leaks:
   - DataProcessor: Growing lists without cleanup
   - ImageProcessor: Unclosed file handles
   - CacheManager: Unbounded cache growth

3. Resource Contention:
   - DatabaseManager: Connection pool exhaustion
   - ThreadManager: Thread pool starvation
   - FileManager: File handle exhaustion

4. Inefficient Data Structures:
   - ListManager: List for frequent lookups
   - SetManager: List for unique values
   - MapManager: Nested loops for mapping

5. Unnecessary Computations:
   - MathProcessor: Redundant calculations
   - StringProcessor: Repeated string operations
   - DataValidator: Redundant validations

6. I/O Bottlenecks:
   - FileProcessor: Synchronous I/O
   - NetworkManager: Blocking network calls
   - LogManager: Synchronous logging

7. Concurrency Issues:
   - TaskManager: Thread safety issues
   - QueueManager: Lock contention
   - ResourceManager: Deadlock potential

8. Scalability Issues:
   - DataManager: In-memory data growth
   - CacheManager: Global cache lock
   - ProcessManager: Single-threaded processing

Review the code and identify these performance issues.
"""

import time
import random
import threading
import queue
import sqlite3
import os
import json
import logging
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
import numpy as np
from PIL import Image
import psutil
import gc
from collections import defaultdict
import hashlib
import re
import string
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bug: Inefficient Algorithms
class SearchManager:
    """
    Inefficient Algorithms: O(n) search in sorted data, linear cache lookup.
    """
    def __init__(self):
        self.data = list(range(1000000))  # Bug: Large sorted list
        self.cache = []  # Bug: List for cache (should be dict)

    def search(self, target: int) -> Optional[int]:
        # Bug: O(n) search in sorted data (should use binary search)
        for i, value in enumerate(self.data):
            if value == target:
                return i
        return None

    def cache_lookup(self, key: str) -> Optional[Any]:
        # Bug: O(n) cache lookup (should use dict)
        for k, v in self.cache:
            if k == key:
                return v
        return None

    def add_to_cache(self, key: str, value: Any) -> None:
        # Bug: O(n) cache insertion (should use dict)
        self.cache.append((key, value))

# Bug: Memory Leaks
class DataProcessor:
    """
    Memory Leaks: Growing lists without cleanup, unclosed resources.
    """
    def __init__(self):
        self.processed_data = []  # Bug: Growing list without cleanup
        self.file_handles = []    # Bug: Unclosed file handles
        self.images = []          # Bug: Unclosed image objects

    def process_data(self, data: List[Any]) -> None:
        # Bug: Memory leak - growing list
        self.processed_data.extend(data)

    def process_file(self, filename: str) -> None:
        # Bug: Memory leak - unclosed file handle
        handle = open(filename, 'r')
        self.file_handles.append(handle)
        # Bug: Never closing the file

    def process_image(self, filename: str) -> None:
        # Bug: Memory leak - unclosed image
        image = Image.open(filename)
        self.images.append(image)
        # Bug: Never closing the image

# Bug: Resource Contention
class DatabaseManager:
    """
    Resource Contention: Connection pool exhaustion, thread safety issues.
    """
    def __init__(self):
        self.connections = []  # Bug: No connection pool
        self.lock = threading.Lock()

    def get_connection(self) -> sqlite3.Connection:
        # Bug: Resource contention - no connection pool
        with self.lock:  # Bug: Global lock
            conn = sqlite3.connect('database.db')
            self.connections.append(conn)
            return conn

    def execute_query(self, query: str) -> List[Any]:
        # Bug: Resource contention - connection not released
        conn = self.get_connection()
        try:
            cursor = conn.execute(query)
            return cursor.fetchall()
        finally:
            # Bug: Connection not returned to pool
            pass

# Bug: Inefficient Data Structures
class ListManager:
    """
    Inefficient Data Structures: List for frequent lookups, nested loops.
    """
    def __init__(self):
        self.items = []  # Bug: List for frequent lookups

    def find_item(self, target: Any) -> Optional[int]:
        # Bug: O(n) lookup (should use set/dict)
        for i, item in enumerate(self.items):
            if item == target:
                return i
        return None

    def find_duplicates(self) -> List[Any]:
        # Bug: O(n²) duplicate finding (should use set)
        duplicates = []
        for i, item1 in enumerate(self.items):
            for item2 in self.items[i+1:]:
                if item1 == item2:
                    duplicates.append(item1)
        return duplicates

# Bug: Unnecessary Computations
class MathProcessor:
    """
    Unnecessary Computations: Redundant calculations, repeated operations.
    """
    def __init__(self):
        self.cache = {}  # Bug: No caching of results

    def calculate_fibonacci(self, n: int) -> int:
        # Bug: Redundant calculations (should use dynamic programming)
        if n <= 1:
            return n
        return self.calculate_fibonacci(n-1) + self.calculate_fibonacci(n-2)

    def calculate_primes(self, n: int) -> List[int]:
        # Bug: Inefficient prime calculation
        primes = []
        for num in range(2, n+1):
            # Bug: Redundant divisibility checks
            is_prime = True
            for i in range(2, num):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes

# Bug: I/O Bottlenecks
class FileProcessor:
    """
    I/O Bottlenecks: Synchronous I/O, blocking operations.
    """
    def __init__(self):
        self.files = []

    def process_files(self, filenames: List[str]) -> List[str]:
        # Bug: Synchronous I/O (should use async)
        results = []
        for filename in filenames:
            # Bug: Blocking I/O
            with open(filename, 'r') as f:
                content = f.read()
                # Bug: Synchronous processing
                processed = self.process_content(content)
                results.append(processed)
        return results

    def process_content(self, content: str) -> str:
        # Bug: Synchronous processing
        time.sleep(0.1)  # Simulate processing
        return content.upper()

# Bug: Concurrency Issues
class TaskManager:
    """
    Concurrency Issues: Thread safety issues, lock contention.
    """
    def __init__(self):
        self.tasks = []  # Bug: Not thread-safe
        self.lock = threading.Lock()
        self.thread_pool = ThreadPoolExecutor(max_workers=1)  # Bug: Single worker

    def add_task(self, task: Any) -> None:
        # Bug: Thread safety issue - no atomic operation
        with self.lock:  # Bug: Lock contention
            self.tasks.append(task)

    def process_tasks(self) -> List[Any]:
        # Bug: Single-threaded processing
        results = []
        with self.lock:  # Bug: Long-held lock
            for task in self.tasks:
                # Bug: Synchronous processing
                result = self.process_task(task)
                results.append(result)
        return results

    def process_task(self, task: Any) -> Any:
        # Bug: Synchronous processing
        time.sleep(0.1)  # Simulate processing
        return task

# Bug: Scalability Issues
class DataManager:
    """
    Scalability Issues: In-memory data growth, global locks.
    """
    def __init__(self):
        self.data = {}  # Bug: In-memory storage
        self.lock = threading.Lock()  # Bug: Global lock

    def store_data(self, key: str, value: Any) -> None:
        # Bug: In-memory data growth
        with self.lock:  # Bug: Global lock
            self.data[key] = value

    def process_data(self) -> Dict[str, Any]:
        # Bug: In-memory processing
        with self.lock:  # Bug: Long-held lock
            # Bug: Single-threaded processing
            processed = {}
            for key, value in self.data.items():
                # Bug: Synchronous processing
                processed[key] = self.process_item(value)
            return processed

    def process_item(self, item: Any) -> Any:
        # Bug: Synchronous processing
        time.sleep(0.1)  # Simulate processing
        return item

def main():
    # Test Inefficient Algorithms
    print("Testing Inefficient Algorithms:")
    search_manager = SearchManager()
    try:
        # Bug: Inefficient search
        start_time = time.time()
        result = search_manager.search(500000)
        end_time = time.time()
        print(f"Search took {end_time - start_time:.2f} seconds")
        print(f"Found at index: {result}")
    except Exception as e:
        print(f"Error in search manager: {e}")

    # Test Memory Leaks
    print("\nTesting Memory Leaks:")
    data_processor = DataProcessor()
    try:
        # Bug: Memory leak - growing list
        for i in range(1000):
            data_processor.process_data([i] * 1000)
        print(f"Memory usage: {psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB")
    except Exception as e:
        print(f"Error in data processor: {e}")

    # Test Resource Contention
    print("\nTesting Resource Contention:")
    db_manager = DatabaseManager()
    try:
        # Bug: Resource contention
        threads = []
        for i in range(10):
            thread = threading.Thread(
                target=lambda: db_manager.execute_query("SELECT 1")
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    except Exception as e:
        print(f"Error in database manager: {e}")

    # Test Inefficient Data Structures
    print("\nTesting Inefficient Data Structures:")
    list_manager = ListManager()
    try:
        # Bug: Inefficient data structure
        list_manager.items = list(range(10000))
        start_time = time.time()
        result = list_manager.find_duplicates()
        end_time = time.time()
        print(f"Find duplicates took {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in list manager: {e}")

    # Test Unnecessary Computations
    print("\nTesting Unnecessary Computations:")
    math_processor = MathProcessor()
    try:
        # Bug: Unnecessary computations
        start_time = time.time()
        result = math_processor.calculate_fibonacci(35)
        end_time = time.time()
        print(f"Fibonacci calculation took {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in math processor: {e}")

    # Test I/O Bottlenecks
    print("\nTesting I/O Bottlenecks:")
    file_processor = FileProcessor()
    try:
        # Bug: I/O bottlenecks
        filenames = ['test1.txt', 'test2.txt', 'test3.txt']
        start_time = time.time()
        results = file_processor.process_files(filenames)
        end_time = time.time()
        print(f"File processing took {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in file processor: {e}")

    # Test Concurrency Issues
    print("\nTesting Concurrency Issues:")
    task_manager = TaskManager()
    try:
        # Bug: Concurrency issues
        for i in range(10):
            task_manager.add_task(i)
        start_time = time.time()
        results = task_manager.process_tasks()
        end_time = time.time()
        print(f"Task processing took {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in task manager: {e}")

    # Test Scalability Issues
    print("\nTesting Scalability Issues:")
    data_manager = DataManager()
    try:
        # Bug: Scalability issues
        for i in range(1000):
            data_manager.store_data(f"key_{i}", i)
        start_time = time.time()
        results = data_manager.process_data()
        end_time = time.time()
        print(f"Data processing took {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in data manager: {e}")

if __name__ == "__main__":
    main()