# Deep Dive: Pytest

Pytest is the de-facto standard for testing in Python, superior to the built-in `unittest` due to its simplicity, fixtures, and powerful plugin ecosystem.

---

## 1. The Power of `assert`

`unittest` required `self.assertEqual(a, b)`.
Pytest uses standard Python asserts: `assert a == b`.
*   **Magic**: Pytest rewrites the AST of your test code to provide detailed introspection (it shows you *why* the assertion failed with values).

---

## 2. Fixtures and Scope

Fixtures are functions that run before (and optionally after) tests to set up state (DB connections, test data).
**Dependency Injection**: Tests request fixtures by name.

```python
import pytest

@pytest.fixture(scope="module")
def db_connection():
    print("Connecting to DB...")
    conn = connect_db()
    yield conn  # Test runs here
    print("Closing DB...")
    conn.close()

def test_query(db_connection):
    assert db_connection.query("SELECT 1") == 1
```

**Scopes**:
*   `function` (default): Setup once per test.
*   `class`: Once per class.
*   `module`: Once per file.
*   `session`: Once per entire test run (great for Docker containers).

---

## 3. Parametrization

Run the same test with different inputs. Reduces code duplication.

```python
@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
def test_eval(input, expected):
    assert eval(input) == expected
```

---

## 4. `conftest.py`

A special file in Pytest.
*   Fixtures defined here are automatically available to all tests in the directory (and subdirectories).
*   No need to `import` fixtures.

---

## 5. Plugins

*   `pytest-cov`: Coverage reporting.
*   `pytest-xdist`: Run tests in parallel (`-n auto`).
*   `pytest-django` / `pytest-flask`: Framework integration.
