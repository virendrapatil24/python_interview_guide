# Python Data Types: A Deep Dive for Interviews

## 1. Introduction to Data Types

In Python, every value has a data type. Data types are classifications that specify which type of value a variable can hold and what type of mathematical, relational, or logical operations can be applied to it without causing an error. Python is a **dynamically typed** language, meaning you don't need to declare the type of a variable; the interpreter infers it at runtime.

Understanding data types is crucial, especially the distinction between **mutable** and **immutable** types, as it affects how your data is stored and manipulated.

---

## 2. Core Data Types & Mutability

Here's a breakdown of Python's built-in data types and their mutability.

| Category          | Data Type   | Description                             | Mutability  |
| ----------------- | ----------- | --------------------------------------- | ----------- |
| **Numeric**       | `int`       | Whole numbers                           | Immutable   |
|                   | `float`     | Floating-point numbers                  | Immutable   |
|                   | `complex`   | Complex numbers (real + imaginary)      | Immutable   |
| **Text Sequence** | `str`       | Sequence of Unicode characters          | Immutable   |
| **Sequence**      | `list`      | Ordered, changeable collection          | **Mutable** |
|                   | `tuple`     | Ordered, unchangeable collection        | Immutable   |
|                   | `range`     | Sequence of numbers                     | Immutable   |
| **Mapping**       | `dict`      | Unordered collection of key-value pairs | **Mutable** |
| **Set**           | `set`       | Unordered, unindexed, no duplicates     | **Mutable** |
|                   | `frozenset` | Immutable version of a set              | Immutable   |
| **Boolean**       | `bool`      | `True` or `False`                       | Immutable   |
| **None**          | `NoneType`  | Represents the absence of a value       | Immutable   |

---

## 3. Immutable Types Explained

Immutable objects **cannot be changed** after they are created. Any operation that appears to "modify" an immutable object actually creates a new object in memory.

### Examples: `int`, `str`, `tuple`

```python
# String (str)
my_string = "hello"
print(f"Initial ID: {id(my_string)}") # e.g., 4388683376

# This creates a NEW string object
my_string = my_string + " world"
print(f"New ID: {id(my_string)}")     # e.g., 4388826352 (different ID)

# Tuple (tuple)
my_tuple = (1, 2, 3)
# The following line would raise a TypeError:
# my_tuple[0] = 99 # TypeError: 'tuple' object does not support item assignment
```

**Key Implications:**

- **Predictable:** Safe to use as dictionary keys or in sets.
- **Safer in Functions:** When passed to a function, you can be sure the original object won't be accidentally modified.
- **Performance:** Can be less efficient if you perform many "modifications" (e.g., concatenating strings in a loop), as each change creates a new object.

---

## 4. Mutable Types Explained

Mutable objects **can be changed in-place** after they are created. Operations can modify the internal state of the object without creating a new one.

### Examples: `list`, `dict`, `set`

```python
# List (list)
my_list = [1, 2, 3]
print(f"Initial ID: {id(my_list)}") # e.g., 4388791616

# This modifies the list IN-PLACE
my_list.append(4)
print(f"New ID: {id(my_list)}")     # e.g., 4388791616 (same ID)
print(my_list) # [1, 2, 3, 4]

# Dictionary (dict)
my_dict = {'name': 'Alice'}
print(f"Initial ID: {id(my_dict)}") # e.g., 4388827200

# Modifying the dictionary IN-PLACE
my_dict['age'] = 30
print(f"New ID: {id(my_dict)}")     # e.g., 4388827200 (same ID)
print(my_dict) # {'name': 'Alice', 'age': 30}
```

**Key Implications:**

- **Flexibility:** Useful for collections that need to grow or change, like a list of items in a shopping cart.
- **Potential for Bugs:** If a mutable object is passed to a function, the function can modify it, leading to unexpected side effects elsewhere in the code.
- **Cannot be Dictionary Keys:** Mutable types like lists and dicts cannot be used as dictionary keys because their value (and hash) can change.

---

## 5. Common Interview Questions & Concepts

### Q1: What is the difference between a list and a tuple?

**Answer:** The core difference is **mutability**.

