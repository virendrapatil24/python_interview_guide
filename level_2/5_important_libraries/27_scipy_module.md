# Deep Dive: SciPy

SciPy builds on NumPy. Where NumPy provides the *array*, SciPy provides the *algorithms* (Linear Algebra, FFT, Optimization, Stats).

---

## 1. Sparse Matrices

Storing a 100,000 x 100,000 matrix in NumPy consumes ~80GB. If most entries are zero, use **Sparse Matrices**. They only store non-zero values.

```python
from scipy import sparse
import numpy as np

# Create standard matrix
eye = np.eye(1000)
# Convert to Compressed Sparse Row (CSR) format
sparse_eye = sparse.csr_matrix(eye)
```

---

## 2. Optimization (`scipy.optimize`)

Finding minima/maxima of functions.

```python
from scipy.optimize import minimize

def func(x):
    return x**2 + 5*Math.sin(x)

result = minimize(func, x0=0)
print(result.x) # The x value that minimizes func
```

---

## 3. Integration (`scipy.integrate`)

Solving integrals (area under curve) or Ordinary Differential Equations (ODEs).
`odeint` or `solve_ivp` are standards for simulating physics/biological systems.
