# Hands-on: Messaging with IPC (Queue vs Pipe)

Since we cannot share variables, we use IPC to pass messages. This example compares Queue (safe) and Pipe (fast).

## The Scenario
1.  **Queue**: A worker generates numbers and puts them in a Queue. The parent consumes them.
2.  **Pipe**: A bidirectional chat between Parent and Child.

## Code Implementation

```python
import multiprocessing
import os

# --- Queue Worker ---
def queue_worker(q):
    print(f"[Queue Worker {os.getpid()}] Starting work...")
    for i in range(3):
        q.put(f"Message {i}")
    q.put("DONE")

# --- Pipe Worker ---
def pipe_worker(conn):
    print(f"[Pipe Worker {os.getpid()}] Waiting for ping...")
    msg = conn.recv() # Blocking
    print(f"[Pipe Worker] Received: {msg}")
    conn.send("PONG")
    conn.close()

if __name__ == "__main__":
    # 1. Queue Example
    print("--- 1. Queue Example ---")
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=queue_worker, args=(q,))
    p1.start()
    
    while True:
        m = q.get()
        if m == "DONE": break
        print(f"[Parent] Got: {m}")
    p1.join()

    # 2. Pipe Example
    print("\n--- 2. Pipe Example ---")
    parent_conn, child_conn = multiprocessing.Pipe()
    p2 = multiprocessing.Process(target=pipe_worker, args=(child_conn,))
    p2.start()
    
    parent_conn.send("PING")
    reply = parent_conn.recv()
    print(f"[Parent] Got reply: {reply}")
    p2.join()
```

## Key Discussion Points
1.  **Queue**: Is heavy but foolproof. Use it when you have multiple producers or consumers.
2.  **Pipe**: Is lightweight but requires careful coordination. Note that `recv()` blocks indefinitely if the other side dies without sending.
3.  **Serialization**: In both cases, the strings/objects are being pickled. If you pass a custom object, ensure it is picklable.