- **Lists** are mutable, meaning their contents can be changed after creation. They are defined with square brackets `[]`.
- **Tuples** are immutable, meaning they cannot be changed. They are defined with parentheses `()`.

Use tuples for fixed collections of data (e.g., coordinates `(x, y)`) and lists for collections that you intend to modify. Tuples can also be used as dictionary keys, while lists cannot.

### Q2: Why can't a list be a dictionary key?

**Answer:** Dictionary keys must be **hashable**, which means their hash value must be constant throughout their lifetime. Since lists are mutable, their contents (and thus their hash value) could change. If a list were used as a key and then modified, the dictionary would be unable to find the entry. Immutable types like strings, numbers, and tuples have a constant hash value, making them suitable as keys.

```python
d = {}
my_list = [1, 2]
# d[my_list] = "value"  # Raises TypeError: unhashable type: 'list'

my_tuple = (1, 2)
d[my_tuple] = "value" # This works perfectly
print(d) # {(1, 2): 'value'}
```

### Q3: Explain the "mutable default argument" problem.

**Answer:** This is a classic Python "gotcha". Default arguments for a function are evaluated only **once**, when the function is defined. If a mutable type like a list is used as a default, it gets shared across all calls to that function.

```python
# The Problem
def add_item(item, my_list=[]):
    my_list.append(item)
    return my_list

print(add_item(1)) # [1]
print(add_item(2)) # [1, 2] <- Unexpected! The list is shared.

# The Solution
def add_item_fixed(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

print(add_item_fixed(1)) # [1]
print(add_item_fixed(2)) # [2] <- Correct!
```

The correct pattern is to use `None` as the default and create a new mutable object inside the function if one isn't provided.

### Q4: How does mutability affect variable assignment and copying?

**Answer:**

- For **immutable** types, assignment creates a copy of the value.
- For **mutable** types, assignment creates a new reference to the _same_ object.

```python
# Mutable example
list_a = [1, 2, 3]
list_b = list_a  # list_b is a reference to list_a

list_b.append(4) # Modifying list_b also modifies list_a

print(f"List A: {list_a}") # List A: [1, 2, 3, 4]
print(f"List B: {list_b}") # List B: [1, 2, 3, 4]
print(f"IDs are same: {id(list_a) == id(list_b)}") # True
```

To create a true copy of a mutable object, you must do so explicitly using `copy()` (shallow copy) or `copy.deepcopy()` (deep copy).

---

## 6. Type Checking

While Python is dynamically typed, you sometimes need to check an object's type.

### `type()` vs `isinstance()`

- `type(obj)`: Returns the exact type of an object. `type(True)` is `bool`.
- `isinstance(obj, classinfo)`: Returns `True` if the object is an instance of the class _or any of its subclasses_. This is generally the preferred way to check types.

```python
print(isinstance(True, bool)) # True
print(isinstance(True, int))  # True, because bool is a subclass of int

print(type(True) is bool) # True
print(type(True) is int)  # False, because the exact type is bool
```

**Interview Tip:** Always prefer `isinstance()` for type checking unless you need to know the exact type and want to exclude subclasses.

---

## 7. Best Practices & Pitfalls

### Best Practices

1.  **Use Immutable Types for Keys:** Always use immutable types (`str`, `int`, `tuple`) for dictionary keys.
2.  **Prefer Tuples for Fixed Data:** If a sequence of data is not meant to change, store it in a tuple.
3.  **Be Explicit with Copies:** When you need a distinct copy of a mutable object, use `list.copy()`, `dict.copy()`, or the `copy` module.
4.  **Avoid Mutable Default Arguments:** Use the `None`-as-default pattern shown above.
5.  **Use `isinstance()` for Type Checking:** It's more robust and aligns with object-oriented principles.

### Common Pitfalls

1.  **Accidental Modification:** Modifying a mutable object that is referenced in multiple places in your code.
2.  **Using `is` for Value Comparison:** `is` checks for object identity, `==` checks for value equality. You almost always want `==` for comparing values.
3.  **Assuming a Function Doesn't Modify Your List/Dict:** If you pass a mutable object to a function, it can be changed. Pass a copy if you need to preserve the original.
4.  **Forgetting Tuples Need a Comma for a Single Element:** `(1)` is just the integer `1`. `(1,)` is a tuple with one element.
