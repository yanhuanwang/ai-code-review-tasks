#!/usr/bin/env python3
"""
Task 07: Concurrency and Threading Challenge

This file contains several intentional concurrency and threading issues for code review practice.
The task is to identify and fix the following issues:
1. Race condition in BankAccount
2. Deadlock in ResourceManager
3. Thread safety issues in Cache
4. Improper thread synchronization in TaskQueue
5. Resource starvation in WorkerPool
6. Improper thread cleanup in ImageProcessor
7. Lost updates in Counter
8. Improper use of threading primitives in MessageBroker

Review the code and identify these concurrency and threading issues.
"""

import threading
import time
import queue
import random
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Lock, RLock, Event, Condition
import uuid

# Global logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankAccount:
    """
    Represents a bank account with balance operations.
    Bug: Race condition in balance updates.
    """
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self._balance = initial_balance
        # Bug: No lock for balance updates

    def deposit(self, amount: float) -> None:
        """Deposit money into account."""
        # Bug: Race condition - non-atomic operation
        current_balance = self._balance
        time.sleep(0.1)  # Simulate processing time
        self._balance = current_balance + amount

    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account."""
        # Bug: Race condition - non-atomic operation
        if self._balance >= amount:
            current_balance = self._balance
            time.sleep(0.1)  # Simulate processing time
            self._balance = current_balance - amount
            return True
        return False

    @property
    def balance(self) -> float:
        """Get current balance."""
        return self._balance

class ResourceManager:
    """
    Manages access to shared resources.
    Bug: Potential deadlock in resource acquisition.
    """
    def __init__(self):
        self._resources: Dict[str, threading.Lock] = {}
        self._resource_locks: Dict[str, threading.Lock] = {}

    def acquire_resource(self, resource_id: str) -> bool:
        """Acquire a resource."""
        # Bug: Potential deadlock - locks acquired in different order
        if resource_id not in self._resources:
            self._resources[resource_id] = threading.Lock()
            self._resource_locks[resource_id] = threading.Lock()

        # Bug: Nested locks without proper ordering
        self._resource_locks[resource_id].acquire()
        try:
            self._resources[resource_id].acquire()
            return True
        except Exception:
            self._resource_locks[resource_id].release()
            return False

    def release_resource(self, resource_id: str) -> None:
        """Release a resource."""
        # Bug: Locks released in wrong order
        if resource_id in self._resources:
            self._resources[resource_id].release()
            self._resource_locks[resource_id].release()

class Cache:
    """
    Thread-safe cache implementation.
    Bug: Thread safety issues in cache operations.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._access_count: Dict[str, int] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        # Bug: Incomplete thread safety - access count not protected
        if key in self._cache:
            self._access_count[key] = self._access_count.get(key, 0) + 1
            return self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        # Bug: Incomplete thread safety - partial lock coverage
        with self._lock:
            self._cache[key] = value
        self._access_count[key] = 0  # Bug: Not protected by lock

    def clear(self) -> None:
        """Clear the cache."""
        # Bug: Incomplete thread safety - access count not cleared
        with self._lock:
            self._cache.clear()

class TaskQueue:
    """
    Queue for managing tasks.
    Bug: Improper thread synchronization.
    """
    def __init__(self):
        self._queue = queue.Queue()
        self._processing = set()
        self._lock = threading.Lock()
        # Bug: Missing condition variable for task completion

    def add_task(self, task_id: str, task_data: Any) -> None:
        """Add a task to the queue."""
        with self._lock:
            self._processing.add(task_id)
        self._queue.put((task_id, task_data))

    def get_task(self) -> Optional[tuple]:
        """Get next task from queue."""
        # Bug: No proper synchronization for task processing
        try:
            task_id, task_data = self._queue.get_nowait()
            return task_id, task_data
        except queue.Empty:
            return None

    def mark_complete(self, task_id: str) -> None:
        """Mark a task as complete."""
        # Bug: No notification of task completion
        with self._lock:
            self._processing.discard(task_id)

