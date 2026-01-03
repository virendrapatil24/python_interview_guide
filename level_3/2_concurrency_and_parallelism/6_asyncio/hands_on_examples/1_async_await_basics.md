# Async/Await and Event Loop Basics

This guide introduces the fundamental building blocks of `asyncio`: defining coroutines with `async def`, pausing execution with `await`, and running the event loop with `asyncio.run`.

## 1. The Basics: Coroutines and `asyncio.run`

In Python, a function defined with `async def` is a **coroutine**. Calling it does not execute the code immediately; instead, it returns a coroutine object. To execute it, you must schedule it on an event loop.

### Example: Hello World

```python
import asyncio
import time

async def say_hello():
    print(f"Start: {time.strftime('%X')}")
    print("Hello, Async World!")
    # Simulating a small IO operation (non-blocking sleep)
    await asyncio.sleep(1) 
    print(f"End: {time.strftime('%X')}")

if __name__ == "__main__":
    # asyncio.run() creates a new event loop, runs the coroutine, 
    # and closes the loop.
    asyncio.run(say_hello())
```

**Key Concept**: `asyncio.run(main())` is the standard entry point for asyncio programs (Python 3.7+). It manages the event loop lifecycle for you.

## 2. The `await` Keyword

The `await` keyword is used to pause the execution of the current coroutine until the awaited awaitable (like another coroutine or a Future) completes.

- When you `await` something, you yield control back to the event loop.
- This allows the event loop to run other tasks if any are scheduled (we'll see this in later sections).
- If you just calling `await` in sequence, the code is still executed **sequentially**.

### Example: Sequential Execution

Many beginners think `async` implies automatic parallelism. It does not. If you `await` coroutines one after another, they run one after another.

```python
import asyncio
import time

async def brew_coffee():
    print("Start brewing coffee...")
    await asyncio.sleep(2) # Simulates I/O work (2 seconds)
    print("Coffee is ready!")
    return "Coffee"

async def toast_bread():
    print("Start toasting bread...")
    await asyncio.sleep(1) # Simulates I/O work (1 second)
    print("Toast is ready!")
    return "Toast"

async def main():
    start = time.perf_counter()
    
    # These will run SEQUENTIALLY
    print("--- Starting Breakfast (Sequential) ---")
    coffee = await brew_coffee()
    toast = await toast_bread()
    
    end = time.perf_counter()
    print(f"Finished: {coffee} and {toast}")
    print(f"Total time taken: {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

**Expected Output**:
```text
--- Starting Breakfast (Sequential) ---
Start brewing coffee...
Coffee is ready!
Start toasting bread...
Toast is ready!
Finished: Coffee and Toast
Total time taken: 3.0X seconds
```

Even though we used `asyncio`, it took 3 seconds (2 + 1) because we awaited the first task to finish before starting the second. To run them at the same time, we need **Tasks** (covered in the next section).

## 3. What is valid to `await`?

You can await objects generally called **Awaitables**:
1. **Coroutines**: Results of calling an `async def` function.
2. **Tasks**: Wrappers around coroutines allowing them to run in the "background".
3. **Futures**: Low-level objects often used by library authors (bridges strictly callback-based code).

## Interview Tip
> **Q**: What happens if I call a coroutine function but don't await it?
> 
> **A**: The code inside the function will NOT execute. You will get a warning `RuntimeWarning: coroutine '...' was never awaited`. A coroutine object is created but never scheduled.
