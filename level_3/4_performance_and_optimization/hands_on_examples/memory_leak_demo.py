import tracemalloc
import gc

class LeakyBucket:
    def __init__(self, name):
        self.name = name
        # Large allocation
        self.data = ['a'] * (10**5) 

# Global list causing a leak if not cleared
global_store = []

def cause_leak():
    obj = LeakyBucket("leaky")
    global_store.append(obj) # Still referenced globally!
    return

def safe_function():
    obj = LeakyBucket("safe")
    # obj goes out of scope here, memory reclaimed
    return

def monitor_memory():
    print("Starting Tracemalloc...")
    tracemalloc.start()
    
    snapshot1 = tracemalloc.take_snapshot()
    
    print("Running leaky function...")
    cause_leak()
    
    print("Running safe function...")
    safe_function()
    
    # We must force GC sometimes to be sure circular refs are gone, 
    # though here it's a simple global ref
    gc.collect() 

    snapshot2 = tracemalloc.take_snapshot()
    
    print("\n[ Top 5 Memory Allocations ]")
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    for stat in top_stats[:5]:
        print(stat)

if __name__ == "__main__":
    monitor_memory()
    print(f"\nGlobal store size: {len(global_store)}")
