# Deep Dive: Context Managers (`with` Statement)

Context Managers are Python's mechanism for managing resources (setup and teardown) automatically. They are the backbone of the `with` statement, ensuring that resources like file handles, network connections, and locks are released reliably, even if exceptions occur.

---

## 1. The Basics: Why `with`?

Traditional `try...finally` blocks are verbose.

```python
# The Old Way
f = open("file.txt", "w")
try:
    f.write("Hello")
finally:
    f.close() # cleanup

# The Modern Way
with open("file.txt", "w") as f:
    f.write("Hello")
# f.close() is called automatically here
```

---

## 2. Protocol: `__enter__` and `__exit__`

Any class implementing these two methods is a Context Manager.

### `__enter__(self)`
*   Executed before the block starts.
*   The return value is bound to the variable after `as`.

### `__exit__(self, exc_type, exc_value, traceback)`
*   Executed after the block ends (normally or via exception).
*   Arguments describe the exception (if any).
*   **Return `True`** to suppress the exception. **Return `False` (or None)** to propagate it.

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self # Bound to 't' below

    def __exit__(self, *args):
        self.end = time.perf_counter()
        print(f"Elapsed: {self.end - self.start:.4f}s")
        # Returning None -> propagate exceptions

with Timer() as t:
    time.sleep(1)
```

---

## 3. Function-Based Managers (`contextlib`)

You don't always need a class. `contextlib.contextmanager` turns a generator into a Context Manager.
*   Code *before* `yield` runs in `__enter__`.
*   Code *after* `yield` runs in `__exit__`.

```python
from contextlib import contextmanager

@contextmanager
def temp_file(filename):
    f = open(filename, "w")
    try:
        yield f
    finally:
        f.close()
        # Allows cleanup (e.g. deleting file)
        import os
        os.remove(filename)

with temp_file("test.tmp") as f:
    f.write("temp data")
# File acts as normal during block, deleted after block
```

---

## 4. Nested Context Managers

You can open multiple contexts in one line.

```python
# Copying a file
with open("input.txt") as src, open("output.txt", "w") as dst:
    dst.write(src.read())
```

---

## 5. Standard Library Usage (Beyond Files)

Context managers are everywhere in Python.
1.  **Locks**: `with lock:` (acquires/releases thread lock).
2.  **Decimal**: `with decimal.localcontext():` (temp changes precision).
3.  **Testing**: `with pytest.raises(ValueError):` (asserts exception happens).
4.  **mock**: `with patch("module.func"):` (temporarily replaces objects).

---

## 6. Advanced: `ExitStack`

Often you need to manage a dynamic number of context managers (e.g., opening a list of files). You can't write `with f1, f2, f3...` if the list is unknown at runtime.

`contextlib.ExitStack` allows you to programmatically enter contexts.

```python
from contextlib import ExitStack

filenames = ["a.txt", "b.txt", "c.txt"]

with ExitStack() as stack:
    # 1. Dynamically enter N contexts
    files = [stack.enter_context(open(fname)) for fname in filenames]
    
    # 2. Do work
    for f in files:
        print(f.read())

# All files closed here automatically, in reverse order
```

---

## 7. Reentrant Context Managers

A "Reentrant" context manager can be reused or nested.
*   Most (like files) are **single-use**.
*   Some (like locks) are **reentrant**.

```python
lock = threading.Lock()

with lock:
    # ...
    with lock: # Deadlock! Standard Lock is NOT reentrant.
        pass

# RLock (Reentrant Lock) handles this safely.
```

---

## 8. Expert Interview Questions

### Q1: How do you suppress exceptions with a context manager?
By returning `True` in `__exit__`.
```python
class SuppressErrors:
    def __enter__(self): pass
    def __exit__(self, exc_type, exc_val, tb):
        return True # Swallows everything!

with SuppressErrors():
    raise ValueError("Ignored") 
```
*Note: `contextlib.suppress` does exactly this.*

### Q2: Is the context manager object reused?
It depends on implementation, but typically **no** for resources (files are closed on exit and can't be reopened). State cleanup happens in `__exit__`.

### Q3: What happens if `__enter__` raises an exception?
`__exit__` is **NOT** called. The cleanup code inside `__exit__` will be skipped. You must handle exceptions during setup carefully.

### Q4: Explain `async with`.
It uses `__aenter__` and `__aexit__`. These must be `async def` methods (coroutines). Used for managing async resources like DB connections in `asyncio`.
