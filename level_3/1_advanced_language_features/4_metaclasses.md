# Deep Dive: Metaclasses

Metaclasses are often touted as one of Python's most "black magic" features.
**Definition**: A Metaclass is the class of a class. Just as an object is an instance of a class, a class is an instance of a metaclass.

> "Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't." — Tim Peters

However, understanding them is crucial for understanding how Python classes are constructed, and they are vital for building frameworks (like Django ORM or Pydantic).

---

## 1. Type is the Metaclass

By default, all classes are instances of `type`.

```python
class Foo:
    pass

x = Foo()
print(type(x))   # <class '__main__.Foo'>
print(type(Foo)) # <class 'type'>
```

### Dynamic Class Creation
You can create classes dynamically using `type()` call.
`type(name, bases, attrs)`

```python
# Regular Class
class MyClass:
    x = 10
    def say(self): print("Hi")

# Equivalent Dynamic Class
def say_func(self): print("Hi")

MyClassDynamic = type(
    'MyClassDynamic',    # Implementation Name
    (),                  # Bases (Tuple)
    {'x': 10, 'say': say_func} # Attributes (Dict)
)
```

---

## 2. Defining a Custom Metaclass

A metaclass is typically a class that inherits from `type`.
It interacts with the creation of other classes.

### The `__new__` hook
Typically, you override `__new__` to intercept the class dictionary *before* the class object is created.

```python
class Meta(type):
    # cls: The metaclass itself
    # name: Name of the class being created
    # bases: Parent classes
    # dct: Class attributes (methods/vars)
    def __new__(cls, name, bases, dct):
        print(f"Creating class: {name}")
        # Hook: Force all attributes to uppercase
        uppercase_attr = {}
        for key, val in dct.items():
            if not key.startswith('__'):
                uppercase_attr[key.upper()] = val
            else:
                uppercase_attr[key] = val
        
        return super().__new__(cls, name, bases, uppercase_attr)

# Usage
class MyClass(metaclass=Meta):
    foo = "bar"

print(MyClass.FOO) # "bar"
# print(MyClass.foo) # AttributeError
```

---

## 3. Use Cases for Metaclasses

When should you actually use this?

### 1. Verification / Validation
Ensure that classes conform to a standard. 
*   **Concept**: You are building an App that allows users to write their own extensions ("Plugins"). You want to guarantee that every plugin is valid before the app starts.
*   **Goal**: "All subclasses of `Plugin` must implicitly implement a `process()` method."

```python
class InterfaceMeta(type):
    def __new__(cls, name, bases, dct):
        # We skip the base class 'Plugin' itself from this check
        if name != 'Plugin' and 'process' not in dct:
            raise TypeError(f"Class {name} missing mandatory 'process' method")
        return super().__new__(cls, name, bases, dct)

class Plugin(metaclass=InterfaceMeta):
    """Base class for all plugins."""
    pass

# This fails because it doesn't define 'process' in its body
# class BrokenPlugin(Plugin): pass 

# This works
class AudioPlugin(Plugin):
    def process(self):
        print("Processing audio...")
```

### 2. Registration (The "Registry" pattern)
Automatically maintaining a list of all subclasses. Used extensively in plugins or frameworks.

```python
registry = {}

class RegistryMeta(type):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        registry[name] = new_cls
        return new_cls

class Widget(metaclass=RegistryMeta): pass
class Button(Widget): pass
class Slider(Widget): pass

print(registry.keys()) # ['Widget', 'Button', 'Slider']
```

---

## 4. `__init_subclass__`: The Modern Alternative

Since Python 3.6, `__init_subclass__` provides a simpler hook for customizing subclass creation without writing a full metaclass. **It is preferred for 90% of use cases.**

### Reimplementing the Registry Pattern
```python
class Plugin:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registry.append(cls)

class AudioPlugin(Plugin): pass
class VideoPlugin(Plugin): pass

print(Plugin.registry) # [<class 'AudioPlugin'>, <class 'VideoPlugin'>]
```

**Interview Insight**: If asked "How to enforce rules on subclasses?", mention `__init_subclass__` first. It shows you know modern Python. Only mention Metaclasses if you need to modify the class *name*, *bases*, or creating a class *factory*.

---

## 5. Internals: Class Creation Process

1.  Python reads the `class` statement.
2.  It identifies the metaclass (defaults to `type`).
3.  It executes the class body (creating the `dct`).
4.  It calls `metaclass(name, bases, dct)` -> which triggers `__new__` and then `__init__` of the metaclass.

---

## 6. Expert Interview Questions

### Q1: Can a class have two metaclasses?
Only if they are compatible.
If Class A has metaclass M1 and Class B has metaclass M2, a class C inheriting from both A and B (`class C(A, B)`) will fail with a `TypeError: metaclass conflict`, unless you create a new metaclass M3 inheriting from both M1 and M2.

### Q2: What is the difference between `__new__` and `__init__` in a metaclass?
*   `__new__`: Creates the class object (allocates memory). It receives the dictionary of attributes. Use this to **modify** the class (rename it, add attributes).
*   `__init__`: Initializes the class object after creation. Use this to configure the class or register it.

### Q3: Why do ORMs like Django use Metaclasses?
They need to inspect the class attributes (like `name = CharField()`) *at definition time* and rewrite the class to map these attributes to database columns. The resulting class often behaves completely differently than the code definition suggests.

### Q4: How does `abc.ABC` work?
It uses a metaclass (`abc.ABCMeta`) to enforce that all abstract methods (decorated with `@abstractmethod`) are implemented in concrete subclasses. It overrides the instance creation logic to raise an error if abstract methods are missing.
