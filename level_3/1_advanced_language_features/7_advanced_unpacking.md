# Deep Dive: Advanced Unpacking in Python

Unpacking (also known as Destructuring) is a syntactic convenience that allows assigning elements of an iterable to multiple variables in a single statement. While basic unpacking is common, advanced techniques distinguish expert Pythonistas.

---

## 1. Basic Iterable Unpacking

Any iterable (tuple, list, string, generator) can be unpacked if the number of variables matches the number of elements.

```python
# Tuples/Lists
a, b = (1, 2)
x, y, z = [10, 20, 30]

# Strings
first, second, third = "ABC"

# Generators/Iterators
gen = (x * x for x in range(3))
i, j, k = gen # Consumes the generator
```

**Common Pattern**: Swapping variables without a temp variable.
```python
a, b = b, a
```
*Internals*: This works by creating a tuple on the RHS and unpacking it to LHS. No temporary variable is managed by the user, though the stack handles values.

---

## 2. Extended Iterable Unpacking (`*` Operator)

Introduced in **PEP 3132** (Python 3.0), the `*` operator allows capturing "excess" items into a list. This is similar to `rest` syntax in JavaScript or Lisp.

### The Syntax of `*`
*   Only **one** starred expression is allowed in assignment.
*   The starred variable is *always* a **list**, even if empty.

```python
data = [1, 2, 3, 4, 5]

# Capture the tail
head, *tail = data
# head=1, tail=[2, 3, 4, 5]

# Capture the head
*beginning, last = data
# beginning=[1, 2, 3, 4], last=5

# Capture the middle
first, *middle, last = data
# first=1, middle=[2, 3, 4], last=5
```

### Edge Cases
```python
single = [1]
head, *tail = single
# head=1, tail=[] (Empty list, not None)

# Error: Two starred expressions
# *a, *b = [1, 2] # SyntaxError: two starred expressions in assignment
```

---

## 3. Ignoring Variables (`_`)

By convention, `_` is used for variables we intend to ignore.

```python
# Only care about first and last
first, *_, last = [1, 2, 3, 4, 5, 6]

# Ignore specific positions
x, _, y = (100, 200, 300)
```

**Note**: In the REPL (Interactive Shell), `_` automatically holds the result of the last evaluated expression. In a script/module, it functions as a regular variable name. Using `_` for ignored variables is a community convention (and supported by linters like Pylint), but it has no special behavior in the language itself.

---

## 4. Nested Unpacking

Python supports unpacking deep, complex structures if the shape matches. This is powerful for parsing JSON-like structures or database rows.

```python
record = ("Alice", 25, ("NY", "USA"))

name, age, (city, country) = record
# city="NY", country="USA"

# Combined with *
rect_data = ("Rectangle", (0, 0), (10, 20))
shape, (x, y), *dims = rect_data
# shape="Rectangle", x=0, y=0, dims=[(10, 20)]
```

---

## 5. Generalized Unpacking (PEP 448)

Python 3.5 extended unpacking to work *inside* list/tuple/set/dict literals.

### In Collections
```python
l1 = [1, 2]
l2 = [3, 4]

# Merging lists
combined = [*l1, *l2] # [1, 2, 3, 4]

# Merging sets
s1 = {1}
s2 = {2}
combined_set = {*s1, *s2}
```

### In Dictionaries (`**`)
This superceded `dict.update()` for clean merging of dictionaries in expressions.

```python
defaults = {"theme": "light", "verbose": False}
user_config = {"verbose": True, "path": "/bin"}

# Merge (last one wins)
config = {**defaults, **user_config}
# {'theme': 'light', 'verbose': True, 'path': '/bin'}
```

**Interview Question**: What happens if keys collide?
*   **Answer**: The value from the *rightmost* dictionary takes precedence.

---

## 6. Functional Unpacking (Call-Site)

You can use `*` and `**` to "explode" collections into function arguments. This is incredibly powerful for writing wrappers or passing data dynamically.

### Positional Unpacking (`*`)
The `*` operator unpacks an iterable (list, tuple, generator) into positional arguments.

```python
def add(x, y, z):
    return x + y + z

numbers = [10, 20, 30]

# Equivalent to add(10, 20, 30)
print(add(*numbers)) 

# Mixing with static args
# Equivalent to add(1, 2, 3)
print(add(1, *[2, 3])) 
```

### Keyword Unpacking (`**`)
The `**` operator unpacks a dictionary into keyword arguments. The dictionary keys **must** be strings that match the function argument names.

```python
def configure(host, port, debug=False):
    print(f"Connecting to {host}:{port} (Debug={debug})")

config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

# Equivalent to configure(host="localhost", port=8080, debug=True)
configure(**config)

# Useful for overriding/merging defaults at call time
base_config = {"host": "127.0.0.1", "port": 5000}
# Here we pass 'debug' explicitly and unpack the rest
configure(debug=False, **base_config)
```

---

## 7. Internals & Performance

### Bytecode Analysis
Python uses specific opcodes for unpacking.

*   `UNPACK_SEQUENCE`: Used for fixed-size unpacking (e.g., `a, b = x`). It checks the length of the iterable and raises `ValueError` if it doesn't match exactly.
*   `UNPACK_EX`: Used for extended unpacking (e.g., `a, *b = x`). It handles the variable-length list creation.

### Performance Implications
Unpacking is highly optimized in CPython, but consider memory:
1.  **Iterators**: Unpacking a generator (`a, *rest = gen`) forces the entire remaining generator to be consumed and stored in memory as a list (`rest`). Do not do this on infinite streams!
2.  **Indexing vs Unpacking**: 
    `a, b = data[0], data[1]` is slightly slower than `a, b = data` (extended unpacking) because indexing involves `__getitem__` calls, while `UNPACK_SEQUENCE` is an optimized C-level iteration.

---

## 8. Expert Interview Questions

### Q1: Can you unpack an iterator of unknown length?
**Yes**, using `*`.
```python
gen = (i for i in range(10))
first, *rest = gen
# first=0, rest=[1, 2, ...9]
```

### Q2: What is type of `*args` inside the function?
It is **always** a **Tuple**.
Even if you pass a list to a function `func(*my_list)`, inside `func(*args)`, `args` receives a tuple copy of that list. This ensures immutability of arguments inside the function.

### Q3: Can you use `*` multiple times in a function call?
**Yes**, starting from Python 3.5.
```python
print(*[1, 2], *[3, 4]) 
# Equivalent to print(1, 2, 3, 4)
```

### Q4: How does `{**d1, **d2}` differ from `d1.update(d2)`?
*   `{**d1, **d2}` creates a **NEW** dictionary. `d1` and `d2` remain unmodified.
*   `d1.update(d2)` modifies `d1` **in-place** and returns `None`.

### Q5: Is deep merging supported?
**No**. Standard dictionary unpacking `{**d1, **d2}` performs a **shallow** merge.
If `d1` has key `"a": {"x": 1}` and `d2` has key `"a": {"y": 2}`, the result will simply overwrite `"a"` with `{"y": 2}`.

To deep merge, you must use recursion or `copy.deepcopy` logic, or libraries like `deepmerge`.
