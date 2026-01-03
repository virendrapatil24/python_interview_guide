# Structured Concurrency: TaskGroup

Python 3.11 introduced `asyncio.TaskGroup`, which provides a modern, safer way to manage concurrent tasks, inspired by "Structured Concurrency" principles (like Trio).

## What is Structured Concurrency?

In traditional `create_task`, tasks can be "fire and forget". If a parent function crashes, orphan tasks might keep running, or exceptions might get swallowed if not explicitly checked. 

Structured concurrency guarantees:
- If a parent block exits, all child tasks are finalized (completed or cancelled).
- If any child task raises an exception, the others are cancelled, and the exception is propagated.

## Using `TaskGroup` (Python 3.11+)

`TaskGroup` is used as an async context manager.

### Example: Basic Usage

```python
import asyncio
import time

async def worker(n):
    print(f"Worker {n} starting")
    await asyncio.sleep(1)
    print(f"Worker {n} done")
    return n * 2

async def main():
    async with asyncio.TaskGroup() as tg:
        # Schedule tasks on the group
        # Note: tg.create_task differs slightly from asyncio.create_task
        task1 = tg.create_task(worker(1))
        task2 = tg.create_task(worker(2))
    
    # The 'async with' block EXITS only when ALL tasks are done.
    print("All workers finished.")
    print(f"Results: {task1.result()}, {task2.result()}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Automatic Cancellation on Error

One of the most powerful features is that `TaskGroup` cancels siblings if one task fails.

```python
import asyncio

async def successful_task():
    try:
        print("Task 1 running...")
        await asyncio.sleep(5)
        print("Task 1 finished")
    except asyncio.CancelledError:
        print("Task 1 was cancelled!")
        raise

async def failing_task():
    print("Task 2 running...")
    await asyncio.sleep(1)
    raise ValueError("Something went wrong in Task 2")

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(successful_task())
            tg.create_task(failing_task())
    except Exception as e:
        # The ValueError from Task 2 will bubble up here
        # specifically wrapped in an ExceptionGroup (Python 3.11+)
        print(f"Caught exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Output Explanation**:
1. Both start.
2. `failing_task` crashes after 1 second.
3. The `TaskGroup` sees the error and immediately cancels `successful_task`.
4. `successful_task` handles the cancellation.
5. The `TaskGroup` exits, raising an `ExceptionGroup` containing the `ValueError`.

**Interview Tip**:
> Always prefer `TaskGroup` over `gather` in Python 3.11+ for complex workflows because it prevents "dangling tasks" and makes error handling more predictable.
