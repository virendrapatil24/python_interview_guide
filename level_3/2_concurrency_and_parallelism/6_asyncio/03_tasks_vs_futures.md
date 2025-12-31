# Tasks vs Futures

Understanding the difference between a Coroutine, a Task, and a Future is critical for advanced control flow.

## 1. The Hierarchy
```text
Awaitable
├── Coroutine (The raw generator)
└── Future (A placeholder for a result)
    └── Task (A wrapper that runs a Coroutine)
```

## 2. Future (`asyncio.Future`)
This is a low-level object that acts as a bridge between the "Callback World" and the "Async/Await World".
*   It represents a result that will exist later.
*   **State**: It starts "Pending". Eventually, someone calls `future.set_result(val)` or `future.set_exception(err)`.
*   **Usage**: You `await` the future. The loop pauses you until `.set_result()` is called by someone else (e.g., the library handling the network socket).

## 3. Task (`asyncio.Task`)
A **Task** is a subclass of Future.
*   **Purpose**: To run a Coroutine **concurrently** in the background.
*   **Creation**: `task = asyncio.create_task(my_coro())`.
*   **Lifecycle**:
    1.  The Task is added to the Event Loop immediately.
    2.  The Loop will run it at the next opportunity (after current code awaits).
    3.  When the wrapped coroutine finishes, the Task (which is a Future) calls `self.set_result(return_value)`.

## 4. Why Create Tasks?
If you just write `await func()`, you are running **sequentially**.
```python
# Sequential (Takes 2 seconds)
await func1() # waits 1s
await func2() # waits 1s

# Concurrent (Takes 1 second)
t1 = asyncio.create_task(func1()) # Schedule it
t2 = asyncio.create_task(func2()) # Schedule it
await t1 # Wait for result
await t2
```
**Interview Insight**:
> "A Coroutine is just code. A Task is that code *running* on the Loop. To run things in parallel, you must wrap coroutines in Tasks."
