# Deep Dive: Virtual Environments (`venv`)

A Virtual Environment is a self-contained directory tree that contains a Python installation for a specific version of Python, plus a number of additional packages.

**Golden Rule**: NEVER install packages globally (unless strictly system-wide tools). Always use a virtual environment for projects.

---

## 1. Why Isolation? The "Dependency Hell"

Imagine Project A needs `django==2.2` and Project B needs `django==4.0`.
If you install libraries globally (system-wide), you can only have **one** version of Django installed. Upgrading it for Project B breaks Project A.

**Virtual Environments solve this by creating an isolated folder (`.venv`) containing:**
1.  A copy (or symlink) of the Python binary.
2.  A standalone `site-packages` directory where `pip` installs libraries for *that specific project*.

---

## 2. Creating and Activating (`venv`)

The standard library module `venv` is the modern way to do this.

### Step 1: Creation
Run this in your project root.
```bash
# General syntax: python -m venv <directory_name>
python3 -m venv .venv
```
*Note: We name the folder `.venv` (hidden) or `venv` by convention.*

### Step 2: Activation
Activation modifies your shell's environment variables to point to the virtual environment's python/pip.

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
# cmd.exe
.venv\Scripts\activate.bat

# PowerShell
.venv\Scripts\Activate.ps1
```

### Step 3: Verifying
Once activated, your prompt usually changes (e.g., `(.venv) user@host $`).

```bash
which python
# Output should be: /path/to/project/.venv/bin/python
# NOT: /usr/bin/python
```

### Step 4: Deactivation
To exit the environment and return to system python:
```bash
deactivate
```

---

## 3. Internals: How it Works

When you run `source bin/activate`, it is a **shell script** that does effectively one thing:
**It prepends the virtual environment's `bin` directory to your `$PATH`.**

**Before Activation**:
`PATH=/usr/bin:/bin:/usr/sbin`

**After Activation**:
`PATH=/my/project/.venv/bin:/usr/bin:/bin:/usr/sbin`

When you type `python`, the shell looks in `$PATH` from left to right. It finds the local python first!

**Note**: You don't *strictly* need to activate. You can run the binary directly:
```bash
./.venv/bin/python my_script.py
```
This is how cron jobs or systemd services usually run python scripts.

---

## 4. Best Practices

1.  **Gitignore**: **ALWAYS** add your venv directory to `.gitignore`.
    *   Binaries are not portable across OS (Mac venv won't work on Linux).
    *   It bloats the repo size by 100s of MBs.
    ```text
    # .gitignore
    venv/
    .venv/
    ```

2.  **Recreating**: If you move the project folder, the venv might break (hardcoded paths in scripts). It's safer to delete the old `venv` folder and recreate it.

3.  **Specific Python Versions**:
    If you have multiple python versions installed:
    ```bash
    python3.10 -m venv venv_310
    python3.11 -m venv venv_311
    ```
