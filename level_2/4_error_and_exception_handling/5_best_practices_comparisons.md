# Best Practices: Architecture and Design Choices

When designing Python applications, knowing *how* to catch exceptions is only half the battle. Knowing *when* to raise them (versus asserting or returning values) is what separates junior from senior developers.

---

## 1. Assert vs. Raise

A common confusion is when to use `assert` and when to `raise` an exception. They look similar but serve opposite purposes.

### `assert`: For Internal Invariants (The "This Should Never Happen" scenarios)
Assertions are for **debugging**. They declare that something is strictly true about your code's internal logic. If an assertion fails, it means there is a **bug** in your code, not an error in the user's input.

**Critical Note**: Python can be run with the `-O` (optimize) flag (e.g., `python -O script.py`). This **removes all assert statements** from the bytecode. Never use asserts for validation that is required for safety or security.

```python
def apply_discount(price, discount):
    # Internal invariant: Logic elsewhere ensures discount is never negative
    assert 0 <= discount <= 1, "Discount must be between 0 and 1"
    return price * (1 - discount)
```

### `raise`: For Predictable Runtime Errors
Exceptions are for conditions that *can* happen during normal execution (bad user input, network down, file missing). These checks must run in production.

```python
def create_user(username, age):
    # Validation constraint: User input must be valid
    if age < 0:
        raise ValueError("Age cannot be negative")
    # ... logic ...
```

| Feature | `assert` | `raise` |
| :--- | :--- | :--- |
| **Purpose** | Debugging internal logic bugs | Handling runtime errors / input validation |
| **Audience** | The Developer | The Caller / User |
| **Production** | Can be disabled (`-O`) | Always runs |
| **Handling** | Crash (AssertionError) | Catchable (`try...except`) |

---

## 2. Return vs. Raise

Coming from C or Go, you might be tempted to return error codes or `None` to indicate failure. In Python, this is generally discouraged in favor of raising exceptions.

### The Problem with "Return None" (Or Error Codes)
1.  **Ambiguity**: Does `None` mean "Wait 0 seconds" or "Calculation Failed"?
2.  **Boilerplate**: The caller *must* check the return value immediately, leading to nested `if` statements.
3.  **Silent Failures**: If the caller forgets to check, the `None` value propagates until it causes a confusing `AttributeError` far away from the source.

**Anti-Pattern (C-Style):**
```python
def divide(a, b):
    if b == 0:
        return None  # Failure
    return a / b

result = divide(10, 0)
if result is None:   # Forced check
    print("Error")
else:
    print(result + 1)
```

### The Pythonic Way: Exception Handling
Exceptions force the caller to deal with the error (or crash), which prevents undefined states.

**Pattern:**
```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

try:
    print(divide(10, 0) + 1)
except ZeroDivisionError:
    print("Error")
```

---

## 3. EAFP vs. LBYL

Python culture heavily favors **EAFP** (Easier to Ask for Forgiveness than Permission).

### LBYL (Look Before You Leap)
You check every condition before making the call. This is common in C/Java.
**Risk**: Race conditions. Between the "Check" and the "Leap", the state might change.

```python
import os

# LBYL
if os.path.exists("file.txt"):
    # What if another process deletes the file right HERE?
    with open("file.txt") as f:
        data = f.read()
else:
    print("File missing")
```

### EAFP (Easier to Ask for Forgiveness than Permission)
You just assume it works and catch the error if it doesn't. This is often faster (no double checks) and atomic (avoids race conditions).

```python
# EAFP
try:
    with open("file.txt") as f:
        data = f.read()
except FileNotFoundError:
    print("File missing")
```

### When to use which?
*   Use **EAFP** for I/O operations (files, network, DB) where race conditions are possibilities.
*   Use **LBYL** for simple local type checks or value constraints where exceptions would be too expensive or control flow is complex.

---

## 4. Duck Typing vs. `isinstance`

This is a specific subset of EAFP. Instead of checking if an object *is* a specific type (LBYL), you check if it *behaves* like that type (EAFP).

**Non-Pythonic (Type Checking):**
```python
def process(items):
    if isinstance(items, list):
        for item in items:
            print(item)
    else:
        raise TypeError("Must be a list")
```

**Pythonic (Duck Typing):**
```python
def process(items):
    try:
        iterator = iter(items)
    except TypeError:
        raise TypeError("Argument is not iterable")
        
    for item in iterator:
        print(item)
```
This allows `process` to accept lists, tuples, generators, or custom objects that implement `__iter__`.
