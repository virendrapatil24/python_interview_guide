# ThreadPoolExecutor Basics

The `concurrent.futures` module (introduced in Python 3.2) provides the modern way to handle threading. It abstracts away the `threading.Thread` loop and locking mechanisms.

## 1. The Interface

```python
from concurrent.futures import ThreadPoolExecutor
```

The standard usage should almost always be with a **Context Manager**:

```python
def my_task(x):
    return x * x

# Context manager ensures threads are cleaned up (calls .shutdown() automatically)
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(my_task, 10)
```

## 2. `max_workers`: How many threads?

Usually, the hard limit is the GIL (Global Interpreter Lock). ThreadPools are useful for **I/O Bound** tasks (file read/write, network requests), not **CPU Bound** tasks (computation).

-   **I/O Bound**: Set `max_workers` high (e.g., 5-10x number of cores). Since threads spend time waiting for IO, one core can manage many waiting threads.
-   **CPU Bound**: ThreadPool is arguably useless here due to the GIL. Use `ProcessPoolExecutor`.

**Default Value**: Since Python 3.8, the default `max_workers` is `min(32, os.cpu_count() + 4)`. This formula attempts to preserve I/O capacity while avoiding OS limit overloads.

## 3. `submit()` vs `map()`

These are the two main ways to assign work.

### Using `map`
Strictly like the builtin `map()`, but changes order of execution (potentially) while **preserving the order of results**.

-   **Returns**: An iterator that yields results *in the order tasks were submitted*, blocking if necessary.
-   **Pros**: Simple API.
-   **Cons**: Stops if one task raises an exception (unless handled inside the task). You cannot process "whichever finishes first".

```python
with ThreadPoolExecutor() as ex:
    # Blocks until all are done (or iterating)
    results = ex.map(my_task, [1, 2, 3]) 
    for r in results:
        print(r) # Printed in order 1, 4, 9
```

### Using `submit`
More flexible. Returns a `Future` object immediately.

-   **Returns**: `Future` object.
-   **Pros**: Non-blocking submission. Can handle exceptions per task. Can process results `as_completed`.
-   **Cons**: slightly more verbose.

```python
with ThreadPoolExecutor() as ex:
    future = ex.submit(my_task, 10)
    print(future.result()) # Blocks here to get result
```
