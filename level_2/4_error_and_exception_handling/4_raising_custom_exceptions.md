# Raising and Creating Custom Exceptions

While handling exceptions (`try...except`) keeps your program from crashing, **raising** exceptions (`raise`) is how you enforce rules and communicate errors to the caller. This guide covers advanced techniques for defining and raising exceptions in Python.

---

## 1. The `raise` Statement

The `raise` keyword is used to explicitly trigger an exception. You can raise instances of any class derived from `BaseException` (though usually you derive from `Exception`).

### Usage Patterns

1.  **Raising a built-in exception**:
    ```python
    def validate_age(age):
        if age < 0:
            raise ValueError("Age cannot be negative")
    ```

2.  **Raising an instance**:
    ```python
    err = ValueError("Something is wrong")
    raise err
    ```

3.  **Re-raising** (inside an `except` block):
    ```python
    try:
        process_data()
    except KeyError:
        print("Logging the error...")
        raise  # Re-raises the active KeyError exactly as is
    ```

---

## 2. Why Create Custom Exceptions?

Python has a rich set of built-in exceptions (`ValueError`, `TypeError`, `KeyError`), but they are generic. You should create custom exceptions when:
1.  **Context**: You want to distinguish *your* library's errors from standard Python errors.
2.  **Granularity**: You want callers to be able to catch specific error conditions without catching generic ones.
3.  **Payload**: You need to attach extra data (like error codes, failed inputs, or remediation steps) to the exception.

---

## 3. Defining Custom Exceptions

All custom user exceptions should inherit from `Exception`, not `BaseException` (reserved for system events like `SystemExit`).

### The Minimalist Approach
Often, a class with a meaningful name is enough. You don't need to override `__init__`.

```python
class InsufficientFundsError(Exception):
    """Raised when an account has insufficient balance for a transaction."""
    pass

# Usage
raise InsufficientFundsError("Balance is too low")
```

### The Hierarchical Approach (Best Practice)
When building a library or a module, define a **base exception** for your package. This allows users to catch **any** error from your library with one `except` block.

```python
# 1. The Base
class PaymentGatewayError(Exception):
    """Base class for all payment errors."""
    pass

# 2. Specific Errors inheriting from the Base
class AuthenticationError(PaymentGatewayError):
    pass

class TransactionDeclinedError(PaymentGatewayError):
    pass

# Usage for the Client
try:
    process_payment()
except PaymentGatewayError:
    # Catches AuthError AND TransactionDeclinedError, but NOT ValueError
    print("Payment failed, please try another method.")
```

---

## 4. Advanced: Exceptions with State (Payloads)

You can override `__init__` to accept and store more information than just a string message. This is useful for programmatic handling of the error.

```python
class HttpError(Exception):
    def __init__(self, status_code, url, message="HTTP request failed"):
        self.status_code = status_code
        self.url = url
        self.message = message
        # Initialize the base class so the standard traceback works
        super().__init__(self.message)

    def __str__(self):
        # Custom string representation
        return f"[Status {self.status_code}] {self.message} (URL: {self.url})"

# Usage
try:
    raise HttpError(404, "http://api.example.com/user", "User not found")
except HttpError as e:
    if e.status_code == 404:
        print("Resource missing, creating it now...")
    elif e.status_code == 500:
        print("Server exploded.")
    
    print(e)  # Uses our custom __str__
```

---

## 5. Best Practices

### 1. Don't hide the true error
Avoid raising generic exceptions when a specific one applies.
*   **Bad**: `raise Exception("Invalid input")` -> Forces user to catch `Exception`.
*   **Good**: `raise ValueError("Invalid input")` -> Standard and expected.
*   **Better**: `raise ValidationError("Invalid input")` -> Custom and semantic.

### 2. Suffix with 'Error'
Follow PEP 8 naming conventions. Exception classes should end with `Error` (e.g., `JSONDecodeError`, `OperationalError`).

### 3. Keep `__init__` simple
Exceptions can be pickled (execution across processes). If you store complex objects (like open file handles or lambdas) in `self.args` or attributes, pickling might fail.

### 4. Docstrings matter
Since exceptions are part of your API, document *when* they are raised.

```python
def login(username, password):
    """
    Authenticates a user.
    
    Raises:
        AuthenticationError: If credentials are invalid.
        ConnectionError: If the auth server is unreachable.
    """
    ...
```

---

## 6. Interview Questions

### Q1: Why should custom exceptions inherit from `Exception` and not `BaseException`?
**Answer**: `BaseException` is reserved for system-exiting events like `SystemExit` (`sys.exit()`) and `KeyboardInterrupt` (Ctrl+C). If your custom exception inherits from `BaseException`, a generic `except Exception:` block (which is common in main loops) will **catch** your error but **miss** the system exit signals, effectively preventing the user from stopping the program or exiting gracefully. Always use `Exception` for logic/runtime errors.

### Q2: What is the difference between `raise` and `raise e` inside an except block?
**Answer**:
*   `raise` (without arguments) re-raises the **active** exception, preserving the original stack trace exactly as it was.
*   `raise e` re-raises the specific exception object `e`. While it often looks the same, in some older Python versions or specific contexts, it might truncate the stack trace to start from the current line, losing the history of where the error *originally* occurred. **Best practice**: Use `raise` alone to propagate the original error.

### Q3: Why is it recommended to define a base exception class for a Python library?
**Answer**: It allows users of your library to catch **all** errors specific to your library with a single `except YourLibraryBaseError:` block, without having to catch `Exception` (which is too broad) or list every single exception class your library might raise. It provides granular control and better API usability.

### Q4: How do you access the arguments passed to an exception if you didn't override `__init__`?
**Answer**: Python's `BaseException` class (the parent of all exceptions) stores positional arguments passed to the constructor in the `.args` tuple attribute.
```python
try:
    raise ValueError("A", "B")
except ValueError as e:
    print(e.args) # Output: ('A', 'B')
```

