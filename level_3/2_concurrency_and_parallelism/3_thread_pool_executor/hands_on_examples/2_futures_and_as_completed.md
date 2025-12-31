# Hands-on: Futures and `as_completed`

In real-world systems, tasks don't finish in the order they started. Some network requests are fast, others stall. The `as_completed` pattern is essential for high-performance processing pipelines where you want to handle results **immediately** as they arrive.

## The Scenario

We submit tasks with varying execution times. We want to print the result of the fast tasks immediately, not waiting for the slow ones.

## Code Implementation

```python
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def variable_task(task_id):
    # Simulate a task processing time between 1 and 4 seconds
    duration = random.randint(1, 4)
    print(f"Task {task_id} started (will take {duration}s)")
    time.sleep(duration)
    return f"Task {task_id} result (slept {duration}s)"

def main():
    print("--- Submitting Tasks ---")
    
    # Storage for Future objects
    futures = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(1, 6):
            # submit() returns a Future object immediately.
            # It does NOT block.
            future = executor.submit(variable_task, i)
            
            # We can attach metadata to the future object if needed
            # (though strictly it's better to use a dictionary mapping)
            future.task_id = i 
            futures.append(future)
            
        print("--- All tasks submitted, waiting for results ---")
        
        # as_completed yields futures as they resolve (finish or raise exception)
        for completed_future in as_completed(futures):
            # At this point, the task is guaranteed done.
            result = completed_future.result()
            print(f"Received: {result}")

if __name__ == "__main__":
    main()
```

## Interview Deep Dive: `map` vs `as_completed`

| Feature | `executor.map` | `as_completed(futures)` |
| :--- | :--- | :--- |
| **Return Type** | Iterator of **results** | Iterator of **Future objects** |
| **Order** | Preserves submission order | Order of **completion** |
| **Blocking** | Blocks if next item isn't ready | Blocks until *any* item is ready |
| **Error Handling** | Stops/Raises on first error (default iteration) | You handle `future.exception()` per item |

### When to use which?
-   **Use `map`** when: You need simple parallelization and the order of results matters (e.g., processing a list of items and keeping them aligned).
-   **Use `submit` + `as_completed`** when: Tasks have varying durations, and you want to update the UI, save to DB, or log progress immediately.
