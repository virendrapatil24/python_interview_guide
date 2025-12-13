# Advanced Exception Handling in Python

This guide covers advanced patterns and internals of Python's exception handling mechanism. It goes beyond the basic `try-except` to explore robust error management strategies suitable for production-grade applications.

---

## 1. The Full Exception Block Structure

Python's exception handling isn't just `try` and `except`. The full structure includes `else` and `finally`, each serving a distinct purpose in the resource lifecycle.

```python
try:
    # 1. RUN: Risky code that might raise an exception
    resource = acquire_resource()
    result = resource.process()
except ValueError as e:
    # 2. RUN (If Error): Handle specific expected error
    log_error(e)
except (TypeError, RuntimeError) as e:
    # 3. RUN (If Error): Handle multiple error types gracefully
    recover_from_runtime_error(e)
except Exception:
    # 4. RUN (If Error): Catch-all for unexpected errors (use sparingly!)
    log_critical_failure()
    raise  # Re-raise to ensure the crash is visible up the stack
else:
    # 5. RUN (If NO Error): content that requires the try block to succeed
    # Placing code here prevents catching exceptions that you didn't intend to protect.
    # It also clearly separates "risky" code from "dependent" code.
    confirm_success(result)
finally:
    # 6. RUN (ALWAYS): Cleanup code. Runs whether an exception occurred or not.
    # Even if the 'try' block has a 'return' statement, this still runs!
    resource.close()
```

### The `pass` Statement
Using `pass` in an `except` block explicitly swallows the error.
**Warning**: This is generally bad practice ("silent failure") unless you are 100% sure the error is irrelevant.
```python
try:
    os.remove("temp_file.txt")
except FileNotFoundError:
    pass # It's fine if the file is already gone
```

---

## 2. Advanced Handling Patterns

### Handling Multiple Exceptions
You can catch multiple specific exceptions in a single line using a tuple. This is cleaner than duplicating code in separate blocks.
```python
try:
    check_status()
except (ConnectionError, TimeoutError) as e:
    retry_connection()
```

### General Exception Logging (The "Catch-All")
When building services, you often want to catch *everything* at the top level to prevent the server from crashing, but you MUST log it.
```python
import logging

try:
    main_loop()
except Exception as e: # NOTE: Does not catch SystemExit or KeyboardInterrupt
    logging.exception(f"Fatal error in main loop: {e}")
```

---

## 3. Nested Try Blocks & Propagation

Exceptions bubble up (propagate) through the call stack until they encounter a matching `except` block. Nesting `try` blocks allows you to handle specific, recoverable errors locally while letting more severe or unexpected errors ripple up to a general handler.

### How Propagation Works
1.  **Inner Try**: Python attempts to execute code here.
2.  **Inner Exception**: Upon an error, Python checks the **inner** `except` blocks.
3.  **Match Found**: If a match is found, the inner handler executes, and execution continues **after the inner block** (not the outer one, unless re-raised).
4.  **No Match (Propagation)**: If no match is found, the exception bubbles up to the **outer** `try` block.
5.  **Outer Exception**: Python now checks the **outer** `except` blocks.

### Detailed Example

```python
def main_process():
    print("Start Main Process")
    try:
        # Outer block: The safety net
        print("  Entering Outer Try")
        
        try:
            # Inner block: The specific risky operation
            print("    Attempting risky operation...")
            # Uncomment one line below to test different scenarios:
            # raise ValueError("Invalid input")   # Scenario A
            # raise OSError("Disk full")          # Scenario B
            # raise KeyError("Missing key")       # Scenario C (Uncaught)
            print("    Success!")
            
        except ValueError as e:
            # Handles ONLY ValueError locally
            print(f"    (Inner Catch) Recovered from: {e}")
            # Execution continues in the outer block
        
        print("  Continuing Outer Block execution...")
        
    except OSError as e:
        # Handles OSError from ANYWHERE in the outer block (including inner)
        print(f"  (Outer Catch) System error detected: {e}")
        
    except Exception as e:
        # Catch-all for anything else (like KeyError)
        print(f"  (Outer Catch) Unexpected crash: {e}")
        
    print("End Main Process")
```

### Execution Scenarios
Here is exactly what happens in different situations based on the code above:

**Scenario A: `ValueError` is raised**
1. Inner `try` raises `ValueError`.
2. check inner `except ValueError`: **MATCH**.
3. Prints: `(Inner Catch) Recovered from: Invalid input`.
4. Inner block finishes.
5. Outer block continues: Prints `Continuing Outer Block execution...`.
6. Prints: `End Main Process`.

