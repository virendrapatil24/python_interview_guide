# Sorting in Python: `sort()` vs `sorted()`

Python provides powerful, stable, and highly optimized sorting mechanisms. Understanding the difference between in-place sorting and creating new sorted lists is crucial.

## 1. The Two Approaches

### `list.sort()`
-   **In-Place:** Modifies the original list directly.
-   **Returns:** `None`.
-   **Applies to:** Only Lists.

```python
nums = [3, 1, 4, 1, 5]
nums.sort()
print(nums) # [1, 1, 3, 4, 5]

# Common Mistake:
# print(nums.sort()) # Prints "None"
```

### `sorted()`
-   **New Object:** Creates and returns a *new* sorted list.
-   **Original Unchanged:** The original iterable remains untouched.
-   **Applies to:** Any Iterable (Lists, Tuples, Dictionaries, Sets).

```python
nums = [3, 1, 4, 1, 5]
sorted_nums = sorted(nums)

print(sorted_nums) # [1, 1, 3, 4, 5]
print(nums)        # [3, 1, 4, 1, 5] (Original intact)
```

## 2. Advanced Sorting with `key`
Both `sort()` and `sorted()` accept a `key` argument. This expects a **function** that transforms each element before comparison.

### Case-Insensitive Sort
```python
names = ["alice", "Bob", "charlie"]
# Normal sort puts 'Bob' first because 'B' < 'a' (ASCII)
print(sorted(names)) # ['Bob', 'alice', 'charlie']

# Key sort
print(sorted(names, key=str.lower)) # ['alice', 'Bob', 'charlie']
```

### Sorting Complex Objects (Dictionaries/Tuples)
Sort students by their score (descending).

```python
students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 95}
]

# Sort by score descending
students.sort(key=lambda x: x['score'], reverse=True)
print(students)
# Output: Charlie (95), Alice (90), Bob (75)
```

## 3. High-Performance Keys: `operator` Module
Using `lambda` is common, but slightly slower than using the optimized functions from the `operator` module.

```python
from operator import itemgetter, attrgetter

students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 75}
]

```python
# Faster than lambda x: x['score']
sorted_students = sorted(students, key=itemgetter('score'))
```

## 4. Advanced Custom Sorting (Tuple Hacks)
You can encode complex logic into a tuple. Python compares tuples element-by-element.

### The Logic
`key = lambda x: (A, B)`
1.  Python sorts by `A` first.
2.  If `A` is equal, it breaks ties using `B`.

### Example: Prioritizing Specific Values
Imagine an event log where you want to sort by:
1.  **Timestamp** (Primary).
2.  **Priority**: "MESSAGE" events must come *after* other events if timestamps are equal.

```python
events = [
    ("CONNECT", "100"),
    ("MESSAGE", "100"),
    ("e", "50"),
    ("d", "50")
]

# Logic:
# 1. int(event[1]): Sort by timestamp numerically.
# 2. event[0] == "MESSAGE": 
#    - Returns False (0) for non-MESSAGES.
#    - Returns True (1) for MESSAGES.
#    - Since 0 < 1, non-MESSAGES come FIRST.

sorted_events = sorted(events, key=lambda x: (int(x[1]), x[0] == "MESSAGE"))

print(sorted_events)
# Output:
# [('d', '50'), ('e', '50'),   <- Timestamp 50 (Order undefined between d/e unless specified)
#  ('CONNECT', '100'),         <- Timestamp 100, False (0) comes before True
#  ('MESSAGE', '100')]         <- Timestamp 100, True (1) comes last
```

## 5. Stability
Python’s sort (Timsort) is **stable**. This means that when multiple records have the same key, their original order is preserved.

```python
# A list of orders with Status and Timestamp
orders = [
    {'id': 1, 'status': 'completed', 'timestamp': '10:00'},
    {'id': 2, 'status': 'pending',   'timestamp': '10:05'},
    {'id': 3, 'status': 'pending',   'timestamp': '09:30'},
    {'id': 4, 'status': 'completed', 'timestamp': '09:00'}
]

# Goal: Sort by Status (primary), but keep earliest timestamps first (secondary).

# 1. First, sort by the Secondary Key (Timestamp)
orders.sort(key=lambda x: x['timestamp'])
# Result: [ID 4 (09:00), ID 3 (09:30), ID 1 (10:00), ID 2 (10:05)]

# 2. Now, sort by Primary Key (Status)
orders.sort(key=lambda x: x['status']) # 'completed' comes before 'pending'

# Final Result:
# Because sort is STABLE, items with the same 'status' REMAIN ordered by timestamp.
# [
#   {'id': 4, 'status': 'completed', 'timestamp': '09:00'}, <- Earliest completed
#   {'id': 1, 'status': 'completed', 'timestamp': '10:00'}, <- Later completed (Stable!)
#   {'id': 3, 'status': 'pending',   'timestamp': '09:30'}, <- Earliest pending
#   {'id': 2, 'status': 'pending',   'timestamp': '10:05'}  <- Later pending (Stable!)
# ]
```

## Common Interview Questions

**Q: What is the time complexity of Python's sort?**
-   **A:** $O(N \log N)$ in the worst case. Python uses **Timsort**, a hybrid of Merge Sort and Insertion Sort.

**Q: Can you sort a dictionary?**
-   **A:** A dictionary itself is inherently unordered (or insertion-ordered in new Python), but you cannot "sort" it in-place. You can, however, use `sorted(my_dict)` which returns a sorted list of *keys*. To get a sorted representation of items, use `sorted(my_dict.items(), key=...)`.

**Q: How do you sort by multiple criteria? (e.g., Score DESC, then Name ASC)**
-   **A:** Tuples are compared element-by-element. Valid strategy: return a tuple from the key function. To mix Ascending/Descending for numbers, negate the number.
    ```python
    # Sort by score DESC, then name ASC
    # (Assuming score is numeric)
    sorted(students, key=lambda x: (-x['score'], x['name']))
    ```
