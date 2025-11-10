# Defining Functions with `def` in Python

Functions are reusable blocks of code that perform a specific task. They are a cornerstone of modular, readable, and maintainable programming. In Python, you define a function using the `def` keyword.

---

## 1. Basic Function Definition

A function is defined with a name, a list of parameters, and a block of code. It can optionally return a value.

### Syntax

```python
def function_name(parameter1, parameter2):
    """
    This is a docstring. It explains what the function does.
    """
    # Code block (suite)
    # ...
    return some_value
```

- **`def`**: The keyword that starts a function definition.
- **`function_name`**: The name you give to the function (follows standard variable naming rules).
- **`parameters`**: Variables that accept values (arguments) when the function is called. They are optional.
- **`:`**: The colon marks the end of the function header.
- **Docstring**: An optional string literal to document the function's purpose. It's a crucial best practice.
- **`return`**: The keyword to exit the function and optionally send back a value. If omitted, the function returns `None`.

### Example

```python
def greet(name):
    """Returns a simple greeting message."""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

---

## 2. Parameters and Arguments

It's important to distinguish between parameters (the names in the function definition) and arguments (the actual values passed during the function call).

### Positional vs. Keyword Arguments

- **Positional Arguments**: Passed in the order the parameters are defined.
- **Keyword Arguments**: Passed using `name=value` syntax. Their order doesn't matter.

```python
def describe_pet(animal_type, pet_name):
    """Displays information about a pet."""
    print(f"I have a {animal_type} named {pet_name}.")

# Positional arguments
describe_pet("hamster", "Harry")

# Keyword arguments
describe_pet(pet_name="Willy", animal_type="whale")

# Mixing both (positional must come first)
describe_pet("cat", pet_name="Whiskers")
```

### Default Argument Values

You can provide a default value for a parameter, making it optional during the function call.

```python
def describe_pet(pet_name, animal_type="dog"): # animal_type has a default
    """Displays information about a pet."""
    print(f"I have a {animal_type} named {pet_name}.")

describe_pet("Fido") # Uses the default animal_type
describe_pet("Mittens", "cat") # Overrides the default
```

**Pitfall**: Avoid using mutable objects (like lists or dictionaries) as default arguments. They are created only once when the function is defined and are shared across all calls, leading to unexpected behavior.

---

## 3. Advanced Argument Types

### Arbitrary Positional Arguments (`*args`)

To accept an arbitrary number of positional arguments, use `*args`. It collects them into a **tuple**.

```python
def make_pizza(size, *toppings):
    """Summarizes the pizza being ordered."""
    print(f"\nMaking a {size}-inch pizza with the following toppings:")
    for topping in toppings:
        print(f"- {topping}")

make_pizza(12, "mushrooms", "green peppers", "extra cheese")
```

### Arbitrary Keyword Arguments (`**kwargs`)

To accept an arbitrary number of keyword arguments, use `**kwargs`. It collects them into a **dictionary**.

```python
def build_profile(first, last, **user_info):
    """Build a dictionary containing everything we know about a user."""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile("albert", "einstein",
                             location="princeton",
                             field="physics")
print(user_profile)
# Output: {'location': 'princeton', 'field': 'physics', 'first_name': 'albert', 'last_name': 'einstein'}
```

### Positional-Only and Keyword-Only Arguments (Python 3.8+)

You can enforce how arguments are passed using `/` and `*`.

- Arguments before `/` are **positional-only**.
- Arguments after `*` are **keyword-only**.

```python
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
    # ---
    # pos1, pos2: Must be positional
    # pos_or_kwd: Can be positional or keyword
    # kwd1, kwd2: Must be keyword
    # ---
    print("Function executed")

# Valid call
f(1, 2, 3, kwd1=4, kwd2=5)
f(1, 2, pos_or_kwd=3, kwd1=4, kwd2=5)

# Invalid call: f(1, pos2=2, ...) -> pos2 cannot be a keyword argument
```

---

## 4. The `return` Statement

- A function stops executing as soon as it hits a `return` statement.
- A function can return any type of object.
- If no `return` statement is specified, or `return` is used alone, the function implicitly returns `None`.

### Returning Multiple Values

You can return multiple values by separating them with commas. They are automatically packed into a tuple.

```python
def find_range(numbers):
    """Returns the smallest and largest numbers from a list."""
    if not numbers:
        return None, None
    smallest = largest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
        if num > largest:
            largest = num
    return smallest, largest

numbers = [1, 5, 3, 9, 4]
lowest, highest = find_range(numbers)
print(f"Lowest: {lowest}, Highest: {highest}")  # Output: Lowest: 1, Highest: 9
```

---

## 5. Common Interview Questions

1.  **Q: What's the difference between a parameter and an argument?**

    - **A:** A parameter is the variable name in the function's definition. An argument is the actual value supplied to that parameter when the function is called.

2.  **Q: What are `*args` and `**kwargs` and why are they used?\*\*

    - **A:** `*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. They are used to create flexible functions that can accept a variable number of inputs.

3.  **Q: What is the danger of using a mutable object like a list as a default argument?**

    - **A:** The default object is created only once when the function is defined. Any modification to it within the function will persist across subsequent calls, leading to unexpected shared state. The standard solution is to use `None` as the default and create a new mutable object inside the function if needed.

4.  **Q: What does a function return if it has no `return` statement?**

    - **A:** It implicitly returns `None`.

5.  **Q: In what order must different types of arguments appear in a function definition?**
    - **A:** The standard order is:
      1.  Standard positional arguments.
      2.  `*args`.
      3.  Keyword-only arguments.
      4.  `**kwargs`.
          If using positional-only arguments (Python 3.8+), they come first: `pos_only, /, standard, *, kwd_only, **kwargs`.

---

## 6. Best Practices & Common Pitfalls

- **Best Practice**: Keep functions small and focused on a single task (Single Responsibility Principle).
- **Best Practice**: Use clear, descriptive names for functions and parameters.
- **Best Practice**: Always write a docstring to explain the function's purpose, arguments, and return value.
- **Pitfall**: The mutable default argument trap (see above).
- **Pitfall**: Modifying a global variable without using the `global` keyword. If you assign to a variable inside a function, Python assumes it's a local variable unless told otherwise.
- **Pitfall**: Creating overly long functions that are hard to read and debug. If a function is too complex, break it down into smaller helper functions.
