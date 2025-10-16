# Sets in Python

## 1. Introduction to Sets

- Sets are unordered collections of unique, immutable elements.
- Defined using curly braces `{}` or the `set()` constructor.
- Useful for membership tests, removing duplicates, and mathematical set operations.

```python
empty_set = set()
numbers = {1, 2, 3, 4}
mixed = {1, 'a', 3.14, True}
```

## 2. How Sets are Built Internally

- Sets are implemented as hash tables (like dictionaries, but only keys).
- Each element's hash determines its position in the internal array.
- Membership tests, addition, and removal are typically O(1) (constant time).
- Only immutable and hashable objects can be set elements.
- Collisions are handled by probing for the next available slot.
- The set resizes automatically to maintain performance.

## 3. Creating and Modifying Sets

- Use `{}` for non-empty sets, `set()` for empty sets (since `{}` creates a dict).
- Add elements with `add()`, remove with `remove()` or `discard()`.
- Use `update()` to add multiple elements.

```python
s = set()
s.add(1)
s.update([2, 3])
s.remove(2)      # Raises KeyError if not present
s.discard(4)     # No error if not present
```

## 4. Set Operations

- Mathematical set operations: union, intersection, difference, symmetric difference.

```python
A = {1, 2, 3}
B = {3, 4, 5}

A | B      # Union: {1, 2, 3, 4, 5}
A & B      # Intersection: {3}
A - B      # Difference: {1, 2}
A ^ B      # Symmetric difference: {1, 2, 4, 5}
```

- Subset and superset tests:

```python
A <= B     # A is subset of B
A >= B     # A is superset of B
A < B      # Proper subset
A > B      # Proper superset
```

## 5. When and Why to Use Sets

- Remove duplicates from sequences
- Fast membership tests
- Mathematical set operations
- Data deduplication and filtering
- Checking for unique elements
- Efficient algorithms for intersection/union

## 6. Advanced Set Concepts

- `frozenset`: Immutable version of set, can be used as dict/set keys

```python
fs = frozenset([1, 2, 3])
```

- Set comprehensions:

```python
squares = {x**2 for x in range(5)}
```

- Iterating and copying:

```python
for x in numbers:
    print(x)
copy = numbers.copy()
```

- Removing all elements:

```python
numbers.clear()
```

## 7. Common Interview Questions

1. **Remove duplicates from a list:**
   ```python
   unique = set([1, 2, 2, 3])  # {1, 2, 3}
   ```
2. **Find intersection of two lists:**
   ```python
   set(a) & set(b)
   ```
3. **Check if all elements are unique:**
   ```python
   len(some_list) == len(set(some_list))
   ```
4. **Why can't lists be set elements?**
   - Lists are mutable and not hashable.
5. **How to use frozenset as a dict key?**
   ```python
   d = {frozenset([1,2]): 'value'}
   ```

## 8. Best Practices

- Use sets for fast membership tests and deduplication
- Use set operations for clean, readable code
- Prefer `discard()` over `remove()` if unsure about element presence
- Use `frozenset` for immutable sets
- Avoid using mutable objects as set elements

## 9. Common Pitfalls

- Using `{}` for empty set (creates dict)
- Trying to add mutable objects (like lists)
- Assuming sets are ordered
- Modifying set during iteration
- Forgetting that sets are mutable and passed by reference

## 10. Performance Tips

- Set operations are fast due to hash table implementation
- Use set comprehensions for efficient creation
- For large data, sets outperform lists for membership tests
