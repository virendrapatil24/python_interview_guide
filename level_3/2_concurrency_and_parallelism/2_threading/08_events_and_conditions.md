# Communication: Events and Conditions

Locks ensure threads don't step on each other. Events and Conditions ensure threads can **talk** to each other ("I'm done, you can start").

---

## 1. `threading.Event` (The Simple Signal)

An `Event` is a simple Thread-Safe boolean flag.
-   **Threads wait** for the flag to be True.
-   **One thread sets** the flag to True.
-   **Result**: All waiting threads wake up simultaneously (Broadway).

### Operations
-   `e = threading.Event()` (Starts False)
-   `e.wait()`: Blocks until flag is True.
-   `e.set()`: Sets flag to True. Wakes everyone.
-   `e.clear()`: Resets flag to False.

### Use Case: Application Startup
The main thread initializes the database. Worker threads wait until the DB is ready.

```python
import threading
import time

db_ready = threading.Event()

def worker(w_id):
    print(f"Worker {w_id} waiting for DB...")
    db_ready.wait() # <--- Block here
    print(f"Worker {w_id} starting work!")

# Start workers
for i in range(3):
    threading.Thread(target=worker, args=(i,)).start()

print("Main: Initializing DB...")
time.sleep(2)
print("Main: DB Ready!")
db_ready.set() # <--- Wakes all 3 workers instantly
```

---

## 2. `threading.Condition` (Advanced Coordination)

A `Condition` variable is a combination of a **Lock** and an **Event**. It is used when threads need to wait for a *specific state* change (e.g., "Queue is not empty").

### The Producer-Consumer Pattern
Using raw events is inefficient for a queue:
-   Producer adds item. `event.set()`.
-   All 10 consumers wake up.
-   Consumer 1 gets item.
-   Consumer 2-10 find queue empty again. (Thundering Herd Problem).

### Condition Operations
-   **Must wrap in `with condition:`**.
-   `wait()`: Releases lock, sleeps. When woken, re-acquires lock.
-   `notify(n=1)`: Wakes up `n` waiting threads.
-   `notify_all()`: Wakes up everyone.

### Example: Producer-Consumer

```python
import threading
import collections

queue = collections.deque()
cv = threading.Condition()

def producer():
    for i in range(5):
        with cv:
            print(f"Producing {i}")
            queue.append(i)
            cv.notify() # Wake up ONE consumer
        time.sleep(1)

def consumer():
    while True:
        with cv:
            while not queue: # IMPORTANT: Always check condition in a loop!
                print("Consumer waiting...")
                cv.wait() # Drops lock, sleeps. Re-acquires on wake.
            
            item = queue.popleft()
            print(f"Consumed {item}")
```

**Why `while not queue`?**
Because strictly speaking, `wait()` can return arbitrarily (spurious wakeups), or another consumer could steal the item between the `notify` and the lock re-acquisition.

---

## Summary

| Primitive | Purpose | Analogy |
| :--- | :--- | :--- |
| **Event** | One-Time broadcast | Traffic Light (Red/Green). |
| **Condition** | State based coordination | Waiting Room. "Doctor is ready for *next* patient". |
