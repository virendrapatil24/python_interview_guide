# Lab 4: Semaphores & Deadlocks

## 1. Connection Pool (Semaphore)

### Objective
Limit concurrent access to a simulated database.

### Code
```python
import threading
import time
import random

class ConnectionPool:
    def __init__(self, size):
        # BoundedSemaphore prevents releasing more than size
        self.pool = threading.BoundedSemaphore(value=size)

    def query(self, thread_name):
        print(f"{thread_name} waiting for connection...")
        with self.pool:
            print(f"{thread_name} acquired connection!")
            # Simulate query latency
            time.sleep(random.uniform(0.5, 1.5)) 
            print(f"{thread_name} released connection.")

def main():
    pool = ConnectionPool(size=2) # Only 2 at a time
    threads = []
    
    # Spawn 5 threads
    for i in range(5):
        t = threading.Thread(target=pool.query, args=(f"Worker-{i}",))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
```

---

## 2. Creating & Fixing a Deadlock

### Objective
Show how easy it is to freeze a program by misordering locks, and the solution.

### Code (Deadlock)
```python
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def task_1():
    with lock_a:
        print("Task 1 acquired Lock A")
        time.sleep(0.1) # Wait for Task 2 to grab B
        print("Task 1 waiting for Lock B...")
        with lock_b: # BLOCKS FOREVER
            print("Task 1 acquired Lock B")

def task_2():
    with lock_b:
        print("Task 2 acquired Lock B")
        time.sleep(0.1)
        print("Task 2 waiting for Lock A...")
        with lock_a: # BLOCKS FOREVER
            print("Task 2 acquired Lock A")

# If you run this, it eventually freezes. 
# Ctrl+C to exit.
```

### The Fix: Lock Ordering
Always acquire resources in a strict global order (A then B).

```python
def task_2_fixed():
    # Even though I'm Task 2, I must respect the global order: A first.
    with lock_a: 
        with lock_b:
            print("Task 2 acquired both locks safely.")
```
