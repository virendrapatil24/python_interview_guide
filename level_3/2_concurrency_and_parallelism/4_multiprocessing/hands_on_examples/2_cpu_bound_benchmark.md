# Hands-on: CPU Bound Benchmark (GIL Bypass)

This benchmark proves that `multiprocessing` can utilize multiple cores, while `threading` cannot.

## The Scenario
We perform a CPU-heavy task: decrementing a large number (100,000,000).
-   **Sequential**: Run task twice (1 core).
-   **Threading**: Run task twice in parallel threads (1 core due to GIL).
-   **Multiprocessing**: Run task twice in parallel processes (2 cores).

## Code Implementation

```python
import time
import threading
import multiprocessing

def cpu_bound_task(n):
    while n > 0:
        n -= 1

if __name__ == "__main__":
    COUNT = 50_000_000
    
    # 1. Sequential
    start = time.time()
    cpu_bound_task(COUNT)
    cpu_bound_task(COUNT)
    print(f"Sequential: {time.time() - start:.2f} seconds")
    
    # 2. Threading (GIL Limited)
    t1 = threading.Thread(target=cpu_bound_task, args=(COUNT,))
    t2 = threading.Thread(target=cpu_bound_task, args=(COUNT,))
    start = time.time()
    t1.start(); t2.start()
    t1.join(); t2.join()
    print(f"Threading:  {time.time() - start:.2f} seconds (Same or Slower!)")
    
    # 3. Multiprocessing (GIL Bypassed)
    p1 = multiprocessing.Process(target=cpu_bound_task, args=(COUNT,))
    p2 = multiprocessing.Process(target=cpu_bound_task, args=(COUNT,))
    start = time.time()
    p1.start(); p2.start()
    p1.join(); p2.join()
    print(f"Processes:  {time.time() - start:.2f} seconds (True Parallelism)")
```

## Key Discussion Points
1.  **Threading Result**: You will usually see that Threading is *slower* than sequential execution. This is because the threads fight over the GIL, adding switching overhead without gaining parallel execution speed.
2.  **Process Result**: Should be roughly ~0.5x the sequential time (assuming you have >1 core), proving true parallelism.
