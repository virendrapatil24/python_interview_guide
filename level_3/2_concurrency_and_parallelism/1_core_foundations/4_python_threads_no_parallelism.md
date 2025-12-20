# Why Python Threads Don't Provide CPU Parallelism

It is a common source of confusion for developers coming from languages like Java or C++: *"I created 4 threads on my 4-core machine, but my Python script is not running 4 times faster. In fact, it's slightly slower. Why?"*

This document explains the technical reasons why standard Python threads fail to achieve parallelism for CPU-bound tasks.

---

## 1. The Core Restriction: The GIL

The primary reason is the **Global Interpreter Lock (GIL)**.

In CPython (the standard Python), the interpreter is not thread-safe. To prevent race conditions within the interpreter's own state (like memory allocation and reference counting), a global lock is engaged.

### The Mechanism of Serialization
1.  **Native Threads**: Python threads are actual native OS threads (pthreads on Linux/Mac, Windows threads on Windows). They are not "green threads" or "simulated threads" (mostly).
2.  **The Checkpoint**: However, before any thread can execute a single Python bytecode, it must acquire the GIL.
3.  **The Bottleneck**: Since there is only **one** GIL for the entire process, only **one** thread can hold it at a time.

**Visualizing the Bottleneck:**
Imagine a 4-lane highway (4 CPU cores) merging into a single toll booth (The GIL). No matter how many cars (threads) you have, they must pass through the toll booth one by one.

---

## 2. Bytecode Execution vs. System Calls

To understand the nuance, we must distinguish between running Python code and running System code.

### A. Python Bytecodes (No Parallelism)
When you write `x = x + 1`, Python compiles this into bytecodes:
1.  `LOAD_FAST` (load x)
2.  `LOAD_CONST` (load 1)
3.  `BINARY_ADD` (add them)
4.  `STORE_FAST` (save result)

The interpreter loop requires the GIL to execute *any* of these. Therefore, mathematical calculations, logic, and string parsing are strictly serialized.

### B. System Calls / C-Extensions (Potential Parallelism)
The GIL is **released** when:
1.  **I/O is performed**: `time.sleep()`, `socket.recv()`, `file.read()`.
2.  **Heavy C-Extension work is done**: Libraries like **NumPy** or **Pandas** explicitly release the GIL before starting a heavy matrix operation in C, and re-acquire it when done.

**Key Takeaway**: You *can* get parallelism in Python threads, but ONLY if the heavy lifting is happening *outside* the Python interpreter (e.g., inside a C function or waiting for the OS). You generally cannot get parallelism for pure Python logic.

---

## 3. Overhead and The "Slowdown" Effect

Not only do you get *zero* speedup for CPU tasks, you often get a **slowdown**.

### Context Switching Overhead
When Thread A pauses and Thread B starts:
1.  The OS must save the state (registers, stack) of Thread A.
2.  The OS must load the state of Thread B.
3.  CPUs caches might get missed.

### GIL Contention
In a multi-core machine, multiple threads see the GIL is free and attempt to grab it simultaneously.
1.  Thread A releases GIL.
2.  Thread B and Thread C wake up and fight to grab it.
3.  The OS locks and signaling mechanism consumes CPU cycles keeping order.

**Result**: A CPU-bound script running on 2 threads might take **1.5x longer** than the single-threaded version simply due to the overhead of the threads fighting for the lock.

---

## 4. Advanced: The "Ticket" System (Python 3.2+)

In older Python (2.x), the GIL released every `N` bytecodes. This led to a "convoy effect" where I/O threads would fight CPU threads and lose, leading to high latency.

In modern Python (3.2+), GIL management uses a time-based heuristic (default 5ms).
-   If a thread runs for 5ms and hasn't released the GIL, other threads set a flag saying "I want to run!"
-   The running thread sees this flag, releases the GIL, and signals the waiter.
-   **Crucially**: The thread that just released the GIL is forced to wait for a signal before trying to re-acquire it, ensuring the other thread actually gets a turn.

While fairer, this switching logic adds overhead and does not solve the fundamental lack of parallelism.

---

## Summary

1.  **Python threads are real OS threads**, but they are leash-constrained by the GIL.
2.  **Parallelism is impossible for Python bytecode**: The interpreter can only run one instruction at a time per process.
3.  **Use Threads only for I/O**: Parallelism *is* achieved when waiting for network/disk because the GIL is dropped.
4.  **Use Multiprocessing for CPU**: To get CPU parallelism, you need multiple interpreters (processes), each with their own GIL.
