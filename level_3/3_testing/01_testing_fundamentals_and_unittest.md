# Testing Fundamentals & `unittest` Framework

## 1. Introduction to Software Testing

Software testing is the process of evaluating a system or its component(s) with the intent to find whether it satisfies the specified requirements or not.

### The Testing Pyramid
A healthy testing strategy usually follows the "Testing Pyramid":

1.  **Unit Tests (Base)**:
    *   Test individual components (functions, classes) in isolation.
    *   Fast execution.
    *   High volume.
    *   Example: Testing a function that calculates the sum of two numbers.

2.  **Integration Tests (Middle)**:
    *   Test how different components work together.
    *   Slower than unit tests.
    *   Example: Testing if a service layer correctly saves data to a database.

3.  **End-to-End (E2E) Tests (Top)**:
    *   Test the entire flow from a user's perspective.
    *   Slowest and most brittle.
    *   Example: Selenium/Playwright script logging in, clicking a button, and checking the result.

## 2. Unit Testing in Python

The goal of unit testing is to isolate each part of the program and show that the individual parts are correct.

### The `unittest` Framework

Python comes with a built-in testing framework called `unittest` (inspired by Java's JUnit).

#### Key Concepts:
*   **TestCase**: A class that behaves as a test fixture.
*   **TestSuite**: A collection of test cases.
*   **TestRunner**: A component that orchestrates the execution of tests and provides the outcome.

#### Basic Boilerplate

```python
import unittest

# The code to be tested
def add(x, y):
    return x + y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

# The Test Case
class TestMathOperations(unittest.TestCase):
    
    # Lifecycle method: Runs before EACH test method
    def setUp(self):
        # Good for setting up database connections, creating temporary files, etc.
        print("Setup called")
        self.x = 10
        self.y = 5

    # Lifecycle method: Runs after EACH test method
    def tearDown(self):
        # Clean up resources
        print("Teardown called")

    # Test methods must start with 'test_'
    def test_add(self):
        result = add(self.x, self.y)
        # Assertions
        self.assertEqual(result, 15)
        self.assertNotEqual(result, 0)

    def test_divide(self):
        result = divide(self.x, self.y)
        self.assertEqual(result, 2.0)

    def test_divide_by_zero(self):
        # Context manager to check for exceptions
        with self.assertRaises(ValueError):
            divide(10, 0)

# Entry point
if __name__ == '__main__':
    unittest.main()
```

#### Common Assertions
| Method | Checks that |
| :--- | :--- |
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `bool(x) is True` |
| `assertFalse(x)` | `bool(x) is False` |
| `assertIs(a, b)` | `a is b` |
| `assertIsNone(x)` | `x is None` |
| `assertIn(a, b)` | `a in b` |
| `assertIsInstance(a, b)` | `isinstance(a, b)` |
| `assertRaises(exc, fun, *args)` | `fun(*args)` raises `exc` |

### Running `unittest`
From the CLI:
```bash
python -m unittest test_module.py
# Or auto-discovery
python -m unittest discover
```
