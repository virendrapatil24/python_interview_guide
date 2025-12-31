# Hands-on: ThreadPool vs ProcessPool (The CPU Benchmark)

This experiment demonstrates why ThreadPoolExecutor is useless for CPU-heavy tasks and how ProcessPoolExecutor scales.

## The Scenario
Calculate the sum of squares for a large range (Standard CPU task).
1.  **Sequential**: Baseline.
2.  **ThreadPool**: Should be slower than sequential (GIL + Overhead).
3.  **ProcessPool**: Should be faster (Parallelism).

## Code

```python
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def cpu_task(n):
    return sum(i * i for i in range(10_000_000))

def run_benchmark(executor_class, name):
    start = time.time()
    # We submit 4 heavy tasks
    with executor_class(max_workers=4) as executor:
        results = list(executor.map(cpu_task, range(4)))
    duration = time.time() - start
    print(f"{name:<20}: {duration:.4f}s")

if __name__ == "__main__":
    print("--- Structuring Benchmark ---")
    
    # 1. Sequential
    start = time.time()
    for _ in range(4):
        cpu_task(0)
    print(f"{'Sequential':<20}: {time.time() - start:.4f}s")
    
    # 2. ThreadPool
    run_benchmark(ThreadPoolExecutor, "ThreadPoolExecutor")
    
    # 3. ProcessPool
    run_benchmark(ProcessPoolExecutor, "ProcessPoolExecutor")
```

## Key Takeaways
1.  **ThreadPool** is often 1.1x SLOWER than Sequential due to context switching overhead and GIL contention.
2.  **ProcessPool** should be nearly 4x FASTER (on a 4+ core machine).
3.  **Lesson**: Never use ThreadPool for math.
