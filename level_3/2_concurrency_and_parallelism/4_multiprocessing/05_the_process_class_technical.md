# Deep Dive: The `Process` Class and Lifecycle

The `multiprocessing.Process` class is the fundamental abstraction that mirrors `threading.Thread` but maps to an OS-level process.

## 1. The Class Anatomy
```python
class Process:
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        ...
```
*   **target**: The function to run.
*   **args/kwargs**: Arguments to pass. **Crucially**, these must be picklable.
*   **daemon**: If `True`, the child process is abruptly killed when the parent process exits. If `False` (default), the parent waits for the child to finish.

## 2. Critical Properties & Methods

### `pid` (Process ID)
*   The OS-assigned unique identifier.
*   `None` before `.start()`.
*   Useful for logging or sending OS signals (e.g., `os.kill(p.pid, signal.SIGTERM)`).

### `exitcode`
*   `None`: Process is still running.
*   `0`: Process finished successfully.
*   `> 0`: Process had an error or exited with a code.
*   `< 0`: Process was terminated by a signal (e.g., `-15` for SIGTERM).

### `terminate()` vs `kill()`
*   **`terminate()`**: Sends `SIGTERM` (Unix) or `TerminateProcess` (Windows). It allows the process to (theoretically) handle the signal, though Python often doesn't.
*   **`kill()`**: Sends `SIGKILL` (Unix). Immediate termination. Process cannot cleanup.
*   **Danger**: using either method can corrupt shared resources (Queues, Locks, Pipes) if the process was holding them at the moment of death.

## 3. Daemon Processes (`daemon=True`)
*   **Use Case**: Background tasks (metrics collector, health checker) that shouldn't block the program from exiting.
*   **Restriction**: Daemon processes are **not allowed to create child processes**. This prevents orphan chains.

## 4. Subclassing `Process`
For complex behaviors, you can subclass `Process` and override `run()`.

```python
class Worker(multiprocessing.Process):
    def __init__(self, task_queue):
        super().__init__() # CRITICAL
        self.task_queue = task_queue

    def run(self):
        # This code runs in the NEW process
        while True:
            task = self.task_queue.get()
            if task is None: break
            self.process(task)
```
