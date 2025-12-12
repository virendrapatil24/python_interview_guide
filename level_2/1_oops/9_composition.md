# Composition in Python

## Part-Of Relationship (Strong Association)

Composition is a restricted form of Aggregation. It represents a **"Part-of"** relationship. It implies a strong ownership where the child object resides within the parent and cannot exist independently.

### Key Characteristics
1.  **Dependence:** The child object is typically created **inside** the parent's constructor.
2.  **Lifecycle:** If the parent is destroyed, the child object is **also destroyed** (or becomes inaccessible/meaningless).

### Example: Car and Engine
A Car *has an* Engine. But strictly speaking, an Engine defines the Car for that specific context. If we scrap the Car, that specific Engine instantiation effectively goes with it (in this model). The Engine is a *part of* the Car.

```python
class Engine:
    def __init__(self, type):
        self.type = type

    def start(self):
        return f"{self.type} engine started"

class Car:
    def __init__(self, make, engine_type):
        self.make = make
        # Engine is created INSIDE the Car (Composition)
        # It is tightly coupled to this specific Car instance
        self.engine = Engine(engine_type)

    def start_car(self):
        print(f"{self.make} is starting: {self.engine.start()}")

    def __del__(self):
        print(f"Car {self.make} is being crushed.")
        # In Python's Garbage Collection, if Car goes, Engine usually goes 
        # because no other reference exists to it.

# 1. Create the Car (which strictly creates the Engine)
my_car = Car("Toyota", "V8")

# 2. Usage
my_car.start_car()

# 3. Lifecycle Demonstration
# We cannot access the engine independently easily like in aggregation
# engine_ref = my_car.engine 
del my_car 
# The engine associated with that car is now also gone (collected by GC)
```

### Composition vs. Aggregation Checklist

| Feature | Aggregation | Composition |
| :--- | :--- | :--- |
| **Relationship** | "Has-A" | "Part-Of" |
| **Strength** | Weak | Strong |
| **Creation** | Child created outside | Child created inside |
| **Lifecycle** | Independent | Dependent (Parent kills Child) |
| **Python Code** | Passed to `__init__` | Instantiated in `__init__` |
