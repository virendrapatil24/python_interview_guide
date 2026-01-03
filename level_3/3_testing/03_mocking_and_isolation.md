# Mocking and Isolation

Mocking is a technique to replace parts of your system under test with "fake" objects. This allows you to test a component in isolation without relying on external dependencies like databases, APIs, or filesystems.

## 1. Concepts

*   **Mock**: An object that records interactions (method calls, arguments).
*   **Stub**: An object that returns predefined data.
*   **Patching**: The act of replacing a real object with a mock during a test.

## 2. `unittest.mock`

Python's standard library provides `unittest.mock`.

### `Mock` vs `MagicMock`
*   `Mock`: A flexible object that creates attributes and methods as you access them.
*   `MagicMock`: A subclass of `Mock` that pre-configures magic methods (e.g., `__len__`, `__getitem__`, `__str__`). **Use this by default.**

```python
from unittest.mock import MagicMock

# Create a mock
mock_api = MagicMock()

# Configure return value
mock_api.get_user.return_value = {"id": 1, "name": "Bob"}

# Use it
result = mock_api.get_user(1)
assert result["name"] == "Bob"

# Verify interaction
mock_api.get_user.assert_called_with(1)
```

### Side Effects
You can simulate exceptions or dynamic returns using `side_effect`.

```python
mock_api.get_user.side_effect = TimeoutError("Connection lost")

# Calling this now raises the exception
try:
    mock_api.get_user(1)
except TimeoutError:
    print("Caught expected error")
```

Or return different values for sequential calls:
```python
m = MagicMock(side_effect=[1, 2, 3])
print(m(), m(), m()) # Prints 1, 2, 3
```

## 3. Patching (`patch`)

The `patch` decorator (or context manager) replaces an object with a Mock for the duration of the test.

**CRITICAL RULE**: "Patch where it is used, not where it is defined."

If `my_module.py` imports `helper` from `utils.py`:
```python
# my_module.py
from utils import helper

def do_work():
    return helper()
```

You must patch `my_module.helper`, NOT `utils.helper`.

```python
from unittest.mock import patch
import my_module

# Decorator style
@patch('my_module.helper')
def test_do_work(mock_helper):
    mock_helper.return_value = "Mocked Result"
    
    result = my_module.do_work()
    
    assert result == "Mocked Result"
    mock_helper.assert_called_once()
```

## 4. Pytest-Mock Plugin

While you can use `unittest.mock` in pytest, the `pytest-mock` plugin provides a cleaner fixture called `mocker`.

### Installation
```bash
pip install pytest-mock
```

### Usage
It automatically undoes patches after the test, even if it fails. It uses the same API as `unittest.mock.patch` but wraps it in `.patch`.

```python
def test_with_mocker(mocker):
    # Same as @patch('os.remove')
    mock_remove = mocker.patch('os.remove')
    
    import os
    os.remove("fake_file.txt")
    
    mock_remove.assert_called_once_with("fake_file.txt")
```

### Mocking Properties
```python
mocker.patch.object(MyClass, 'my_property', new_callable=mocker.PropertyMock).return_value = 42
```

## 5. When NOT to Mock
*   **Value Objects/Data Classes**: Just use the real objects.
*   **Built-ins**: Avoid mocking `open()`, `datetime.now()` unless absolutely necessary (use libraries like `freezegun` for time).
*   **Too much**: If you are mocking everything, you might be testing implementation details, not behavior.
