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

### Tricky Questions

- What happens if you assign to a variable inside a function without declaring it global?
- How does Python handle variable references and garbage collection?
- What is the difference between `is` and `==`?
- How do mutable default arguments behave in functions?

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
