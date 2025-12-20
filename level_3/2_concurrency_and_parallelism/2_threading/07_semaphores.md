# Semaphores: Controlling Traffic

While a `Lock` allows only **one** thread to enter, a `Semaphore` allows **N** threads to enter. It is essentially a Lock with a counter.

---

## 1. Concepts

A Semaphore manages an internal counter:
-   `acquire()`: If counter > 0, decrement it and return. If counter == 0, **block** until it becomes > 0.
-   `release()`: Increment the counter and wake up a waiting thread.

### Analogy: The Nightclub Bouncer
-   **Capacity**: 50 people.
-   **Lock**: Single-occupancy restroom. Only 1 person inside.
-   **Semaphore**: The Club Entrance. 50 people can be inside. If 51st comes, they wait in line until someone leaves.

---

## 2. Practical Use Case: Rate Limiting / Pools

The most common use of Semaphores is to limit the usage of a scarce resource, like database connections or network sockets.

### Example: Connection Pool Simulation

```python
import threading
import time
import random

# Only allow 3 threads to access the database at once
db_semaphore = threading.Semaphore(value=3)

def query_database(thread_id):
    print(f"Thread {thread_id} Waiting...")
    with db_semaphore:
        print(f"Thread {thread_id} ACQUIRED connection! Running query...")
        time.sleep(random.uniform(1, 2))
        print(f"Thread {thread_id} RELEASED connection.")

threads = []
for i in range(10):
    t = threading.Thread(target=query_database, args=(i,))
    threads.append(t)
    t.start()
```

**Behavior**: You will see exactly 3 "ACQUIRED" messages, then a pause, then 1 releases and another acquires.

---

## 3. `Semaphore` vs. `BoundedSemaphore`

There is a subtle bug risk with the standard `Semaphore`.

### The Bug (Over-Release)
If you call `.release()` more times than you called `.acquire()`, the internal counter grows *beyond* the initial value.
-   Start with 3.
-   Thread A acquires (2).
-   Thread A releases (3).
-   Thread A releases AGAIN (4). -> **Now 4 threads can enter!**

### The Fix: `BoundedSemaphore`
`threading.BoundedSemaphore` checks if the counter would exceed the initial value. If so, it raises a `ValueError`.

**Recommendation**: Always use `BoundedSemaphore` unless you have a specific reason to artificially increase capacity at run-time.

---

## Summary

-   **Lock**: Mutex (1 at a time).
-   **Semaphore**: Limiter (N at a time).
-   **BoundedSemaphore**: Safe Limiter (Prevents buggy code from increasing the limit).
