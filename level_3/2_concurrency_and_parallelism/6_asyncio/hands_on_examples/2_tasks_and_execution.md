# Running Concurrently: Tasks, Gather, and Wait

To achieve concurrency in `asyncio` (doing multiple things at once), you must schedule coroutines as **Tasks**. This allows the event loop to switch between them while they are waiting for I/O.

## 1. `asyncio.create_task`

This function takes a coroutine and creates a `Task` object. The task is immediately scheduled to run on the event loop.

### Example: Making Breakfast Concurrently

Refactoring our previous example to run concurrently.

```python
import asyncio
import time

async def brew_coffee():
    print("Start brewing coffee...")
    await asyncio.sleep(2)
    print("Coffee is ready!")
    return "Coffee"

async def toast_bread():
    print("Start toasting bread...")
    await asyncio.sleep(1)
    print("Toast is ready!")
    return "Toast"

async def main():
    start = time.perf_counter()
    
    print("--- Starting Breakfast (Concurrent) ---")
    
    # Schedule both tasks immediately
    task1 = asyncio.create_task(brew_coffee())
    task2 = asyncio.create_task(toast_bread())
    
    # At this point, tasks are scheduled but haven't started running yet 
    # (because main() still has control).
    
    # Await them to ensure they finish and to get results.
    # We can await them in any order, they are already running in parallel.
    coffee = await task1
    toast = await task2
    
    end = time.perf_counter()
    print(f"Finished: {coffee} and {toast}")
    print(f"Total time taken: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

**Expected Output**:
The total time will be roughly **2 seconds** (the longest task), not 3.

## 2. `asyncio.gather`

`gather` is a high-level helper to run multiple awaitables concurrently and return their results as a list, preserving the order of inputs.

```python
import asyncio

async def fetch_data(id):
    print(f"Fetching {id}...")
    await asyncio.sleep(1)
    return {"id": id, "data": "some data"}

async def main():
    # Schedule and wait for all concurrently
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    
    # results is [result1, result2, result3]
    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(main())
```

### Handling Exceptions in Gather
By default, if any awaitable raises an exception, `gather` raises it immediately. You can pass `return_exceptions=True` to have exceptions returned in the list instead of raised.

```python
# ... inside main
    results = await asyncio.gather(
        good_task(),
        failing_task(),
        return_exceptions=True
    )
    # results might look like: ["Success", ValueError("Error"), "Success"]
```

## 3. `asyncio.wait`

`wait` is a lower-level function than `gather`. It allows you to wait for a collection of tasks and gives you more control over when to stop waiting (e.g., when the first one completes).

It returns two sets: `(done, pending)`.

### Example: Wait for First Completion

```python
import asyncio
import random

async def download_file(server_name):
    delay = random.uniform(1, 3)
    await asyncio.sleep(delay)
    return f"Data from {server_name}"

async def main():
    tasks = [
        asyncio.create_task(download_file("Server A")),
        asyncio.create_task(download_file("Server B")),
        asyncio.create_task(download_file("Server C")),
    ]
    
    # Wait until the FIRST task completes
    done, pending = await asyncio.wait(
        tasks, 
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"Completed tasks: {len(done)}")
    print(f"Pending tasks: {len(pending)}")
    
    for task in done:
        print(f"Winner: {task.result()}")
        
    # Optional: Cancel pending tasks if you don't need them
    for task in pending:
        task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
```

**Comparison**:
- Use `gather` when you care about easy result collection.
- Use `wait` when you need finer control (e.g., `FIRST_COMPLETED`, `FIRST_EXCEPTION`) or when you are dealing with a set of Task objects created earlier.
