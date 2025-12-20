# Locking Mechanisms: Lock and RLock

The `threading.Lock` and `threading.RLock` are the most fundamental synchronization primitives. They implement the **Mutual Exclusion (Mutex)** pattern, ensuring that only one thread can execute a critical section of code at a time.

---

## 1. `threading.Lock` (The Primitive Mutex)

A standard Lock has two states: **locked** and **unlocked**.

### Basic Usage
1.  **Creation**: `l = threading.Lock()`
2.  **Acquire**: `l.acquire()`
    -   If unlocked: Sets state to locked and returns immediately.
    -   If locked: **Blocks** (sleeps) until another thread releases it.
3.  **Release**: `l.release()`
    -   Sets state to unlocked.
    -   Wakes up *one* of the waiting threads (if any).

### The Context Manager Pattern
Always use the `with` statement. It guarantees the lock is released even if an exception occurs.

```python
import threading

balance_lock = threading.Lock()
balance = 100

def withdraw(amount):
    global balance
    # DANGEROUS WAY
    # balance_lock.acquire()
    # if amount > balance: raise ValueError("Not enough") <-- Lock never released!
    # balance -= amount
    # balance_lock.release()

    # PYTHONIC WAY
    with balance_lock:
        if balance >= amount:
            balance -= amount
```

---

## 2. `threading.RLock` (Reentrant Lock)

### The Problem with `Lock`
A standard `Lock` does not care *who* locked it. If Thread A holds the lock and tries to acquire it *again* before releasing it, **Thread A will block forever waiting for itself**. This is a self-deadlock.

```python
lock = threading.Lock()

def first_step():
    with lock:
        print("First step")
        second_step()

def second_step():
    with lock: # <--- DEADLOCK HERE! 
        # The lock is already held by this thread, but Lock() doesn't know that.
        print("Second step")
```

### The Solution: RLock
A **Reentrant Lock** allows the **same thread** to acquire the lock multiple times without blocking.
-   It keeps a counter of recursion depth.
-   `acquire()` increments the counter (if thread owns lock).
-   `release()` decrements the counter.
-   The lock is effectively released ONLY when the counter hits 0.

### Corrected Example
```python
rlock = threading.RLock()

def recursive_function(n):
    with rlock:
        if n <= 0:
            return
        print(f"Depth {n}")
        recursive_function(n-1) # Works perfectly!
```

---

## 3. When to use which?

| Feature | `Lock` | `RLock` |
| :--- | :--- | :--- |
| **Speed** | Slightly Faster | Slightly Slower (overhead of checking thread ID) |
| **Recursion** | **Deadlocks** | **Allowed** |
| **Ownership** | Can be released by *any* thread (technically) | Can ONLY be released by the owning thread |
| **Use Case** | Simple critical sections | Recursive functions, Class methods calling other methods |

### Best Practice
Start with `Lock`. Only switch to `RLock` if you have complex logic where methods call other methods that both require the same lock.
