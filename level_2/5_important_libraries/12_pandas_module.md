# Deep Dive: Pandas (`pandas`)

Pandas is built on top of NumPy and provides high-performance structures (`DataFrame`, `Series`) for manipulating tabular data.

---

## 1. DataFrame Architecture

A DataFrame is logically a collection of Series (columns).
Physically, it consolidates columns of the same dtype into **Blocks**.
*   All `float64` columns might be stored in one NumPy array.
*   All `int64` columns in another.
*   This makes column-wise operations very fast, but row-wise operations slow (as they cross memory blocks).

---

## 2. Method Chaining (The Fluent API)

Modern Pandas code avoids intermediate variables in favor of chaining.

```python
# Bad: Intermediate variables
df = pd.read_csv('data.csv')
df = df.dropna()
df['total'] = df['a'] + df['b']
df = df[df['total'] > 100]

# Good: Method Chaining
df = (
    pd.read_csv('data.csv')
    .dropna()
    .assign(total=lambda x: x['a'] + x['b'])
    .query('total > 100')
)
```

---

## 3. The `.loc` vs `.iloc` confusion

*   `.iloc`: **Integer** location. "Give me row 5".
*   `.loc`: **Label** location. "Give me row with index 'user_123'".

**Trap**: If your index is Integers (0, 1, 2...), `loc[0]` refers to the *Label* 0, not necessarily the *first* row (if the index is unsorted).

---

## 4. Memory Optimization (`category` dtype)

String columns are notoriously expensive in Pandas (stored as Python objects). Converting low-cardinality strings to `category` dtype can save 90%+ memory.

```python
# 'gender' has only 2 unique values but repeats million times
df['gender'] = df['gender'].astype('category')
```

---

## 5. GroupBy: Split-Apply-Combine

The most powerful pattern in Pandas.
1.  **Split**: Break data into groups based on keys.
2.  **Apply**: Compute a function (sum, mean, custom) for each group.
3.  **Combine**: Merge results back.

```python
# Calculate mean salary per department
df.groupby('department')['salary'].mean()

# Advanced: Named Aggregation
df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    max_age=('age', 'max')
)
```
