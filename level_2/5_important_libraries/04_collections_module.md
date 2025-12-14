# Deep Dive: The `collections` Module

The `collections` module implements specialized container datatypes providing alternatives to Python's general purpose built-in containers, `dict`, `list`, `set`, and `tuple`.

---

## 1. `deque`: The Thread-Safe Double-Ended Queue

`collections.deque` is a generalisation of stacks and queues. It is the preferred way to implement a **Queue** in Python.

### Core Operations (O(1))
Unlike lists, `deque` is optimized for adding/removing from *both* ends.

*   `append(x)`: Add to right.
*   `appendleft(x)`: Add to left.
*   `pop()`: Remove from right.
*   `popleft()`: Remove from left.

### 1. Using as a Queue (FIFO)
```python
from collections import deque

queue = deque(["Alice", "Bob", "Charlie"])

# Enqueue (Add to right)
queue.append("Dave")

# Dequeue (Remove from left)
served = queue.popleft()
print(served) # "Alice"
print(queue)  # deque(['Bob', 'Charlie', 'Dave'])
```

### 2. Using as a Stack (LIFO)
```python
stack = deque()

# Push (Add to right)
stack.append("Page 1")
stack.append("Page 2")

# Pop (Remove from right)
last_page = stack.pop()
print(last_page) # "Page 2"
```

### 3. Rotating and Sizing
```python
# Ring Buffer Pattern (Size Limited)
# Useful for keeping track of the "last N items" seen
d = deque(maxlen=3)
d.append(1)
d.append(2)
d.append(3)
d.append(4) # Pushes out '1' automatically
print(d)    # deque([2, 3, 4], maxlen=3)

# Rotate elements (Round Robin)
d.rotate(1) # Right rotation
print(d)    # deque([4, 2, 3], maxlen=3)
```

**Performance Note**: `list.pop(0)` is **O(n)**. `deque.popleft()` is **O(1)**. Always use `deque` for queues.

---

## 2. `defaultdict`: The Missing Key Handler

A subclass of `dict` that calls a factory function to supply missing values.

### The internals: `__missing__`
When you access `d[key]`, if the key is missing, `defaultdict` calls `self.default_factory()` and inserts the result.

### 1. Grouping Pattern (`list`)
```python
from collections import defaultdict

# Grouping items by key
data = [('A', 1), ('B', 2), ('A', 3)]
grouped = defaultdict(list)

for key, val in data:
    grouped[key].append(val)

print(grouped) # defaultdict(<class 'list'>, {'A': [1, 3], 'B': [2]})
```

### 2. Counting Pattern (`int`)
The default value of `int()` is 0. Ideally suited for counting.

```python
s = "mississippi"
d = defaultdict(int)

for char in s:
    d[char] += 1

print(d['i']) # 4
print(d['z']) # 0 (No KeyError, just returns 0)
```

### 3. Unique Grouping Pattern (`set`)
Use this to collect unique items.

```python
data = [('A', 'apple'), ('B', 'ball'), ('A', 'apple')]
unique_grouped = defaultdict(set)

for key, val in data:
    unique_grouped[key].add(val)

print(unique_grouped) 
# {'A': {'apple'}, 'B': {'ball'}} -> 'apple' added once
```

### 4. Advanced: Constant / Custom Factory
You can use *any* callable (function/lambda/class).

```python
# Constant default value
d = defaultdict(lambda: "Unknown")
print(d['any_key']) # "Unknown"
```

---

## 3. `Counter`: Set Algebra with Multiset

A `Counter` is a dict subclass for counting hashable objects. It is effectively a **Multiset**.

### Set Operations
Counters support rich mathematical operations that regular dicts don't.

### 1. Initialization
```python
from collections import Counter

# From iterable
c = Counter(['a', 'b', 'c', 'a', 'b', 'b'])
print(c) # Counter({'b': 3, 'a': 2, 'c': 1})

# From dict
c = Counter({'a': 2, 'b': 3})

# From keyword args
c = Counter(a=2, b=3)
```

### 2. Common Patterns (`most_common`, `update`)
```python
# Finding Top N items
print(c.most_common(2)) # [('b', 3), ('a', 2)]

# Updating counts (Adds to existing, doesn't replace)
c.update(['a', 'd'])
print(c['a']) # 3 (2 + 1)
```

### 3. Set Algebra
Counters support rich mathematical operations.

```python
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

### 1. Merging & Scoping
```python
from collections import ChainMap

defaults = {'theme': 'dark', 'show_index': True}
config_file = {'show_index': False}
cli_args = {'theme': 'light'}

# Search order: CLI -> Config -> Defaults
settings = ChainMap(cli_args, config_file, defaults)

print(settings['theme'])      # 'light' (from CLI)
print(settings['show_index']) # False   (from Config)
```

### 2. The `new_child()` pattern
Accessing `new_child()` creates a new map at the front of the chain, effectively creating a new "local scope".

```python
root = {'global_var': 1}
scope1 = ChainMap(root) # acts like a child scope

scope1 = scope1.new_child({'local_var': 2})
print(scope1['global_var']) # 1
print(scope1['local_var'])  # 2

# Modifications only happen in the first map
scope1['new_var'] = 3
print(root) # {'global_var': 1} (Unchanged)
```

---

## 5. `namedtuple`: Memory Efficient Structure

Used to create tuple-like objects with named fields.

*   **Memory**: Uses exactly the same memory as a regular tuple (no per-instance dictionary overhead).
*   **Validation**: It is immutable.

### 1. Basic Definition
```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

print(p.x, p.y)   # Readable access
print(p[0], p[1]) # Backward compatible index access
x, y = p          # Unpacking
```

### 2. Power Methods (`_make`, `_asdict`, `_replace`)
`namedtuple` adds methods starting with `_` to avoid conflicts with field names.

```python
# Create from list/iterable
data = [30, 40]
p2 = Point._make(data)

# Convert to dict
print(p2._asdict()) # {'x': 30, 'y': 40}

# Replace (Create new instance with modified values)
# Remember: Tuples are immutable, so this returns a NEW object
p3 = p2._replace(x=100)
print(p3) # Point(x=100, y=40)
```

### 3. Adding Methods (Inheritance)
Since `namedtuple` returns a class, you can inherit from it.

```python
class AdvancedPoint(Point):
    def hypot(self):
        return (self.x**2 + self.y**2) ** 0.5

ap = AdvancedPoint(3, 4)
print(ap.hypot()) # 5.0
```
