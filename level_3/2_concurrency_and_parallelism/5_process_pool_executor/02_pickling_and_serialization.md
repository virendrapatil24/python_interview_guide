# Pickling: The Hidden Requirement

The most common error developers face with `ProcessPoolExecutor` is `PickleError` (or `AttributeError`).

## 1. Why Pickling?
Because processes have isolated memory, Python cannot just pass a pointer to a function. It must:
1.  **Serialize** (Pickle) the function code AND the arguments in the Parent process.
2.  **Send** bytes over a specialized Pipe.
3.  **Deserialize** (Unpickle) them in the Child process.

## 2. What is NOT Picklable (The Deal Breakers)

### A. Lambdas (The most common crash)
```python
# FAILS
executor.map(lambda x: x**2, [1, 2, 3])
# Error: Can't pickle <function <lambda> at ...> because it has no name context.
```

### B. Instance Methods (Sometimes)
Depending on Python version and OS, passing an instance method can fail if the *instance itself* is not picklable (e.g., holds a socket).

```python
class DatabaseWorker:
    def __init__(self):
        self.conn = sqlite3.connect(...) # Sockets/Connectors are NOT picklable

    def run(self, query):
        return self.conn.execute(query)

# FAILS
worker = DatabaseWorker()
executor.submit(worker.run, "SELECT *") 
# Crash: "TypeError: cannot pickle sqlite3.Connection objects"
```

## 3. The "Top-Level" Fix
To ensure picklability, define functions at the **Module Level** or use `staticmethods` that don't rely on `self`.

```python
# GOOD: Standalone function
def process_query(query_str):
    # Create connection INSIDE the worker
    conn = sqlite3.connect(...) 
    return conn.execute(query_str)

with ProcessPoolExecutor() as ex:
    ex.submit(process_query, "SELECT 1")
```

## 4. The "ImportMain" Trap
On Windows and macOS (spawn method), the child process imports the main script effectively.

### The Bug
```python
# script.py
print("I am running!") # <--- This runs in EVERY child process!

if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:
        ...
```
**Result**: If you spawn 4 workers, you see "I am running!" printed 5 times (1 Parent + 4 Children).

### The Fix
Wrap **all** executable code in the guard:
```python
# script.py
def main():
    with ProcessPoolExecutor() as ex:
        ...

if __name__ == "__main__":
    print("I run only once.")
    main()
```
