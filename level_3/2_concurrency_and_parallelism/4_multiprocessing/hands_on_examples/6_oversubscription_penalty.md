# Hands-on: Oversubscription Penalty

More processes ≠ More Speed. This demo shows what happens when you create more processes than you have CPU cores.

## The Scenario
*   We have a CPU-heavy task (calculating primes).
*   We run it on a `Pool` with `os.cpu_count()` workers (Optimal).
*   We run it on a `Pool` with `os.cpu_count() * 4` workers (Oversubscribed).

## Code Implementation
```python
import multiprocessing
import time
import os

def heavy_computation(x):
    # Inefficient prime check to burn CPU
    count = 0
    for i in range(2, x):
        if x % i == 0:
            count += 1
    return count

if __name__ == "__main__":
    cpu_count = os.cpu_count()
    tasks = [30000 + i for i in range(100)] # 100 heavy tasks
    
    # 1. Optimal Pool
    print(f"--- 1. Optimal Pool ({cpu_count} workers) ---")
    start = time.time()
    with multiprocessing.Pool(processes=cpu_count) as pool:
        pool.map(heavy_computation, tasks)
    print(f"Optimal Time: {time.time() - start:.2f}s")
    
    # 2. Oversubscribed Pool
    worker_count = cpu_count * 4
    print(f"\n--- 2. Oversubscribed Pool ({worker_count} workers) ---")
    start = time.time()
    with multiprocessing.Pool(processes=worker_count) as pool:
        pool.map(heavy_computation, tasks)
    print(f"Oversubscribed Time: {time.time() - start:.2f}s")
```

## Key Discussion Points
*   **Context Switching**: In the oversubscribed case, the OS scheduler has to constantly pause one process to run another. This context switch invalidates CPU caches (L1/L2), drastically reducing performance.
*   **Verdict**: Never set `processes` higher than `os.cpu_count()` for **CPU-bound** tasks.
*   **Exception**: For **I/O-bound** tasks (scraping), oversubscription is fine (and recommended) because processes spend most time sleeping.
