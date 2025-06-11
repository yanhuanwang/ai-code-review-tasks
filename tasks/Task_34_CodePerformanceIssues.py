#!/usr/bin/env python3
"""
Task 34: Code Performance Issues Challenge

This file contains several intentional performance issues for code review practice.
The task is to identify and fix the following performance problems:

1. Inefficient Algorithms:
   - SearchManager: O(n²) search
   - SortManager: bubble sort
   - DataProcessor: inefficient data processing

2. Memory Leaks:
   - CacheManager: unbounded cache
   - DataManager: unclosed resources
   - ImageProcessor: unmanaged memory

3. Blocking Operations:
   - NetworkManager: synchronous I/O
   - FileManager: blocking file operations
   - DatabaseManager: blocking queries

4. Resource Management:
   - ConnectionManager: unclosed connections
   - ThreadManager: thread leaks
   - ProcessManager: process leaks

5. Inefficient Data Structures:
   - DataManager: inappropriate data structures
   - CacheManager: inefficient caching
   - TreeManager: unbalanced trees

6. CPU Intensive Operations:
   - MathProcessor: redundant calculations
   - ImageProcessor: unoptimized processing
   - DataTransformer: inefficient transformations

7. I/O Bottlenecks:
   - FileManager: small I/O operations
   - NetworkManager: inefficient transfers
   - LogManager: frequent disk writes

8. Concurrency Issues:
   - ThreadManager: poor thread management
   - ProcessManager: inefficient multiprocessing
   - AsyncManager: blocking async code

Review the code and identify these performance issues.
"""

import time
import random
import json
import sqlite3
import os
import threading
import logging
import traceback
import asyncio
import aiohttp
import psycopg2
import numpy as np
from typing import List, Dict, Any, Optional, Union, Tuple, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from contextlib import contextmanager
import requests
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image
import io
import gc
import weakref
import queue
import heapq
from collections import defaultdict, deque

# Bug: Inefficient Algorithms
class SearchManager:
    """
    Search manager with inefficient algorithms.
    """
    def __init__(self):
        self.data = []

    def add_data(self, items: List[Dict[str, Any]]) -> None:
        # Bug: Inefficient data storage
        self.data.extend(items)  # Bug: No indexing

    def search(self, query: str) -> List[Dict[str, Any]]:
        # Bug: O(n²) search algorithm
        results = []
        for item in self.data:
            # Bug: Inefficient string matching
            for key, value in item.items():
                if isinstance(value, str):
                    # Bug: Inefficient substring search
                    if query in value:
                        results.append(item)
                        break  # Bug: Only checking first match
        return results

    def find_duplicates(self) -> List[Dict[str, Any]]:
        # Bug: O(n²) duplicate finding
        duplicates = []
        for i, item1 in enumerate(self.data):
            for item2 in self.data[i+1:]:
                if item1 == item2:
                    duplicates.append(item1)
        return duplicates

# Bug: Memory Leaks
class CacheManager:
    """
    Cache manager with memory leaks.
    """
    def __init__(self):
        # Bug: Unbounded cache
        self.cache = {}  # Bug: No size limit
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        # Bug: No cache eviction
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def set(self, key: str, value: Any) -> None:
        # Bug: No size check
        self.cache[key] = value  # Bug: Memory leak

    def clear(self) -> None:
        # Bug: Incomplete cleanup
        self.cache.clear()  # Bug: References might still exist

# Bug: Blocking Operations
class NetworkManager:
    """
    Network manager with blocking operations.
    """
    def __init__(self):
        self.session = requests.Session()

    def fetch_data(self, urls: List[str]) -> List[Dict[str, Any]]:
        # Bug: Synchronous I/O
        results = []
        for url in urls:
            # Bug: Blocking network call
            response = self.session.get(url)
            results.append(response.json())
        return results

    def download_files(self, urls: List[str], directory: str) -> None:
        # Bug: Sequential downloads
        for url in urls:
            # Bug: Blocking file download
            response = self.session.get(url, stream=True)
            filename = os.path.join(directory, url.split("/")[-1])
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

