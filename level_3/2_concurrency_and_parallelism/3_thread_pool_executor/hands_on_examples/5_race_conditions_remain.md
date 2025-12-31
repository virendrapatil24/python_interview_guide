# Hands-on: Race Conditions (They Still Exist!)

A common beginner mistake is assuming that `ThreadPoolExecutor` handles thread safety for you. **It does not.** The code running inside the workers is executed by standard threads as we saw in the previous section. If they touch shared state, you MUST use locks.

## The Broken Counter

We will increment a shared counter 100,000 times across multiple workers without a lock.

```python
from concurrent.futures import ThreadPoolExecutor
import threading

# Shared State
counter = 0
# A simple lock (we will toggle using it)
lock = threading.Lock()

def unsafe_increment():
    global counter
    for _ in range(100000):
        # Read-Modify-Write Race Condition
        counter += 1

def safe_increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

def run_test(func, name):
    global counter
    counter = 0 # Reset
    print(f"--- Testing {name} ---")
    
    with ThreadPoolExecutor(max_workers=4) as ex:
        # Submit 4 distinct tasks
        futures = [ex.submit(func) for _ in range(4)]
        # Wait for all to finish
        for f in futures:
            f.result()
            
    print(f"Expected: 400,000")
    print(f"Actual:   {counter}")
    if counter != 400_000:
        print("Result: ❌ DATA CORRUPTION")
    else:
        print("Result: ✅ SAFE")

if __name__ == "__main__":
    run_test(unsafe_increment, "Unsafe Increment")
    run_test(safe_increment, "Locked Increment")
```

## Takeaway

The `ThreadPoolExecutor` abstraction manages **Thread Lifecycle** (creation, destruction, pooling), but it does **not** manage **Data Integrity**. You still need to understand `threading.Lock`, `RLock`, and shared memory rules.
