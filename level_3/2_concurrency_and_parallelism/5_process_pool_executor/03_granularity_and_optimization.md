# Optimization: Granularity and Chunking

A common mistake is submitting millions of tiny tasks to a process pool.

## 1. The Overhead Math
Submitting a task has a fixed overhead. Let's visualize the cost breakdown.

```python
Total Time = (Pickle_Args + IPC_Send + Unpickle_Args) + EXECUTION + (Pickle_Res + IPC_Rev + Unpickle_Res)
```

If `EXECUTION` is fast (e.g., `x + 1`), the math looks like this:
*   Overhead: **0.001s**
*   Execution: **0.000001s**
*   Ratio: **99.9% Overhead**. You are burning CPU just to move data around.

## 2. Solution: Chunksize (Batching)
Instead of sending 1 item at a time, send a "Chunk" of items.

### Visualizing Chunking
**Without Chunking (chunksize=1)**:
```text
Parent -> [Task 1] -> Child
Parent -> [Task 2] -> Child
Parent -> [Task 3] -> Child
(3 Round Trips)
```

**With Chunking (chunksize=3)**:
```text
Parent -> [Task 1, Task 2, Task 3] -> Child
(1 Round Trip)
```

### Code Example: Measuring Impact
```python
# Scenario: 100,000 tiny tasks
data = range(100_000)

# 1. BAD: Default (chunksize=1)
executor.map(math.sqrt, data) 
# Result: ~5.0 seconds (mostly overhead)

# 2. GOOD: tuned (chunksize=1000)
executor.map(math.sqrt, data, chunksize=1000)
# Result: ~0.2 seconds (25x faster!)
```

## 3. How to Calculate Optimal Chunksize?
There is no magic number, but a heuristic formula is:

$$ \text{Chunksize} = \frac{\text{Total Tasks}}{\text{Cores} \times 4} $$

*   **Logic**: You want enough chunks so that all cores stay busy (if one finishes early, it can grab another chunk), but not so many that overhead kills you.
*   **Example**: 
    *   Tasks: 10,000
    *   Cores: 10
    *   Chunksize = 10,000 / 40 = **250**.
