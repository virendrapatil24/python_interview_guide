# Hands-on Testing Examples

This directory contains runnable code to practice testing concepts.

## Files
*   `app.py`: The application code (UserManager and Math functions).
*   `conftest.py`: Shared pytest fixtures (Mock Database).
*   `test_app_pytest.py`: Tests using Pytest (Best Practice).
*   `test_app_unittest.py`: Tests using unittest (Legacy/Standard Lib).

## How to Run

### Prerequisite
Install pytest and pytest-mock (and optionally coverage):
```bash
pip install pytest pytest-mock pytest-cov
```

### Running Pytest Examples
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app
```

### Running Unittest Examples
```bash
python -m unittest test_app_unittest.py
```
