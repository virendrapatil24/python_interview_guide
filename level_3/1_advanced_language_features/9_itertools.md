# Deep Dive: Itertools Module

The `itertools` module is the "jewel in the crown" of Python's standard library for efficient looping. It implements core computer science algorithms for iterators, inspired by APL, Haskell, and SML.

**Key Concept**: All `itertools` functions return **iterators**. They are lazy and memory efficient.

---

## 1. Infinite Iterators

These generate infinite streams of data. **Warning**: Always use `break` or `islice`!

### `count(start, step)`
Infinite arithmetic progression.
```python
from itertools import count

# 10, 12, 14, 16...
for i in count(10, 2): 
    if i > 16: break
    print(i)
```

### `cycle(iterable)`
Repeats the sequence indefinitely.
```python
from itertools import cycle

# A, B, C, A, B, C...
cycler = cycle('ABC')
print(next(cycler)) # A
```

### `repeat(obj, times=None)`
Repeats an object. Useful for supplying constant arguments to `map`.
```python
# [10, 10, 10]
list(repeat(10, 3)) 

# Fast approach to constantstream
squares = map(pow, range(3), repeat(2)) # 0^2, 1^2, 2^2
```

---

## 2. Combinatoric Iterators

These are heavy lifters for interview questions involving permutations/combinations.

| Function | Description | Order Matters? | Duplicates? |
| :--- | :--- | :--- | :--- |
| `product(p, q)` | Cartesian Product | Yes | Yes |
| `permutations(p, r)` | All possible orderings | Yes | No |
| `combinations(p, r)` | Sorted tuples, no repeats | No | No |
| `combinations_with_replacement` | Sorted tuples, repeats allowed | No | Yes |

```python
from itertools import product, permutations, combinations

# Product (Nested Loops replacement)
# Equivalent to: ((x, y) for x in 'AB' for y in range(2))
list(product('AB', range(2)))
# Output: [('A', 0), ('A', 1), ('B', 0), ('B', 1)]

# Permutations
list(permutations('AB', 2))
# Output: [('A', 'B'), ('B', 'A')]

# Combinations
list(combinations('AB', 2))
# Output: [('A', 'B')]
```

---

## 3. Terminating Iterators (Data Processing)

### `chain(*iterables)`
Treats multiple sequences as a single sequence. Avoids concatenating lists (memory savings).

```python
from itertools import chain

# Iterates over 1, 2, 3, 4, 5, 6
for i in chain([1, 2, 3], [4, 5, 6]):
    pass
```

### `compress(data, selectors)`
Filters data where corresponding selector is true.

```python
from itertools import compress
data = ['A', 'B', 'C', 'D']
mask = [1, 0, 1, 0]

list(compress(data, mask)) # ['A', 'C']
```

### `groupby(iterable, key=None)`
Groups consecutive keys. **CRITICAL**: The input **MUST** be sorted by the key first, or it won't group correctly.

```python
from itertools import groupby

data = [('A', 1), ('A', 2), ('B', 3), ('A', 4)]
# Sort first!
data.sort(key=lambda x: x[0]) 

for key, group in groupby(data, lambda x: x[0]):
    print(key, list(group))
# Output:
# A [('A', 1), ('A', 2), ('A', 4)]
# B [('B', 3)]
```

### `islice(iterable, start, stop, step)`
Slicing for iterators (which don't support `[start:stop]`).

```python
gen = count()
# Take elements from index 10 to 20
subset = islice(gen, 10, 20)
```

### `tee(iterable, n=2)`
Splits one iterator into `n` independent iterators.
**Warning**: Once verified, you should not touch the original iterator. Also, if one tee advances far ahead of the other, `tee` must store the consumed data in memory.

---

## 4. `accumulate` vs `reduce`

*   `functools.reduce()` returns a single final value.
*   `itertools.accumulate()` returns the stream of intermediate results.

```python
from itertools import accumulate
import operator

# Default is addition (running sum)
list(accumulate([1, 2, 3, 4])) 
# [1, 3, 6, 10]

# Running Max
list(accumulate([1, 5, 3, 4], max))
# [1, 5, 5, 5]
```

---

## 5. Expert Interview Questions

### Q1: How do you flatten a list of lists using itertools?
```python
items = [[1, 2], [3, 4], [5, 6]]
flat = chain.from_iterable(items)
# list(flat) -> [1, 2, 3, 4, 5, 6]
```
This is faster than `sum(items, [])` (which is quadratic time).

### Q2: What is the risk of using `tee()`?
Memory usage. `tee` creates FIFO queues. If you consume one iterator fully before touching the second, `tee` essentially stores the *entire* list in memory, defeating the purpose of using a generator.

### Q3: Why does `groupby` often fail for beginners?
Because they assume it works like SQL's `GROUP BY`. In Python, `groupby` only groups **consecutive** elements. If the list isn't sorted by the grouping key, you get multiple fragmented groups.

### Q4: Implement `take(n, iterable)` efficiently.
```python
def take(n, iterable):
    return list(islice(iterable, n))
```

### Q5: How to iterate pairs in a list `(s[0], s[1]), (s[1], s[2])`?
```python
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None) # Advance b by one
    return zip(a, b)
```
*Note: Python 3.10+ added `itertools.pairwise` natively.*
