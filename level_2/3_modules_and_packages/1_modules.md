# Python Modules: Organizing Your Code

One of the keys to writing maintainable Python code is organizing it into separate files, known as **Modules**.

## 1. What is a Module?

Technically, any file ending in `.py` is a module. The name of the module is the file name (without `.py`).

**Why use modules?**
1.  **Organization:** Group logical code together (e.g., `db_connection.py`, `user_utils.py`).
2.  **Reusability:** Write code once, import it anywhere.
3.  **Namespace Management:** Avoid variable name collisions.

## 2. Importing Modules

Suppose you have a file `math_utils.py`:

```python
# math_utils.py
PI = 3.14159

def add(a, b):
    return a + b
```

### Option A: Import the entire module
This keeps the namespace clean. You must access contents via the module name.

```python
import math_utils

print(math_utils.add(5, 3))
print(math_utils.PI)
```

### Option B: Import specific items
Importing directly into the current namespace.

```python
from math_utils import add, PI

print(add(5, 3)) # No need for 'math_utils.' prefix
```

### Option C: Import everything (`*`)
**Warning:** This is generally bad practice (except in interactive sessions) because it pollutes the namespace and makes it unclear where variables came from.

```python
from math_utils import *
```

### Option D: Aliasing
Useful for long names or to avoid conflicts.

```python
import math_utils as mu
print(mu.add(1, 2))

from math_utils import add as sum_two
print(sum_two(1, 2))
```

## 3. The `if __name__ == "__main__":` Block

This is a very common interview question.

Every module has a special built-in variable called `__name__`.
-   If you run the file directly (`python my_module.py`), `__name__` is set to `"__main__"`.
-   If you import the file (`import my_module`), `__name__` is set to the module's name (`"my_module"`).

**Use Case:**
This allows you to include executable test code in your module that only runs when you execute the file specifically, but not when you import it elsewhere.

```python
# calculator.py

def add(a, b):
    return a + b

if __name__ == "__main__":
    # This block only runs if you run 'python calculator.py'
    print("Running manual tests...")
    print(add(2, 2))
```

## 4. How Python Finds Modules (`sys.path`)

When you import a module, Python searches effectively in this order:
1.  **Current Directory**: The folder where the script is running.
2.  **PYTHONPATH**: Environment variable with custom paths.
3.  **Standard Library**: Built-in modules like `os`, `sys`, `math`.
4.  **Site-Packages**: Third-party packages installed via `pip`.

You can view (and modify) this path at runtime:

```python
import sys
print(sys.path)

# You can theoretically add a path manually (though rarely recommended)
# sys.path.append("/path/to/my/modules")
```

## Common Interview Questions

**Q: What is `__pycache__`?**
-   **A:** When you import a module, Python compiles it into "bytecode" for faster loading next time. It stores these `.pyc` files in the `__pycache__` directory. You can ignore/delete them; Python recreates them as needed.

**Q: What happens if you import a module twice?**
-   **A:** Python runs the module code only **once** per session. Subsequent imports just return the already loaded module object from `sys.modules`. If you need to reload a module (e.g., during development), you must use `importlib.reload()`.
