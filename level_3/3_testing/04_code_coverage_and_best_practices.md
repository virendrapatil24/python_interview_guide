# Code Coverage & Best Practices

## 1. Understanding Code Coverage

Code coverage is a metric used to measure the percentage of your source code executed when tests are run.

*   **Line Coverage**: Has this line of code been executed?
*   **Branch Coverage**: Have both the `True` and `False` paths of an `if` statement been executed?

### Limitations
High coverage != High Quality.
coverage tells you what code was *executed*, not if it was *verified*. You can execute code without asserting anything about its behavior.

## 2. Using `pytest-cov`

`pytest-cov` is a plugin that integrates the `coverage.py` tool with pytest.

### Installation
```bash
pip install pytest-cov
```

### Running Coverage
```bash
# Run tests and report coverage for the current directory
pytest --cov=.

# Report coverage for a specific package
pytest --cov=my_package
```

### Output Formats
```bash
# Terminal report (default)
pytest --cov=my_app

# HTML report (Detailed view with highlighted source code)
pytest --cov=my_app --cov-report=html
# Open htmlcov/index.html to view
```

### Configuration
You can configure coverage rules in `.coveragerc` or `pyproject.toml`.

Example `.coveragerc`:
```ini
[run]
# Measure branch coverage
branch = True
omit = 
    */tests/*
    */migrations/*

[report]
# Fail if coverage is below 90%
fail_under = 90
show_missing = True
```

## 3. Best Practices for Testing

### 1. Arrange-Act-Assert (AAA)
Structure your tests clearly:
*   **Arrange**: Prepare inputs and targets.
*   **Act**: Perform the operation.
*   **Assert**: Verify the results.

```python
def test_sort():
    # Arrange
    input_list = [3, 1, 2]
    
    # Act
    result = sorted(input_list)
    
    # Assert
    assert result == [1, 2, 3]
```

### 2. Test Behavior, Not Implementation
Avoid testing internal "private" methods or implementation details. Test the public API. If you refactor the code (change implementation generally) but keep the behavior the same, your tests should NOT fail.

### 3. Keep Tests Independent
One test should not depend on the state left by another. Pytest creates a fresh instance of the test function, but global state (DB, files) must be reset (use fixtures with tear down).

### 4. Descriptive Names
*   `test_add` (Bad)
*   `test_add_two_positive_numbers_returns_sum` (Good)
*   `test_add_negative_numbers` (Good)

### 5. Deterministic Tests
Tests should pass or fail consistently.
*   Avoid `random` directly (seed it).
*   Avoid depending on system time (mock it).
*   Avoid relying on network calls (mock them).
