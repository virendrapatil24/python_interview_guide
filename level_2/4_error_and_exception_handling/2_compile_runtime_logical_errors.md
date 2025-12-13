# Compile-time vs Runtime vs Logical Errors in Python

Understanding the lifecycle of an error is the first step in debugging. Python errors generally fall into three categories based on *when* they are detected.

---

## 1. Compile-time Errors (Syntax Errors)

### Definition
These are errors that violate the grammatical rules of the Python language. They are detected by the Python parser **before** the code actually starts running. If a file contains even one syntax error, none of the code in that file will execute.

### When it Happens
- **Parsing Stage**: When you invoke `python script.py`, the interpreter first reads the file and compiles it to bytecode. Syntax errors are caught here.

### Examples
- Missing colons (`:`)
- Unmatched parentheses
- Indentation errors (mixing tabs/spaces or bad levels)
- Invalid syntax like `if x = 5` (assignment instead of equality)

```python
# CODE
def my_func()  # Missing colon
    print("Hello")

# ERROR (Compile-time)
# SyntaxError: expected ':'
```

### Debugging Strategy
- Read the error message carefully; it usually points to the exact line (or the line just before it).
- Look for common typos (missing closing brackets are a frequent culprit).
- An IDE or linter (like Pylint, Flake8) will highlight these immediately.

---

## 2. Runtime Errors (Exceptions)

### Definition
These errors occur **during** the execution of the program. The code has passed the syntax check, but something went wrong while the interpreter was running the instructions.

### When it Happens
- **Execution Stage**: Specific lines of code trigger an illegal operation.

### Examples
- `ZeroDivisionError`: Dividing by zero.
- `TypeError`: Adding a string to an integer.
- `IndexError`: Accessing an invalid list index.
- `FileNotFoundError`: Trying to open a file that doesn't exist.

```python
# CODE
def divide(a, b):
    return a / b

print("Start") # This WILL print
divide(10, 0)  # Crash happens here
print("End")   # This will NOT print

# ERROR (Runtime)
# ZeroDivisionError: division by zero
```

### Debugging Strategy
- **Traceback**: Read the traceback from bottom to top. It tells you exactly where the crash happened and the sequence of function calls that led there.
- **Logging/Print**: Check variable values just before the crash.
- **Exception Handling**: Use `try...except` blocks to handle predictable runtime errors gracefully.

---

## 3. Logical Errors (Bugs)

### Definition
The most dangerous and difficult type of error. The program runs without crashing (no Syntax or Runtime errors), but it produces **incorrect results**. The logic of the code is flawed.

### When it Happens
- **Post-Execution / User Verification**: The computer does exactly what you told it to do, but what you told it to do was wrong.

### Examples
- Using the wrong formula (e.g., `area = 2 * 3.14 * r` instead of `3.14 * r**2`).
- Loop that runs one too many or too few times (off-by-one error).
- Assigning a value to the wrong variable.
- Incorrect boolean logic (e.g., using `and` instead of `or`).

```python
# CODE: Calculate average of two numbers
def average(a, b):
    return a + b / 2  # LOGIC ERROR! Should be (a + b) / 2

result = average(10, 20)
print(f"Average is: {result}")

# OUTPUT
# "Average is: 20.0" -> INCORRECT (Should be 15.0)
# No crash, just wrong math.
```

### Debugging Strategy
- **Unit Testing**: Write tests with known inputs and expected outputs.
- **Step-by-step Execution**: Use a debugger (like pdb or VS Code debugger) to step through the code and watch how variables change.
- **Code Review**: Explain your logic to someone else (Rubber Duck Debugging).
