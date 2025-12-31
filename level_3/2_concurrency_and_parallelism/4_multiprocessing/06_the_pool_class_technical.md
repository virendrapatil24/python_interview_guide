# Deep Dive: The Worker Pool (`multiprocessing.Pool`)

The `Pool` class abstracts away the manual management of `Process` objects. It is the industry standard for "Data Parallelism" (doing the same function to a list of data).

## 1. Pool vs Process
*   **`Process`**: You manage the lifecycle. Good for long-running, unique tasks (e.g., "Start a database server").
*   **`Pool`**: It manages a fixed set of workers. Good for processing chunks of data (e.g., "Resize 1000 images").

## 2. Key Methods & Differences

### `map(func, iterable, chunksize=None)`
*   **Behavior**: Blocks until *all* results are ready.
*   **Returns**: A list `[result1, result2, ...]`.
*   **Pros**: Simple. Preserves order.
*   **Cons**: Consumes memory for the whole list. You wait for the *slowest* task.

### `imap(func, iterable, chunksize=1)`
*   **Behavior**: Lazy. Returns an iterator.
*   **Returns**: Yields results *as soon as possible*, but **preserves order**.
*   **Pros**: Memory efficient. You can start processing result #1 while #100 is still running.

### `imap_unordered(func, iterable, chunksize=1)`
*   **Behavior**: Lazy. Returns iterator.
*   **Returns**: Yields results **as soon as they finish**, regardless of order.
*   **Pros**: Fastest specific "time-to-first-byte".

### `apply_async(func, args=(), callback=None)`
*   **Behavior**: Submits a *single* task. Non-blocking.
*   **Returns**: `AsyncResult` object. You must call `.get()` to retrieve value (which blocks).
*   **Use Case**: When tasks are not uniform logic (e.g., "Task 1 resize image", "Task 2 send email").

## 3. Important Parameters

### `processes`
Defaults to `os.cpu_count()`.

### `maxtasksperchild`
*   **Problem**: Python processes often leak small amounts of memory over time.
*   **Solution**: Set `maxtasksperchild=100`. After a worker completes 100 tasks, the Pool kills it and replaces it with a fresh process. This reclaims memory.

## 4. Best Practice Pattern
```python
with multiprocessing.Pool(processes=4) as pool:
    # Use imap_unordered for speed if order doesn't matter
    for result in pool.imap_unordered(expensive_func, data):
        print(result)
```
