# Memory Management, GC, and Leaks

Understanding how Python handles memory is often the differentiator between a mid-level implementation and an expert-level architecture.

---

## 1. How Python Manages Memory

Python uses a **Private Heap** to store all objects and data structures. The programmer does not access this heap directly; the Python memory manager handles it.

### Everything is an Object (PyObject)
In CPython, every object is represented by a C struct called `PyObject`. It contains:
*   **`ob_refcnt`**: The reference count (number of pointers pointing to this object).
*   **`ob_type`**: A pointer to the object type (int, str, list, etc.).

### Introduction to Reference Counting
This is Python's *primary* mechanism for memory management.
*   **Mechanism**: When an object is created, ref count = 1. When copied/assigned, ref count increments. When deleted/out of scope, ref count decrements.
*   **Deallocation**: When `ob_refcnt` drops to **0**, the memory is *immediately* reclaimed.

```python
import sys
import ctypes

a = []
# 2 references: 1 from variable 'a', 1 from getrefcount's argument
print(sys.getrefcount(a)) # Output: 2

b = a
print(sys.getrefcount(a)) # Output: 3

del b
print(sys.getrefcount(a)) # Output: 2
```

**Pros**: Real-time. Memory is freed as soon as it's not needed.
**Cons**: Cannot handle **Reference Cycles** (e.g., A points to B, B points to A).

---

## 2. The Cyclic Garbage Collector (GC)

To solve the reference cycle problem, Python has a Garbage Collector module (`gc`). It runs periodically to find and clean up cycles.

### Generational Garbage Collection
Scanning *all* objects in memory to find cycles is expensive. Python cheats by assuming **"Most objects die young."** (The Generational Hypothesis).

Python maintains 3 lists (generations) of objects:
*   **Generation 0 (Youngest)**: Created output objects start here. Scanned frequently.
*   **Generation 1**: Objects that survive Gen 0 scans are moved here. Scanned less frequently.
*   **Generation 2 (Oldest)**: Objects that survive Gen 1 scans are moved here. Scanned rarely.

**How it works:**
1.  When (allocations - deallocations) > threshold_0, GC scans Gen 0.
2.  If an object survives, it is promoted to Gen 1.
3.  If Gen 1 fills up, it is scanned and survivors move to Gen 2.

### Viewing/Changing Thresholds
```python
import gc
print(gc.get_threshold()) 
# Output typically: (700, 10, 10)
# - 700: Run GC on Gen 0 if count exceeds 700
# - 10: Run GC on Gen 1 after Gen 0 has been run 10 times
# - 10: Run GC on Gen 2 after Gen 1 has been run 10 times
```

---

## 3. Memory Leaks in Python

"But Python has a GC, how can it leak memory?"
A leak in Python usually means **objects effectively referenced but no longer useful**.

### Common Causes

1.  **Global Variables/State**: Objects at the module level never go out of scope.
2.  **Unbounded Caches**: using a dict as a cache without a cleanup policy.
    *   *Fix*: Use `functools.lru_cache(maxsize=128)` instead of a raw dict.
3.  **Reference Cycles with `__del__` (Legacy)**:
    *   Before Python 3.4, if a cycle involved objects with `__del__` methods, Python wouldn't know which one to call first, so it would just *keep both* forever (uncollectable).
    *   *Note*: Fixed in Python 3.4+ (PEP 442), but still good to know for history.

### Debugging Leaks

**Tools:**
*   **`tracemalloc`**: Built-in. Tracks memory blocks allocated by Python.
*   **`objgraph`**: Can draw graphs of reference chains (requires `graphviz`).

**Example: Using `tracemalloc`**

```python
import tracemalloc

def app_logic():
    # Simulate a leak
    l = []
    for i in range(10000):
        l.append(str(i))
    return l

tracemalloc.start()
snapshot1 = tracemalloc.take_snapshot()

# Run your code
leaky_list = app_logic()

snapshot2 = tracemalloc.take_snapshot()

top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("[ Top 10 differences ]")
for stat in top_stats[:10]:
    print(stat)
```

---

## Summary

*   **Reference Counting**: The main way memory is managed (deterministic, immediate).
*   **Garbage Collection**: Handles cycles using generations (non-deterministic).
*   **Leaks**: Usually caused by global references or unbounded caches, not the language itself.

## Interview Checkpoint

**Q: "When would you disable Garbage Collection?"**
*   **Answer**: In highly deterministic, performance-critical real-time loops (e.g., High Frequency Trading). GC pauses can be unpredictable ("Stop the world"). You might `gc.disable()`, run your critical loop, and then `gc.enable()` or `gc.collect()` manually afterwards.

**Q: "What is the difference between `__del__` and `__exit__`?"**
*   **Answer**: 
    *   `__exit__`: Used in Context Managers (`with` statement). Deterministic; runs exactly when the block ends. Good for cleanup (files, locks).
    *   `__del__`: Called when the GC is about to destroy the object. **Non-deterministic**; you don't know *when* (or even *if*) it will be called. Avoid relying on it.
