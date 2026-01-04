# Profiling: Identifying Bottlenecks

> **"Premature optimization is the root of all evil."** — Donald Knuth

Before you change a single line of code to make it faster, you must prove *where* it is slow. Profiling is the art of measuring your code's performance to identify bottlenecks.

---

## 1. Basic Timing (Stopwatch method)

For simple checks, you might just want to know "how long did this take?".

### `time.time()` / `time.perf_counter()`
`perf_counter` is preferred as it measures elapsed time with the highest available resolution.

```python
import time

start_time = time.perf_counter()

# ... code to benchmark ...
_ = [i**2 for i in range(1000000)]

end_time = time.perf_counter()
print(f"Execution time: {end_time - start_time:.4f} seconds")
```

### `timeit` Module
The `timeit` module is designed specifically for small code snippets to avoid common pitfalls (like system background processes skewing results) by running the statement multiple times.

```python
import timeit

setup_code = "import math"
stmt_code = "math.sqrt(12345)"

# Runs the statement 1,000,000 times by default
# returns the TOTAL time for all runs
execution_time = timeit.timeit(stmt=stmt_code, setup=setup_code, number=1_000_000)

print(f"Total time: {execution_time:.4f} seconds")
```

---

## 2. Deterministic Profiling (`cProfile`)

Built into Python, `cProfile` is a C extension that provides deterministic profiling of Python programs. It describes **how often** and **for how long** various parts of the program executed.

### Usage

**From the Command Line:**
This is the most common way to profile an entire script.

```bash
python -m cProfile -s should_be_sorted_by myscript.py
# Common sort options: 'time' (tottime), 'cumulative' (cumtime), 'calls'
python -m cProfile -s tottime myscript.py
```

**Inside Code:**

```python
import cProfile
import pstats

def my_heavy_function():
    # ... logic ...
    pass

profiler = cProfile.Profile()
profiler.enable()
my_heavy_function()
profiler.disable()

# Sort by cumulative time (time spent in function + sub-calls)
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(10) # Print top 10
```

### Understanding the Output

| Column | Meaning |
| :--- | :--- |
| `ncalls` | Number of calls. |
| `tottime` | Total time spent in the function (excluding calls to sub-functions). **High tottime = The bottleneck is HERE.** |
| `percall` | `tottime` divided by `ncalls`. |
| `cumtime` | Cumulative time spent in this and all sub-functions. **High cumtime = The bottleneck is here OR in a child function.** |
| `percall` | `cumtime` divided by `ncalls`. |
| `filename` | File and line number information. |

**Optimization Tip:** If `tottime` is high, optimize the logic *inside* that function. If `cumtime` is high but `tottime` is low, the function calls expensive children; optimize the structure or the children.

---

## 3. Line-by-Line Profiling

`cProfile` tells you *which function* is slow, but not *which line* inside it. For that, we use `line_profiler` (install via `pip install line_profiler`).

### Usage

1.  Decorate the function you want to profile with `@profile` (no import needed if running via `kernprof`).
2.  Run with `kernprof`.

```python
# fast_test.py

@profile
def complex_math():
    total = 0
    for i in range(100000):
        total += i * i    # Simple op
        total += i ** 5   # Heavier op
    return total

if __name__ == "__main__":
    complex_math()
```

**Run it:**
```bash
# -l for line-by-line, -v for verbose output (print to stdout)
kernprof -l -v fast_test.py
```

**Output:**
It shows `% Time` for every single line. This is the "User vs. CPU" microscopic view.

---

## 4. Memory Profiling

Sometimes the bottleneck isn't CPU, it's RAM (swapping, allocation overhead).
Use `memory_profiler` (install via `pip install memory_profiler`).

```python
from memory_profiler import profile

@profile
def memory_hog():
    a = [1] * (10**6)
    b = [2] * (2 * 10**7)
    del b
    return a

if __name__ == "__main__":
    memory_hog()
```

Run with `python -m memory_profiler myscript.py`. It shows memory increment per line.

---

## 5. Visualization

Reading text stats is hard. Tools like **SnakeViz** or **Tuna** generate flame graphs from your cProfile data.

1.  **Generate output:** `python -m cProfile -o program.prof myscript.py`
2.  **Visualize:** `snakeviz program.prof`

This opens a browser window with an interactive sunburst or icicle chart, allowing you to drill down into call stacks visually.

---

## Summary

*   **Rule 1**: Don't guess. Profile before you optimize.
*   **Tools**: Use `timeit` for snippets, `cProfile` for regular use, and `line_profiler` for deep dives.
*   **Metrics**: Differentiate between `tottime` (this function) and `cumtime` (this function + children).
*   **Memory**: High CPU usage is often a symptom; memory churn might be the cause.

## Interview Checkpoint

**Q: "I have a Python script that takes 5 minutes to run. How do you optimize it?"**
*   **Strategy**:
    1.  **Reproduce**: Ensure I can run it locally in a controlled environment.
    2.  **Profile first**: Run `cProfile` (sorted by `tottime`) to find the function consuming the most CPU.
    3.  **Analyze**: Is it an algorithmic complexity issue ($O(N^2)$ vs $O(N)$)? Is it I/O bound?
    4.  **Drill down**: If a specific function is complex, use `line_profiler` to pinpoint lines.
    5.  **Optimize**: Change algorithm, use caching (`functools.lru_cache`), or use vectorization (`numpy`).

**Q: "What is the difference between wall-clock time and CPU time?"**
*   **Answer**: Wall-clock time (`time.time()`) includes execution time + waiting for I/O + system pauses. CPU time (`time.process_time()`) only measures time the CPU spent working on your process. If Wall >> CPU, you are I/O bound (waiting for DB, Network, Disk).