# Bug: Resource Management
class ConnectionManager:
    """
    Connection manager with resource leaks.
    """
    def __init__(self):
        self.connections = []
        self.pool = []

    def create_connection(self) -> sqlite3.Connection:
        # Bug: Unmanaged connection
        conn = sqlite3.connect(":memory:")
        self.connections.append(conn)  # Bug: Never closed
        return conn

    def get_connection(self) -> sqlite3.Connection:
        # Bug: No connection pooling
        if not self.pool:
            return self.create_connection()
        return self.pool.pop()

    def release_connection(self, conn: sqlite3.Connection) -> None:
        # Bug: No connection cleanup
        self.pool.append(conn)  # Bug: Connections never closed

# Bug: Inefficient Data Structures
class DataManager:
    """
    Data manager with inefficient data structures.
    """
    def __init__(self):
        # Bug: Inappropriate data structure
        self.data = []  # Bug: List for frequent lookups

    def add_item(self, item: Dict[str, Any]) -> None:
        # Bug: Inefficient insertion
        self.data.append(item)  # Bug: O(n) lookup

    def find_item(self, key: str, value: Any) -> Optional[Dict[str, Any]]:
        # Bug: Linear search
        for item in self.data:
            if item.get(key) == value:
                return item
        return None

    def remove_item(self, key: str, value: Any) -> bool:
        # Bug: Inefficient removal
        for i, item in enumerate(self.data):
            if item.get(key) == value:
                self.data.pop(i)  # Bug: O(n) removal
                return True
        return False

# Bug: CPU Intensive Operations
class MathProcessor:
    """
    Math processor with CPU intensive operations.
    """
    def __init__(self):
        self.cache = {}  # Bug: No cache invalidation

    def calculate_fibonacci(self, n: int) -> int:
        # Bug: Inefficient recursive calculation
        if n in self.cache:
            return self.cache[n]
        if n <= 1:
            return n
        result = self.calculate_fibonacci(n-1) + self.calculate_fibonacci(n-2)
        self.cache[n] = result
        return result

    def calculate_prime_factors(self, n: int) -> List[int]:
        # Bug: Inefficient prime factorization
        factors = []
        for i in range(2, n+1):
            while n % i == 0:
                factors.append(i)
                n //= i
        return factors

    def calculate_matrix_product(self, matrix1: List[List[int]],
                               matrix2: List[List[int]]) -> List[List[int]]:
        # Bug: Inefficient matrix multiplication
        result = []
        for i in range(len(matrix1)):
            row = []
            for j in range(len(matrix2[0])):
                sum = 0
                for k in range(len(matrix2)):
                    sum += matrix1[i][k] * matrix2[k][j]
                row.append(sum)
            result.append(row)
        return result

# Bug: I/O Bottlenecks
class FileManager:
    """
    File manager with I/O bottlenecks.
    """
    def __init__(self):
        self.buffer_size = 1024  # Bug: Small buffer size

    def read_file(self, filename: str) -> str:
        # Bug: Inefficient file reading
        content = ""
        with open(filename, "r") as f:
            while True:
                chunk = f.read(self.buffer_size)  # Bug: Small chunks
                if not chunk:
                    break
                content += chunk  # Bug: String concatenation
        return content

    def write_file(self, filename: str, content: str) -> None:
        # Bug: Inefficient file writing
        with open(filename, "w") as f:
            for i in range(0, len(content), self.buffer_size):
                f.write(content[i:i+self.buffer_size])  # Bug: Small writes

    def copy_file(self, source: str, destination: str) -> None:
        # Bug: Inefficient file copying
        with open(source, "rb") as src, open(destination, "wb") as dst:
            while True:
                chunk = src.read(self.buffer_size)  # Bug: Small chunks
                if not chunk:
                    break
                dst.write(chunk)

