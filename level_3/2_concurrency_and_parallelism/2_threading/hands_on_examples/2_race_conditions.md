# Lab 2: Race Conditions & Synchronization

In this lab, we prove that Python threads are *not* safe by default and fix it using Locks.

## 1. The Broken Bank (Race Condition)

### Objective
Simulate a bank account accessed by 100 threads, showing lost updates.

### Code (Buggy)
```python
import threading
import time

class BankAccount:
    def __init__(self):
        self.balance = 0
    
    def deposit(self, amount):
        # Read-Modify-Write (Non-Atomic)
        current = self.balance
        time.sleep(0.0001) # Force a context switch to guarantee failure
        self.balance = current + amount

def run_simulation():
    account = BankAccount()
    threads = []
    
    print("Starting 100 threads to deposit $1 each...")
    for _ in range(100):
        t = threading.Thread(target=account.deposit, args=(1,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Final Balance: ${account.balance}")
    print("Expected: $100")
    if account.balance != 100:
        print("FAIL: Race Condition detected!")
    else:
        print("Pass (Lucky?)")

if __name__ == "__main__":
    run_simulation()
```
**Expected Output**: Likely `Final Balance: $1` or `$2` due to massive overwrites.

---

## 2. The Fix (Using Lock)

### Objective
Make the deposit method atomic.

### Code (Fixed)
```python
import threading

class SafeBankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock() # 1. Create Lock
    
    def deposit(self, amount):
        # 2. Context Manager automatically acquires/releases
        with self.lock:
            current = self.balance
            # Even with sleep, no one else can enter this block
            # time.sleep(0.0001) 
            self.balance = current + amount

# (Run same simulation as above with SafeBankAccount)
# Final Balance will be $100 guaranteed.
```

---

## 3. RLock (Recursive Locking)

### Objective
Show how standard `Lock` deadlocks on recursion, and `RLock` solves it.

### Code
```python
import threading

class RecursiveTask:
    def __init__(self):
        self.lock = threading.RLock() # Try changing to Lock() -> Deadlock
        self.count = 0

    def increment(self, n):
        with self.lock:
            self.count += 1
            if n > 0:
                print(f"Recursion level {n}, re-acquiring lock...")
                # If this was Lock(), we would freeze here forever.
                self.increment(n-1)

def main():
    task = RecursiveTask()
    task.increment(5)
    print("Finished recursion without deadlocking!")

if __name__ == "__main__":
    main()
```
