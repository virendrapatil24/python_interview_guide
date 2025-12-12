# Map, Filter, and Zip: Functional Programming Tools

These three built-in functions allow for efficient data processing without managing explicit loops. In modern Python (3.x), `map` and `filter` return **iterators**, which means they are lazy and memory efficient.

## 1. Map
Applies a function to every item in an iterable.

**Syntax:** `map(function, iterable, ...)`

```python
# Function to apply
def square(x):
    return x ** 2

nums = [1, 2, 3, 4]

# Using named function
mapped_obj = map(square, nums) 
# mapped_obj is an Iterator. We must cast to list to view it.
print(list(mapped_obj)) # [1, 4, 9, 16]

# Using Lambda (Common Pattern)
squared = list(map(lambda x: x**2, nums))
print(squared) # [1, 4, 9, 16]
```

### Advanced: Multiple Iterables
`map` can accept multiple iterables. The function must accept that many arguments.

```python
nums1 = [1, 2, 3]
nums2 = [10, 20, 30]

# Adds elements from both lists: 1+10, 2+20, 3+30
sums = list(map(lambda x, y: x + y, nums1, nums2))
print(sums) # [11, 22, 33]
```

## 2. Filter
Creates an iterator of elements from the iterable for which the function returns `True`.

**Syntax:** `filter(function, iterable)`

```python
nums = [1, 2, 3, 4, 5, 6]

# Using Lambda to keep evens
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens) # [2, 4, 6]

# Using None as function
# Filters out "Falsey" values (0, "", None, False, [])
mixed = [1, 0, "Hello", "", False, True]
truthy = list(filter(None, mixed))
print(truthy) # [1, 'Hello', True]
```

## 3. Zip
Combines multiple iterables elements into tuples. It stops when the *shortest* iterable is exhausted.

**Syntax:** `zip(*iterables)`

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# Combine them
zipped = list(zip(names, scores))
print(zipped) 
# Output: [('Alice', 85), ('Bob', 90), ('Charlie', 95)]

# Unzipping (Common Trick)
unzipped_names, unzipped_scores = zip(*zipped)
print(unzipped_names) # ('Alice', 'Bob', 'Charlie')
```

### Usage with Lambda: Sorting Zipped Lists
A powerful pattern is zipping lists to sort them together.

```python
names = ["Bob", "Alice", "Charlie"]
scores = [70, 95, 80]

# Zip them, sort by score (second item in tuple), then unzip if needed
combined = list(zip(names, scores))
combined.sort(key=lambda x: x[1]) # Sort by score

print(combined)
# Output: [('Bob', 70), ('Charlie', 80), ('Alice', 95)]
```

## Common Interview Questions

**Q: What is the return type of `map()` in Python 3?**
-   **A:** It returns a `map` object, which is an **iterator**. In Python 2, it returned a `list`. This change makes Python 3 memory efficient (Lazy Evaluation).

**Q: What happens if you `zip` two lists of different lengths?**
-   **A:** `zip()` stops as soon as the shortest iterable is exhausted. The remaining items in the longer iterables are ignored. To keep them (padding with `None`), use `itertools.zip_longest`.

**Q: Map/Filter vs List Comprehension?**
-   **A:** 
    -   **Readability:** Comprehensions are usually more readable for simple logic (`[x*2 for x in nums]`).
    -   **Performance:** They are roughly comparable, though comprehensions can be slightly faster for simple operations because they avoid the function call overhead of `lambda`.
    -   **Use Map/Filter when:** You already have a pre-defined function to apply. `map(existing_func, data)`.
