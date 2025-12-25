# Lab 1: Mastering the Thread Lifecycle

Here we will cover the absolute basics: creating, running, waiting, and managing the lifecycle of threads.

## 1. The "Hello World" of Threading

### Objective
Create 5 threads, pass arguments to them, and wait for them to finish.

### Code
```python
import threading
import time
import random

def worker(thread_id, wait_time):
    """
    Simulates a task that takes 'wait_time' seconds.
    """
    print(f"[Start] Thread-{thread_id} processing for {wait_time}s")
    time.sleep(wait_time)
    print(f"[Done]  Thread-{thread_id} finished")

def main():
    print("Main: Starting threads...")
    threads = []
    
    # 1. Creation
    for i in range(5):
        # target: function to run
        # args: tuple of arguments to pass
        t = threading.Thread(target=worker, args=(i, random.randint(1, 3)))
        threads.append(t)
        
        # 2. Execution (Fork/Clone)
        t.start()
    
    print("Main: Waiting for threads to finish...")
    
    # 3. Synchronization (Join)
    for t in threads:
        t.join() # Main thread blocks here until 't' is dead.
        
    print("Main: All threads completed. Exiting.")

if __name__ == "__main__":
    main()
```

---

## 2. Daemon vs Non-Daemon (The Trap)

### Objective
Understand how Daemon threads die instantly when the main thread exits.

### Code
```python
import threading
import time
import sys

def daemon_service():
    print("[Daemon] Starting background service...")
    while True:
        print("[Daemon] Heartbeat... (I will run forever until Main dies)")
        time.sleep(1)

def non_daemon_worker():
    print("[Worker] I am critical. I must finish.")
    time.sleep(5)
    print("[Worker] Work complete!")

def main():
    # Daemon=True: Will be killed abruptly when Main exits
    d = threading.Thread(target=daemon_service, daemon=True)
    d.start()
    
    # Daemon=False (Default): Prevents program from exiting
    n = threading.Thread(target=non_daemon_worker)
    n.start()
    
    print("[Main] Main thread is sleeping for 2 seconds...")
    time.sleep(2)
    print("[Main] Main thread exiting!")
    
    # OBSERVATION:
    # 1. Main prints "Exiting".
    # 2. The program DOES NOT QUIT yet.
    # 3. It waits 3 more seconds for [Worker] to finish.
    # 4. Once [Worker] is done, the program quits, killing [Daemon] instantly.

if __name__ == "__main__":
    main()
```

---

## 3. Subclassing `Thread` (OOP Approach)

### Objective
Encapsulate state and behavior in a class. Useful for complex workers.

### Code
```python
import threading
import time

class ImageResizer(threading.Thread):
    def __init__(self, image_path, resolution):
        super().__init__() # CRITICAL: Must initialize Parent
        self.image_path = image_path
        self.resolution = resolution
        self.result_path = None

    def run(self):
        """
        This method is the entry point when t.start() is called.
        """
        print(f"Resizing {self.image_path} to {self.resolution}...")
        time.sleep(1)
        self.result_path = f"{self.image_path}_{self.resolution}.jpg"
        print(f"Finished {self.image_path}")

def main():
    t = ImageResizer("photo.jpg", "1024x768")
    t.start()
    t.join()
    print(f"Result available at: {t.result_path}")

if __name__ == "__main__":
    main()
```
