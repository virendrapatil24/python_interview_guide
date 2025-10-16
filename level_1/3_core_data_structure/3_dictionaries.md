# Dictionaries in Python

## 1. Constructing a Dictionary

## How Dictionaries Work Internally (Constant Time Lookups)

- Python dictionaries are implemented as hash tables.
- When you add a key-value pair, Python computes a hash of the key (using `__hash__`).
- The hash determines where the value is stored in an internal array.
- Lookup, insertion, and deletion are usually O(1) (constant time) because the hash allows direct access to the location.
- If two keys have the same hash (a collision), Python uses probing to find the next available slot.
- The hash table automatically resizes to maintain performance as more items are added.
- Keys must be immutable and hashable so their hash value does not change.

**Summary:**

> Dictionary operations are fast because they use hash tables, allowing direct access to values by key without searching through all items.

```python
empty_dict = {}
d = {'a': 1, 'b': 2, 'c': 3}
from_list = dict([('x', 10), ('y', 20)])
from_kwargs = dict(a=1, b=2)
```

## 2. Accessing Objects from a Dictionary

- Access values using keys:

```python
d = {'name': 'Alice', 'age': 25}
print(d['name'])      # 'Alice'
# print(d['gender']) # KeyError if key not found
```

- Use `get()` to avoid KeyError:

```python
print(d.get('gender'))        # None
print(d.get('gender', 'N/A')) # 'N/A'
```

- Check for key existence:

```python
if 'name' in d:
    print('Name exists')
```

## 3. Nesting Dictionaries

- Dictionaries can contain other dictionaries (and lists, etc.)

```python
nested = {
    'user1': {'name': 'Alice', 'age': 25},
    'user2': {'name': 'Bob', 'age': 30}
}
print(nested['user1']['name'])  # 'Alice'
```

## 4. Basic Dictionary Methods

- `keys()`: Returns a view of keys
- `values()`: Returns a view of values
- `items()`: Returns a view of key-value pairs
- `get(key, default)`: Returns value for key or default
- `setdefault(key, default)`: Returns value, sets default if missing
- `update(other_dict)`: Updates with another dict or iterable
- `pop(key[, default])`: Removes and returns value for key
- `popitem()`: Removes and returns last inserted key-value pair
- `clear()`: Removes all items
- `copy()`: Shallow copy

```python
d = {'a': 1, 'b': 2}
print(list(d.keys()))      # ['a', 'b']
print(list(d.values()))    # [1, 2]
print(list(d.items()))     # [('a', 1), ('b', 2)]
d.update({'c': 3})         # {'a': 1, 'b': 2, 'c': 3}
d.pop('a')                # 1
d.popitem()               # ('c', 3)
d.clear()                 # {}
```

## 5. Dictionary Comprehensions

- Concise way to create dictionaries

```python
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
filtered = {k: v for k, v in d.items() if v > 1}
```

## 6. Advanced Dictionary Features

- Dictionary views (`keys()`, `values()`, `items()`) are dynamic
- Dictionaries preserve insertion order (Python 3.7+)
- Keys must be hashable (immutable types)
- Use `collections.defaultdict` for automatic default values
- Use `collections.OrderedDict` for explicit order (pre-3.7)

```python
from collections import defaultdict
counts = defaultdict(int)
counts['a'] += 1
print(counts['b'])  # 0
```

## 7. Common Interview Questions

1. **How do you merge two dictionaries?**
   ```python
   d1 = {'a': 1}
   d2 = {'b': 2}
   merged = {**d1, **d2}
   # Or: d1.update(d2)
   ```
2. **How do you invert a dictionary?**
   ```python
   d = {'a': 1, 'b': 2}
   inverted = {v: k for k, v in d.items()}
   ```
3. **How do you remove a key safely?**
   ```python
   d.pop('key', None)
   ```
4. **How do you iterate over keys and values?**
   ```python
   for k, v in d.items():
       print(k, v)
   ```
5. **How do you count occurrences efficiently?**
   ```python
   from collections import Counter
   counts = Counter(['a', 'b', 'a'])
   ```

## 8. Best Practices

- Use `get()` for safe access
- Prefer dictionary comprehensions for clarity
- Use `defaultdict` for counting/grouping
- Avoid using mutable objects as keys
- Use `items()` for iteration
- Use `copy()` for shallow copies

## 9. Common Pitfalls

- KeyError when accessing missing keys
- Using mutable objects as keys
- Forgetting that dictionaries are mutable and passed by reference
- Not handling nested dictionaries properly
- Confusing `update()` with overwriting keys

## 10. Performance Tips

- Dictionary lookups are fast (O(1) average)
- Use comprehensions for efficient creation
- For large data, consider `collections.Counter`, `defaultdict`, or specialized libraries
