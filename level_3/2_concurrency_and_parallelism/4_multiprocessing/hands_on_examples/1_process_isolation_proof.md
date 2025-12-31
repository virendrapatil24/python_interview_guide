# Hands-on: Process Isolation Proof

This experiment demonstrates the most fundamental difference between Threads and Processes: **Memory Isolation**.

## The Scenario
1.  We define a global variable `GLOBAL_List`.
2.  We modify this list inside a **Thread**.
3.  We modify this list inside a **Process**.
4.  We observe if the changes persist in the main program.

## Code Implementation

```python
import multiprocessing
import threading
import time

# Global State
GLOBAL_LIST = []

def thread_worker():
    """Threads share memory, so this should affect the global list."""
    global GLOBAL_LIST
    GLOBAL_LIST.append("Item from Thread")
    print(f"[Thread] Appended item. List ID: {id(GLOBAL_LIST)}")

def process_worker():
    """Processes have separate memory, so this should NOT affect the parent's list."""
    global GLOBAL_LIST
    GLOBAL_LIST.append("Item from Process")
    print(f"[Process] Appended item. List ID: {id(GLOBAL_LIST)}")

if __name__ == "__main__":
    print(f"[Main] Initial List ID: {id(GLOBAL_LIST)}")
    
    # 1. Thread Modification
    t = threading.Thread(target=thread_worker)
    t.start()
    t.join()
    print(f"[Main] After Thread: {GLOBAL_LIST}")
    
    # 2. Process Modification
    p = multiprocessing.Process(target=process_worker)
    p.start()
    p.join()
    print(f"[Main] After Process: {GLOBAL_LIST}")
```

## Key Discussion Points
1.  **Thread Output**: You will see `"Item from Thread"` in the main list. Threads operate on the *same* heap.
2.  **Process Output**: You will **NOT** see `"Item from Process"` in the main list.
3.  **Memory IDs**: On `fork` (Linux), the `id()` might initially look the same due to Copy-on-Write optimization, but logically they are distinct. On `spawn` (Mac/Win), the memory address space is completely fresh.
