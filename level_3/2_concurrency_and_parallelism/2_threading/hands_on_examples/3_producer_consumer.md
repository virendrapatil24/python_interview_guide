# Lab 3: The Producer-Consumer Pattern

This is the most common architectural pattern in concurrency. One set of threads creates work, another processes it.

## 1. The Hard Way (Conditions)

### Objective
Implement a thread-safe Queue using `threading.Condition` manually. This teaches deep understanding of signaling.

### Code
```python
import threading
import time
import collections

class ManualQueue:
    def __init__(self, capacity):
        self.queue = collections.deque()
        self.capacity = capacity
        # Condition uses a Lock internally
        self.cv = threading.Condition()

    def put(self, item):
        with self.cv:
            # 1. Wait if full
            while len(self.queue) >= self.capacity:
                print("[Producer] Queue full, waiting...")
                self.cv.wait() # Drops lock, sleeps
            
            # 2. Add item
            self.queue.append(item)
            print(f"[Producer] Added {item}")
            
            # 3. Notify consumers
            self.cv.notify_all()

    def get(self):
        with self.cv:
            # 1. Wait if empty
            while not self.queue:
                print("[Consumer] Queue empty, waiting...")
                self.cv.wait()
            
            # 2. Remove item
            item = self.queue.popleft()
            print(f"[Consumer] Got {item}")
            
            # 3. Notify producers (space available now)
            self.cv.notify_all()
            return item

def main():
    q = ManualQueue(capacity=2)
    
    def producer():
        for i in range(5):
            q.put(i)
            time.sleep(0.5)

    def consumer():
        for _ in range(5):
            q.get()
            time.sleep(1)

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start(); t2.start()
    t1.join(); t2.join()

if __name__ == "__main__":
    main()
```

---

## 2. The Easy Way (`queue.Queue`)

### Objective
Use the standard library. **This is what you should use in production.**

### Code
```python
import threading
import queue
import time

def producer(q):
    for i in range(5):
        print(f"Producing {i}")
        q.put(i) # Blocks if full
        time.sleep(0.5)

def consumer(q):
    while True:
        try:
            # timeout prevents getting stuck if producer dies
            item = q.get(timeout=3) 
            print(f"Consumed {item}")
            q.task_done() # Signal that work is complete
        except queue.Empty:
            print("Queue empty properly.")
            break

def main():
    # maxsize=2 makes it block producers if they are too fast
    q = queue.Queue(maxsize=2)
    
    t1 = threading.Thread(target=producer, args=(q,))
    t2 = threading.Thread(target=consumer, args=(q,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
```
