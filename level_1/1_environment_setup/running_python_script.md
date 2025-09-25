# Using the Command Line to Run a Python Script

## Introduction

Running Python scripts from the command line is a fundamental skill for any developer or interview candidate.

---

## 1. Basic Usage

- Save your Python code in a file, e.g., `hello.py`:
  ```python
  print("Hello, World!")
  ```
- Open your terminal (Command Prompt, PowerShell, Terminal, etc.).
- Navigate to the directory containing your script:
  ```sh
  cd path/to/your/script
  ```
- Run the script:
  ```sh
  python hello.py
  # or
  python3 hello.py
  ```

---

## 2. Using Arguments

- Python scripts can accept command-line arguments using `sys.argv`:
  ```python
  import sys
  print("Arguments:", sys.argv)
  ```
- Run with arguments:
  ```sh
  python script.py arg1 arg2
  ```

---

## 3. Running Scripts in Virtual Environments

- Activate your environment:
  - **venv:**
    ```sh
    source venv/bin/activate  # macOS/Linux
    .\venv\Scripts\activate  # Windows
    ```
  - **uv:**
    ```sh
    source myenv/bin/activate
    ```
- Run your script as above.

---

## 4. Using uv to Run Scripts

- uv can run scripts directly in isolated environments:
  ```sh
  uv pip install -r requirements.txt
  uv run python script.py
  ```

---

## 5. Interview Tips

- Be comfortable with basic and advanced script execution.
- Know how to pass arguments and use virtual environments.
- Mention modern tools like uv for reproducible runs.

---

## References

- [Python sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)
- [uv Project](https://github.com/astral-sh/uv)
