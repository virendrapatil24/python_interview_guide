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
except Exception: # NOTE: Does not catch SystemExit or KeyboardInterrupt
    logging.exception("Fatal error in main loop")
```

---

## 3. Nested Try Blocks & Propagation

Exceptions propagate up the call stack. A `try` block inside another `try` block allows for granular handling.

```python
try:
    # Outer block: Handles general failures
    try:
        # Inner block: Handles specific file parsing issues
        parse_config_file()
    except ValueError:
        print("Config file format is bad, using defaults.")
        use_defaults()
    
    # If parse_config_file() raised a generic OSError, the inner except
    # missed it, so it naturally bubbles up to here.
    connect_to_db()

except OSError:
    print("System level IO failure, aborting.")
```

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

When writing libraries or abstraction layers, you often want to wrap a low-level error (like `KeyError`) into a high-level error (like `ConfigurationError`) without losing the original context.

**Implicit Chaining**: Happens automatically if an error occurs inside an `except` block.
**Explicit Chaining**: Using `raise ... from ...`.

```python
class DatabaseError(Exception):
    pass

def connect():
    try:
        _internal_connect()
    except ConnectionRefusedError as original_error:
        # Wrap the error, but attach the original cause
        raise DatabaseError("Could not connect to DB") from original_error

# When the user sees this traceback, Python will print:
# "The above exception was the direct cause of the following exception:"
```

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
