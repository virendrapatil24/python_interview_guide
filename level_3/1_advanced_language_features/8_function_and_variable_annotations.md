# Deep Dive: Function and Variable Annotations

Python is dynamically typed, but **Function and Variable Annotations** (introduced in PEP 3107 and PEP 526) allow developers to attach metadata to code. While usually associated with **Type Hinting** (PEP 484), annotations are generic metadata storage systems.

---

## 1. The Basics: Syntax & Semantics

**Crucial Concept**: Annotations are **metadata**. Python does **NOT** enforce them at runtime. A function annotated to accept an `int` will happily accept a `str` unless you add explicit runtime checks or use a static analyzer (like mypy).

### Function Annotations (PEP 3107)
You can annotate parameters and the return value.

```python
def calculate_area(radius: float) -> float:
    return 3.14159 * (radius ** 2)

# Accessing Metadata
print(calculate_area.__annotations__)
# Output: {'radius': <class 'float'>, 'return': <class 'float'>}
```

### Variable Annotations (PEP 526)
Introduced in Python 3.6, allowing type hints on variables.

```python
# With initial value
count: int = 0

# Without initial value (defines type but doesn't assign value)
name: str
# 'name' is NOT available in locals() until assigned!
```

---

## 2. Type Hinting (The `typing` Module)

While annotations can be strings or expressions, the standard use case is Type Hinting. The `typing` module provides specialized definitions.

### Pre-Python 3.9 Syntax
Use capital types from `typing`.

```python
from typing import List, Dict, Optional, Union, Any

# List of integers
numbers: List[int] = [1, 2, 3]

# Dictionary mapping String keys to Integer values
scores: Dict[str, int] = {"Alice": 100}

# Optional: Could be int OR None
user_id: Optional[int] = None 

# Union: Could be int OR float
width: Union[int, float] = 10.5

# Any: Disable type checking for this variable
data: Any = "Could be anything"
```

### Modern Syntax (Python 3.9 / 3.10+) -> **PREFERRED**
PEP 585 (Py3.9) and PEP 604 (Py3.10) simplified syntax significantly.

| Concept | Old (`typing`) | New (Built-in) | Version |
| :--- | :--- | :--- | :--- |
| **Generics** | `List[int]`, `Dict[str, int]` | `list[int]`, `dict[str, int]` | 3.9+ |
| **Collections** | `Tuple[int, str]` | `tuple[int, str]` | 3.9+ |
| **Unions** | `Union[int, str]` | `int | str` | 3.10+ |
| **Optional** | `Optional[int]` | `int | None` | 3.10+ |

```python
# Modern Idiomatic Python
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def get_id(uid: int | str | None) -> int:
    # Handles int, str, and None
    if uid is None: return 0
    return int(uid)
```

---

## 3. Advanced Features

### Generics and TypeVars
For defining functions that work on variables of *any* type, but maintain that type constraint.

```python
from typing import TypeVar, Sequence

T = TypeVar("T")

# If input is list[int], return is int. 
# If input is list[str], return is str.
def first_element(seq: Sequence[T]) -> T:
    return seq[0]
```

### Static Duck Typing (`Protocol`)
PEP 544 introduced Protocols. Instead of inheriting from a class, a class matches a `Protocol` if it implements the required methods.

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing a circle")

def render(shape: Drawable):
    shape.draw()

# Circle passes type check because it has a 'draw' method
render(Circle())
```

### Callable
Describing functions passed as arguments.

```python
from typing import Callable

# A function taking two ints and returning an int
Operation = Callable[[int, int], int]

def apply(a: int, b: int, op: Operation) -> int:
    return op(a, b)
```

---

## 4. The "Forward Reference" Problem & PEP 563

Problem: You cannot use a Class name as a type hint inside its own definition, because the class isn't fully defined yet.

```python
class Node:
    # Error in vanilla Python 3.6-3.9: Name 'Node' is not defined
    def add_child(self, child: Node): 
        pass
```

### Solution 1: String Literal
```python
def add_child(self, child: "Node"): ...
```

### Solution 2: Postponed Evaluation (PEP 563)
Using a `__future__` import turns **all** annotations in the file into strings automatically. This will likely become default in future Python versions.

```python
from __future__ import annotations

class Node:
    # This works now!
    def add_child(self, child: Node):
        pass
```

---

## 5. Runtime Access: `__annotations__` vs `get_type_hints`

Usually, usage of annotations is static (IDEs, CI pipelines). However, sophisticated frameworks (like **Pydantic** or **FastAPI**) use them at runtime for validation.

**Do not access `obj.__annotations__` directly.**
It doesn't handle string forward references or inheritance correctly.

**Use `typing.get_type_hints()`**:
```python
from typing import get_type_hints

def foo(x: "int") -> "str":
    pass

# Raw access (Still strings)
print(foo.__annotations__) 
# {'x': 'int', 'return': 'str'}

# Correct resolution
print(get_type_hints(foo)) 
# {'x': <class 'int'>, 'return': <class 'str'>}
```

---

## 6. Expert Interview Questions

### Q1: Do Python annotations affect performance?
**At Runtime**: Technically, yes, but negligibly. Python has to parse the annotation expressions and store them in `__annotations__` when defining the function.
**With `from __future__ import annotations`**: The performance cost is reduced because the expressions are not evaluated at definition time; they are stored as raw strings.

### Q2: What is the difference between `NewType` and Type Alias?
*   **Type Alias**: `UserId = int`. `UserId` is exactly `int`. Static checkers treat them identically.
*   **`NewType`**: `UserId = NewType('UserId', int)`. Checks treat `UserId` as a *subclass* of `int`. You cannot accidentally pass a plain `int` to a function expecting `UserId`.

### Q3: How do you annotate `*args` and `**kwargs`?
You annotate the type of *each individual element*, not the tuple/dict itself.

```python
# args is tuple[int, ...], but we annotate it as 'int'
def sum_all(*args: int) -> int:
    return sum(args)

# kwargs is dict[str, float], but we annotate values as 'float'
def process_scores(**kwargs: float):
    pass
```

### Q4: What is `TypedDict`?
Available in Python 3.8+. It's used to type hint dictionaries with specific keys and strict value types, acting as a lightweight struct.

```python
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int

u: User = {"name": "Bob", "age": 30} # Valid
```