**Scenario B: `OSError` is raised**
1. Inner `try` raises `OSError`.
2. Check inner `except ValueError`: **NO MATCH**.
3. Exception **propagates** to outer `try`.
4. Outer block stops executing immediately (skips `Continuing Outer Block...`).
5. Check outer `except OSError`: **MATCH**.
6. Prints: `(Outer Catch) System error detected: Disk full`.
7. Prints: `End Main Process`.

**Scenario C: `KeyError` is raised** (Unanticipated error)
1. Inner `try` raises `KeyError`.
2. Check inner `except`: **NO MATCH**.
3. Propagates to outer `try`.
4. Check outer `except OSError`: **NO MATCH**.
5. Check outer `except Exception`: **MATCH**.
6. Prints: `(Outer Catch) Unexpected crash: Missing key`.
7. Prints: `End Main Process`.

---

## 4. Re-raising Exceptions

Sometimes you catch an exception to perform a side effect (like logging) but you still want the error to propagate.

```python
try:
    process_payment()
except PaymentError:
    logger.error("Payment failed")
    raise # Re-raises the exact active exception, preserving the stack trace
```

---

## 5. Exception Chaining (PEP 3134)

Exception chaining solves a specific problem: **How do we report a high-level error to the user without losing the technical details of what actually went wrong?**

### The Problem
Imagine you are writing a database library. If a low-level `socket.error` occurs, you don't want to crash the user's app with a raw socket error. You want to tell them "Database Connection Failed". *But*, for debugging, you still need to see that it was a socket error, not an authentication error.

### Explicit Chaining (`raise ... from e`)
This allows you to wrap an exception while pointing to the original cause. The `__cause__` attribute is set on the new exception.

```python
class DatabaseConnectionError(Exception):
    pass

def connect_to_db():
    try:
        # Simulate a low-level networking error
        raise ConnectionRefusedError("Port 5432 unreachable")
    except ConnectionRefusedError as original_e:
        # Wrap it in our custom error, but Keep the Link
        raise DatabaseConnectionError("DB Connection Failed") from original_e

# Execution Result:
# 1. Python prints the ConnectionRefusedError traceback.
# 2. Python prints: "The above exception was the direct cause of the following exception:"
# 3. Python prints the DatabaseConnectionError traceback.
```

### Suppressing Context (`raise ... from None`)
Sometimes, the original error is "noise" or implementation detail that you explicitly want to hide from the user (or the logs). You can use `from None` to disable chaining.

```python
def load_config():
    try:
        # We try to open a file, but it fails
        raise FileNotFoundError("config.json missing")
    except FileNotFoundError:
        # We don't care WHY it failed, just that configuration is invalid.
        # "from None" tells Python: "Forget the previous error, start fresh here."
        raise RuntimeError("Configuration failed to load") from None

# Execution Result:
# Python ONLY prints the RuntimeError. The FileNotFoundError is gone.
```

### Implicit Chaining
If you raise an exception *while handling another exception* (and don't use `from`), Python allows you to see both, noting that "During handling of the above exception, another exception occurred". This usually indicates a bug in your error handler (e.g., trying to log an error to a file that is read-only).

---

## 6. Traceback and Logging

For advanced debugging, you often need the raw string of the traceback without crashing the program.

```python
import traceback

try:
    1 / 0
except ZeroDivisionError:
    # Get the traceback as a string
    tb_str = traceback.format_exc()
    print(f"I caught an error, here is where it happened:\n{tb_str}")
```

---

## 7. Global Exception Hooks (`sys.excepthook`)

What happens if an exception is NOT caught by any try/except block? Python calls `sys.excepthook`. You can override this to implement global "crash reporting".

```python
import sys

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print("CRITICAL: Uncaught exception occurred!")
    # Send email to developer, log to Sentry/Datadog, etc.
    print(f"Type: {exc_type}, Message: {exc_value}")

sys.excepthook = global_exception_handler
# Now any unhandled crash will go through your function first
```

---

## 8. Signal Handling

Some "errors" come from the OS, like the user hitting `Ctrl+C` (SIGINT). While Python turns SIGINT into `KeyboardInterrupt`, other signals require the `signal` module.

```python
import signal
import sys
import time

def graceful_shutdown(signum, frame):
    print(f"\nReceived signal {signum}. Cleaning up...")
    # Close DB connections, save buffers, etc.
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

print("Running... (Press Ctrl+C to test)")
while True:
    time.sleep(1)
```
