# Hands-on: Handling Process Crashes

This script demonstrates how `ProcessPoolExecutor` reacts when a worker process is forcibly killed (simulating a Segfault or OOM).

## The Scenario
1.  We run a task that kills its own process using `os.kill`.
2.  We observe `BrokenProcessPool` in the parent.

## Code

```python
import time
import os
import signal
from concurrent.futures import ProcessPoolExecutor, BrokenProcessPool

def suicidal_worker(x):
    print(f"[Worker {os.getpid()}] processing {x}")
    if x == "KILL":
        print(f"[Worker {os.getpid()}] GOODBYE WORLD!")
        os.kill(os.getpid(), signal.SIGKILL)
    return x * 2

if __name__ == "__main__":
    print("--- Crash Resilience Demo ---")
    
    try:
        with ProcessPoolExecutor(max_workers=2) as executor:
            # We submit 3 tasks. The second one kills the worker.
            futures = [
                executor.submit(suicidal_worker, 10),
                executor.submit(suicidal_worker, "KILL"), 
                executor.submit(suicidal_worker, 20)
            ]
            
            for f in futures:
                try:
                    print(f"Result: {f.result()}")
                except BrokenProcessPool as e:
                    print(f"CRITICAL ERROR: The Pool is broken! {e}")
                    break # The pool is dead. Stop trying.
                except Exception as e:
                    print(f"Task Error: {e}")
                    
    except BrokenProcessPool:
        print("Outer Catch: The entire pool context collapsed.")

    print("\nRecovery Strategy: Re-instantiate the Executor.")
```

## Key Takeaways
1.  **Fragility**: A single worker crashing corrupts the *entire* pool state in standard `ProcessPoolExecutor`.
2.  **Detection**: The exception `BrokenProcessPool` is your signal that something went wrong at the OS level (not just a Python exception).
