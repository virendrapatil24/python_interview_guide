# Timeouts and Cancellation

Controlling long-running tasks is critical. `asyncio` provides built-in mechanisms to timeout or explicitly cancel tasks.

## 1. `asyncio.wait_for` (Timeouts)

Wait for an awaitable to complete with a timeout. If it takes too long, it is cancelled and `TimeoutError` is raised.

```python
import asyncio

async def long_running_task():
    try:
        print("Task started...")
        await asyncio.sleep(10) # Simulate 10s work
        print("Task finished!")
    except asyncio.CancelledError:
        print("Task was cancelled due to timeout!")
        raise # Best practice: re-raise CancelledError

async def main():
    try:
        # Wait at most 2 seconds
        await asyncio.wait_for(long_running_task(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Main: The task timed out.")

if __name__ == "__main__":
    asyncio.run(main())
```

## 2. Manual Cancellation (`task.cancel`)

You can manually cancel a specific task.

```python
import asyncio

async def heartbeat():
    try:
        while True:
            print("Heartbeat...")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("Heartbeat stopping...")
        # Cleanup code goes here
        raise

async def main():
    task = asyncio.create_task(heartbeat())
    
    # Let it run for 2 seconds
    await asyncio.sleep(2)
    
    print("Main: Stopping heartbeat")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("Main: Heartbeat stopped successfully")

if __name__ == "__main__":
    asyncio.run(main())
```

## 3. Shielding from Cancellation

Sometimes you want a task to **continue** even if the waiting caller is cancelled (e.g., saving data to DB). Use `asyncio.shield`.

```python
import asyncio

async def critical_save():
    print("Saving critical data...")
    await asyncio.sleep(3)
    print("Data saved!")

async def main():
    task = asyncio.create_task(critical_save())
    
    try:
        # Attempt to wait for it, but with a short timeout
        # shield() prevents the inner task from being cancelled
        await asyncio.wait_for(asyncio.shield(task), timeout=1.0)
    except asyncio.TimeoutError:
        print("Main: Timeout! But saving continues...")
        
    # The task is still running
    await task 

if __name__ == "__main__":
    asyncio.run(main())
```

**Interview Tip**:
>Cancellation in `asyncio` is cooperative. Tasks must `await` something to be cancellable. If a task runs a long CPU-bound loop without awaiting, it CANNOT be cancelled until it finishes or yields control.
