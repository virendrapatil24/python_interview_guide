# Iterators in Python: Zero to Advanced

Understanding Iterators is fundamental to mastering Python. They form the backbone of `for` loops, generators, and memory-efficient programming.

## 1. Iterable vs Iterator

This distinction is the most common interview question in this domain.

### Iterable
An object is **Iterable** if it can be looped over.
-   **Technical Definition:** It has an `__iter__()` method that returns an **Iterator**.
-   **Examples:** Lists, Tuples, Dictionaries, Sets, Strings.

### Iterator
An object is an **Iterator** if it represents a stream of data.
-   **Technical Definition:** 
    1.  It has an `__next__()` method that returns the next item.
    2.  It has an `__iter__()` method that returns `self`.
-   **Behavior:** It remembers its state during iteration. Once exhausted, it cannot be reused.

### The Relationship
> You get an **Iterator** *from* an **Iterable**.

```python
# List is an Iterable
my_list = [1, 2, 3]

# Loop automatically does this:
# 1. Calls iter(my_list) to get an Iterator
# 2. Calls next(iterator) repeatedly
# 3. Handles StopIteration

# Manual Verification
iterator = iter(my_list)

print(next(iterator)) # 1
print(next(iterator)) # 2
print(next(iterator)) # 3
# print(next(iterator)) # Raises StopIteration
```

## 2. Building a Custom Iterator

To build a custom iterator, you need to implement a class with `__iter__` and `__next__`. This is useful when you need complex logic that a simple generator function cannot handle.

### Example: A Range Iterator
Let's re-implement Python's `range()` function.

```python
class MyRange:
    def __init__(self, start, end):
        self.value = start
        self.end = end

    def __iter__(self):
        # Iterator must return itself
        return self

    def __next__(self):
        if self.value >= self.end:
            raise StopIteration
        
        current = self.value
        self.value += 1
        return current

# Usage
nums = MyRange(1, 4)
for num in nums:
    print(num)
# Output: 1, 2, 3
```

## 3. Infinite Iterators

Iterators are perfect for infinite sequences since they generate values one by one (Lazy Evaluation).

```python
class InfiniteCounter:
    def __init__(self, start=0):
        self.num = start

    def __iter__(self):
        return self

    def __next__(self):
        self.num += 1
        return self.num

# Usage
counter = InfiniteCounter()
print(next(counter)) # 1
print(next(counter)) # 2
# ... can go on forever
```

## 4. Common Interview Questions

**Q: What is the `StopIteration` exception?**
-   **A:** It is the signal used by an iterator to indicate that there are no more items to return. The `for` loop catches this exception internally to stop the loop gracefully.

**Q: Can you slice an iterator?**
-   **A:** No. Iterators process items one by one and do not support random access (indexing or slicing) like lists do. You would need to use `itertools.islice` for that.

**Q: Why do we need `__iter__` in an Iterator class if it just returns `self`?**
-   **A:** To make the iterator itself **iterable**. This ensures you can use the iterator directly in a `for` loop (`for item in my_iterator:`). Using an iterator in a for loop calls `iter()` on it, so `__iter__` must exist and return `self`.
