# Deep Dive: Typer (CLI)

Typer (built on Click) allows you to build CLI apps using Python type hints. It is to CLIs what FastAPI is to APIs.

---

## 1. Type Inference -> CLI Arguments

Typer uses the function signature to determine CLI arguments and options.

```python
import typer

def main(name: str, verbose: bool = False):
    """
    Say hello to NAME.
    """
    if verbose:
        print("We are in verbose mode")
    print(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
```

Run: `python main.py Virendra --verbose`
*   `name` is mandatory (positional).
*   `verbose` is optional (flag).

---

## 2. Subcommands (Command Groups)

Building tools like `git` (`git commit`, `git push`).

```python
app = typer.Typer()

@app.command()
def create(username: str):
    print(f"Creating user: {username}")

@app.command()
def delete(username: str):
    print(f"Deleting user: {username}")

if __name__ == "__main__":
    app()
```

---

## 3. Prompts and Validation

Typer makes interactivity easy.

```python
delete = typer.confirm("Are you sure?")
if not delete:
    typer.abort()
```