# Bug: Concurrency Issues
class ThreadManager:
    """
    Thread manager with concurrency issues.
    """
    def __init__(self):
        # Bug: Unbounded thread pool
        self.executor = ThreadPoolExecutor()  # Bug: No max_workers
        self.threads = []

    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Bug: Thread leak
        def process_item(item: Dict[str, Any]) -> Dict[str, Any]:
            # Bug: CPU-bound task in thread
            time.sleep(0.1)  # Bug: Simulated work
            return {k: v*2 for k, v in item.items()}

        # Bug: Inefficient thread usage
        futures = []
        for item in data:
            future = self.executor.submit(process_item, item)
            futures.append(future)

        # Bug: No thread cleanup
        return [f.result() for f in futures]

    def parallel_search(self, items: List[Dict[str, Any]],
                       query: str) -> List[Dict[str, Any]]:
        # Bug: Thread overhead for I/O
        def search_chunk(chunk: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            return [item for item in chunk if query in str(item)]

        # Bug: Inefficient chunking
        chunk_size = len(items) // os.cpu_count()
        chunks = [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]

        # Bug: No thread management
        futures = [self.executor.submit(search_chunk, chunk) for chunk in chunks]
        results = []
        for future in futures:
            results.extend(future.result())
        return results

# Bug: Process Management
class ProcessManager:
    """
    Process manager with inefficient multiprocessing.
    """
    def __init__(self):
        # Bug: Unbounded process pool
        self.pool = ProcessPoolExecutor()  # Bug: No max_workers
        self.processes = []

    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Bug: Process overhead
        def process_chunk(chunk: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            # Bug: Small work per process
            return [{k: v*2 for k, v in item.items()} for item in chunk]

        # Bug: Inefficient chunking
        chunk_size = 1  # Bug: Too small chunks
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        # Bug: No process management
        futures = [self.pool.submit(process_chunk, chunk) for chunk in chunks]
        results = []
        for future in futures:
            results.extend(future.result())
        return results

    def parallel_sort(self, items: List[int]) -> List[int]:
        # Bug: Inefficient parallel sorting
        def sort_chunk(chunk: List[int]) -> List[int]:
            # Bug: Inefficient sorting algorithm
            return sorted(chunk, reverse=True)  # Bug: Unnecessary reverse

        # Bug: Too many processes
        chunk_size = 1  # Bug: Too small chunks
        chunks = [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]

        # Bug: No process cleanup
        futures = [self.pool.submit(sort_chunk, chunk) for chunk in chunks]
        results = []
        for future in futures:
            results.extend(future.result())
        return sorted(results)  # Bug: Final sort in main process

def main():
    """
    Main function to demonstrate performance issues.
    """
    print("Code Performance Issues Demonstration:")
    print("====================================")

    try:
        # Test SearchManager
        search_manager = SearchManager()
        data = [{"id": i, "value": f"test{i}"} for i in range(1000)]
        search_manager.add_data(data)
        result = search_manager.search("test")  # Inefficient search
        print(f"SearchManager found {len(result)} results")

        # Test CacheManager
        cache_manager = CacheManager()
        for i in range(10000):
            cache_manager.set(f"key{i}", "value" * 1000)  # Memory leak
        print(f"CacheManager cache size: {len(cache_manager.cache)}")

        # Test NetworkManager
        network_manager = NetworkManager()
        urls = ["http://example.com"] * 10
        result = network_manager.fetch_data(urls)  # Blocking operations
        print(f"NetworkManager fetched {len(result)} URLs")

        # Test DataManager
        data_manager = DataManager()
        for i in range(1000):
            data_manager.add_item({"id": i, "value": f"test{i}"})  # Inefficient structure
        result = data_manager.find_item("id", 500)  # Linear search
        print(f"DataManager found item: {result}")

        # Test MathProcessor
        math_processor = MathProcessor()
        result = math_processor.calculate_fibonacci(30)  # CPU intensive
        print(f"MathProcessor fibonacci: {result}")

        # Test FileManager
        file_manager = FileManager()
        content = "test" * 1000000
        file_manager.write_file("test.txt", content)  # I/O bottleneck
        print("FileManager wrote file")

        # Test ThreadManager
        thread_manager = ThreadManager()
        data = [{"value": i} for i in range(1000)]
        result = thread_manager.process_data(data)  # Thread issues
        print(f"ThreadManager processed {len(result)} items")

        # Test ProcessManager
        process_manager = ProcessManager()
        data = [{"value": i} for i in range(1000)]
        result = process_manager.process_data(data)  # Process issues
        print(f"ProcessManager processed {len(result)} items")

    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()