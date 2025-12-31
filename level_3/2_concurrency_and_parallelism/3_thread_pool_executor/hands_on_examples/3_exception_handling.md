# Hands-on: Exception Handling in Pools

A critical difference between `threading.Thread` and `ThreadPoolExecutor` is how they handle crashes. 
-   In raw threads, an uncaught exception prints a traceback to stderr (usually) but doesn't crash the main interpreter.
-   In Executors, exceptions are **swallowed** (captured) by the Future and only revealed when you inspect it. If you forget to check, tasks can fail silently.

## The Silent Failure Trap

```python
from concurrent.futures import ThreadPoolExecutor
import time

def risky_task(x):
    if x == 3:
        raise ValueError("Boom! I don't like 3.")
    return x * 10

def demo_silent_failure():
    print("--- 1. Submitting without checking results ---")
    with ThreadPoolExecutor() as ex:
        ex.submit(risky_task, 3) 
    print("FINISHED. Did you see an error? No. (That's bad!)")

def demo_proper_handling():
    print("\n--- 2. Proper Exception Handling ---")
    with ThreadPoolExecutor() as ex:
        # Submit tasks
        futures = [ex.submit(risky_task, i) for i in [1, 3, 5]]
        
        for f in futures:
            try:
                # .result() re-raises the exception if one happened
                res = f.result()
                print(f"Success: {res}")
            except Exception as e:
                print(f"Caught Failed Task: {e}")

if __name__ == "__main__":
    demo_silent_failure()
    demo_proper_handling()
```

## Best Practices

1.  **Always Retrieve Results**: Even if a task returns `None`, calling `.result()` ensures you catch exceptions.
2.  **Use `done_callback` (Advanced)**: You can attach a callback to a future, but note that the callback runs in the *thread that completes the future*, which complicates error handling logic. Iteration is usually cleaner.
3.  **App Crash**: If you want the whole application to crash on a worker error (fail-fast), you must manually catch the exception in your main loop and `sys.exit()`.
