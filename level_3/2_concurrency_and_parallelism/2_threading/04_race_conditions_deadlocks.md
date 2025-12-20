# Concurrency Bugs: Race Conditions, Deadlocks, and Starvation

Concurrency introduces a new class of bugs that are notoriously difficult to reproduce because they depend on the timing of the OS scheduler.

## 1. Race Conditions (The "Flaky" Bug)

**Definition**: When the system's behavior depends on the sequence or timing of other uncontrollable events (threads).
**Symptom**: "It runs fine on my machine, but crashes 1% of the time in production."

### Types of Race Conditions
1.  **Data Race**: Two threads modify the same variable. (Fixed with Locks).
2.  **Check-Then-Act Race**:
    ```python
    if file_path not in processed_files:
        # Context Switch Here! Another thread adds file_path.
        processed_files.add(file_path)
        process(file_path) # Oops, processed twice.
    ```
    **Fix**: The check and the action must be wrapped in the *same* lock block.

---

## 2. Deadlocks (The Program Freeze)

**Definition**: A situation where a set of processes are blocked because each process is holding a resource and waiting for another resource acquired by some other process.
**Cycle of Death**: A -> waits for B -> waits for A.

### The Coffman Conditions
For a deadlock to occur, four conditions must hold:
1.  **Mutual Exclusion**: Resources cannot be shared.
2.  **Hold and Wait**: Process holds a resource while waiting for another.
3.  **No Preemption**: Resources cannot be forcibly taken away.
4.  **Circular Wait**: A closed chain of processes exists.

### Reproducing a Deadlock in Python
```python
import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        time.sleep(1) # Ensure thread 2 gets lock_b
        with lock_b: # WAITS FOREVER
            print("Thread 1 done")

def thread_2():
    with lock_b:
        time.sleep(1)
        with lock_a: # WAITS FOREVER
            print("Thread 2 done")
```

### Solutions
-   **Lock Ordering**: Always acquire `lock_a` before `lock_b` in all threads.
-   **Timeouts**: Use `lock.acquire(timeout=5)`. If it fails, log an error and retry.

---

## 3. Starvation (The Priority Bully)

**Definition**: A thread is perpetually denied access to necessary resources to process its work. It's not "stuck" (deadlocked), but it never makes progress.

### Causes
-   **Priority Scheduling**: If high-priority threads constantly arrive, low-priority threads never run.
-   **Reader-Writer Problem**: If you have 1000 threads reading a database and 1 trying to write:
    -   The Writer waits for Readers to finish.
    -   New Readers keep arriving and active count never hits 0.
    -   The Writer "starves" waiting for a quiet moment that never comes.

---

## 4. Livelock (The Polite Standoff)

**Definition**: Threads are not blocked, but they change their state in response to each other without making progress.

**Analogy**: Two people meet in a narrow corridor.
-   Person A steps left. Person B steps right. (Block)
-   Person A steps right. Person B steps left. (Block)
-   They are moving (burning CPU), but stuck.

**In Code**: Often happens with aggressive deadlock-recovery algorithms that back off and retry at the exact same intervals.

## Summary

| Bug | Symptom | Cause | Solution |
| :--- | :--- | :--- | :--- |
| **Race Condition** | Data corruption, double processing | Unsynchronized shared access | Atomic blocks (Locks) |
| **Deadlock** | Application freezes (0% CPU) | Circular dependency on resources | Strict Lock Ordering |
| **Starvation** | Task takes forever to complete | Unfair scheduling / infinite stream of high-prio tasks | Fair Queues / Limit Readers |
| **Livelock** | App freezes (100% CPU) | Infinite state-change loops | Randomized backoff (jitter) |
