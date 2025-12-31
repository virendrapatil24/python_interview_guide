# Hands-on: The Cost of Data Transfer (Pickling Overhead)

This experiment proves why you should **never** pass large data structures (like 100MB Lists or DataFrames) through a Queue.

## The Scenario
1.  **Bad Approach**: Generate a large list (10MB) and pass it to a worker via Queue.
2.  **Good Approach**: Write the list to a temporary file and pass the *filename* to the worker.

## Code Implementation
```python
import multiprocessing
import time
import os
import tempfile
import pickle

def receiver_large_data(q):
    """Receives data from queue (Deserialization happens here)"""
    start = time.time()
    data = q.get()
    end = time.time()
    print(f"[Worker] Received {len(data)} items. Deserialize time: {end - start:.4f}s")

def receiver_filepath(q):
    """Receives a filepath and reads it (Manual I/O, no IPC overhead)"""
    start = time.time()
    path = q.get()
    with open(path, 'rb') as f:
        data = pickle.load(f)
    end = time.time()
    print(f"[Worker] Read file. Load time: {end - start:.4f}s")

if __name__ == "__main__":
    # Create a 50MB list
    large_data = [i for i in range(1_000_000)]
    
    print(f"--- 1. Passing Data Direct (Pickle + Pipe Overhead) ---")
    q1 = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=receiver_large_data, args=(q1,))
    p1.start()
    
    start = time.time()
    q1.put(large_data) # Serialization happens here (Blocking)
    print(f"[Main] Put data into Queue. Serialize time: {time.time() - start:.4f}s")
    p1.join()
    
    print(f"\n--- 2. Passing Reference (File I/O) ---")
    # Write to disk first
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        pickle.dump(large_data, tmp)
        tmp_path = tmp.name
        
    q2 = multiprocessing.Queue()
    p2 = multiprocessing.Process(target=receiver_filepath, args=(q2,))
    p2.start()
    
    start = time.time()
    q2.put(tmp_path) # Sending just a string!
    print(f"[Main] Put path into Queue: {time.time() - start:.4f}s")
    p2.join()
    
    os.remove(tmp_path)
```

## Key Discussion Points
*   **Method 1 (Direct)**: You will see significant lag in `q.put()` (Parent CPU usage) and `q.get()` (Child CPU usage) because Python is serializing/deserializing 50MB of data.
*   **Method 2 (Reference)**: `q.put()` is instant. The child reads from disk. While disk I/O is slow, it is often **faster** than the CPU-overhead of pickling+piping for massive objects, and it keeps the IPC channel free for control signals.
