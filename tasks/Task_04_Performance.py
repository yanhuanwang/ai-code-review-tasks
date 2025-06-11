#!/usr/bin/env python3
"""
Task 04: Performance and Optimization Challenge

This file contains several intentional performance issues for code review practice.
The task is to identify and fix the following issues:
1. Inefficient list operations in process_data
2. Memory leak in cache implementation
3. Unnecessary database queries in get_user_stats
4. Inefficient string concatenation in generate_report
5. CPU-bound operation blocking in process_images
6. Inefficient algorithm in find_duplicates

Review the code and identify these performance issues.
"""

import time
import random
import threading
import queue
from typing import List, Dict, Set, Any, Optional
from datetime import datetime
import sqlite3
from pathlib import Path
from collections import defaultdict
import hashlib
from concurrent.futures import ThreadPoolExecutor
import weakref

# Global cache (intentional memory leak)
CACHE = {}

def process_data(data: List[int]) -> List[int]:
    """
    Process a list of numbers.
    Bug: Inefficient list operations - creating new lists repeatedly.
    """
    result = []
    # Bug: Inefficient list operations
    for i in range(len(data)):
        # Bug: Creating new list in each iteration
        result = result + [data[i] * 2]  # Should use list comprehension or append
    return result

class Cache:
    """
    Simple caching implementation.
    Bug: Memory leak - no cache size limit or cleanup.
    """
    def __init__(self):
        self._cache = {}
        self._access_count = defaultdict(int)

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        Bug: No cache invalidation or size management.
        """
        self._access_count[key] += 1
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in cache.
        Bug: Never removes old entries, causing memory leak.
        """
        self._cache[key] = value
        # Bug: No cache size management or cleanup

def get_user_stats(user_id: str) -> Dict[str, Any]:
    """
    Get user statistics from database.
    Bug: N+1 query problem and no caching.
    """
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Bug: Multiple separate queries instead of JOIN
        cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM posts WHERE user_id = ?", (user_id,))
        post_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM comments WHERE user_id = ?", (user_id,))
        comment_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM likes WHERE user_id = ?", (user_id,))
        like_count = cursor.fetchone()[0]

        return {
            'user': user[0],
            'post_count': post_count,
            'comment_count': comment_count,
            'like_count': like_count
        }

def generate_report(items: List[Dict[str, Any]]) -> str:
    """
    Generate a report from a list of items.
    Bug: Inefficient string concatenation in loop.
    """
    report = ""
    # Bug: String concatenation in loop
    for item in items:
        report += f"Item: {item['id']}\n"
        report += f"Name: {item['name']}\n"
        report += f"Value: {item['value']}\n"
        report += "---\n"
    return report

def process_images(image_paths: List[str]) -> List[str]:
    """
    Process a list of images.
    Bug: CPU-bound operation blocking main thread.
    """
    results = []
    # Bug: CPU-intensive work on main thread
    for path in image_paths:
        # Simulate CPU-intensive image processing
        time.sleep(0.1)  # Simulate work
        results.append(f"processed_{path}")
    return results

def find_duplicates(items: List[str]) -> Set[str]:
    """
    Find duplicate items in a list.
    Bug: Inefficient O(n²) algorithm.
    """
    duplicates = set()
    # Bug: O(n²) algorithm instead of using a set
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                duplicates.add(items[i])
    return duplicates

def main():
    # Test inefficient list operations
    print("Testing list operations:")
    data = list(range(1000))
    start_time = time.time()
    result = process_data(data)
    end_time = time.time()
    print(f"Processed {len(data)} items in {end_time - start_time:.2f} seconds")

    # Test memory leak in cache
    print("\nTesting cache memory leak:")
    cache = Cache()
    for i in range(1000):
        cache.set(f"key_{i}", "x" * 1000)  # Store large strings
    print(f"Cache size: {len(cache._cache)} items")
    print("Memory usage growing without bounds...")

    # Test database queries
    print("\nTesting database queries:")
    try:
        # Create test database
        with sqlite3.connect('users.db') as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (id TEXT, name TEXT);
                CREATE TABLE IF NOT EXISTS posts (user_id TEXT);
                CREATE TABLE IF NOT EXISTS comments (user_id TEXT);
                CREATE TABLE IF NOT EXISTS likes (user_id TEXT);
            """)
            conn.commit()

        start_time = time.time()
        stats = get_user_stats("user1")
        end_time = time.time()
        print(f"Retrieved user stats in {end_time - start_time:.2f} seconds")
        print(f"Stats: {stats}")
    except Exception as e:
        print(f"Database error: {e}")

    # Test string concatenation
    print("\nTesting string concatenation:")
    items = [{'id': i, 'name': f'Item {i}', 'value': i * 10} for i in range(1000)]
    start_time = time.time()
    report = generate_report(items)
    end_time = time.time()
    print(f"Generated report in {end_time - start_time:.2f} seconds")
    print(f"Report length: {len(report)} characters")

    # Test CPU-bound operations
    print("\nTesting CPU-bound operations:")
    image_paths = [f"image_{i}.jpg" for i in range(10)]
    start_time = time.time()
    processed = process_images(image_paths)
    end_time = time.time()
    print(f"Processed {len(processed)} images in {end_time - start_time:.2f} seconds")
    print("Note: Main thread was blocked during processing")

    # Test duplicate finding
    print("\nTesting duplicate finding:")
    # Create a list with some duplicates
    items = [f"item_{i % 100}" for i in range(1000)]
    start_time = time.time()
    duplicates = find_duplicates(items)
    end_time = time.time()
    print(f"Found {len(duplicates)} duplicates in {end_time - start_time:.2f} seconds")
    print(f"First few duplicates: {list(duplicates)[:5]}")

if __name__ == "__main__":
    main()