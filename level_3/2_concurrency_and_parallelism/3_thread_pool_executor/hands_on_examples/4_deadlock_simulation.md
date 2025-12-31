# Hands-on: The Pool Exhaustion Deadlock

This is the most dangerous pattern in `ThreadPoolExecutor`. It happens when a task running **inside** the pool waits for the result of another task submitted to the **same** pool.

If the pool runs out of workers (exhaustion), the parent task is holding a worker slot while waiting for a child task that can never start (because no slots are free).

## The Deadlock Simulation

```python
from concurrent.futures import ThreadPoolExecutor
import time

# A Pool with only 1 slot!
executor = ThreadPoolExecutor(max_workers=1)

def child_task():
    return "I am the child"

def parent_task():
    print("Parent: Running... submitting child")
    
    # DANGER: Submitting to the SAME executor instance
    future = executor.submit(child_task)
    
    print("Parent: Waiting for child result...")
    # DEADLOCK: This line blocks the ONLY worker.
    # The 'child_task' sits in the queue, waiting for a worker.
    # But the worker is busy waiting for the child.
    result = future.result(timeout=2) 
    return result

if __name__ == "__main__":
    try:
        # Submit the parent
        f = executor.submit(parent_task)
        print("Main: Waiting for parent")
        f.result() # Blocks main thread
    except Exception as e:
        print(f"\nCRASH: {e}")
        print("Reason: The single worker was blocked by Parent, so Child never started.")
```

## How to Fix It?

1.  **Never wait synchronously** (`.result()`) inside a task for another task in the same pool.
2.  **Separate Pools**: Use `worker_pool` for heavy lifting and `dispatch_pool` for orchestration.
3.  **AsyncIO**: This problem is largely solved in `asyncio` because `await` yields control of the thread.

## Why does `max_workers=2` fix this specific case?
If we had 2 workers, the Parent would take Slot 1. The Child would take Slot 2. They would both run.
**However**, if you submit 2 Parent tasks simultaneously, both slots are taken, and both wait for children. You effectively just raised the deadlock threshold, not fixed the bug.
