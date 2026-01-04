
import threading
import time
from multiprocessing import Process

# A heavy CPU-bound function
def count_down(n):
    while n > 0:
        n -= 1

def run_threaded(n):
    t1 = threading.Thread(target=count_down, args=(n // 2,))
    t2 = threading.Thread(target=count_down, args=(n // 2,))
    
    start = time.perf_counter()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time.perf_counter()
    return end - start

def run_sequential(n):
    start = time.perf_counter()
    count_down(n)
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    N = 100_000_000
    
    print(f"Counting to {N}...")
    
    # 1. Sequential Run
    seq_time = run_sequential(N)
    print(f"Sequential: {seq_time:.4f} seconds")
    
    # 2. Threaded Run (2 threads)
    # Theoretically, on a dual-core machine, this should be 2x faster (0.5 time).
    # But because of the GIL, it's usually EQUAL or SLOWER.
    thread_time = run_threaded(N)
    print(f"Threaded:   {thread_time:.4f} seconds")
    
    if thread_time > seq_time:
        print("\n[Result]: Threading was SLOWER! The GIL prevented parallel execution,\n"
              "          and context-switching overhead added extra cost.")
    else:
        print("\n[Result]: Threading was comparable (or slightly faster due to OS scheduling quirks),\n"
              "          but definitely not the 2x speedup expected from parallelism.")
