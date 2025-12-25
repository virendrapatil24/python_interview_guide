# Futures and Exception Handling

The `Future` object is the core primitive of `concurrent.futures`. It represents **"A result that doesn't exist yet, but will eventually."**

## 1. The Future Object

When you call `executor.submit()`, you get a `Future` instantly. The task is likely still in the queue or running.

### Lifecycle methods
-   `done()`: Returns `True` if the call was successfully cancelled or finished running.
-   `running()`: Returns `True` if currently being executed.
-   `cancel()`: Attempts to remove the task from the queue. If it's already running, it cannot be cancelled.

## 2. Getting Results and Exceptions

The most critical aspect of `Future` is how it handles errors. 

**Exceptions are NOT raised in the worker thread.** They are **captured** and stored inside the Future object. They are effectively "teleported" to the main thread and re-raised only when you ask for the result.

### `.result(timeout=None)`
Blocking call to get the return value.
-   If the task finished successfully: returns value.
-   If the task raised an exception: **raises that exception** here.
-   If `timeout` is reached: raises `TimeoutError`.

### `.exception(timeout=None)`
Non-throwing way to check errors.
-   Returns the exception object (e.g., `ValueError`) if one occurred.
-   Returns `None` if the task succeeded.

```python
def buggy_task():
    raise ValueError("Oops")

with ThreadPoolExecutor() as ex:
    f = ex.submit(buggy_task)
    
    # This line will NOT crash. The error is silent inside 'f'.
    
    try:
        data = f.result() # CRASH! ValueError is raised here.
    except ValueError as e:
        print("Caught captured exception:", e)
```

## 3. Processing `as_completed`

Often you want to submit 10 tasks and process them **as soon as they finish**, regardless of submission order. `concurrent.futures.as_completed` gives you exactly this iterator.

```python
from concurrent.futures import as_completed

urls = ['slow_url', 'fast_url', 'medium_url']
futures = [executor.submit(fetch, url) for url in urls]

for f in as_completed(futures):
    # This loop iterates the moment ANY task finishes
    try:
        print(f.result())
    except Exception as e:
        print("Task failed")
```
