# Deep Dive: Managing Dependencies

In a real-world project, you never just "remember" what to install. You record dependencies in a `requirements.txt` file (or strictly speaking, a lock file) to ensure reproducibility.

---

## 1. The `requirements.txt` Workflow

This file lists packages to install, one per line.

### Generating the file
Use `pip freeze` to output installed packages in requirements format.
```bash
# Capture current environment state
pip freeze > requirements.txt
```

### Installing from the file
When a new developer joins, or you deploy to production:
```bash
pip install -r requirements.txt
```

---

## 2. Versioning Strategies (Pinning)

How strictly should you define versions?

### Loose (Bad for reproducibility, good for updates)
```text
requests
pandas
```
*Risk*: If `requests` releases a breaking change tomorrow, your production build might break.

### Pinned (Strict Reproducibility)
```text
requests==2.28.1
pandas==1.5.3
```
*Benefit*: Everyone has the EXACT same code.
*Drawback*: You must manually upgrade packages.

### Constrained (The Middle Ground)
Compatible versioning prevents major breaking changes.
```text
# Allow any version 2.x.x >= 2.28.0
requests>=2.28.0,<3.0.0
```

---

## 3. Advanced: Development Dependencies

You typically don't want `pytest`, `black`, or `pylint` in your production docker image. Use separate files.

**`requirements.txt` (Base/Prod)**
```text
flask==2.2.0
gunicorn==20.1.0
```

**`requirements-dev.txt`**
```text
-r requirements.txt  # Include base requirements
pytest==7.0.0
black==22.3.0
```

**Install commands**:
*   Prod: `pip install -r requirements.txt`
*   Dev: `pip install -r requirements-dev.txt`

---

## 4. The "Dependency Hell" (Transitive Dependencies)

A "Transitive Dependency" is a dependency OF a dependency.
*   You install `Flask`.
*   `Flask` installs `Werkzeug`, `Jinja2`, `click`...

**The Problem**:
If Library A requires `requests==1.0` and Library B requires `requests==2.0`, `pip` (older versions) would just install whatever. Modern `pip` has a **dependency resolver** that will error out if conflicts are impossible to solve.

**The Solution**:
For complex projects, simple `requirements.txt` isn't enough. Tools like **`poetry`** or **`pip-tools`** manage dependency locking/resolution much better than raw pip.
