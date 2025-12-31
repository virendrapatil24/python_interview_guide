# Coroutines: `async` and `await`

Coroutines are specialized Python functions that can **pause** and **resume** execution, maintaining their state (local variables) between pauses.

## 1. Defining a Coroutine
Before Python 3.5, we used generators (`yield`). Now we have native syntax.

```python
async def my_coroutine():
    print("Start")
    await asyncio.sleep(1) # PAUSE HERE
    print("End")
```
*   **Calling it**: `c = my_coroutine()` does NOT run the code. It returns a **Coroutine Object**.
*   **Running it**: You must schedule it on the loop: `await c` or `asyncio.run(c)`.

## 2. The `await` Keyword
`await` basically means:
> "I cannot proceed until this result is ready. I yield control back to the Event Loop. Please wake me up when it's done."

You can only `await` **Awaitables**:
1.  **Coroutines**: Another `async def` function.
2.  **Tasks**: Wrappers around coroutines (we'll cover this).
3.  **Futures**: Low-level objects representing a result that hasn't arrived yet.

## 3. Cooperative Multitasking
This is the key difference from Threading.
*   **Threading (Preemptive)**: The OS can pause your thread at ANY line of code (statistically) to run another thread. You need Locks.
*   **Asyncio (Cooperative)**: Your code ONLY pauses at explicit `await` points.
    *   **Pro**: You almost never need Locks for internal state logic (e.g., `counter += 1` is safe because no other task runs until you `await`).
    *   **Con**: You must cooperate. If you forget to `await`, you block everyone.

## 4. Under the Hood (Generators)
Technically, coroutines are built on top of Python Generators.
*   `await` is similar to `yield from`.
*   The Event Loop calls `send()` on the generator to resume it.
*   The coroutine raises `StopIteration` when it returns a value.
