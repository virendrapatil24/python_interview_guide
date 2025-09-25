# Choosing and Setting Up a Code Editor (VS Code)

## Introduction

A good code editor boosts productivity and helps with debugging, linting, and code navigation. VS Code is the most popular choice for Python development.

---

## 1. Why VS Code?

- Free, open-source, cross-platform.
- Rich extension ecosystem (Python, Jupyter, Git, etc.).
- Integrated terminal, debugger, and source control.
- Excellent support for Python and modern tools like uv.

---

## 2. Installing VS Code

- Download from [code.visualstudio.com](https://code.visualstudio.com/).
- Install for your OS (Windows, macOS, Linux).

---

## 3. Setting Up Python in VS Code

- Install the **Python extension** (by Microsoft).
- Open the Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`), search for "Python: Select Interpreter" and choose your Python environment (venv, uv, etc.).
- Install helpful extensions:
  - **Pylance** (fast, feature-rich Python language server)
  - **Jupyter** (for notebooks)
  - **Black** (code formatter)
  - **isort** (import sorter)
  - **GitLens** (git integration)

---

## 4. Using uv with VS Code

- Create and activate a uv environment:
  ```sh
  uv venv myenv
  source myenv/bin/activate
  ```
- In VS Code, select the interpreter from your uv environment.
- Use uv for dependency management and script execution.

---

## 5. Interview Tips

- Be able to set up VS Code from scratch.
- Know how to configure Python interpreters and extensions.
- Mention integration with modern tools like uv.
- Demonstrate debugging, linting, and code navigation features.

---

## References

- [VS Code Official Site](https://code.visualstudio.com/)
- [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [uv Project](https://github.com/astral-sh/uv)
