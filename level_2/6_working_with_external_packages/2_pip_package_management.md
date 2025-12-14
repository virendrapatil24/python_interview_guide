# Deep Dive: Package Management (`pip`)

`pip` is the standard package installer for Python. It connects to the **Python Package Index (PyPI)** to download and install third-party libraries.

---

## 1. Basic Commands

These are the daily bread-and-butter commands.

### Installing Packages
```bash
# Latest version
pip install requests

# Specific Version (Recommended for Prod)
pip install pandas==1.5.3

# Minimum Version
pip install "numpy>=1.20"
```

### Managing Installed Packages
```bash
# List all installed packages
pip list

# Show details of a specific package (Location, Version, Dependencies)
pip show flask

# Check for broken dependencies
pip check
# Output (ideal): "No broken requirements found."
```

### Removing Packages
```bash
pip uninstall requests
```

---

## 2. Installing from other sources

`pip` isn't limited to PyPI.

### Installing from Git
Useful when you need a bug fix that is merged into `main` but not yet released on PyPI.
```bash
# General syntax: pip install git+https://github.com/user/repo.git
pip install git+https://github.com/psf/requests.git@main
```

### Installing from Local Disk (Editable Mode)
This is critical for package development. It installs the package in "Editable" mode (`-e`). Changes you make to the source code are immediately reflected without reinstalling.

```bash
# Run this where setup.py or pyproject.toml is located
pip install -e .
```

---

## 3. Configuration & Caching

### The Cache
`pip` caches downloads to speed up future installs.
```bash
# Location varies by OS
pip cache dir

# To clear cache (fix corrupt downloads)
pip cache purge
```

### Configuration (`pip.conf` / `pip.ini`)
You can globally configure pip behavior (e.g., setting a timeout, or a custom index URL for enterprise).

**Example `pip.conf`**:
```ini
[global]
timeout = 60
index-url = https://my-private-pypi.company.com/simple
```

---

## 4. Troubleshooting Common Issues

### "Pip not found"
If `pip` command is missing but python is installed:
```bash
python -m pip install requests
```
Using `python -m pip` is arguably safer because it guarantees you are installing modules for *that specific python interpreter*.

### Permission Denied
**Bad Practice**: `sudo pip install package` (Don't do this! It messes up system python).
**Good Practice**: Fix permissions or use a Virtual Environment.
**Fallback**: `pip install --user package` (Installs to `~/.local`).
