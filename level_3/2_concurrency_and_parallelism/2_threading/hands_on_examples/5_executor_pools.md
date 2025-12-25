# Lab 5: Modern Threading (Executor Pools)

In modern Python (3.2+), you rarely need to instantiate `threading.Thread` manually. The `concurrent.futures` module provides a higher-level abstraction called the **Executor**.

## 1. ThreadPoolExecutor

### Objective
Submit tasks to a pool and retrieve results without manual queue management.

### Code
```python
import concurrent.futures
import time

def square_number(n):
    print(f"Processing {n}...")
    time.sleep(1)
    return n * n

def main():
    start = time.time()
    
    # Context manager handles pooling and shutdown
    # max_workers=3: Only 3 run at once
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        numbers = [1, 2, 3, 4, 5]
        
        # Method 1: Map (Like standard map(), but parallel)
        print("Submitting safely via map()...")
        results = executor.map(square_number, numbers)
        
        # Results are yielded as they complete (implied join)
        for res in results:
            print(f"Result: {res}")
            
    end = time.time()
    print(f"Total time: {end - start:.2f}s")
    # Expected: Approx 2 seconds (3 run parallel, then 2 run parallel)

if __name__ == "__main__":
    main()
```

---

## 2. Handling Exceptions in Futures

### Objective
Handle crashes in worker threads gracefully.

### Code
```python
import concurrent.futures

def risky_task(n):
    if n == 3:
        raise ValueError("Something went wrong with 3!")
    return n * 10

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # submit() returns a Future object immediately
        futures = {executor.submit(risky_task, n): n for n in [1, 2, 3, 4]}
        
        for future in concurrent.futures.as_completed(futures):
            arg = futures[future]
            try:
                result = future.result() # Exception raised HERE if task failed
                print(f"Task {arg} Result: {result}")
            except Exception as e:
                print(f"Task {arg} FAILED: {e}")

if __name__ == "__main__":
    main()
```

## Summary

| Feature | Manual `Thread` | `ThreadPoolExecutor` |
| :--- | :--- | :--- |
| **Control** | High (Daemon, precise start) | Medium (Queued jobs) |
| **Return Values** | Hard (Need Query/Shared Var) | Easy (`future.result()`) |
| **Exceptions** | Crashes thread silently | Captures and re-raises |
| **Code Style** | Verbose | Clean / Functional |

**Recommendation**: Use `ThreadPoolExecutor` for 90% of tasks. Use `threading.Thread` only when you need long-running background daemons.
