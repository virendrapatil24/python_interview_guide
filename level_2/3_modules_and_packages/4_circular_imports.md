# Circular Imports in Python

A **Circular Import** occurs when two or more modules depend on each other. This is a common architectural problem in Python.

## 1. The Scenario

**Module A (`a.py`)** requires `b.py`.
**Module B (`b.py`)** requires `a.py`.

```python
# a.py
import b

def func_a():
    print("Function A")
    b.func_b()

func_a()
```

```python
# b.py
import a  # <--- Problem!

def func_b():
    print("Function B")
    a.func_a()
```

**The Result:** `ImportError` or `AttributeError`.
When you run `a.py`:
1.  `a.py` starts executing.
2.  It sees `import b` and halts to load `b.py`.
3.  `b.py` starts executing.
4.  It sees `import a`.
5.  Python checks `sys.modules`. It sees `a` is "partially initialized" (currently loading), so it returns that object.
6.  `b.py` continues. It might try to access `a.func_a`.
7.  **CRASH!** `a.func_a` hasn't been defined yet because `a.py` paused at line 1.

## 2. Solutions

### Solution A: Delayed Import (Inline Import)
Import the module only **inside** the function that needs it. This keeps the conditional dependency out of the top-level scope.

```python
# b.py

def func_b():
    import a  # <--- Moved inside
    print("Function B")
    a.func_a()
```

**Pros:** Quick fix.
**Cons:** Hides dependencies; can be slightly slower (negligible).

### Solution B: Import at the Bottom
Place the import statement at the end of the file.

```python
# b.py
def func_b():
    pass

# ... rest of file ...

import a # <--- At the end
```

**Pros:** Works for some script scenarios.
**Cons:** Unconventional and confusing to read (imports usually belong at the top).

### Solution C: Architectural Refactoring (Best Practice)
Circular imports usually indicate **tight coupling**. The best fix is to create a third module.

**Refactor:**
1.  Create `common.py`.
2.  Move the shared logic/functions that both `a` and `b` need into `common.py`.
3.  Have `a.py` import `common.py` and `b.py` import `common.py`.

Now, neither `a` nor `b` need to import each other.

```python
# common.py
def shared_logic():
    ...

# a.py
import common

# b.py
import common
```

## 3. Typing Imports (`TYPE_CHECKING`)

Sometimes you only need the import for Type Hinting, which causes a circular dependency at runtime.

**Fix:** Use `typing.TYPE_CHECKING`.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from b import ClassB # Only imports during static analysis (mypy)

def func(obj: "ClassB"): # Use string forward reference
    ...
```
