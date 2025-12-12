# Generators and `yield`: Managing Memory Efficiently

Generators are a powerful way to create iterators in Python. Unlike standard functions that compute a value and `return` it, generators return an iterator that yields a stream of data one value at a time.

## 1. The `yield` Keyword

When a function contains `yield`, it becomes a generator function.

-   **`return`**: Terminates the function and returns a result.
-   **`yield`**: Pauses the function, saving its state, and produces a value. The next time the function is called, it resumes from where it left off.

### Basic Example

```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen)) # 1
print(next(gen)) # 2
print(next(gen)) # 3
# print(next(gen)) # Raises StopIteration Error
```

## 2. Why use Generators? (Memory Efficiency)

This is the most important interview concept regarding generators.

Imagine reading a 10GB file.
-   **List Approach**: Loads the entire file into RAM. Crash! 💥
-   **Generator Approach**: Reads one line at a time. Safe! ✅

```python
# Bad: Creating a huge list
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i*i)
    return result

# Good: Using a generator
def get_squares_gen(n):
    for i in range(n):
        yield i*i

# Comparison
# list_ver = get_squares_list(10000000) # Consumes massive memory
gen_ver = get_squares_gen(10000000)   # Almost zero memory usage

print(next(gen_ver)) # 0
print(next(gen_ver)) # 1
```

## 3. Generator Expressions

Just like list comprehensions, but using parenthesis `()`.

```python
squares_gen = (x*x for x in range(10)) 
# This is NOT a tuple. It's a generator object.

for n in squares_gen:
    print(n)
```

## 4. Advanced: Infinite Sequences

Generators are perfect for representing infinite streams of data.

```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

gen = infinite_sequence()
print(next(gen)) # 0
print(next(gen)) # 1
# Keeps going forever...
```

## Common Interview Questions

**Q: What is the difference between `return` and `yield`?**
-   **A:** `return` sends a specified value back to its caller and terminates the function. `yield` produces a value and suspends the function’s execution, maintaining its local variables. Execution resumes after the `yield` statement on the next call.

**Q: What happens if you call `next()` on a generator that is finished?**
-   **A:** It raises a `StopIteration` exception. This is how `for` loops know when to stop iterating; they handle this exception internally.

**Q: Can you iterate over a generator twice?**
-   **A:** No! Generators are "one-time use". Once you iterate through them (exhaust them), you cannot restart them. You must create a new generator instance.
