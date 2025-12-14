# Deep Dive: The `sys` Module

The `sys` module interacts with the Python *interpreter* itself. For a skilled developer, it is extensively used for scripting, debugging imports, and handling standard input/output streams.

---

## 1. Command Line Arguments (`sys.argv`)

The most common use of `sys`. It captures arguments passed to the script.
`sys.argv` is a **list of strings**.

*   `sys.argv[0]`: The name of the script itself.
*   `sys.argv[1:]`: The actual arguments passed by the user.

```python
import sys

# Usage: python script.py debug
if len(sys.argv) > 1 and sys.argv[1] == "debug":
    print("Debug mode enabled")

# Interview Tip: For complex CLI tools, don't parse sys.argv manually.
# Use libraries like 'argparse' (built-in) or 'click'/'typer'.
```

---

## 2. Exiting the Program (`sys.exit`)

Properly terminating a script with an exit status code.
*   `sys.exit(0)`: Success (default).
*   `sys.exit(1)`: Failure (non-zero).

```python
import sys

def connect_db():
    return False

if not connect_db():
    # Prints the message to stderr and exits with status 1
    sys.exit("Critical Error: Database connection failed!")
```

**Why keep it handy?**: It's the standard way to signal failure to CI/CD pipelines or shell scripts executing your Python code.

---

## 3. Standard I/O Streams (`stdin`, `stdout`, `stderr`)

Sometimes `print()` isn't enough. You need direct access to the file objects.

*   `sys.stdout`: Where `print()` sends data.
*   `sys.stderr`: For error messages. (Unbuffered, often separated in logs).
*   `sys.stdin`: For reading piped input.

```python
import sys

# 1. Printing to Standard Error (Standard Pattern)
# Useful because > redirection only captures stdout, not stderr
print("This is a log", file=sys.stderr)

# 2. Reading Piped Input
# Usage: echo "Hello" | python script.py
if not sys.stdin.isatty():
    # Only read if input is actually being piped
    data = sys.stdin.read()
    print(f"Received from pipe: {data.strip()}")
```

---

## 4. Debugging Imports (`sys.path`)

When you get `ModuleNotFoundError`, checking `sys.path` is your first debugging step. It is the list of directories Python searches for modules.

```python
import sys

# Print where Python is looking for modules
print(sys.path)

# Runtime Hack: Adding a dynamic directory
# (Common in messy or legacy projects to import sibling folder)
sys.path.append("/path/to/custom/libs")
import my_lib
```

---

## 5. Platform Check (`sys.platform`)

Writing cross-platform scripts often requires checking the OS.

```python
import sys

if sys.platform.startswith("linux"):
    # Linux specific code
    pass
elif sys.platform == "darwin":
    # macOS specific code
    pass
elif sys.platform == "win32":
    # Windows specific code
    pass
```

---

## Summary Checklist

| Function | Purpose |
| :--- | :--- |
| `sys.executable` | Absolute path to the python interpreter running the code. |
| `sys.version` | Python version string (often checked as `sys.version_info >= (3, 9)`). |
| `sys.getrecursionlimit()` | Check max stack depth (default 1000). |
| `sys.modules` | Check if a library is already imported/cached. |
