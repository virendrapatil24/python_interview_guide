# Hands-on: Task Granularity (Chunksize Tuning)

This experiment proves that `chunksize` matters when you have many small tasks.

## The Scenario
We process 100,000 tiny tasks (simple addition).
1.  **Default Chunksize (1)**: High overhead (Pickling 100k times).
2.  **Optimized Chunksize (1000)**: Low overhead (Pickling 100 times).

## Code

```python
import time
from concurrent.futures import ProcessPoolExecutor

def tiny_task(x):
    return x + 1

def benchmark(chunksize, name):
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        # We process 100,000 items
        results = list(executor.map(tiny_task, range(100_000), chunksize=chunksize))
    duration = time.time() - start
    print(f"{name:<25} (Chunk={chunksize}): {duration:.4f}s")

if __name__ == "__main__":
    print("--- Granularity Benchmark ---\n")
    
    # 1. High Overhead
    benchmark(1, "Fine Grained")
    
    # 2. Low Overhead
    benchmark(1000, "Coarse Grained")
    
    # 3. Too Coarse (Load Imbalance risk, though harmless here)
    benchmark(25000, "Massive Chunks")
```

## Key Takeaways
1.  **Results**: You should see that `Chunk=1` is significantly slower (potentially 2x-5x slower) than `Chunk=1000`.
2.  **Explanation**: The IPC overhead dominates the actual computation time for `tiny_task`. Grouping them amortizes that cost.
