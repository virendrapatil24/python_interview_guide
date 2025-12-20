# Atomic Operations: The Why and How

Why do we spend so much effort on Locks, Semaphores, and Conditions? Because most operations in Python are **Non-Atomic**.

---

## 1. What is an Atomic Operation?

An operation is atomic if it executes in a **single step** relative to other threads. It cannot be paused, interrupted, or split.

-   **Atomic**: "Move this book from Shelf A to Shelf B." (As one indivisible magic trick).
-   **Non-Atomic**: "Pick up book from Shelf A." (Pause). "Walk to Shelf B." (Pause). "Place book."

If an operation is Non-Atomic, a thread switch can happen in the pause, leading to "Race Conditions".

---

## 2. Why They Matter

If you assume non-atomic operations are atomic, you get:
1.  **Lost Updates**: `count += 1` -> Read 10, Add 1, *Switch*, Read 10, Add 1. Write 11. (Should be 12).
2.  **Corrupted Data**: Half-written pointers/references (rare in Python due to GIL, common in C).
3.  **Impossible States**: An item is removed from List A but not yet added to List B. A thread sees it missing from both.

---

## 3. Dissecting Python Atomicity

We use the `dis` module to prove non-atomicity.

`i += 1` compiles to:
```
LOAD_FAST 0 (i)
LOAD_CONST 1 (1)
INPLACE_ADD      <-- GIL can switch threads here!
STORE_FAST 0 (i)
```

The GIL only protects the execution of a *single opcode*. It does not protect the logical sequence of opcodes.

### Atomic Built-ins
Some operations in Python *are* atomic because the underlying C-code is one block that doesn't check for GIL switches.
-   `list.append()`
-   `list.pop()`
-   `dict.__setitem__` (`d[k] = v`)
-   `dict.update()`

Generally, modification of a single container item is atomic.

---

## 4. The Standard Solution: `queue.Queue`

Instead of memorizing which opcodes are atomic, experienced Python developers use the `queue` module.

The `Queue` class is a **Thread-Safe**, fully synchronized Data Structure. It handles all the locking for you.

-   `q.put(item)`: Atomic. Blocks if full.
-   `q.get()`: Atomic. Blocks if empty.

**The Golden Rule**:
**Don't communicate by sharing memory (variables); share memory by communicating (Queues).**

### Example: Thread-Safe Counter with Queue
Instead of locking an integer, push "1" tokens into a queue and count the queue length.

```python
import queue
import threading

q = queue.Queue()

def worker():
    q.put(1) # Thread-safe

threads = [threading.Thread(target=worker) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()

print(f"Count: {q.qsize()}") # 100 guaranteed.
```

## Summary

1.  **Trust No One**: Assume `x += 1` is unsafe.
2.  **Lock Critical Sections**: If you must modify shared variables, allow only 1 thread.
3.  **Prefer Queues**: Use `queue.Queue` to pass data between threads safely without explicit locks.
