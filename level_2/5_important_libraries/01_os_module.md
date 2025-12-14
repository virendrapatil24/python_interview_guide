# Deep Dive: The `os` Module

The `os` module provides a portable way of using operating system dependent functionality. While `pathlib` is modern, `os` and `os.path` remain widely used in legacy method bases and specific interview questions.

---

## 1. File Path Manipulation (`os.path`)

This is the most "asked about" section in interviews involving the `os` module.

### Common Operations

```python
import os

# 1. Joining Paths (Cross-platform safe)
# Windows: folder\file.txt, Linux/Mac: folder/file.txt
full_path = os.path.join("folder", "subfolder", "file.txt")

# 2. Checking Existence
if os.path.exists(full_path):
    print("Path exists")

if os.path.isfile(full_path):
    print("It is a specific file")

if os.path.isdir(dir_path):
    print("It is a directory")

# 3. Splitting Paths
# Returns ('/path/to', 'file.txt')
dirname, filename = os.path.split("/path/to/file.txt")

# Returns ('file', '.txt')
name, ext = os.path.splitext("file.txt")
```

---

## 2. Directory Operations

Handling directories is a core task.

### Creating and Deleting

```python
import os

# Create a single directory
# Fails if parent doesn't exist
os.mkdir("new_folder")

# Create nested directories (mkdir -p)
# exist_ok=True prevents error if it already exists
os.makedirs("parent/child/grandchild", exist_ok=True)

# Remove a file
os.remove("file.txt")

# Remove an EMPTY directory
os.rmdir("empty_folder")

# To remove a non-empty directory, use shutil
import shutil
shutil.rmtree("full_folder")
```

### Current Working Directory

```python
# Get current directory
cwd = os.getcwd()

# Change directory (cd)
os.chdir("/tmp")
```

---

## 3. Traversing Directories (`os.walk`)

The standard way to recursively process a directory tree.

```python
import os

root_dir = "."

# Yields a 3-tuple for every directory it visits
for dirpath, dirnames, filenames in os.walk(root_dir):
    print(f"Currently in: {dirpath}")
    
    for file in filenames:
        if file.endswith(".py"):
            print(f"Found python file: {os.path.join(dirpath, file)}")
```

**Interview Note**: `os.walk` is convenient but can be slow on massive file systems. Python 3.5+ introduced `os.scandir` (which `os.walk` now uses internally) for better performance.

---

## 4. Environment Variables

Accessing system environment variables (API keys, config).

```python
import os

# Get variable (returns None if missing, doesn't crash)
user = os.getenv("USER", "default_user")

# Get variable (raises KeyError if missing)
# path = os.environ["PATH"]

# Set variable (only for this process and children)
os.environ["MY_VAR"] = "production"
```

---

## 5. Running Shell Commands

### `os.system` (Simple but Limited)
Executes a command in a subshell. Return value is the **exit status**.

```python
exit_code = os.system("echo Hello World")
# Prints "Hello World" to stdout
# Returns 0 (success)
```

**Interview Tip**: For anything complex (capturing output, piping), **always** suggest the `subprocess` module instead of `os.system` or `os.popen`.

---

## Summary Checklist

| Function | Purpose |
| :--- | :--- |
| `os.path.abspath(path)` | Returns absolute path (`/home/user/rel/path`). |
| `os.path.expanduser("~")` | Expands `~` to the user's home directory. |
| `os.rename(src, dst)` | Renames a file or directory. |
| `os.cpu_count()` | Returns number of CPUs (useful for threads/multiprocessing). |
