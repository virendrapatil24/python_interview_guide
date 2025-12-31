# Hands-on: Startup Costs (Fork vs Spawn)

This demonstrates the performance impact of starting a new process using different methods.

## The Scenario
-   We create 20 empty processes.
-   We measure the total time taken to start (and join) them.
-   We try `fork` (fast, unsafe) vs `spawn` (slow, safe).

## Code Implementation

```python
import multiprocessing
import time
import sys

def do_nothing():
    pass

def benchmark(method):
    try:
        ctx = multiprocessing.get_context(method)
    except ValueError:
        print(f"Method '{method}' is not supported on this OS.")
        return

    start = time.time()
    procs = []
    
    # Create 20 processes
    for _ in range(20):
        p = ctx.Process(target=do_nothing)
        p.start()
        procs.append(p)
        
    for p in procs:
        p.join()
        
    print(f"Method '{method:<10}': {time.time() - start:.4f} seconds")

if __name__ == "__main__":
    print(f"Current OS: {sys.platform}")
    available = multiprocessing.get_all_start_methods()
    print(f"Available methods: {available}\n")
    
    for method in ['fork', 'spawn', 'forkserver']:
        if method in available:
            benchmark(method)
```

## Key Discussion Points
1.  **Results**: You should see `fork` is 10x-50x faster than `spawn`.
    -   *Why?* `fork` just copies page tables. `spawn` re-initializes Python from scratch.
2.  **macOS Warning**: Even though `fork` is fast, do NOT use it if you are using high-level macOS frameworks (like `requests` with SSL, or `matplotlib`). It will likely crash. Python defaults to `spawn` on macOS for a reason.
