# Synchronization Primitives: Locks and Semaphores

Asyncio is single-threaded, so you don't have "typical" race conditions (like two threads modifying memory at the exact same CPU cycle). However, you **DO** have race conditions when `await` is involved.

If a task pauses (`await`) in the middle of a critical section, another task can run and modify shared state, leading to inconsistency.

## 1. `asyncio.Lock`

Use a Lock when you need to ensure exclusive access to a resource across `await` points.

### Example: The "Awaited Update" Race Condition

Without a lock, if two tasks read a value, pause, and then write it back, one update will be lost.

```python
import asyncio

# Shared Resource
database = {"value": 0}
lock = asyncio.Lock()

async def unsafe_update():
    # READ
    current = database["value"]
    print(f"Read: {current}")
    
    # PAUSE (simulating IO/Network lag)
    await asyncio.sleep(0.1)
    
    # WRITE
    database["value"] = current + 1

async def safe_update():
    async with lock:
        # Now this block is exclusive. 
        # Even if we await, no one else can acquire the lock.
        current = database["value"]
        print(f"Safe Read: {current}")
        await asyncio.sleep(0.1)
        database["value"] = current + 1

async def main():
    # 1. Unsafe Example
    database["value"] = 0
    await asyncio.gather(unsafe_update(), unsafe_update())
    print(f"Unsafe Result (Expected 2): {database['value']}") 
    # Likely 1, because both read 0 before writing.

    # 2. Safe Example
    database["value"] = 0
    await asyncio.gather(safe_update(), safe_update())
    print(f"Safe Result (Expected 2): {database['value']}")
    # Guaranteed 2.

if __name__ == "__main__":
    asyncio.run(main())
```

## 2. `asyncio.Semaphore`

A Semaphore limits the number of tasks that can access a resource simultaneously. Common use case: limiting concurrent network requests (rate limiting).

### Example: Limiting Concurrency

```python
import asyncio
import time

async def limited_worker(sem, id):
    async with sem:
        print(f"Worker {id} acquired semaphore. Running...")
        await asyncio.sleep(1)
        print(f"Worker {id} releasing semaphore.")

async def main():
    # Allow only 2 concurrent workers
    sem = asyncio.Semaphore(2)
    
    tasks = [limited_worker(sem, i) for i in range(5)]
    
    start = time.perf_counter()
    await asyncio.gather(*tasks)
    end = time.perf_counter()
    
    print(f"Total time: {end - start:.2f} seconds")
    # Expected: ~3 seconds (2 run, then 2 run, then 1 runs)
    # Without semaphore, it would be 1 second (all 5 run at once).

if __name__ == "__main__":
    asyncio.run(main())
```
