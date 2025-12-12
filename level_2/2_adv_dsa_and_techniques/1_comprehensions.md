# Python Comprehensions: Zero to Advanced

Comprehensions provide a concise, readable, and "Pythonic" way to create lists, dictionaries, and sets. They are often faster and more expressive than standard `for` loops.

## 1. List Comprehensions

**Syntax:**
```python
[expression for item in iterable if condition]
```

### Basic Example
Create a list of squares for numbers 0-9.

```python
# Traditional Loop
squares = []
for i in range(10):
    squares.append(i * i)

# List Comprehension
squares = [i * i for i in range(10)]
```

### With Filtering (`if`)
Get only even numbers.

```python
evens = [x for x in range(10) if x % 2 == 0]
```

### With Conditional Logic (`if-else`)
Note: When using `else`, the structure changes slightly. It effectively becomes a ternary operator *before* the loop.

```python
# "Even" or "Odd" labels
labels = ["Even" if x % 2 == 0 else "Odd" for x in range(5)]
# Output: ['Even', 'Odd', 'Even', 'Odd', 'Even']
```

### Nested Comprehensions (Advanced)
Flatten a matrix (list of lists).

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent Loop:
# for row in matrix:
#     for num in row:
#         flattened.append(num)
```

---

## 2. Dictionary Comprehensions

**Syntax:**
```python
{key_expression: value_expression for item in iterable if condition}
```

### Example
Create a mapping of numbers to their squares.

```python
squares_dict = {x: x*x for x in range(5)}
# Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Swapping Keys and Values
```python
original = {'a': 1, 'b': 2}
swapped = {v: k for k, v in original.items()}
# Output: {1: 'a', 2: 'b'}
```

---

## 3. Set Comprehensions

**Syntax:**
```python
{expression for item in iterable if condition}
```

Similar to list comprehensions, but uses `{}` and returns a unique set.

```python
nums = [1, 1, 2, 2, 3, 4]
unique_squares = {x*x for x in nums}
# Output: {1, 4, 9, 16} (Orders may vary)
```

---

## Common Interview Questions

**Q: Are list comprehensions faster than for loops?**
- **A:** Generally, yes. Comprehensions execute at C-language speed inside the Python interpreter, avoiding the overhead of appending items one by one in a Python loop. However, for extremely complex logic, a for loop might be more readable.

**Q: Can comprehension become too complex?**
- **A:** Yes. If you have multiple nested loops and complex conditions, a comprehension can become unreadable. As a rule of thumb, if it spans more than 2-3 lines or is hard to read at a glance, prefer a normal loop.

**Q: What is a Generator Expression?**
- **A:** It looks like a tuple comprehension `(x for x in range(10))`, but there is no such thing as a "tuple comprehension". This syntax creates a **Generator**, which yields items one by one instead of creating the entire list in memory. (See the Generators section).

**Q: Why is there no Tuple Comprehension? (Technical Deep Dive)**
- **A:** This is a common trick question.
    -   **Syntactic Ambiguity:** Parentheses `()` are already used for **Generator Expressions**. If `(x for x in iterable)` created a tuple, we would lose the syntax for generators, which are crucial for memory efficiency.
    -   **Immutability:** Tuples are immutable. A comprehension typically implies building a collection element-by-element (like `list.append()`). Since tuples cannot be appended to, constructing one this way would essentially require building a list first and converting it to a tuple, or using internal optimizations that generator expressions already provide.
    -   **Workaround:** To get a tuple, simply cast the generator expression: `tuple(x for x in iterable)`.
