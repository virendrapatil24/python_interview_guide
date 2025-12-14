# Deep Dive: PyTorch

PyTorch is a machine learning framwork optimizing for flexibility and speed. It is famous for its "Pythonic" nature.

---

## 1. Dynamic Computational Graphs (Define-by-Run)

Unlike TensorFlow's static graph (historically), PyTorch builds the graph **as you run the code**.
This means you can use standard Python control flow (`if`, `for`, `while`) inside your model, and backpropagation will still handle it correctly.

---

## 2. Autograd

The engine that powers neural network training. It tracks the history of operations on Tensors.

```python
import torch

x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward() # Computes gradients

print(x.grad) # tensor(6.0)
```

---

## 3. `nn.Module`

The base class for all neural network modules.

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 50)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        # Define the connectivity here
        return self.relu(self.fc1(x))
```

---

## 4. Dataset and DataLoader

Abstracts data batching, shuffling, and multiprocess loading.

```python
from torch.utils.data import DataLoader

loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
for batch in loader:
    train(batch)
```
