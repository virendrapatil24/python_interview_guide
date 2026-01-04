import time
from functools import lru_cache
import sys

# 1. Naive Recursive (O(2^n)) - The worst case
def fib_naive(n):
    if n < 2: return n
    return fib_naive(n-1) + fib_naive(n-2)

# 2. Optimized with Built-in Caching (O(n))
@lru_cache(maxsize=None)
def fib_memoized(n):
    if n < 2: return n
    return fib_memoized(n-1) + fib_memoized(n-2)

# 3. Iterative (O(n) time, O(1) space) - Usually faster due to no recursion overhead
def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def timestamp(func, arg):
    start = time.perf_counter()
    result = func(arg)
    end = time.perf_counter()
    return end - start

def main():
    n = 35 
    
    print(f"Calculating Fibonacci of {n}...\n")
    
    # Measure Naive
    if n <= 35: # Don't run naive for large N or it hangs forever
        t_naive = timestamp(fib_naive, n)
        print(f"Naive Recursive:   {t_naive:.6f} sec")
    else:
        print("Naive Recursive:   SKIPPED (Too slow for this N)")

    # Measure Memoized
    # Note: Recursion limit in Python is usually 1000
    try:
        t_memo = timestamp(fib_memoized, n)
        print(f"Memoized (@lru):   {t_memo:.6f} sec")
    except RecursionError:
        print("Memoized (@lru):   FAILED (Recursion Limit Exceeded)")

    # Measure Iterative
    t_iter = timestamp(fib_iterative, n)
    print(f"Iterative Loop:    {t_iter:.6f} sec")

if __name__ == "__main__":
    # Increase recursion limit just in case for the test
    sys.setrecursionlimit(5000)
    main()
