
import time
import cProfile
import pstats
import io

def slow_function():
    print("Starting heavy computation...")
    total = 0
    # O(N) loop but large N
    for i in range(5_000_000):
        total += i
    return total

def heavy_wrapper():
    # Simulate a wrapper calling a slow function
    return slow_function()

def main():
    # 1. Profiler Setup
    profiler = cProfile.Profile()
    
    # 2. Start measuring
    profiler.enable()
    
    # 3. Code to profile
    result = heavy_wrapper()
    print(f"Result: {result}")
    
    # 4. Stop measuring
    profiler.disable()
    
    # 5. Report
    s = io.StringIO()
    # Sort by 'cumulative' time to see which high-level function is the bottleneck
    sortby = 'cumulative'
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    
    print("\n--- Profiling Report ---")
    ps.print_stats()
    print(s.getvalue())

if __name__ == "__main__":
    main()
