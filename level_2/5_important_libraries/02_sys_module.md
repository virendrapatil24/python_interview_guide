# Deep Dive: The `sys` Module

The `sys` module provides access to variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter. It is your window into the Python Runtime itself.

---

## 1. Runtime Internals: `sys.modules` and `sys.path`

### `sys.modules`: The Registry of Loaded Modules
This is a dictionary that maps module names to module objects.
*   **Performance**: When you import `math`, Python first checks `if 'math' in sys.modules`. If yes, it returns the cached object. This makes repeated imports essentially free.
*   **Hacking**: You can monkey-patch modules globally by modifying `sys.modules`.

```python
import sys

# Check if a module is loaded
if 'math' in sys.modules:
    print("Math is already loaded!")

# Dangerous Trick: Prevent a module from loading
sys.modules['os'] = None
try:
    import os
except ImportError:
    print("OS module is disabled!")
```

### `sys.path` risks
`sys.path` is the list of strings specifying the search path for modules.
*   **Index 0**: Usually the directory containing the input script.
*   **Modification**: You can append to `sys.path` at runtime to import from non-standard locations, but be careful of **Shadowing** (accidentally naming your folder `json` or `email`).

---

## 2. Memory Profiling: `getsizeof` vs Reality

`sys.getsizeof(obj)` returns the size of an object in bytes. However, it is **shallow**.

```python
import sys

lst = [1, 2, 3]
print(sys.getsizeof(lst)) 
# Output: ~88 bytes (overhead of list struct + 3 pointers)
# It does NOT include the size of the integers 1, 2, 3!

# To measure deep size, you need a recursive function or Pympler library.
```

### Reference Counting: `sys.getrefcount`
Python uses Reference Counting + Garbage Collection (for cycles). `sys.getrefcount(obj)` returns the number of references to `obj`.

**Note**: The count is typically 1 higher than you expect because passing the object to `getrefcount` creates a temporary reference.

---

## 3. Interpreter Hooks (Auditing & Debugging)

### `sys.settrace`
Allows you to implement a debugger or code coverage tool in Python. The trace function is called for every line of code executed.

```python
import sys

def trace_calls(frame, event, arg):
    if event == 'call':
        print(f"Calling function: {frame.f_code.co_name}")
    return trace_calls

sys.settrace(trace_calls)

def demo():
    return 1

demo()
# Output: Calling function: demo
```

### `sys.excepthook`
(Covered in Exception Handling) - The global callback for unhandled exceptions.

---

## 4. The Import System: `sys.meta_path`

This is where the magic of "how Python finds code" happens. `sys.meta_path` is a list of *finder* objects.

*   By default, it contains `BuiltinImporter`, `FrozenImporter`, and `PathFinder` (file system).
*   **Advanced usage**: You can insert a custom finder to load modules from a Database, invalid ZIP files, or over a Network.

```python
import sys
from importlib.abc import MetaPathFinder

class NetworkImporter(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith('remote_'):
            print(f"Attempting to load {fullname} from network...")
            # Return a ModuleSpec here if found
        return None

sys.meta_path.insert(0, NetworkImporter())

try:
    import remote_utils
except ImportError:
    pass
# Output: Attempting to load remote_utils from network...
```

---

## 5. Bytecode and Recursion

*   `sys.setrecursionlimit(n)`: Increases the maximum stack depth. Vital for deep recursion algorithms (like DFS on large trees), but risky (C-stack overflow causes segfault).
*   `sys.set_int_max_str_digits(n)`: (New in 3.11) Mitigates DoS attacks via massive integer string conversion.

---

## Summary Checklist

| Attribute | Purpose | Principal Note |
| :--- | :--- | :--- |
| `sys.argv` | Command line args | `argv[0]` is the script name. |
| `sys.executable` | Path to python binary | Use this to spawn subprocesses using the *same* interpreter environment. |
| `sys.platform` | OS Identifier | `win32`, `linux`, `darwin`. Use for cross-platform logic. |
| `sys.stdout` | Standard Output | Can be redirected (e.g., to a file or StringIO) to capture print statements. |
