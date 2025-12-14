# Deep Dive: Matplotlib

Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations. Ideally, you should use the "Object-Oriented" API, not the MATLAB-style `pyplot` API directly.

---

## 1. State-machine (pyplot) vs OO Interface

*   **Pyplot (`plt.plot`)**: Implicitly tracks the "current" figure and axes. Easy for simple scripts, bad for complex/dashboard apps.
*   **OO (`fig, ax = plt.subplots`)**: Explicitly manages Figure and Axes objects.

```python
import matplotlib.pyplot as plt

# Recommended
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title("OO Graph")
```

---

## 2. Anatomy of a Plot (The `Artist` hierarchy)

Everything you see is an `Artist`.
1.  **Figure**: The whole window/page.
2.  **Axes**: The plot region (contains x-axis, y-axis, lines, legend).
3.  **Axis**: The actual number line (ticks, labels).

---

## 3. Performance with Large Data

Rendering 10 million points is slow.
*   **Rasterization**: Vector graphics (PDF/SVG) for millions of points are huge. Use `rasterized=True` to save the heavy part as a bitmap.
*   **Fast Style**: Use `mpl.style.use('fast')` to disable fancy effects.

```python
ax.scatter(x, y, rasterized=True)
plt.savefig("plot.pdf") # PDF remains vector, but points are an image
```
