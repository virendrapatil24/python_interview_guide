# Deep Dive: NumPy (`numpy`)

NumPy is the foundation of the Python Data Science stack. It introduces the `ndarray` object, which provides efficient storage and data operations capable of outperforming standard Python lists by orders of magnitude.

---

## 1. Vectorization vs Loops

The core philosophy of NumPy is "No Loops". You apply operations to whole arrays at once.

```python
import numpy as np

# Standard Python Loop (Slow)
a = [1, 2, 3]
b = [4, 5, 6]
result = []
for x, y in zip(a, b):
    result.append(x * y)

# NumPy Vectorization (Fast)
# Handled in optimized C code
na = np.array([1, 2, 3])
nb = np.array([4, 5, 6])
result = na * nb
```

---

## 2. Broadcasting Rules

Broadcasting allows arithmetic on arrays of different shapes. It "stretches" the smaller array to match the larger one without copying data.

**Rule**: Two dimensions are compatible when:
1.  They are equal, or
2.  One of them is 1.

```python
A = np.zeros((3, 3)) # Shape (3, 3)
v = np.array([1, 2, 3]) # Shape (3,)

# Shape Mismatch Resolution:
# (3,) becomes (1, 3) -> Stretched to (3, 3)
result = A + v 
```

---

## 3. Views vs Copies

Assignments and slicing usually return **Views** (references to same memory), not copies.

```python
arr = np.array([1, 2, 3, 4, 5])

# Slice is a view
sub = arr[0:2]
sub[0] = 99

print(arr) 
# Output: [99, 2, 3, 4, 5] (Original was modified!)

# To get a copy:
sub_copy = arr[0:2].copy()
```

---

## 4. Advanced Indexing

*   **Boolean Indexing**: Filtering data.
    ```python
    arr[arr > 50] # Returns all elements > 50
    ```
*   **Fancy Indexing**: Using arrays of integers to access specific indices.
    ```python
    # Access elements at index 1, 3, 4
    arr[[1, 3, 4]]
    ```

---

## 5. Memory Layout (C vs Fortran)

NumPy arrays are explicitly typed and stored contiguously in memory.
*   **C-order (Row-major)**: Default. Iterating over rows is fast.
*   **F-order (Column-major)**: Fortran style. Iterating over columns is fast.

```python
# Check memory stride
print(arr.flags)
```