class WorkerPool:
    """
    Pool of worker threads.
    Bug: Resource starvation and improper thread management.
    """
    def __init__(self, max_workers: int = 4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._active_tasks = set()
        self._lock = threading.Lock()
        # Bug: No task queue or work distribution mechanism

    def submit_task(self, task_func: callable, *args, **kwargs) -> None:
        """Submit a task to the worker pool."""
        # Bug: No limit on active tasks
        with self._lock:
            if len(self._active_tasks) >= self._executor._max_workers:
                # Bug: Busy waiting
                while len(self._active_tasks) >= self._executor._max_workers:
                    time.sleep(0.1)

        future = self._executor.submit(task_func, *args, **kwargs)
        with self._lock:
            self._active_tasks.add(future)

        # Bug: No proper task completion handling
        future.add_done_callback(self._task_done)

    def _task_done(self, future) -> None:
        """Handle task completion."""
        # Bug: No error handling
        with self._lock:
            self._active_tasks.discard(future)

class ImageProcessor:
    """
    Processes images using multiple threads.
    Bug: Improper thread cleanup and resource management.
    """
    def __init__(self):
        self._workers = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        # Bug: No proper thread cleanup mechanism

    def start_processing(self, image_paths: List[str]) -> None:
        """Start processing images."""
        for path in image_paths:
            # Bug: Threads not properly managed
            worker = threading.Thread(
                target=self._process_image,
                args=(path,),
                daemon=True  # Bug: Daemon threads might be killed abruptly
            )
            self._workers.append(worker)
            worker.start()

    def _process_image(self, image_path: str) -> None:
        """Process a single image."""
        # Bug: No proper resource cleanup
        try:
            # Simulate image processing
            time.sleep(random.uniform(0.1, 0.5))
            logger.info(f"Processed image: {image_path}")
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")

    def stop_processing(self) -> None:
        """Stop all processing threads."""
        # Bug: No proper thread cleanup
        self._stop_event.set()
        for worker in self._workers:
            worker.join(timeout=1.0)  # Bug: Hard-coded timeout

class Counter:
    """
    Thread-safe counter implementation.
    Bug: Lost updates due to improper synchronization.
    """
    def __init__(self):
        self._value = 0
        # Bug: No proper synchronization primitive

    def increment(self) -> None:
        """Increment the counter."""
        # Bug: Lost updates - non-atomic operation
        current = self._value
        time.sleep(0.1)  # Simulate processing
        self._value = current + 1

    def decrement(self) -> None:
        """Decrement the counter."""
        # Bug: Lost updates - non-atomic operation
        current = self._value
        time.sleep(0.1)  # Simulate processing
        self._value = current - 1

    @property
    def value(self) -> int:
        """Get current counter value."""
        return self._value

class MessageBroker:
    """
    Message broker for inter-thread communication.
    Bug: Improper use of threading primitives.
    """
    def __init__(self):
        self._messages = queue.Queue()
        self._subscribers: Dict[str, List[callable]] = {}
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        # Bug: Condition variable used incorrectly

    def subscribe(self, topic: str, callback: callable) -> None:
        """Subscribe to a topic."""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)

    def publish(self, topic: str, message: Any) -> None:
        """Publish a message to a topic."""
        # Bug: Condition variable used without proper wait/notify
        with self._condition:
            self._messages.put((topic, message))
            # Bug: Notify all subscribers even if not waiting
            self._condition.notify_all()

    def process_messages(self) -> None:
        """Process messages in the queue."""
        while True:
            # Bug: No proper message processing synchronization
            try:
                topic, message = self._messages.get_nowait()
                with self._lock:
                    if topic in self._subscribers:
                        for callback in self._subscribers[topic]:
                            callback(message)
            except queue.Empty:
                time.sleep(0.1)  # Bug: Busy waiting

def main():
    # Test BankAccount race condition
    print("Testing BankAccount race condition:")
    account = BankAccount("acc1", 1000.0)
    threads = []

    def deposit_task():
        for _ in range(100):
            account.deposit(10.0)

    def withdraw_task():
        for _ in range(100):
            account.withdraw(10.0)

    for _ in range(5):
        threads.append(threading.Thread(target=deposit_task))
        threads.append(threading.Thread(target=withdraw_task))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"Final balance: {account.balance}")  # Should be 1000.0

    # Test ResourceManager deadlock
    print("\nTesting ResourceManager deadlock:")
    manager = ResourceManager()

    def acquire_resources():
        # Simulate potential deadlock
        manager.acquire_resource("A")
        time.sleep(0.1)
        manager.acquire_resource("B")
        manager.release_resource("B")
        manager.release_resource("A")

    threads = [threading.Thread(target=acquire_resources) for _ in range(2)]
    for t in threads:
        t.start()

    for t in threads:
        t.join(timeout=2.0)  # Timeout to prevent infinite wait

    # Test Cache thread safety
    print("\nTesting Cache thread safety:")
    cache = Cache()

    def cache_operations():
        for i in range(100):
            cache.set(f"key_{i}", i)
            cache.get(f"key_{i}")

    threads = [threading.Thread(target=cache_operations) for _ in range(4)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Test TaskQueue synchronization
    print("\nTesting TaskQueue synchronization:")
    task_queue = TaskQueue()

    def process_tasks():
        while True:
            task = task_queue.get_task()
            if task is None:
                break
            task_id, _ = task
            time.sleep(0.1)  # Simulate processing
            task_queue.mark_complete(task_id)

    # Add some tasks
    for i in range(10):
        task_queue.add_task(f"task_{i}", f"data_{i}")

    # Start processing
    threads = [threading.Thread(target=process_tasks) for _ in range(2)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Test WorkerPool resource starvation
    print("\nTesting WorkerPool resource starvation:")
    pool = WorkerPool(max_workers=2)

    def long_task(task_id: str):
        time.sleep(1.0)  # Simulate long-running task
        print(f"Completed task {task_id}")

    # Submit more tasks than workers
    for i in range(5):
        pool.submit_task(long_task, f"task_{i}")

    time.sleep(6.0)  # Wait for tasks to complete

    # Test ImageProcessor thread cleanup
    print("\nTesting ImageProcessor thread cleanup:")
    processor = ImageProcessor()
    processor.start_processing([f"image_{i}.jpg" for i in range(5)])
    time.sleep(1.0)
    processor.stop_processing()

    # Test Counter lost updates
    print("\nTesting Counter lost updates:")
    counter = Counter()

    def counter_operations():
        for _ in range(100):
            counter.increment()
            counter.decrement()

    threads = [threading.Thread(target=counter_operations) for _ in range(4)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"Final counter value: {counter.value}")  # Should be 0

    # Test MessageBroker threading primitives
    print("\nTesting MessageBroker threading primitives:")
    broker = MessageBroker()

    def message_handler(message: Any):
        print(f"Received message: {message}")

    broker.subscribe("test", message_handler)
    broker.publish("test", "Hello, World!")

    # Start message processing in a separate thread
    processor = threading.Thread(target=broker.process_messages, daemon=True)
    processor.start()

    time.sleep(1.0)  # Wait for message processing

if __name__ == "__main__":
    main()