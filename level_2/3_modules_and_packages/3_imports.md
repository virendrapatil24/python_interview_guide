# Absolute vs Relative Imports

Understanding how to navigate your project structure via imports is crucial, especially for testing and Refactoring.

## 1. Absolute Imports

**Definition:** An import that uses the full path of the module starting from the project's root folder (the entry point).

**Example:**
Assumed Structure:
```
project/
    main.py
    package_a/
        module_a.py
    package_b/
        module_b.py
```

Inside `module_b.py`, if you want to import `module_a.py`:
```python
# Absolute Import
from package_a import module_a

def func():
    module_a.do_something()
```

### PROS:
1.  **Clarity:** Specifically shows exactly where the module is.
2.  **Standard:** It is the PEP 8 recommended way.
3.  **Easy to Debug:** Error messages are straightforward.

### CONS:
1.  **Verbosity:** Paths can get very long (`from org.team.project.sub.mod import foo`).
2.  **Refactoring:** If you rename the root package, you have to rewrite all imports.

## 2. Relative Imports

**Definition:** An import that specifies the location relative to the *current file*. It uses dot notation.

-   `.` (Single Dot): Current directory.
-   `..` (Double Dot): Parent directory.
-   `...` (Triple Dot): Grand-parent directory.

**Example:**
Assumed Structure:
```
project/
    package_a/
        __init__.py
        module_x.py
        sub_package/
            __init__.py
            module_y.py
```

Inside `module_y.py`, to import `module_x.py`:
```python
# Relative Import
from .. import module_x

# Or explicit items
from ..module_x import some_function
```

Inside `module_y.py`, to import a sibling in `sub_package` (e.g., `helper.py`):
```python
from . import helper
```

### PROS:
1.  **Concise:** Shortens import statements significantly.
2.  **Portable:** You can move the entire package `package_a` inside another package, and internal links remain broken.

### CONS:
1.  **Confusing:** Harder to tell where a file is just by looking at the code.
2.  **Execution Constraint:** **Crucial!** Relative imports **do not work** if you execute the file directly (e.g., `python module_y.py`). They only work if the file is imported as part of a package.
    -   *Error:* `ImportError: attempted relative import with no known parent package`.

## 3. Best Practices (Interview Answers)

1.  **Prefer Absolute Imports** whenever possible. They are explicit and less prone to "script vs module" execution errors.
2.  **Use Relative Imports** only for highly coupled internal modules within a deep package structure where moving the whole package is a likely scenario.
3.  **Never mix them** in confusing ways. Stick to a style guide.

## 4. The `sys.path` Hack (Anti-Pattern)

Sometimes, developers hit an import error and do this:

```python
import sys
import os
sys.path.append(os.path.abspath(".."))
import my_module
```

**Interview Tip:** Do **NOT** recommend this. This is brittle and indicates a poor project structure. The correct fix is usually to run the script as a module (`python -m package.module`) or install the project in editable mode (`pip install -e .`).
