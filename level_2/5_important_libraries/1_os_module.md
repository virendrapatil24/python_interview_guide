# Deep Dive: The `os` Module

The `os` module is the bridge between Python and the underlying Operating System (kernel). While most developers use it for file paths, its true power lies in low-level process management and I/O operations.

---

## 1. File Objects vs. File Descriptors

In Python, `open()` returns a **File Object** (a high-level wrapper). The OS kernel, however, uses **File Descriptors (FDs)**—integers acting as handles to open files, sockets, or pipes.

### The Low-Level `os.open`
`os.open()` returns a raw FD (integer), unlike the built-in `open()`.

```python
import os

# Low-level open: Returns an integer (FD)
# os.O_RDWR : Open for reading and writing
# os.O_CREAT : Create file if it doesn't exist
fd = os.open("deep_file.txt", os.O_RDWR | os.O_CREAT)

# Write bytes directly to the file descriptor
# Note: os.write expects bytes, not strings
os.write(fd, b"Hello from the kernel level!\n")

# Seek to beginning
os.lseek(fd, 0, os.SEEK_SET)

# Read bytes
data = os.read(fd, 1024)
print(f"Read: {data}")

# ALWAYS close raw FDs
os.close(fd)
```

**Why care?**
*   **Performance**: Bypassing buffering for raw I/O.
*   **Pipes/Sockets**: Networking libraries often work with raw FDs.
*   **Locking**: `fcntl` (on Unix) requires FDs, not file objects.

---

## 2. Process Management: `fork` and `exec`

This is the foundation of how Unix-like systems (Linux, Mac) run programs. Windows handles this differently (via `subprocess` module abstraction), so `os.fork` is **Unix-only**.

### The `fork()` System Call
`os.fork()` creates a copy of the current process. It returns `0` to the child process and the `child_pid` to the parent process.

```python
import os
import time

print(f"Parent Process PID: {os.getpid()}")

try:
    pid = os.fork()  # Splitting reality here
except AttributeError:
    print("OS does not support fork (probably Windows)")
    pid = None

if pid == 0:
    # CHILD PROCESS
    print(f"  [Child] I am the new process! My PID is {os.getpid()}")
    print(f"  [Child] My Parent's PID is {os.getppid()}")
    # Child usually does work and exits
    os._exit(0)  # fast exit, skipping cleanup handlers
elif pid:
    # PARENT PROCESS
    print(f"  [Parent] I created a child with PID {pid}")
    # Wait for child to finish to prevent "Zombie Processes"
    os.waitpid(pid, 0)
    print("  [Parent] Child has finished.")
```

**Interview Tip**: If you don't `wait()` for your children, they become **Zombies** (entries in the process table that are dead but not reaped) until the parent (or init) reaps them.

---

## 3. High-Performance Filesystem Traversal (`os.scandir`)

Before Python 3.5, `os.listdir()` was used to list files. It returned a list of strings (filenames). To check if a file was a directory, you had to call `os.stat()` on every single file, which meant **N+1 system calls**.

### `os.scandir()` (Iterator Protocol)
Returns `DirEntry` objects that cache file type information (and sometimes size) from the initial directory read. This can be **2-20x faster** on network drives.

```python
import os

def count_files_fast(path):
    total = 0
    # Returns an iterator, not a list (memory efficient)
    with os.scandir(path) as it:
        for entry in it:
            # entry.is_file() usually requires NO system call!
            if entry.is_file():
                total += 1
            elif entry.is_dir():
                total += count_files_fast(entry.path)
    return total
```

---

## 4. Environment and `os.environ`

`os.environ` captures the environment variables **at the time Python started**.

**Gotcha**: Modifying `os.environ` updates the environment for the current process and any *future* child processes spawned by it, but it does **not** affect the *parent* shell (bash/zsh) that launched Python.

```python
import os

# Setting a variable
os.environ["API_KEY"] = "secret_123"

# Spawning a child sees it
# Using os.system or subprocess inherits this env by default
os.system("echo Child sees key: $API_KEY") 
```

---

## 5. Critical `os` Functions Checklist

| Function | Purpose | Principal Note |
| :--- | :--- | :--- |
| `os.cpu_count()` | Logical CPU cores | Use to determine worker pool size for `multiprocessing`. |
| `os.pipe()` | Inter-process communication | Returns a read/write FD pair. |
| `os.urandom(n)` | Cryptographically strong random bytes | Used by `secrets` module. Blocks if entropy pool is empty (rare). |
| `os.replace(src, dst)` | Atomic file move | **Atomic** on POSIX. Guarantees file integrity better than `shutil.move`. |
| `os.getcwd()` / `os.chdir()` | Working directory | **Thread-unsafe**: `chdir` changes CWD for the *entire* process (all threads). Avoid using `chdir` in multithreaded apps. |
