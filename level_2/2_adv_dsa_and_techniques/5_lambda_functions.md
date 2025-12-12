# Lambda Functions (Anonymous Functions)

A Lambda function is a small, anonymous function defined with the `lambda` keyword. It can take any number of arguments, but can only have **one expression**.

## 1. Syntax

```python
lambda arguments: expression
```

### Comparison with Regular Function

```python
# Regular function
def add(x, y):
    return x + y

# Equivalent Lambda
add_lambda = lambda x, y: x + y

print(add(5, 3))        # 8
print(add_lambda(5, 3)) # 8
```

## 2. Common Use Cases

Lambdas are rarely assigned to variables like above. They are mostly used as short-term arguments to higher-order functions like `map`, `filter`, and `sort`.

### A. Cleaning Data with `map()`
Apply a function to every item in an iterable.

```python
nums = [1, 2, 3, 4]
squared = list(map(lambda x: x**2, nums))
# Output: [1, 4, 9, 16]
```

### B. Filtering Data with `filter()`
Keep items where the function returns `True`.

```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
# Output: [2, 4, 6]
```

### C. Advanced Sorting (Key Functions)
This is a frequent interview task: "Sort this list of dictionaries by a specific key."

```python
students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 95}
]

# Sort by 'score'
students.sort(key=lambda x: x['score'])
print(students)
# Output: [{'name': 'Bob', 'score': 75}, {'name': 'Alice', 'score': 90}, {'name': 'Charlie', 'score': 95}]

# Sort by name length
students.sort(key=lambda x: len(x['name']))
```

## Common Interview Questions

**Q: What are the limitations of lambda functions?**
-   **A:** They are restricted to a **single expression**. They cannot contain statements (like `print`, `return`, `if` statements without `else`, or `while` loops). If you need complex logic, write a formal `def` function.

**Q: Why use lambda instead of a named function?**
-   **A:** Conciseness. When you need a throwaway function for a short period (like inside a `sort` key), defining a full function adds unnecessary boilerplate code.

**Q: Is lambda faster than a regular function?**
-   **A:** No. A lambda function creates the exact same function object bytecode as a regular `def` function. The difference is purely syntactic sugar.
