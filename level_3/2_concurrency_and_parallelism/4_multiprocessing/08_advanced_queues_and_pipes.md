# Deep Dive: `Queue` and `Pipe` Internals

Understanding the implementation details helps avoid deadlocks and performance pitfalls.

## 1. `multiprocessing.Queue`
This is **NOT** just a `collections.deque` with a lock. It is a complex system involving a background thread.

### Architecture
1.  **Buffer**: A `collections.deque` in memory.
2.  **Pipe**: An OS Pipe (or Unix Domain Socket) to transmit data.
3.  **Feeder Thread**: A background thread that moves items from the buffer into the Pipe.

### Why is there a Feeder Thread?
*   `pickle.dumps` can be slow. We don't want to block the main process while pickling.
*   Writing to the pipe can block if the OS buffer is full.
*   **The Problem**: If the main process exits abruptly (`kill -9`), the Feeder Thread dies. Data still in the memory buffer but not yet flushed to the Pipe is **lost forever**.

### `JoinableQueue`
Adds `.task_done()` and `.join()` methods.
*   Used for the **Producer-Consumer** pattern.
*   `.join()` blocks until `.task_done()` has been called for every item put in the queue.

## 2. `multiprocessing.Pipe`
Low-level IPC primitive.

### `Pipe(duplex=True)`
*   **duplex=True**: Both ends can send/receive.
*   **duplex=False**: `conn1` can only receive, `conn2` can only send.

### The Deadlock Risk
Pipes have a limited OS buffer capacity (e.g., 64KB on Linux).
*   If Process A writes 1MB of data to the pipe...
*   And Process B is NOT reading...
*   Process A will **block** at the 64KB mark waiting for space.
*   If Process B was waiting for A to finish before reading -> **Deadlock**.

### Performance Hint
*   **Queue**: Safer, easier.
*   **Pipe**: Faster. Good for "Ping-Pong" signals or passing small tokens.

## 3. Implementation Check
When asked "How does Python send data between processes?", the answer is:
1.  **Pickle** the object to bytes.
2.  Write bytes to a file descriptor (Pipe/Socket).
3.  Read bytes from file descriptor.
4.  **Unpickle** to reconstruct object.
