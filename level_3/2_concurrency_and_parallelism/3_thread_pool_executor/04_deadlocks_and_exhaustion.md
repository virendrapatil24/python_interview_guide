# Thread Pool Exhaustion and Deadlocks

One of the most insidious bugs in concurrent programming is **Pool Exhaustion Deadlock**. This occurs when tasks inside the pool rely on other tasks *also* inside the same pool to complete.

## 1. The Scenario

Imagine a `ThreadPoolExecutor` with `max_workers=1`.

1.  You submit **Task A**.
2.  **Task A** starts running on the single worker.
3.  Inside **Task A**, it submits **Task B** to the *same* executor and calls `b_future.result()`.
4.  **Task B** enters the queue. It needs a worker to run.
5.  **Task A** is blocking the only worker, waiting for B.
6.  **Task B** is waiting for the worker to free up.
7.  **DEADLOCK**.

## 2. Code Example (Don't do this)

```python
executor = ThreadPoolExecutor(max_workers=2)

def dependent_task():
    return "World"

def parent_task():
    # Submit a child task to the SAME executor
    f = executor.submit(dependent_task)
    # Wait for it (Blocking the worker!)
    return f.result() 

# If we flood the pool with parent_tasks, 
# all workers might be busy waiting for children that can never start.
```

## 3. The Fix

### Rule of Thumb
**Never wait synchronously for a `Future` inside a task running in the same thread pool.**

### Solutions
1.  **Multiple Pools**: Use one `ThreadPool` for "Parents" and another for "Children".
2.  **Breadth-First Expansion**: Do not wait. Return the future or use callbacks (though `ThreadPoolExecutor` doesn't support callbacks as cleanly as AsyncIO).
3.  **Increase Workers (Risky)**: Increasing `max_workers` might hide the race condition but doesn't solve it deterministically.
4.  **Use AsyncIO**: Async/Await models handle this elegantly because "waiting" releases the loop to run other tasks.

## 4. Resource Exhaustion (Memory)

The standard `ThreadPoolExecutor` uses an **unbounded queue**. 

If you loop `while True:` and `submit()` tasks faster than they complete:
1.  The internal queue grows infinitely.
2.  Reference counting keeps task objects alive.
3.  **Memory Leak / OOM Crash**.

**fix**: Use a `Semaphore` to limit submissions or check queue depth (not directly exposed in standard API, often requires wrapping or custom `Executor`).
