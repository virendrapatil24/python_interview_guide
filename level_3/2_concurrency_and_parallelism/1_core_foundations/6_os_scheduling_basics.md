# OS Scheduling Basics: Threads and Processes

Unless you are writing bare-metal assembly, you don't decide when your code runs. The **Operating System (OS) Scheduler** decides. Understanding this "black box" is crucial for debugging performance issues.

---

## 1. The Goal of the Scheduler

The CPU is a scarce resource. You might have 4 cores, but 120 processes (Browser, Slack, System services, IDE, Python script) wanting to run.

The Scheduler's job is **Resource Multiplexing**:
1.  **Fairness**: Give everyone a turn.
2.  **Responsiveness**: If you move your mouse, the UI thread must run *immediately*.
3.  **Throughput**: Maximize the actual work done (minimize time spent switching).

---

## 2. Preemption vs. Cooperation

### Preemptive Scheduling (Modern OS)
Windows, Linux, and macOS use preemptive scheduling.
-   The OS sets a hardware timer interrupt.
-   When the timer fires (e.g., every 10ms), the CPU jumps into Kernel Mode.
-   The Scheduler pauses the current running thread, saves its state, and picks the next thread to run.
-   **Implication**: Your code can be stopped *at any line* (or even half-way through an assembly instruction). This is why we need Locks for thread safety.

### Cooperative Scheduling (Old Systems / Python AsyncIO)
-   The current task runs until it explicitly says "I yield" or "I am waiting."
-   If a task crashes or infinite loops, the whole system hangs.
-   **Python AsyncIO** is a cooperative scheduler running *inside* a single preemptive OS thread.

---

## 3. The Details: Context Switching

Switching from Thread A to Thread B is not free. Ideally, it takes microseconds, but at scale, it adds up.

**Steps of a Context Switch:**
1.  **Interrupt**: Hardware timer stops execution used Mode.
2.  **Save Context**: CPU Registers (Stack Pointer, Instruction Pointer) of Thread A are saved to RAM (PCB/TCB - Process Control Block).
3.  **Kernel Logic**: The scheduling algorithm runs to pick the winner (Thread B).
4.  **Restore Context**: Registers for Thread B are loaded from RAM.
5.  **Cache Trashing**: This is the hidden cost. Thread B's data is likely not in the L1/L2 CPU Cache. The CPU stalls while fetching data from slow RAM.

> **Lesson**: If you spawn 10,000 threads, the OS spends more time context switching than actually running your code ("Thrashing").

---

## 4. Scheduling Algorithms (High Level)

### A. Round Robin
-   Simple queue.
-   Run Thread A for 10ms.
-   Stop, move back to end of line.
-   Run Thread B for 10ms.
-   **Pros**: Fair. **Cons**: Bad for real-time responsiveness.

### B. Priority Based
-   Give critical tasks (UI, Audio) higher priority.
-   If a high-priority task wakes up, it *interrupts* the low-priority task immediately.
-   **Risk**: Denial of Service for low priority tasks ("Starvation").

### C. Completely Fair Scheduler (CFS) - Linux Default
-   Uses a "Red-Black Tree" data structure.
-   Tracks the total "virtual runtime" of every task.
-   Always picks the task that has had the *least* CPU time so far to ensure perfect fairness over time.

---

## 5. Thread States

A thread is not just "Running" or "Stopped". It moves through a state machine:

1.  **New**: Created but not yet started.
2.  **Ready**: Waiting in queue for the CPU. Everything is loaded, just needs a core.
3.  **Running**: Actively executing on the CPU (Holding the GIL in Python).
4.  **Blocked / Waiting**: Waiting for I/O (Disk, Network) or a Lock. The OS kicks this thread out of the "Ready" queue so it consumes zero CPU cycles while waiting.
5.  **Terminated**: Python has finished, resources are freed.

---

## 6. How This Affects Python

1.  **I/O Bound**: When your Python thread waits for a network request, it enters the **Blocked** state. The OS immediately schedules another thread. This is why threads work great for I/O.
2.  **CPU Bound**: Your Python thread stays in **Running** state.
    -   Because of the GIL, even if you have 4 threads in "Ready" state on 4 cores, the GIL forces 3 of them to wait.
    -   They might technically wake up (OS schedules them), realize the GIL is locked, and immediately go back to sleep. This "waking up for nothing" burns CPU cycles (System Load).
