# Futures

In `asyncio`, a `Future` is a low-level awaitable object that represents an eventual result of an asynchronous operation.

**Relationship**: `Task` is actually a subclass of `Future`.
- A `Task` wraps a coroutine and manages its execution.
- A `Future` is a container for a result that will be set later (usually by some low-level callback or I/O handler).

You rarely create Futures manually in high-level application code, but understanding them is key for advanced usage and library development.

## 1. Using `loop.create_future()`

You can create a standalone Future attached to the current loop. It will block any `await` on it until `.set_result()` or `.set_exception()` is called.

### Example: Bridging Callback Code

Imagine you are using a legacy library that uses callbacks instead of async/await. You can use a Future to bridge the gap.

```python
import asyncio

# === Legacy / Low-level Callback World ===
def perform_async_operation(callback):
    """Simulates a library that does work and calls a function when done."""
    import threading
    def work():
        import time
        time.sleep(1) # blocking work in a thread
        result = 42
        callback(result)
    
    thread = threading.Thread(target=work)
    thread.start()

# === Asyncio World ===
async def main():
    loop = asyncio.get_running_loop()
    
    # 1. Create a Future
    future = loop.create_future()
    
    # 2. Define a callback that sets the future's result.
    # We use loop.call_soon_threadsafe because the callback comes from another thread.
    def on_done(result):
        loop.call_soon_threadsafe(future.set_result, result)
        
    print("Starting legacy operation...")
    
    # 3. Start the operation
    perform_async_operation(on_done)
    
    print("Waiting for result...")
    
    # 4. Await the future. Execution pauses here until set_result is called.
    result = await future
    print(f"Got result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 2. Key Methods

- `future.set_result(value)`: Sets the result. Any code awaiting this future will resume and receive `value`.
- `future.set_exception(exc)`: The awaiting code will raise this exception.
- `future.cancel()`: Cancel the future.
- `future.add_done_callback(fn)`: Run `fn` when the future finishes.

## Interview Tip
> **Q**: What is the difference between `Task` and `Future`?
>
> **A**: A `Future` is a passive container for a value. It doesn't "run" anything; it just waits to be set.
> A `Task` wraps a coroutine. It actively drives the coroutine towards completion (runs the code). It is a Future that holds the return value of that coroutine.
