# Python Conditional Statements: `if`, `elif`, `else`

Conditional statements are the cornerstone of decision-making in programming. They allow a program to execute different blocks of code based on whether certain conditions are met. In Python, this is primarily handled by the `if`, `elif`, and `else` keywords.

---

## 1. The Basic `if` Statement

The `if` statement is the simplest form of a conditional. It executes a block of code **only if** its condition evaluates to `True`.

### Syntax

```python
if condition:
    # Code to execute if condition is True
```

- **`condition`**: An expression that results in a Boolean value (`True` or `False`).
- **`:`**: The colon is mandatory and signifies the start of a code block.
- **Indentation**: The code block to be executed must be indented (typically 4 spaces).

### Example

```python
age = 20
if age >= 18:
    print("You are eligible to vote.")
# This line will always execute as it is not part of the if block
print("Program finished.")
```

---

## 2. The `if-else` Statement

The `else` statement provides an alternative block of code to execute when the `if` condition is `False`.

### Syntax

```python
if condition:
    # Code to execute if condition is True
else:
    # Code to execute if condition is False
```

### Example

```python
temperature = 15
if temperature > 25:
    print("It's a hot day.")
else:
    print("It's not a hot day.")
```

---

## 3. The `if-elif-else` Chain

For handling multiple, mutually exclusive conditions, you can use `elif` (short for "else if"). Python checks each condition sequentially. The first one that is `True` has its block executed, and the rest of the chain is skipped. The final `else` is optional and acts as a catch-all if no preceding conditions are met.

### Syntax

```python
if condition_1:
    # Executes if condition_1 is True
elif condition_2:
    # Executes if condition_1 is False and condition_2 is True
elif condition_3:
    # Executes if 1 & 2 are False and condition_3 is True
else:
    # Executes if all preceding conditions are False
```

### Example

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"  # This block executes, and the chain stops
elif score >= 70:
    grade = "C"
else:
    grade = "D"

print(f"Your grade is {grade}")  # Output: Your grade is B
```

---

## 4. Truthy and Falsy Values (Advanced Concept)

In Python, conditions don't have to be strictly `True` or `False`. Any object can be evaluated in a Boolean context. This is a critical concept for writing concise, Pythonic code.

**Falsy Values**: These values are treated as `False` in an `if` statement.

- `None`
- `False`
- `0` (of any numeric type: `0`, `0.0`, `0j`)
- Empty sequences and collections: `''`, `[]`, `()`, `{}`, `set()`, `range(0)`

**Truthy Values**: Any object that is not "falsy" is "truthy" and is treated as `True`.

- Non-empty strings (`"hello"`)
- Non-zero numbers (`1`, `-10`, `3.14`)
- Non-empty lists, tuples, dictionaries, and sets

### Example

```python
my_list = []
if my_list:
    print("List is not empty.")
else:
    print("List is empty.")  # This will be printed

name = "Alice"
if name:
    print(f"Hello, {name}!") # This will be printed
```

---

## 5. Logical Operators (`and`, `or`, `not`)

You can combine multiple conditions using logical operators.

- **`and`**: `True` only if **both** conditions are true.
- **`or`**: `True` if **at least one** condition is true.
- **`not`**: Inverts the Boolean value of a condition.

### Example

```python
age = 25
has_license = True

# 'and' example
if age >= 18 and has_license:
    print("You are allowed to drive.")

# 'or' example
day = "Sunday"
if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")

# 'not' example
is_raining = False
if not is_raining:
    print("No need for an umbrella.")
```

**Interview Tip**: Logical operators use **short-circuit evaluation**. `and` stops evaluating as soon as it finds a `False` condition. `or` stops as soon as it finds a `True` one. This can be used to prevent errors.

```python
user = {"name": "Alice", "posts": []}

# Short-circuiting prevents an error if 'posts' key doesn't exist
if "posts" in user and len(user["posts"]) > 0:
    print("User has posts.")
else:
    print("User has no posts or the key is missing.")
```

---

## 6. Ternary Conditional Operator

This is a concise, one-line `if-else` expression used for simple assignments.

### Syntax

`value_if_true if condition else value_if_false`

### Example

```python
# Standard if-else
age = 20
if age >= 18:
    status = "Adult"
else:
    status = "Minor"

# Ternary equivalent
status = "Adult" if age >= 18 else "Minor"
print(status) # Output: Adult
```

---

## 7. Common Interview Questions

1.  **Q: What's the difference between using multiple `if` statements vs. an `if-elif-else` chain?**

    - **A:** Multiple `if`s are all checked independently. An `if-elif-else` chain is for mutually exclusive conditions; only the first true block is executed, and the rest are skipped.

2.  **Q: What values are considered "falsy" in Python?**

    - **A:** `None`, `False`, `0` (any numeric type), and any empty container (`''`, `[]`, `{}`, etc.).

3.  **Q: How should you check if a variable might be `None`?**

    - **A:** The preferred way is `if my_var is not None:`. This is explicit and avoids issues where a valid value like `0` or `''` would be treated as `False` by a simple `if my_var:`.

4.  **Q: Write a one-liner to assign a variable `sign` to `"positive"` if `num > 0` and `"non-positive"` otherwise.**
    - **A:** `sign = "positive" if num > 0 else "non-positive"`

---

## 8. Best Practices & Common Pitfalls

- **Best Practice**: Use `elif` for mutually exclusive choices. It's more efficient and clearly states the logical relationship.
- **Best Practice**: Keep conditions readable. If a condition is very complex, move it into a well-named function.
- **Pitfall**: Using assignment (`=`) instead of comparison (`==`). `if x = 5:` is a `SyntaxError` in Python, but it's a common bug in other languages that new Python developers might make.
- **Pitfall**: Overly complex nested `if` statements. These can often be simplified with logical operators or by restructuring the code.
- **Pitfall**: Misunderstanding truthiness. `if count:` will fail if `count = 0` is a valid state you need to handle. In that case, `if count is not None:` or a more specific check is better.
