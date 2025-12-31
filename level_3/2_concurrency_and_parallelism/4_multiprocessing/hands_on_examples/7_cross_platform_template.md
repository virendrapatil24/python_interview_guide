# Hands-on: Cross-Platform Universal Template

Writing code that works on Linux, Windows, and macOS requires specific patterns. This file serves as a copy-paste template.

## The Template
```python
import multiprocessing
import sys
import os

def worker(name, context_data):
    """
    Worker function.
    NOTE: All imports needed inside the worker should ideally be at the top level,
    but sometimes local imports are safer to avoid circular deps in 'spawn'.
    """
    print(f"[Worker {os.getpid()}] Hello {name}. Context: {context_data}")

def main():
    # 1. ALWAYS protect the entry point
    # This prevents the child process from recursively spawning new processes on import.
    
    # 2. Select Context Explicitly
    # 'spawn' is the safest baseline for all platforms.
    # 'fork' is Linux only and fast but unsafe with threads.
    try:
        ctx = multiprocessing.get_context('spawn')
    except ValueError:
        ctx = multiprocessing.get_context('fork') # Fallback if spawn missing (ancient python)

    # 3. Use the context to create objects (Queues, Pools, Processes)
    # Do NOT use multiprocessing.Queue() directly. Use ctx.Queue().
    q = ctx.Queue() 
    
    # 4. Creating a Process
    p = ctx.Process(target=worker, args=("Alice", {"env": "prod"}))
    p.start()
    p.join()
    
    print("[Main] Done.")

if __name__ == "__main__":
    # 5. Optional: Freeze Support for PyInstaller/Executable builds
    multiprocessing.freeze_support()
    
    main()
```

## Checklist for Cross-Platform Code
1.  **Strict Entry Point**: Is all execution logic inside `if __name__ == "__main__":`?
2.  **No Global State Reliance**: Does the worker function rely on global variables defined in `main`? (It shouldn't).
3.  **Picklability**: Are all arguments passed to `args=(...)` picklable? (Lambdas and local functions are NOT picklable).
4.  **Context**: Are you using `get_context('spawn')` to behave consistently across Linux/Mac/Win?
