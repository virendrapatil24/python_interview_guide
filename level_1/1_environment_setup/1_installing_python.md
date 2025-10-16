# Installing Python on Your OS (Windows, macOS, Linux)

## Introduction

Python is a versatile programming language used in web development, data science, automation, and more. Installing Python correctly is the first step for any developer or interview candidate.

---

## 1. Windows

### Using Official Installer

- Visit [python.org/downloads](https://www.python.org/downloads/).
- Download the latest version for Windows.
- Run the installer. **Important:** Check "Add Python to PATH" during installation.
- Verify installation:
  ```sh
  python --version
  ```

### Using Windows Package Managers

- **winget** (Windows 10/11):
  ```sh
  winget install Python.Python.3
  ```
- **chocolatey**:
  ```sh
  choco install python
  ```

---

## 2. macOS

### Using Official Installer

- Download the macOS installer from [python.org](https://www.python.org/downloads/).
- Run the installer and follow instructions.

### Using Homebrew

- Install Homebrew if not present:
  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- Install Python:
  ```sh
  brew install python
  ```

### Using uv (Modern Python Installer)

- [uv](https://github.com/astral-sh/uv) is a fast Python package manager and environment tool.
- Install uv:
  ```sh
  curl -Ls https://astral.sh/uv/install.sh | sh
  ```
- Create a new Python environment:
  ```sh
  uv venv myenv
  source myenv/bin/activate
  ```
- uv can also manage dependencies and run scripts efficiently.

---

## 3. Linux

### Using System Package Manager

- **Debian/Ubuntu:**
  ```sh
  sudo apt update
  sudo apt install python3 python3-pip
  ```
- **Fedora:**
  ```sh
  sudo dnf install python3 python3-pip
  ```
- **Arch:**
  ```sh
  sudo pacman -S python python-pip
  ```

### Using uv

- Install uv as above (works on Linux).
- Use uv to create and manage environments.

---

## 4. Verifying Installation

- Check Python version:
  ```sh
  python --version
  python3 --version
  ```
- Check pip version:
  ```sh
  pip --version
  pip3 --version
  ```

---

## 5. Interview Tips

- Know how to install Python on all major OSes.
- Understand virtual environments (venv, uv).
- Be able to troubleshoot PATH issues.
- Mention modern tools like uv for fast, reproducible environments.

---

## References

- [Python Official Downloads](https://www.python.org/downloads/)
- [uv Project](https://github.com/astral-sh/uv)
- [Homebrew](https://brew.sh/)
