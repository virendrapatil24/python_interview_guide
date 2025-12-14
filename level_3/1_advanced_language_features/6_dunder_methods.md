# Deep Dive: Python Data Model & Dunder Methods

Python's "Magic Methods" (Double UNDERscore methods) are the tools that allow classes to integrate seamlessly with the language's built-in interactions. This mechanism is formally known as the **Python Data Model**.

---

## 1. Construction and Initialization

### `__new__` vs `__init__`
This is a favorite interview trap.

*   `__new__(cls, ...)`: **The Constructor**. It allocates memory and returns a new instance of the class. It is a static method (though explicit `@staticmethod` isn't required).
*   `__init__(self, ...)`: **The Initializer**. It receives the instance created by `__new__` and sets up initial attributes.

### Use Case 1: Subclassing Immutable Types
When subclassing immutable built-ins like `str`, `int`, or `tuple`, the instance is created *before* `__init__` runs. You cannot modify the value in `__init__`. You must intercept it in `__new__`.

```python
class UpperString(str):
    def __new__(cls, content):
        # The actual string object is created here.
        # We transform 'content' to uppercase BEFORE creation.
        return super().__new__(cls, content.upper())

    def __init__(self, content):
        # By the time this runs, self is already "HELLO". 
        print(f"Init running for {self}")

s = UpperString("hello") 
# Output: "Init running for HELLO"
print(s) # "HELLO"
```

### Use Case 2: The Singleton Pattern
`__new__` allows you to control *which* object is returned. You can return an existing instance instead of creating a new one.

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new connection...")
            cls._instance = super().__new__(cls)
        return cls._instance

db1 = DatabaseConnection() # "Creating new connection..."
db2 = DatabaseConnection() # Returns existing instance
print(db1 is db2) # True
```

---

## 2. String Representation: `__repr__` vs `__str__`

*   `__str__(self)`: User-friendly representation. Used by `print()` and `str()`.
*   `__repr__(self)`: Developer-friendly representation. Used by the interactive shell and debuggers. Ideally, `eval(repr(obj)) == obj`.

**Best Practice**: If you only implement one, implement `__repr__`. Python uses `__repr__` as a fallback if `__str__` is missing.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"
```

---

## 3. Attribute Access Control

These methods intercept dot notation (`obj.attr`).

*   `__getattr__(self, name)`: Called **ONLY** when attribute lookup **fails** (i.e., attribute is not found in instance/class dict).
*   `__getattribute__(self, name)`: Called **ALWAYS**, for *every* attribute access. **Dangerous**: easy to cause infinite recursion.

```python
class DynamicConfig:
    def __init__(self):
        self.data = {}

    def __getattr__(self, name):
        # Called only if 'name' is not found
        return f"Config '{name}' not found"

    def __getattribute__(self, name):
        # CAUTION: calling self.something here triggers recursion
        print(f"Accessing: {name}")
        return super().__getattribute__(name)
```

---

## 4. Operator Overloading

Python supports operator overloading for almost every symbol.

### Comparison
*   `__eq__` (`==`), `__ne__` (`!=`)
*   `__lt__` (`<`), `__le__` (`<=`), `__gt__` (`>`), `__ge__` (`>=`)

### Arithmetic
*   `__add__` (`+`), `__sub__` (`-`), `__mul__` (`*`)
*   `__radd__`: "Reflected" addition. Called when the left operand doesn't support the operation. e.g., `1 + obj`.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented # Crucial for type coercion support
```

---

## 5. Iterators and Collections

To make an object behave like a list or dictionary.

*   `__len__(self)`: Called by `len()`.
*   `__getitem__(self, key)`: Called by `obj[key]`.
*   `__setitem__(self, key, value)`: Called by `obj[key] = val`.
*   `__contains__(self, item)`: Called by `item in obj`.

### Iteration Protocol
*   `__iter__(self)`: Returns an iterator object (typically `self`, if `__next__` is implemented).
*   `__next__(self)`: Returns the next value or raises `StopIteration`.

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        num = self.current
        self.current -= 1
        return num
```

---

## 6. Context Managers (`with` statement)

*   `__enter__(self)`: Executed on entering `with`. Return value is assigned to `as target`.
*   `__exit__(self, exc_type, exc_val, exc_tb)`: Executed on exit. Return `True` to suppress exceptions.

---

## 7. Callables and Slots

### `__call__`
Makes an instance callable like a function: `obj()`. Very useful for stateful decorators or strategies.

### `__slots__`
Optimization mechanism. Tells Python **not** to use a dictionary (`__dict__`) for attributes, but a fixed memory array.
*   **Pros**: Saves massive memory with thousands of objects. Faster access.
*   **Cons**: Cannot add new attributes at runtime.

```python
class OptimizedPoint:
    __slots__ = ['x', 'y'] 
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

---

## 8. Expert Interview Questions

### Q1: What is the difference between `__str__` and `__repr__`?
`__str__` is for end-users (readable), `__repr__` is for developers (unambiguous, preferably valid code). `__repr__` is the fallback.

### Q2: Why would you return `NotImplemented` in `__eq__`?
To allow the *other* object a chance to handle the comparison via its reflected method (e.g., `__eq__` on the other side). If both return `NotImplemented`, Python falls back to object identity.

### Q3: How do you implement a Singleton using Dunder methods?
By overriding `__new__` to store and return a single instance.
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Q4: Explain `__del__` and why it is dangerous.
`__del__` is the destructor. It's dangerous because:
1.  Python does not guarantee *when* it is called (garbage collection is non-deterministic).
2.  It can interfere with GC during circular references (though improved in newer Python).
3.  Exceptions in `__del__` are ignored (printed to stderr) and won't stop execution.
**Preferred**: Use Context Managers (`__enter__`/`__exit__`) for cleanup.
