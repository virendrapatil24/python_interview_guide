# Python Variables

## 1. What is a Variable?

A variable is a name that refers to a value stored in memory. In Python, variables are created by assignment and can hold any type of data.

---

## 2. Rules for Naming Variables

- Must start with a letter (a-z, A-Z) or underscore (\_)
- Can contain letters, digits (0-9), and underscores
- Case-sensitive (`myVar` ≠ `myvar`)
- Cannot use reserved keywords (e.g., `class`, `def`, `if`)
- Avoid using built-in names (e.g., `list`, `str`)

**Examples:**

```python
valid_name = 10
_valid = 20
name_123 = "Alice"
# Invalid:
# 123name = 5
# class = "reserved"
```

---

## 3. Dynamic Typing in Python

Python is dynamically typed:

- Variable types are determined at runtime.
- You can reassign a variable to a value of a different type.

**Example:**

```python
x = 5        # int
y = "hello"  # str
x = "world"  # Now x is str
```

### Pros

- Flexible and fast prototyping
- Less boilerplate code

### Cons

- Type-related bugs can be harder to catch
- Less explicit code, harder to maintain in large projects

---

## 4. Assigning and Reassigning Variables

- Assignment uses `=`
- Multiple assignment:
  ```python
  a, b, c = 1, 2, 3
  x = y = z = 0
  ```
- Swapping values:
  ```python
  a, b = b, a
  ```
- Reassignment changes the reference:
  ```python
  x = 10
  x = "ten"
  ```

---

## 5. Advanced & Tricky Concepts

### Mutable vs Immutable Types

- Immutable: `int`, `float`, `str`, `tuple`
- Mutable: `list`, `dict`, `set`
- Reassigning a variable pointing to a mutable object does not change the original object.

**Example:**

```python
lst = [1, 2, 3]
lst2 = lst
lst2.append(4)
print(lst)  # [1, 2, 3, 4]
```

#### Why are `int` objects immutable even though you can reassign an int variable?

When you assign a value to a variable (e.g., `x = 5`), `x` points to an `int` object in memory. If you reassign `x` (e.g., `x = 10`), Python creates a new `int` object and makes `x` point to it. The original `int` object (`5`) is unchanged and remains immutable. This means the value of an `int` object cannot be altered; only the variable reference changes. Immutability ensures that numbers behave predictably and safely, especially when used as dictionary keys or in sets.

**Example:**

```python
x = 5
y = x
x = 10
print(y)  # 5 (y still points to the original int object)
```

### Variable Scope

- Local, Global, Nonlocal
- Use `global` and `nonlocal` keywords to modify scope

**Example:**

```python
global_var = 5
def foo():
    global global_var
    global_var = 10
```

### Unpacking

```python
a, b, *rest = [1, 2, 3, 4, 5]
print(a, b, rest)  # 1 2 [3, 4, 5]
```

### Shadowing Built-ins

```python
list = [1, 2, 3]  # Shadows built-in 'list'
```

### Tricky Questions & Answers

#### 1. What happens if you assign to a variable inside a function without declaring it global?

**Answer:** Python creates a new local variable with the same name, shadowing any global variable. The global variable remains unchanged.

```python
x = 10  # Global variable

def my_function():
    x = 20  # Creates local variable, doesn't modify global
    print(f"Local x: {x}")

my_function()
print(f"Global x: {x}")  # Still 10
```

**Key Points:**

- Without `global` keyword, assignment creates a local variable
- The global variable is not accessible for modification
- This can lead to `UnboundLocalError` if you try to read before assigning

```python
x = 10

def problematic_function():
    print(x)  # UnboundLocalError!
    x = 20    # This line makes x local

# problematic_function()  # Would raise UnboundLocalError
```

#### 2. How does Python handle variable references and garbage collection?

**Answer:** Python uses reference counting and cyclic garbage collection. Variables are references to objects in memory.

```python
# Reference counting example
x = [1, 2, 3]  # Reference count: 1
y = x          # Reference count: 2
z = x          # Reference count: 3

del x          # Reference count: 2
y = None       # Reference count: 1
z = None       # Reference count: 0 -> Object is garbage collected
```

**Key Points:**

- Each object has a reference count
- When count reaches 0, object is immediately freed
- Circular references are handled by cyclic garbage collector
- `del` removes a reference, not necessarily the object

#### 3. What is the difference between `is` and `==`?

**Answer:** `is` checks identity (same object in memory), `==` checks equality (same value).

```python
# Identity vs Equality
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True (same values)
print(a is b)  # False (different objects)
print(a is c)  # True (same object)

# Special case with small integers
x = 5
y = 5
print(x is y)  # True (Python caches small integers)

# But not always reliable for larger numbers
x = 1000
y = 1000
print(x is y)  # May be True or False depending on implementation
```

**Key Points:**

- Use `is` for identity (None, True, False checks)
- Use `==` for value comparison
- `is` is faster but more restrictive
- Small integers (-5 to 256) are cached and may have same identity

#### 4. How do mutable default arguments behave in functions?

**Answer:** Default arguments are evaluated once when the function is defined, not each time it's called. This can cause unexpected behavior with mutable objects.

```python
# The Problem
def append_to_list(item, target=[]):
    target.append(item)
    return target

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Unexpected!
print(append_to_list(3))  # [1, 2, 3] - Even more unexpected!

# The Solution
def append_to_list_fixed(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

print(append_to_list_fixed(1))  # [1]
print(append_to_list_fixed(2))  # [2] - Correct!
```

**Key Points:**

- Default arguments are evaluated at function definition time
- Mutable defaults are shared across all function calls
- Use `None` as default and create new object inside function
- This is a common Python gotcha that catches many developers

---

## 6. Sample Exercises

1. Assign values to variables and swap them without using a third variable.
2. Create a function that demonstrates local and global variable usage.
3. Show how dynamic typing can lead to bugs.
4. Unpack a list into multiple variables.

---

## 7. Interview Tips

- Be clear on naming rules and scope.
- Understand dynamic typing and its trade-offs.
- Know the difference between mutable and immutable types.
- Be ready to discuss advanced topics like unpacking, shadowing, and scope.
- Practice explaining tricky behaviors (e.g., mutable default arguments).

---

## 8. References

- [Python Variables](https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator)
- [PEP 8 Naming Conventions](https://peps.python.org/pep-0008/#naming-conventions)
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
