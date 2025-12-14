# Deep Dive: The `pathlib` Module

Introduced in Python 3.4, `pathlib` offers an Object-Oriented approach to filesystem paths. It is widely preferred over `os.path` for being more readable and robust.

---

## 1. The Basics: Common Operations

These are the methods you will use 95% of the time.

```python
from pathlib import Path

# 1. Creating Paths
p = Path("folder") / "subfolder" / "file.txt"
print(p) # folder/subfolder/file.txt (Mac/Linux)

# 2. Checking Existence
if p.exists():
    print("It is there!")

# 3. Creating Directories
# parents=True -> mkdir -p (creates missing parents)
# exist_ok=True -> Don't error if it already exists
p.parent.mkdir(parents=True, exist_ok=True)

# 4. File Parts
print(p.name)   # file.txt
print(p.stem)   # file
print(p.suffix) # .txt
print(p.parent) # folder/subfolder

# 5. Renaming / Moving
# p.rename(target_path)
```

---

## 2. Object-Oriented Paths vs Strings

Old `os.path` manipulated strings. `pathlib` manipulates Objects.

**The Old Way (`os.path`)**:
```python
import os
path = "/usr/bin/python3"
parent = os.path.dirname(path)
full = os.path.join(parent, "local", "bin")
```

**The New Way (`pathlib`)**:
```python
from pathlib import Path
path = Path("/usr/bin/python3")
parent = path.parent
full = parent / "local" / "bin"  # Note the '/' operator!
```

**Principal / Interview Insight**:
*   `pathlib` handles **platform differences** (Windows `\` vs Unix `/`) automatically.
*   `Path` objects are immutable and hashable (can be dict keys).

---

## 3. Path Arithmetic and Resolution

### The `/` Operator
The division operator is overloaded to join path components.
`Path("folder") / "subfolder" / "file.txt"`

### `resolve()`: Handling Symlinks and `..`
`resolve()` makes a path absolute and follows symbolic links (like `readlink -f` in bash).

```python
p = Path("src/../src/main.py")
print(p.resolve())
# Output: /abs/path/to/project/src/main.py (Cleaned up)

# Strict check (raises FileNotFoundError if it doesn't exist)
try:
    p.resolve(strict=True)
except FileNotFoundError:
    print("File does not exist on disk")
```

---

## 4. Reading and Writing (Convenience Methods)

Stop writing `with open(...)` for simple whole-file operations.

```python
p = Path("config.json")

# Write text (UTF-8 by default)
p.write_text('{"status": "ok"}')

# Read text
content = p.read_text()

# Check existence and type
if p.exists() and p.is_file():
    print(f"File size: {p.stat().st_size} bytes")
```

---

## 5. Traversing Directories (`glob` vs `rglob`)

`pathlib` integrates globbing directly.

*   `glob(pattern)`: Matches files in the current directory.
*   `rglob(pattern)`: Recursive glob (matches in current AND subdirectories).

```python
root = Path(".")

# Find all Python files recursively
for py_file in root.rglob("*.py"):
    # Iterate efficiently
    print(py_file.name)
```

---

## Summary Checklist

| Operation | `os.path` (Old) | `pathlib` (New) |
| :--- | :--- | :--- |
| Join paths | `os.path.join(a, b)` | `a / b` |
| Get file name | `os.path.basename(p)` | `p.name` |
| Get extension | `os.path.splitext(p)[1]` | `p.suffix` |
| Make dirs | `os.makedirs(p, exist_ok=True)` | `p.mkdir(parents=True, exist_ok=True)` |
