# Python Built-in Errors: A Deep Dive

This guide provides an in-depth technical analysis of common Python built-in exceptions. Understanding these errors is crucial for debugging, writing robust code, and acing technical interviews.

---

## 1. AttributeError

### Technical Definition
Raised when an attribute reference (e.g., `obj.attr`) or assignment failed. This happens when you try to access or assign an attribute that the object does not possess. In Python, objects store attributes in a `__dict__` (usually), and if the lookup fails in the instance, class, and base classes, an `AttributeError` is raised.

### Common Scenarios
- Misspelling a method or attribute name.
- Accessing an attribute on `None` (very common when a function returns `None` unexpectedly).
- attempting to append to a string (which is immutable and doesn't have an `append` method).

### Code Examples

**Scenario 1: Typo in method name**
```python
my_list = [1, 2, 3]
try:
    # Typo: it should be 'append'
    my_list.append(4)
except AttributeError as e:
    print(f"Error: {e}")
```

**Scenario 2: The 'NoneType' object has no attribute**
```python
def returns_none():
    pass

x = returns_none()
try:
    x.some_method()
except AttributeError as e:
    print(f"Error: {e}") 
    # Output: 'NoneType' object has no attribute 'some_method'
```

### Handling
Before accessing an attribute, ensure the object is of the expected type. Use `hasattr()` if you need to check for existence dynamically (though "easier to ask for forgiveness than permission" - EAFP - is often preferred in Python).

---

## 2. ImportError

### Technical Definition
Raised when the `import` statement has trouble loading a module. Also raised when the "from list" in `from ... import` has a name that cannot be found.

### Common Scenarios
- Circular imports (Module A imports B, B imports A).
- Missing dependencies (package not installed).
- Importing a function or class that doesn't exist in the module.

### Code Examples

**Scenario: Circular Import**
*file_a.py*
```python
from file_b import functional_b
def function_a():
    print("Function A")
    functional_b()
```

*file_b.py*
```python
from file_a import function_a
def function_b():
    print("Function B")
    function_a()
```
*Running either file directly might cause an ImportError depending on where the import statement is placed.*

**Scenario: Name not in module**
```python
import math
try:
    from math import non_existent_function
except ImportError as e:
    print(f"Error: {e}")
    # Output: cannot import name 'non_existent_function' from 'math'
```

### Handling
- Check for circular dependencies and refactor code (move imports inside functions if necessary).
- Verify installed packages with `pip list`.
- Check spelling of imported names.

---

## 3. ModuleNotFoundError

### Technical Definition
A subclass of `ImportError` raised specifically when a module could not be located. It's usually raised by `import` when it can't find the module at all in `sys.path`.

### Common Scenarios
- Typo in the module name.
- The module is not installed in the current environment.
- Incorrect file structure or missing `__init__.py` in packages (though less critical in Python 3.3+ namespace packages).

### Code Examples

```python
try:
    import numpy_misspelled
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    # Output: No module named 'numpy_misspelled'
```

### Handling
- Ensure the package is installed: `pip install <package_name>`.
- Check `sys.path` to see where Python is looking for modules.

---

## 4. IndexError

### Technical Definition
Raised when a sequence subscript is out of range. (Slice indices are silently truncated to fall in the allowed range; if an index is not an integer, `TypeError` is raised).

### Common Scenarios
- Accessing an index larger than `len(list) - 1`.
- Accessing an index in an empty list.

### Code Examples

```python
my_list = [10, 20]
try:
    print(my_list[5])
except IndexError as e:
    print(f"Error: {e}")
    # Output: list index out of range
```

### Handling
- Check `len()` before accessing by index.
- Use `try...except` blocks if index validity is uncertain.

---

## 5. KeyError

### Technical Definition
Raised when a mapping (dictionary) key is not found in the set of existing keys.

### Common Scenarios
- Accessing a dictionary with a key that hasn't been added yet.

### Code Examples

```python
users = {"user1": "Alice"}
try:
    print(users["user2"])
except KeyError as e:
    print(f"Error: Key {e} not found")
```

### Handling
- Use `dict.get(key, default)` to avoid the error.
- Check membership with `if key in dict:`.

```python
# Safer access
print(users.get("user2", "Unknown")) # Returns "Unknown" instead of raising error
```

---

## 6. NameError

### Technical Definition
Raised when a local or global name is not found. This applies only to unqualified names. The associated value is an error message that includes the name that could not be found.

### Common Scenarios
- Using a variable that hasn't been defined.
- Typo in variable name.
- Using a variable outside of its scope (e.g., a local variable inside a function used globally).

### Code Examples

```python
try:
    print(my_undefined_variable)
except NameError as e:
    print(f"Error: {e}")
    # Output: name 'my_undefined_variable' is not defined
```

### Handling
- Check for typos.
- Ensure variables are defined before use.
- Understand Python's LEGB (Local, Enclosing, Global, Built-in) scope rule.

---

## 7. NotImplementedError

### Technical Definition
This exception is derived from `RuntimeError`. In user defined base classes, abstract methods should raise this exception when they require derived classes to override the method.

### Common Scenarios
- Defining an abstract base class or interface where child classes MUST implement specific methods.

### Code Examples

```python
class Animal:
    def sound(self):
        raise NotImplementedError("Subclasses must implement this method")

class Dog(Animal):
    def sound(self):
        return "Woof"

class Cat(Animal):
    pass

try:
    c = Cat()
    c.sound()
except NotImplementedError as e:
    print(f"Error: {e}")
```

### Handling
- Implement the required method in the subclass.
- If you are writing a library, use this to enforce API contracts.

---

## 8. StopIteration

### Technical Definition
Raised by built-in function `next()` and an iterator's `__next__()` method to signal that there are no further items produced by the iterator.

### Common Scenarios
- Manually consuming an iterator until it is exhausted.
- Generator functions that return (which raises `StopIteration` internally).

### Code Examples

```python
my_iter = iter([1, 2])
print(next(my_iter))
print(next(my_iter))

try:
    print(next(my_iter))
except StopIteration:
    print("Iterator is empty")
```

### Handling
- Usually handled implicitly by `for` loops (which catch `StopIteration` and exit the loop gracefully).
- When using `next()`, providing a default value avoids the error: `next(iterator, default)`.

---

## 9. SyntaxError

### Technical Definition
Raised when the parser encounters a syntax error. This may occur in an `import` statement, call to the built-in functions `exec()` or `eval()`, or when reading the initial script or standard input (also interactively).

### Common Scenarios
- Missing colons after `if`, `def`, `class`.
- Mismatched parentheses.
- Using a keyword as a variable name.

### Code Examples

```python
# This code will not even run, it fails at parsing stage
try:
    eval('if True print("Hello")') # Missing colon
except SyntaxError as e:
    print(f"Error: {e}")
```

### Handling
- `SyntaxError` is usually fatal and indicates you need to fix your source code. It is rarely caught at runtime unless you are using `eval` or `exec`.

---

## 10. IndentationError

### Technical Definition
Base class for syntax errors related to incorrect indentation. This is a subclass of `SyntaxError`.

### Common Scenarios
- Mixing tabs and spaces.
- Not indenting the body of a function or loop.

### Code Examples

```python
def my_func():
print("Wrong indentation") 
# Raises IndentationError: expected an indented block
```

### Handling
- Use a consistent indentation style (PEP 8 recommends 4 spaces).
- Configure your editor to show whitespace characters.

---

## 11. ValueError

### Technical Definition
Raised when an operation or function receives an argument that has the right type but an inappropriate value, and the situation is not described by a more precise exception such as `IndexError`.

### Common Scenarios
- Converting a string that doesn't look like a number to an integer.
- Unpacking a sequence with the wrong number of items.

### Code Examples

**Scenario: Invalid type conversion**
```python
try:
    int("hello")
except ValueError as e:
    print(f"Error: {e}")
    # Output: invalid literal for int() with base 10: 'hello'
```

**Scenario: Unpacking mismatch**
```python
try:
    a, b = [1, 2, 3]
except ValueError as e:
    print(f"Error: {e}")
    # Output: too many values to unpack (expected 2)
```

### Handling
- Validate input data before processing.
- Wrap risky conversions in `try...except ValueError` blocks.
