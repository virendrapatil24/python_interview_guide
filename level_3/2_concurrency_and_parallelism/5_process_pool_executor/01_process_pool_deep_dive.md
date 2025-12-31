# ProcessPoolExecutor: The Heavy Lifter

`concurrent.futures.ProcessPoolExecutor` is a high-level abstraction over the `multiprocessing.Process` module. It is designed for **CPU-bound parallelism**.

## 1. When to Prefer `ProcessPoolExecutor`

You should choose `ProcessPoolExecutor` over `ThreadPoolExecutor` or `asyncio` ONLY when:

1.  **CPU Intensive Tasks**: The task involves heavy computation (e.g., image resizing, matrix multiplication, encryption, massive regex).
2.  **No Shared State**: The tasks are independent. They take input, compute, and return output.
3.  **GIL Bypass Required**: You need to utilize multiple CPU cores to scale performance limits.

### Decision Matrix

| Scenario | Recommended Executor | Why? |
| :--- | :--- | :--- |
| **Download 1000 URLs** | `ThreadPoolExecutor` | I/O bound. Processes are too heavy/expensive. |
| **Resize 1000 Images** | `ProcessPoolExecutor` | CPU bound. Threads are blocked by GIL. |
| **Database Queries** | `ThreadPoolExecutor` | Waiting for DB is I/O. |
| **Machine Learning Inference** | `ProcessPoolExecutor` | Heavy math requires full core usage. |

## 2. Internals vs `multiprocessing.Pool`
While `multiprocessing.Pool` is older and more "feature-rich" (supports `start_method` tuning easier), `ProcessPoolExecutor` provides a **simpler, uniform API** consistent with ThreadPools.

### Code Comparison

**The Old Way (`multiprocessing.Pool`)**:
```python
from multiprocessing import Pool

# You must manually manage the context manager or close/join
with Pool(4) as p:
    results = p.map(func, data)
```

**The Modern Way (`ProcessPoolExecutor`)**:
```python
from concurrent.futures import ProcessPoolExecutor, as_completed

# Returns Futures, allowing per-task handling
with ProcessPoolExecutor(max_workers=4) as executor:
    # 1. Submit tasks
    futures = [executor.submit(func, item) for item in data]
    
    # 2. Handle as they finish (out of order)
    for f in as_completed(futures):
        print(f.result())
```

## 3. The "Context Switch" Cost
Why not use ProcessPool for everything?

**Example: The Wrong Choice**
```python
# BAD USE CASE
def add(x, y): return x + y

# Measuring 1 simple addition
# ProcessPool: ~10ms (Spawn process + Pickle + Pipe + Unpickle + Add + Pickle + Pipe)
# ThreadPool:  ~0.02ms
# Direct Call: ~0.0001ms
```
*   **Theory**: The OS context switch (loading pages, switching registers) and IPC Serialization often costs **more** than the task itself if the task is trivial.
*   **Rule of Thumb**: If your function takes less than 1ms, `ProcessPool` will make it **slower**.
