# Deep Dive: The `collections` Module

The `collections` module implements specialized container datatypes providing alternatives to Python's general purpose built-in containers, `dict`, `list`, `set`, and `tuple`.

---

## 1. `deque`: The Thread-Safe Ring Buffer

`collections.deque` (Doubly Ended Queue) is a list-like container with fast appends and pops on either end.

### Performance: Deque vs List
*   **List**: Implemented as a dynamic array. `append()` is O(1) amortized, but `pop(0)` (removing from start) is **O(n)** because all subsequent elements must overwrite the previous memory slots.
*   **Deque**: Implemented as a doubly-linked list of blocks. `append()` and `popleft()` are **O(1)**.

```python
from collections import deque
import time

# Ring Buffer Pattern (Size Limited)
# Useful for keeping track of the "last N items" seen
d = deque(maxlen=3)
d.append(1)
d.append(2)
d.append(3)
d.append(4) # Pushes out '1' automatically
print(d)    # deque([2, 3, 4], maxlen=3)
```

**Thread Safety**: Deques are thread-safe for memory efficient appends and pops from either side. Lists are not guaranteed to be thread-safe for all operations.

---

## 2. `defaultdict`: The Missing Key Handler

A subclass of `dict` that calls a factory function to supply missing values.

### The internals: `__missing__`
When you access `d[key]`, if the key is missing, `defaultdict` calls `self.default_factory()` and inserts the result.

```python
from collections import defaultdict

# Grouping Pattern
# Standard Dict way:
# if key not in d: d[key] = []
# d[key].append(item)

# Defaultdict way:
d = defaultdict(list)
d['k1'].append(1) # 'k1' created automatically with empth list
d['k1'].append(2)
```

**Advanced Tip**: You can use *any* callable.
```python
def log_missing():
    print("Key missing!")
    return 0

d = defaultdict(log_missing)
print(d['new_key']) # Prints "Key missing!", then returns 0
```

---

## 3. `Counter`: Set Algebra with Multiset

A `Counter` is a dict subclass for counting hashable objects. It is effectively a **Multiset**.

### Set Operations
Counters support rich mathematical operations that regular dicts don't.

```python
from collections import Counter

c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

# Addition
print(c1 + c2) # Counter({'a': 4, 'b': 3})

# Subtraction (keeps only positive counts)
print(c1 - c2) # Counter({'a': 2}) -> 'b' is gone because 1-2 is negative

# Intersection (min(c1[x], c2[x]))
print(c1 & c2) # Counter({'a': 1, 'b': 1})

# Union (max(c1[x], c2[x]))
print(c1 | c2) # Counter({'a': 3, 'b': 2})
```

---

## 4. `ChainMap`: Scoped Contexts

`ChainMap` links multiple mappings together so they are treated as a single unit. It is often much faster than creating a new dict and running `update()`.

**Use Case**: Managing variable scopes (Local -> Global -> Builtin) or Configuration overrides (CLI Args -> Config File -> Defaults).

```python
from collections import ChainMap

defaults = {'theme': 'dark', 'show_index': True}
config_file = {'show_index': False}
cli_args = {'theme': 'light'}

# Search order: CLI -> Config -> Defaults
settings = ChainMap(cli_args, config_file, defaults)

print(settings['theme'])      # 'light' (from CLI)
print(settings['show_index']) # False   (from Config)

# Writes only affect the first mapping (CLI args)
settings['new_setting'] = True
print(cli_args) # {'theme': 'light', 'new_setting': True}
```

---

## 5. `namedtuple`: Memory Efficient Structure

Used to create tuple-like objects with named fields.

*   **Memory**: Uses exactly the same memory as a regular tuple (no per-instance dictionary overhead).
*   **Validation**: It is immutable.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# Readable access
print(p.x, p.y)

# Backward compatible (it's still a tuple)
print(p[0], p[1])
x, y = p # unpacking works
```
