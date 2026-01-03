# Pytest: The Comprehensive Guide

Pytest is the most popular testing framework in the Python ecosystem. It is preferred over `unittest` because it is:
*   **Less verbose**: No boilerplate classes required.
*   **More readable**: Uses standard Python `assert`.
*   **Powerful**: Fixtures and plugins system.

## 1. Getting Started

### Installation
```bash
pip install pytest
```

### Basic Syntax
Unlike `unittest`, you don't need to inherit from a class. Just write functions starting with `test_`.

```python
# test_sample.py

def add(x, y):
    return x + y

def test_add():
    assert add(1, 2) == 3
```

### Running Tests
```bash
# Run all tests in current dir and subdirs
pytest

# Run specific file
pytest test_sample.py

# Run specific function in a file
pytest test_sample.py::test_add

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## 2. Test Discovery Conventions
Pytest automatically finds your tests if you follow these rules:
1.  File names start with `test_*.py` or end with `*_test.py`.
2.  Test functions start with `test_`.
3.  Test classes start with `Test` (and have no `__init__` method).

## 3. Assertions
Pytest uses Python's standard `assert` keyword. It performs "assertion rewriting" to provide detailed introspection on failure.

```python
def test_dict():
    data = {"a": 1, "b": 2}
    # If this fails, pytest shows exactly what's different!
    assert data == {"a": 1, "b": 3} 
```

validating exceptions:
```python
import pytest

def test_exception():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## 4. Fixtures: The Heart of Pytest
Fixtures are functions that run before (and optionally after) tests to set up state. They are dependency injection for tests.

### Basic Fixture
```python
import pytest

@pytest.fixture
def sample_data():
    return {"id": 1, "name": "Alice"}

# Request fixture by name as an argument
def test_data(sample_data):
    assert sample_data["name"] == "Alice"
```

### Teardown with `yield`
If you need to clean up resources (close DB, delete file), use `yield` instead of `return`.

```python
@pytest.fixture
def db_connection():
    conn = connect_to_db()
    print("Setup DB")
    yield conn  # Test runs here
    conn.close()
    print("Teardown DB")
```

### Fixture Scopes
By default, fixtures are computed **once per test function**. You can change this lifecycle.

1.  `function`: Run once per test (Default).
2.  `class`: Run once per test class.
3.  `module`: Run once per module (file).
4.  `session`: Run once per entire test session (great for expensive setups like connecting to a real DB).

```python
@pytest.fixture(scope="session")
def expensive_resource():
    # Setup
    yield resource
    # Teardown
```

### `conftest.py`
To share fixtures across multiple test files, define them in a `conftest.py` file. Pytest automatically discovers fixtures in this file. **Do not import `conftest.py` manually.**

## 5. Parametrization
Avoid writing duplicate tests for different inputs. Use `@pytest.mark.parametrize`.

```python
@pytest.mark.parametrize("input_a, input_b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -2, 8),
])
def test_addition(input_a, input_b, expected):
    assert input_a + input_b == expected
```

## 6. Markers
Markers allow you to categorize tests.

### Built-in Markers
*   `@pytest.mark.skip(reason="Not implemented yet")`: Skip a test.
*   `@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")`: Conditional skip.
*   @pytest.mark.xfail`: Expect a test to fail (useful for known bugs).

### Custom Markers
You can define your own, e.g., identifying slow tests.

```python
# test_file.py
import pytest
import time

@pytest.mark.slow
def test_heavy_computation():
    time.sleep(5)
    assert True
```

Run only slow tests:
```bash
pytest -m slow
```
(Note: You should register custom markers in `pytest.ini` to avoid warnings).

## 7. Useful CLI Flags
*   `-k "expression"`: Run tests matching a name pattern (e.g., `pytest -k "add or sub"`).
*   `--lf`: Run only the tests that failed in the last run (Looping Failures).
*   `--ff`: Run failed tests first, then the rest.
*   `--pdb`: Drop into the debugger on failure.
*   `--durations=N`: Show the N slowest tests.
