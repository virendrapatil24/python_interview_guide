# Lists in Python

## 1. Introduction to Lists

- Lists are ordered, mutable collections of items.
- Can store elements of any type (mixed types allowed).
- Defined using square brackets: `[ ]`

```python
empty_list = []
numbers = [1, 2, 3, 4]
mixed = [1, 'a', 3.14, True]
```

## 2. Creating Lists

- Direct assignment: `my_list = [1, 2, 3]`
- Using `list()` constructor:
  ```python
  chars = list('hello')  # ['h', 'e', 'l', 'l', 'o']
  nums = list(range(5)) # [0, 1, 2, 3, 4]
  ```
- List from comprehension:
  ```python
  squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
  ```

## 3. Indexing and Slicing Lists

- Indexing starts at 0.
- Negative indices count from the end.

```python
lst = [10, 20, 30, 40, 50]
first = lst[0]      # 10
last = lst[-1]      # 50
second_last = lst[-2] # 40
```

- Slicing: `lst[start:stop:step]`

```python
sub = lst[1:4]      # [20, 30, 40]
reverse = lst[::-1] # [50, 40, 30, 20, 10]
every_other = lst[::2] # [10, 30, 50]
```

## 4. Basic List Methods

- `append(x)`: Add item to end
- `extend(iterable)`: Add all items from iterable
- `insert(i, x)`: Insert item at index
- `remove(x)`: Remove first occurrence of x
- `pop([i])`: Remove and return item at index (default last)
- `clear()`: Remove all items
- `index(x)`: Return first index of x
- `count(x)`: Count occurrences of x
- `sort()`: Sort list in place
- `reverse()`: Reverse list in place
- `copy()`: Shallow copy

```python
lst = [3, 1, 2]
lst.append(4)        # [3, 1, 2, 4]
lst.extend([5, 6])   # [3, 1, 2, 4, 5, 6]
lst.insert(0, 0)     # [0, 3, 1, 2, 4, 5, 6]
lst.remove(1)        # [0, 3, 2, 4, 5, 6]
lst.pop()            # [0, 3, 2, 4, 5]
lst.sort()           # [0, 2, 3, 4, 5]
lst.reverse()        # [5, 4, 3, 2, 0]
```

## 5. Nesting Lists

- Lists can contain other lists (multi-dimensional)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6
```

## 6. List Comprehensions

- Concise way to create lists
- Syntax: `[expression for item in iterable if condition]`

```python
squares = [x**2 for x in range(10)]
even = [x for x in range(10) if x % 2 == 0]
flattened = [item for sublist in matrix for item in sublist]
```

## 7. Advanced List Techniques

- `zip()`: Combine multiple lists
- `enumerate()`: Get index and value
- `filter()`, `map()`: Functional operations
- Unpacking: `a, b, *rest = [1, 2, 3, 4]`

```python
names = ['Alice', 'Bob', 'Charlie']
ages = [24, 25, 23]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

for idx, val in enumerate(names):
    print(idx, val)
```

## 8. Common Interview Questions

1. **Reverse a list:**
   ```python
   lst[::-1]
   lst.reverse()
   ```
2. **Remove duplicates:**
   ```python
   list(set(lst))  # Unordered
   # Ordered:
   def remove_dupes(lst):
       return list(dict.fromkeys(lst))
   ```
3. **Flatten a nested list:**
   ```python
   [item for sublist in matrix for item in sublist]
   ```
4. **Find intersection/union:**
   ```python
   a = [1,2,3]
   b = [2,3,4]
   set(a) & set(b)  # Intersection
   set(a) | set(b)  # Union
   ```

## 9. Best Practices

- Use list comprehensions for clarity and performance
- Avoid modifying lists while iterating
- Use slicing and built-in methods for common tasks
- Prefer `copy()` or slicing for shallow copies
- Use `collections.deque` for efficient queue operations

## 10. Common Pitfalls

- Index out of range errors
- Shallow vs deep copy confusion
- Modifying lists during iteration
- Using `list.remove(x)` when x not in list (raises ValueError)
- Forgetting that lists are mutable and passed by reference

## 11. Performance Tips

- List comprehensions are faster than loops
- Use built-in methods (`sort`, `reverse`, etc.)
- For large data, consider numpy arrays or pandas for efficiency

## 12. Summary Table

| Operation     | Syntax/Method        | Notes             |
| ------------- | -------------------- | ----------------- |
| Create        | `[1,2,3]`, `list()`  |                   |
| Index         | `lst[0]`             | First element     |
| Slice         | `lst[1:3]`           | Sublist           |
| Append        | `lst.append(x)`      | Add to end        |
| Extend        | `lst.extend([x,y])`  | Add multiple      |
| Insert        | `lst.insert(i,x)`    | At index          |
| Remove        | `lst.remove(x)`      | First occurrence  |
| Pop           | `lst.pop(i)`         | Remove at index   |
| Sort          | `lst.sort()`         | In-place          |
| Reverse       | `lst.reverse()`      | In-place          |
| Copy          | `lst.copy()`         | Shallow copy      |
| Nested        | `lst = [[...], ...]` | Multi-dimensional |
| Comprehension | `[x for x in ...]`   | Fast, readable    |
