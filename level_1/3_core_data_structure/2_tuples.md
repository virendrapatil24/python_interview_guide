# Tuples in Python

## 1. Constructing Tuples

- Tuples are ordered, immutable collections of items.
- Defined using parentheses `()` or the `tuple()` constructor.
- Can store elements of any type (mixed types allowed).

```python
empty_tuple = ()
singleton = (1,)  # Note the comma for single-element tuple
tuple1 = (1, 2, 3)
tuple2 = 1, 2, 3  # Parentheses optional
mixed = (1, 'a', 3.14, True)
from_list = tuple([1, 2, 3])
```

## 2. Basic Tuple Methods

- Tuples have fewer methods than lists due to immutability.
- Common methods:
  - `count(x)`: Number of times x appears
  - `index(x)`: First index of x

```python
t = (1, 2, 2, 3)
print(t.count(2))   # 2
print(t.index(3))   # 3
```

- Tuples support indexing and slicing like lists:

```python
t = (10, 20, 30, 40)
print(t[0])      # 10
print(t[-1])     # 40
print(t[1:3])    # (20, 30)
```

## 3. Immutability

- Tuples cannot be changed after creation (no append, remove, etc.)
- Elements cannot be reassigned or deleted
- Immutability makes tuples hashable (usable as dict/set keys)

```python
t = (1, 2, 3)
# t[0] = 10  # Error: 'tuple' object does not support item assignment
# t.append(4)  # Error: 'tuple' object has no attribute 'append'
```

- If a tuple contains mutable objects (like lists), those objects can be changed, but the tuple structure itself cannot.

```python
t = ([1, 2], 3)
t[0].append(3)
print(t)  # ([1, 2, 3], 3)
```

## 4. When to Use Tuples

- When you need an immutable sequence
- As dictionary keys or set elements
- For fixed collections of items (coordinates, RGB values, etc.)
- For unpacking multiple return values from functions
- To ensure data integrity (prevents accidental modification)

```python
def min_max(nums):
    return min(nums), max(nums)

result = min_max([1, 2, 3])  # (1, 3)
```

- Named tuples (from `collections` module) provide readable, immutable records:

```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)  # 1 2
```

## 5. Common Interview Questions

1. **How do you create a single-element tuple?**
   - `(1,)` (comma is required)
2. **Can tuples be used as dictionary keys? Why?**
   - Yes, because they are immutable and hashable
3. **How do you unpack a tuple?**
   ```python
   a, b, c = (1, 2, 3)
   ```
4. **What happens if you try to modify a tuple?**
   - Raises `TypeError`
5. **How do you convert a list to a tuple?**
   - `tuple(my_list)`

## 6. Best Practices

- Use tuples for fixed, immutable data
- Prefer tuples over lists for function returns
- Use namedtuple for readable, immutable records
- Avoid using tuples for collections that may need modification

## 7. Common Pitfalls

- Forgetting the comma in single-element tuples
- Trying to modify tuple elements
- Confusing tuple with list syntax
- Using mutable objects inside tuples (can lead to unexpected behavior)
