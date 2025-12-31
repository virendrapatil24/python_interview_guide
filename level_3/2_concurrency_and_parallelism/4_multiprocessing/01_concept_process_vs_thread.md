# Concept: Process vs Thread (Memory & Isolation)

In Python concurrency, the distinction between a **Process** and a **Thread** is far more critical than in languages like Java or C++ due to the Global Interpreter Lock (GIL). However, the fundamental OS-level differences remain the primary driver of system design decisions.

## 1. The Core Metaphor: The House vs. The Room

To visually understand the difference, use this analogy:

*   **Process = A House**:
    *   Each house has its own kitchen, bathroom, and resources.
    *   If the kitchen in House A catches fire (crash), House B is completely safe.
    *   To share food (data) between houses, you must package it and ship it (IPC). This is slow.
    
*   **Thread = People inside the SAME House**:
    *   They share the same kitchen (Memory Heap).
    *   Communication is instant: "Hey, pass the salt" (read variable).
    *   **Risk**: If two people try to cut the same carrot at the same time, someone loses a finger (Race Condition).
    *   If one person burns down the kitchen, everyone in the house dies (Process Crash).

## 2. Process: The Heavyweight (Isolation)
A Process is an instance of a computer program that is being executed. It is the fundamental unit of *isolation*.

### Key Characteristics
1.  **Separate Memory Space**: This is the most important distinction. Process A cannot access Process B's variables directly.
    *   *Consequence*: You can't just share a global `counter` variable.
    *   *Benefit*: **Fault Tolerance**. If a worker process segfaults (e.g., in C-extension), the main master process survives and can respawn it.
2.  **Resources**: Owns its own file descriptors, network sockets, and signal handlers.
3.  **Overhead**: High. Creating a process (especially via `spawn`) requires the OS to allocate a new memory map, load the interpreter, and initialize the runtime.

## 3. Thread: The Lightweight (Sharing)
A Thread exists *within* a process. A single process can contain hundreds of threads.

### Key Characteristics
1.  **Shared Memory**: All threads in a process share the same Heap.
    *   *Consequence*: Fast communication.
    *   *Risk*: **Race Conditions**. You strictly need Locks/Mutexes.
2.  **Shared Resources**: They share file descriptors. If one thread closes a file, it's closed for *all* threads.
3.  **Overhead**: Low. Creating a thread is just allocating a stack (typically ~8MB) and telling the scheduler to add it to the list.

## 4. The "Global Variable" Trap (Code Example)

A common junior mistake is assuming global variables persist across processes.

```python
import multiprocessing

# Global Data
data = []

def worker():
    # In a THREAD, this would work.
    # In a PROCESS, this appends to the CHILD'S copy of 'data'.
    data.append(1) 
    print(f"Child Data: {data}")

if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
    
    # Parent's 'data' is still empty!
    print(f"Parent Data: {data}") 
```

**Why happened?**
When the process started, the OS gave it a *copy* of the memory. The child modified its copy. The parent's copy remained untouched.

## 5. Summary Check

| Feature | Process | Thread |
| :--- | :--- | :--- |
| **Memory** | Isolated (Private Room) | Shared (Common Room) |
| **Communication** | Slow (IPC / Pickling) | Fast (Shared Variables) |
| **Fault Tolerance** | High (Crash is isolated) | Low (Crash kills process) |
| **CPU Utilization** | Multi-Core (Bypasses GIL) | Single-Core (GIL Limited) |
