# Deep Dive: TensorFlow

TensorFlow is an end-to-end open source platform for machine learning. It uses data flow graphs for numerical computation.

---

## 1. Tensors: The Data Unit

Tensors are multi-dimensional arrays with a uniform type. They are similar to NumPy arrays but are immutable and live on the Accelerator (GPU/TPU).

```python
import tensorflow as tf

# Rank 0 (Scalar)
t0 = tf.constant(4)
# Rank 2 (Matrix)
t2 = tf.constant([[1, 2], [3, 4]])
```

---

## 2. Eager Execution vs Graph

*   **Eager Execution** (Default in TF 2.x): Operations are evaluated immediately. Great for debugging.
*   **Graph Execution** (`@tf.function`): Code is compiled into a static graph. Faster and deployable.

```python
@tf.function
def dense_layer(base):
    return tf.matmul(base, W) + b
```

---

## 3. Keras: The High-Level API

Keras is the official high-level API for TensorFlow.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])
```

---

## 4. Automatic Differentiation (GradientTape)

Deep learning relies on Backpropagation. `tf.GradientTape` records operations for automatic gradient calculation.

```python
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2
    
# Calculate dy/dx = 2*x = 6.0
dy_dx = tape.gradient(y, x)
```
