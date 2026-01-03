# Events

`asyncio.Event` is a simple synchronization object that allows one task to signal one or more other tasks that something has happened.

## Anatomy of an Event
- `event.wait()`: Pause execution until the flag is set.
- `event.set()`: Set the flag to true. All waiting tasks wake up.
- `event.clear()`: Reset the flag to false.

## Example: Coordinator and Workers

Imagine a scenario where workers start but must wait for a "Go" signal from a coordinator (e.g., waiting for cache to warm up).

```python
import asyncio

async def worker(name, event):
    print(f"{name} waiting for signal...")
    await event.wait()
    print(f"{name} received signal! Working...")
    await asyncio.sleep(0.5)
    print(f"{name} done.")

async def coordinator(event):
    print("Coordinator setting up...")
    await asyncio.sleep(2)  # Simulate setup work
    print("Coordinator: GO!")
    event.set()

async def main():
    event = asyncio.Event()
    
    # Create workers
    workers = [
        asyncio.create_task(worker(f"Worker {i}", event)) 
        for i in range(3)
    ]
    
    # Create coordinator
    coord = asyncio.create_task(coordinator(event))
    
    await asyncio.gather(coord, *workers)

if __name__ == "__main__":
    asyncio.run(main())
```

## Useful patterns
- **Startup Sync**: Waiting for DB connection to be ready before accepting requests.
- **Graceful Shutdown**: Signaling all background loops to stop.

Note: `asyncio.Event` is not thread-safe. If you need to set it from another thread, use `loop.call_soon_threadsafe(event.set)`.
