# Deep Dive: Generators (vs Decorators)

While we covered decorators heavily in the last section, this guide focuses entirely on **Generators**. These two features are often confused by beginners because both involve functions, but they serve completely different purposes.

*   **Decorator**: Transforms or wraps a function.
*   **Generator**: Produces a sequence of values lazily over time.

---

## 1. The Iterator Protocol

To understand Generators, you must understand Iterators.
Any object that implements `__iter__` and `__next__` is an iterator.

```python
# The Hard Way (Class-based Iterator)
class RangeIterator:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val
```

---

## 2. Generators: The "Easy" Way

A Generator is a simple way to create an iterator. It is a function that contains `yield`.

### How `yield` Works
When a function calls `yield`, it **pauses execution** and saves its state (local variables, instruction pointer). When `__next__()` is called again, it resumes exactly where it left off.

```python
def my_range(stop):
    current = 0
    while current < stop:
        yield current
        current += 1

gen = my_range(3)
print(next(gen)) # 0
print(next(gen)) # 1
print(next(gen)) # 2
# print(next(gen)) # Raises StopIteration
```

---

## 3. Generator Expressions

Similar to list comprehensions, but wrapped in `()`. They are memory efficient.

```python
# List Comprehension: Creates the whole list in memory immediately.
# [0, 1, 4, 9, ...] 
squares_list = [x**2 for x in range(1000000)] # Consumes ~40MB

# Generator Expression: Creates "recipe" to generate values.
# <generator object <genexpr> at ...>
squares_gen = (x**2 for x in range(1000000))  # Consumes ~100 bytes
```

**Interview Insight**: Use generator expressions for large datasets where you only need to iterate once.

---

## 4. Two-Way Communication (`send`)

Generators aren't just data producers; they can consume data too!
*   `yield val`: Output data.
*   `val = yield`: Input data.

The `.send(value)` method resumes the generator and sends a value *into* the generator, which becomes the result of the `yield` expression.

```python
def jump_counter():
    count = 0
    while True:
        # 1. Output count
        # 2. Pause
        # 3. Wait to receive 'jump'
        jump = (yield count) 
        
        if jump is None:
            jump = 1
        count += jump

gen = jump_counter()
print(next(gen))      # 0 (Start)
print(gen.send(10))   # 10 (Sent jump=10)
print(next(gen))      # 11 (Standard next sends None)
```

---

## 5. Coroutines & `yield from`

**`yield from`** allows a generator to delegate part of its operations to another generator. It handles the `send` and `throw` logic automatically, making it crucial for **asyncio** (pre-3.5) and creating pipelines.

```python
def sub_gen():
    yield 'A'
    yield 'B'

def main_gen():
    yield 'Start'
    yield from sub_gen() # Transfer control to sub_gen until exhaustion
    yield 'End'

# Output: Start, A, B, End
for x in main_gen():
    print(x)
```

**Why is this important?**
Before `async/await` syntax existed in Python, `yield from` was the mechanism used to implement coroutines. It provides a transparent pipe for values and exceptions to flow between the caller and the sub-generator.

---

## 6. Generators vs Decorators (The Comparison)

| Feature | Decorators | Generators |
| :--- | :--- | :--- |
| **Purpose** | Modify function behavior. | Produce a stream of data lazily. |
| **Mechanic** | Higher-order functions ($f(g) \rightarrow h$). | `yield` keyword. |
| **Execution** | Runs once upon definition (mostly). | Runs only when iterated (`next()`). |
| **State** | Can store state in closures. | Stores state in suspended stack frames. |
| **Memory** | Low impact (usually wrapping). | **High impact**: Massive memory savings for large sequences. |

---

## 7. Expert Interview Questions

### Q1: Can a generator be reused?
**No**. Once a generator is exhausted (raises `StopIteration`), it cannot be restarted. You must create a new instance of the generator function.

### Q2: What happens if you return a value in a generator?
In Python 3.3+, `return value` inside a generator:
1.  Raises `StopIteration`.
2.  Attaches `value` as the exceptions `value` attribute.
This is used by `yield from` to capture the "return value" of a sub-generator.

### Q3: How do you debug a generator?
Since they are lazy, you can't just print them.
*   Convert to list (small data): `list(gen)`.
*   Iterate manually: `next(gen)`.
*   Inspect state: Requires tricky frame inspection or pdb.

### Q4: Explain the difference between `range(len(x))` and `enumerate(x)`.
While both are iterable:
*   `range` is a **lazy sequence object** (it supports slicing, `len()`, and multiple iterations).
*   A generator is an **iterator** (single pass, no `len()`, no slicing).
`enumerate` returns an iterator (generator-like), efficiently yielding pairs.

### Q5: What is `GeneratorExit`?
It is the exception raised inside the generator when `.close()` is called. You can catch it to perform cleanup (close files, etc.). If you `yield` again inside this `except` block, Python raises a `RuntimeError`.
