# Hands-on: I/O Bound Performance with ThreadPoolExecutor

This example demonstrates why ThreadPools are critical for I/O-bound applications (like web scrapers, API clients, or database loaders). We will compare **Sequential** execution vs **Concurrent** execution.

## The Scenario

We simulate a "Network Request" that takes 1 second to complete using `time.sleep(1)`.
-   **Task**: "Download" 10 URLs.
-   **Seq Expected Time**: ~10 seconds.
-   **Pool Expected Time**: ~2 seconds (with 5 workers).

## Code implementation

```python
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# Simulated I/O task
def fetch_url(url):
    print(f"[{threading.current_thread().name}] Starting {url}...")
    time.sleep(1) # Simulate network latency
    print(f"[{threading.current_thread().name}] Finished {url}")
    return f"Data from {url}"

def run_sequential(urls):
    start = time.time()
    print("\n--- Starting Sequential Execution ---")
    results = []
    for url in urls:
        results.append(fetch_url(url))
    
    print(f"Sequential took: {time.time() - start:.2f} seconds")

def run_concurrent(urls):
    start = time.time()
    print("\n--- Starting Concurrent Execution (ThreadPool) ---")
    
    # Context Manager handles startup/shutdown
    # max_workers=5 means we can do 5 tasks at once.
    with ThreadPoolExecutor(max_workers=5, thread_name_prefix="Worker") as executor:
        # map() preserves order of results, just like python's built-in map
        results = executor.map(fetch_url, urls)
        
        # Note: map returns a generator. The execution starts immediately,
        # but we iterate here to ensure all are done.
        for result in results:
            pass # We just want to measure time
            
    print(f"Concurrent took: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    target_urls = [f"url_{i}" for i in range(1, 11)] # 10 URLs
    
    run_sequential(target_urls)
    run_concurrent(target_urls)
```

## Key Discussion Points

1.  **Syscall Overhead**: Note we didn't use 10 threads, we used 5. The generic `ThreadPoolExecutor` reuses these 5 threads for all 10 tasks.
2.  **The GIL**: Why did this speed up? Because `time.sleep` (and real I/O operations like `socket.recv`) **release the GIL**. While thread A is sleeping/waiting for bytes, Thread B can run.
3.  **`map` behavior**: If `fetch_url("url_1")` takes 10 seconds and `fetch_url("url_2")` takes 1 second, `executor.map` will block yielding the result of method 2 until method 1 is yielded. It strictly preserves order. Use `as_completed` if you need results immediately.
