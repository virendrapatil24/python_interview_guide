# Deep Dive: Dataclasses (`@dataclass`)

Introduced in Python 3.7 (PEP 557), `dataclasses` are a code generator that automates the boring process of writing classes that primarily store data. They are a modern replacement for `namedtuple` and manual `__init__` writing.

---

## 1. The End of Boilerplate
Without dataclass, a simple class is verbose:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
        
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
```

**With Dataclass**:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```
This automatically generates: `__init__`, `__repr__`, `__eq__`, and type hints.

---

## 2. Controlling Generation (`field()`)

The `@dataclass` decorator accepts parameters to control what is generated:
*   `frozen=True`: Makes instances immutable (and hashable!).
*   `order=True`: Generates `__lt__`, `__le__`, etc. based on fields order.

### Default Values
Naive mutable defaults are dangerous in Python. Dataclasses protect you from them.

```python
from dataclasses import dataclass, field

@dataclass
class Inventory:
    # 1. Simple immutable default
    store_name: str = "Main Store"
    
    # 2. ERROR: items: list = [] (Python forbids this)
    
    # 3. Correct Mutable Default
    items: list[str] = field(default_factory=list)
    
    # 4. Hidden fields (not in __repr__)
    secret_id: str = field(default="HIDDEN", repr=False)
```

---

## 3. Post-Init Processing (`__post_init__`)
Since `__init__` is generated for you, you cannot put custom logic inside it. Instead, define `__post_init__`.

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False) # Don't accept in __init__

    def __post_init__(self):
        # Calculate derived attributes
        self.area = self.width * self.height
```

---

## 4. Dataclasses vs NamedTuples vs Pydantic

**Interview Question**: When to use what?

| Feature | `namedtuple` | `dataclass` | `Pydantic` |
| :--- | :--- | :--- | :--- |
| **Mutability** | Immutable | Mutable (by default) | Mutable |
| **Validation** | None | Limited (Types are just hints) | **Strong** (Runtime validation) |
| **Parsing** | No | No | **Yes** (JSON parsing) |
| **Inheritance** | Awkward | **Native** (Class inheritance) | Native |
| **Performance** | Fastest (Tuple) | Fast (Dict) | Slower (Validation overhead) |

**Rule of Thumb**:
*   Use `namedtuple` for tiny, simple data packets (like x,y coords) where you want memory efficiency.
*   Use `dataclass` for most internal application objects.
*   Use `Pydantic` for external data (API request bodies, config files) that needs strict validation.

---

## 5. Inheritance Behavior
Dataclasses handle inheritance gracefully by merging fields.

```python
@dataclass
class Base:
    x: int = 1

@dataclass
class Child(Base):
    y: int = 2
    x: int = 10 # Override default

print(Child()) # Child(x=10, y=2)
```

**Gotcha**: If a base class has a field with a default value, all subclasses must ensure fields *without* defaults come *before* fields *with* defaults. This often causes `TypeError: non-default argument follows default argument` during inheritance.

---

## 6. Optimization: `__slots__`
By default, dataclasses use `__dict__` storage.
In Python 3.10+, you can enable `slots=True` to automatically generate `__slots__` for memory savings.

```python
@dataclass(slots=True)
class OptimizedPoint:
    x: int
    y: int
```

---

## 7. Expert Interview Questions

### Q1: Can you use a dataclass as a dictionary key?
Only if it is **frozen** (`frozen=True`).
By default, they are mutable and thus unhashable. If you set `frozen=True` (and `eq=True`), Python generates a `__hash__` method for you.

### Q2: How does `asdict` work?
`dataclasses.asdict(obj)` converts the dataclass instance (recursively) into a dictionary.
Warning: It does a deep copy, which can be slow for large objects.

### Q3: What happens if I use `init=False` in `field()`?
The field is excluded from the `__init__` method signature. You are responsible for setting it, usually in `__post_init__`, or it remains uninitialized (risking AttributeError).

### Q4: Does `dataclass` enforce types at runtime?
**No**. `x: int` is purely metadata. You can pass a string to `x`, and the dataclass won't complain. For enforcement, you need Pydantic or a manual check in `__post_init__`.
