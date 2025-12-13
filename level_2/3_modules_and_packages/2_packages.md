# Python Packages: Structuring Large Projects

As your project grows, a single folder of modules becomes messy. You need **Packages**.

## 1. What is a Package?

A **Package** is simply a directory containing multiple modules (and usually a special `__init__.py` file). It allows you to organize modules hierarchically.

**Structure Example:**
```
my_project/
    main.py
    ecommerce/          <-- Package
        __init__.py
        database.py
        payments.py
        utils/          <-- Sub-Package
            __init__.py
            math.py
```

## 2. The Role of `__init__.py`

The `__init__.py` file is what tells Python "Treat this directory as a package."

### A. Initialization
Code inside `__init__.py` runs **automatically** the first time the package is imported. You can use it to initialize package-level variables.

### B. Simplifying Imports (Exports)
This is the most common use case. By default, importing a package **does not** import its sub-modules. You have to be explicit.

**Without `__init__.py` logic:**
```python
# main.py
import ecommerce.database
import ecommerce.payments

ecommerce.database.connect()
```

**With `__init__.py` logic:**
You can expose key functions directly at the package level.

```python
# ecommerce/__init__.py
from .database import connect
from .payments import process_payment
```

 Now in `main.py`, the import is cleaner:
```python
# main.py
import ecommerce

ecommerce.connect() # Works!
ecommerce.process_payment()
```

## 3. Namespace Packages (Advanced)

**Interview Question:** "Is `__init__.py` mandatory?"

-   **Python 2:** Yes. Without it, the folder is just a folder, not a package.
-   **Python 3.3+:** No. "Implicit Namespace Packages" allow you to have a package without `__init__.py`. 

**Why use Namespace Packages?**
It allows a single package to be split across multiple directories (and even multiple separate installed distributions). However, for standard projects, **it is still best practice** to include `__init__.py` to avoid ambiguity and provide initialization logic.

## 4. Importing from Packages

### Absolute Imports (Recommended)
You specify the full path starting from the project root.

```python
# Inside ecommerce/utils/math.py
from ecommerce.database import connect
```

### Relative Imports
You use dots `.` to indicate the current or parent directory.
-   `.`: Current directory.
-   `..`: Parent directory.

```python
# Inside ecommerce/utils/math.py
from ..database import connect  # Go up one level (to ecommerce) then find database
```

## Common Interview Questions

**Q: What is the difference between specific import and star import regarding `__init__.py`?**
-   **A:** If you do `from package import *`, Python looks for a list called `__all__` in `__init__.py`. If it exists, it imports only those names. If not, it does **not** import sub-modules automatically; it only imports names defined directly in `__init__.py`.

**Q: Why might you avoid putting code in `__init__.py`?**
-   **A:** 
    1.  **Circular Imports:** It increases the risk of circular dependencies if sub-modules import the package itself.
    2.  **Performance:** Importing the package imports everything exposed in `__init__.py`. If your package is huge, this can slow down startup time.
