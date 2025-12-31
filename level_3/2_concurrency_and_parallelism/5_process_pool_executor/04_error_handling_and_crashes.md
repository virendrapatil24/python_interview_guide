# Resilience: Crashes, Zombies, and Debugging

Processes are fragile. They can be killed by the OS (OOM Killer) or segfault.

## 1. The "BrokenProcessPool" Error
If a worker process dies violently (e.g., Segfault), the Executor cannot trust the state of the pool anymore.

```python
from concurrent.futures import BrokenProcessPool

try:
    with ProcessPoolExecutor() as ex:
        ex.map(risky_function, data)
except BrokenProcessPool:
    # This means a WORKER DIED (Segfault, Kill -9).
    # You cannot reuse 'ex'. You must create a new executor.
    print("Pool collapsed. Restarting entire batch...")
```

## 2. The Robust Worker Pattern
Since a crash breaks the *entire* pool, you should prevent crashes at all costs. Wrap your worker logic in a "Safety Net".

```python
import traceback

def safe_worker(data):
    try:
        # Perform risky operation
        return perform_calculation(data)
    except Exception as e:
        # Catch unexpected errors to keep the process ALIVE
        return {
            "status": "error", 
            "error": str(e), 
            "trace": traceback.format_exc()
        }
    except BaseException as e:
        # Catch SystemExit or KeyboardInterrupt (optional)
        return {"status": "fatal", "error": str(e)}

# Parent Logic
future = executor.submit(safe_worker, item)
result = future.result()
if isinstance(result, dict) and result.get("status") == "error":
    print(f"Task Failed cleanly: {result['error']}")
```

## 3. Debugging Hanging Pools (Deadlocks)
If your pool just hangs (0% CPU, no progress), it is usually a **Queue Deadlock**.

### The Cause
You tried to return a massive object from the worker.
1.  Worker writes 100MB to Pipe.
2.  Pipe buffer fills up (64KB). Worker BLOCKS waiting for space.
3.  Parent is waiting for *other* tasks and isn't draining the pipe yet.
4.  **Deadlock**.

### The Fix
Do not return large data. Write results to a file, return the filename.

```python
# BAD
def worker():
    return [i for i in range(10_000_000)] # Huge list

# GOOD
def worker():
    fname = f"result_{os.getpid()}.pkl"
    with open(fname, 'wb') as f:
        pickle.dump(large_list, f)
    return fname # Return path string (tiny)
```
