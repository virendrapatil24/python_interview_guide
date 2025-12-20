# Native OS Threads in Python

A common misconception is that Python's `threading` module implements "Green Threads" or "Simulated Threads" because of the GIL limitation. This is **incorrect**.

## 1. The Reality: 1:1 Mapping

Python's `threading.Thread` maps **1:1** to a native Operating System thread.
-   **Linux/macOS**: Uses `pthread` (POSIX Threads).
-   **Windows**: Uses Windows Native Threads.

When you create a thread in Python, the OS kernel is aware of it. The OS scheduler manages its execution, priority, and context switching. This means Python threads are "heavyweight" compared to coroutines (AsyncIO) or Go routines.

### Checking Functionality
You can actually see these threads in your OS monitor (like `htop` or Activity Monitor) if your Python script spawns enough of them.

```python
import threading
import os

def print_ids():
    # Native Thread ID (OS assigned)
    print(f"Native OS Thread ID: {threading.get_native_id()}")
    # Python's internal Thread ID
    print(f"Python Identifier: {threading.get_ident()}")

t = threading.Thread(target=print_ids)
t.start()
t.join()
```

---

## 2. Managing the Lifecycle

### Starting
Threads don't start until `.start()` is called. Creating the object is cheap; calling `.start()` triggers the OS system call (`clone` or `CreateThread`), which is expensive.

### Joining
`.join()` blocks the calling thread until the target thread terminates. This is crucial for program flow control to ensure tasks complete before exiting.

### Daemon vs Non-Daemon
This is a frequent interview question.

-   **Non-Daemon (Default)**: The Python program **will not exit** as long as at least one non-daemon thread is running, even if the Main Thread has finished.
-   **Daemon (`daemon=True`)**: These are "background" threads. The Python program **kills them instantly** and exits as soon as all non-daemon threads (usually just the Main Thread) are done.

**Use Cases**:
-   *Non-Daemon*: Processing critical data (must finish).
-   *Daemon*: Heartbeat ping, Autosave, Garbage collection monitoring (can die anytime).

```python
# Daemon Example
t = threading.Thread(target=background_task, daemon=True)
t.start()
# The script ends immediately after this line, killing 't' instantly.
```

---

## 3. The Threading Module Hierarchy

The `threading` module is a high-level wrapper around the low-level `_thread` module (which you should rarely use).

-   `threading.current_thread()`: Returns the Thread object representing the caller.
-   `threading.main_thread()`: Returns the main thread object.
-   `threading.enumerate()`: Returns a list of all active thread objects.

---

## 4. Advanced: Native Stack Size

Since Python threads are real OS threads, they have a fixed stack size (usually 8MB on Unix, configurable). This limits the maximum recursion depth and the maximum number of threads you can spawn before hitting `MemoryError` (OOM).

-   Reference: `threading.stack_size()` can tune this.
-   Compare: AsyncIO coroutines don't have this OS stack limit, allowing millions of concurrent tasks.

## Summary

-   Python threads are real system threads.
-   They are scheduled by the OS, not the Python interpreter (though the interpreter strictly restricts them via GIL).
-   Daemon threads terminate abruptly; Non-daemon threads keep the app alive.
