# Python Loops: `for` and `while`

Loops are fundamental control flow structures that allow you to repeat a block of code multiple times. Python provides two main types of loops: `for` loops for iterating over sequences and `while` loops for repeating based on a condition.

---

## 1. The `for` Loop

A `for` loop is used for **definite iteration**, meaning you iterate over a collection of items (like a list, tuple, dictionary, set, or string) until the sequence is exhausted.

### Syntax

```python
for item in iterable:
    # Code to execute for each item
```

- **`item`**: A variable that takes the value of the current item in the sequence on each iteration.
- **`iterable`**: A collection of objects that can be looped over (e.g., a list, string, or a `range` object).

### Examples

**Iterating over a list:**

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

**Iterating over a string:**

```python
for char in "Python":
    print(char)
```

**Using `range()` for numerical loops:**
The `range()` function generates a sequence of numbers, which is useful for looping a specific number of times.

```python
for i in range(5):  # Generates numbers from 0 to 4
    print(i)
```

**Iterating over a dictionary:**

```python
person = {"name": "Alice", "age": 25}

# By default, iterates over keys
for key in person:
    print(key, person[key])

# Explicitly iterating over items (key-value pairs)
for key, value in person.items():
    print(f"{key}: {value}")
```

---

## 2. The `while` Loop

A `while` loop is used for **indefinite iteration**. It repeats a block of code as long as a certain condition remains `True`.

### Syntax

```python
while condition:
    # Code to execute as long as condition is True
```

- **`condition`**: A Boolean expression. The loop continues as long as this is `True`.

### Example

```python
count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1  # Important: Update the condition variable to avoid an infinite loop

print("Loop finished.")
```

**Pitfall**: If the condition in a `while` loop never becomes `False`, it will run forever. This is called an **infinite loop**. Always ensure there is a mechanism within the loop to eventually terminate it.

---

## 3. Loop Control Statements

These statements change the normal flow of a loop.

### `break`

Terminates the loop entirely and transfers execution to the statement immediately following the loop.

```python
for i in range(10):
    if i == 5:
        break  # Stop the loop when i is 5
    print(i)
# Output: 0, 1, 2, 3, 4
```

### `continue`

Skips the rest of the code inside the current iteration and proceeds to the next iteration of the loop.

```python
for i in range(5):
    if i == 2:
        continue  # Skip printing when i is 2
    print(i)
# Output: 0, 1, 3, 4
```

### The `else` Clause in Loops (Advanced Concept)

Python loops can have an `else` block that executes **only if the loop completes its full course without being terminated by a `break` statement**. This is a unique and powerful feature.

```python
numbers = [1, 3, 7, 9]
for num in numbers:
    if num % 2 == 0:
        print("Found an even number:", num)
        break
else:
    # This block runs because the loop finished without a 'break'
    print("No even numbers found.")
```

---

## 4. Pythonic Looping Techniques

### `enumerate()`

Use `enumerate()` to get both the index and the value during iteration, which is cleaner than maintaining a manual counter.

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"Index {index}: {fruit}")
```

### `zip()`

Use `zip()` to iterate over multiple iterables in parallel.

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old.")
```

### List Comprehensions

A concise and often faster way to create lists from a `for` loop.

```python
# Traditional for loop
squares = []
for i in range(5):
    squares.append(i * i)

# List comprehension equivalent
squares_comp = [i * i for i in range(5)]
```

---

## 5. Common Interview Questions

1.  **Q: What is the difference between a `for` loop and a `while` loop?**

    - **A:** A `for` loop is for definite iteration over a known sequence. A `while` loop is for indefinite iteration that continues as long as a condition is true.

2.  **Q: What does the `else` block on a loop do? When is it useful?**

    - **A:** The `else` block executes when a loop completes normally (i.e., not terminated by `break`). It's useful for running code after a search loop that didn't find what it was looking for.

3.  **Q: How do you iterate over a list and get both the index and value?**

    - **A:** Use the `enumerate()` function: `for index, value in enumerate(my_list):`.

4.  **Q: What is an iterable in Python?**

    - **A:** An iterable is any Python object capable of returning its members one at a time, permitting it to be iterated over in a `for` loop. Examples include lists, strings, tuples, dictionaries, and sets.

5.  **Q: What is a common pitfall when modifying a list while iterating over it?**
    - **A:** Modifying a list (e.g., removing items) while iterating over it can lead to unexpected behavior like skipping items, because the loop's internal counter and the list's size become out of sync. It's safer to iterate over a copy (`for item in my_list[:]`) or create a new list.

---

## 6. Best Practices & Common Pitfalls

- **Best Practice**: Use `for` loops when you know the number of iterations or are iterating over a collection. Use `while` loops for conditions that don't depend on a sequence.
- **Best Practice**: Prefer `enumerate()` over manual index tracking.
- **Best Practice**: Use list comprehensions for creating new lists from existing iterables as they are more readable and often faster.
- **Pitfall**: Creating an infinite `while` loop by forgetting to update the loop's control variable.
- **Pitfall**: Modifying a collection while iterating over it. This can lead to unpredictable results. Iterate over a copy if modification is necessary.
- **Pitfall**: Using a complex loop when a built-in function or a library function (e.g., from `itertools`) would be simpler and more efficient.
