# The Event Loop: The Heart of Asyncio

To understand `asyncio`, you must first forget about threads and OS scheduling. The Event Loop is a **single-threaded** design pattern.

## 1. The Core Concept
Imagine a **Chess Grandmaster** playing against 50 opponents simultaneously.
*   The Grandmaster (CPU) walks to Board 1, makes a move.
*   The Opponent (I/O) takes 2 minutes to think.
*   Does the Grandmaster wait? **NO**.
*   He moves immediately to Board 2, Board 3, etc.
*   By the time he returns to Board 1, the Opponent has moved.

This is **Cooperative Multitasking**. The tasks (opponents) cooperate by "yielding" control back to the Grandmaster (Event Loop) when they are waiting.

## 2. Low-Level Architecture (Select/Poll/Epoll)
How does the loop know which task is ready? It uses OS system calls: `select`, `poll`, `epoll` (Linux), or `kqueue` (Mac).
1.  **Registration**: When you `await socket.recv()`, the loop registers that file descriptor (FD) with the OS.
2.  **Sleep**: The loop effectively goes to sleep using `epoll_wait()`.
3.  **Wake Up**: The OS wakes the loop ONLY when one of the FDs has data.
4.  **Callback**: The loop resumes the specific coroutine associated with that FD.

**Interview Insight**:
> "Asyncio is not magic parallel CPU execution. It is smart waiting. It leverages the OS kernel to notify Python when data is ready, so Python doesn't waste CPU cycles checking repeatedly."

## 3. The Big Restriction
Because there is only **ONE** thread (The Grandmaster):
*   If you calculate 10 million prime numbers in an async function, the Grandmaster is stuck at that board.
*   All 49 other opponents wait. The entire application freezes.
*   **Rule**: Never perform heavy CPU work in the main event loop.
