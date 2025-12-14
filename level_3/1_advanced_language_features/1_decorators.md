# Deep Dive: Python Decorators

Decorators are one of Python's most powerful functional programming features. At their core, a decorator is simply a **function that takes another function as input and returns a new function**. They allow you to modify or enhance behavior without changing the source code of the decorated function.

---

## 1. The Basics: Syntactic Sugar

The `@` symbol is merely syntactic sugar.

```python
@my_decorator
def my_func():
    pass

# IS EXACTLY EQUIVALENT TO:
def my_func():
    pass
my_func = my_decorator(my_func)
```

### A Minimal Decorator
The standard pattern involves defining a wrapper function inside the decorator.

```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_execution
def add(a, b):
    return a + b

# Output: Calling add -> Finished add
add(2, 3) 
```

---

## 2. Preserving Metadata (`functools.wraps`)

**The Problem**: When you decorate `add`, strictly speaking, `add` becomes `wrapper`.
`print(add.__name__)` would output `"wrapper"`, and the docstring of `add` is lost.

**The Solution**: Use `functools.wraps`.

```python
import functools

def better_logger(func):
    @functools.wraps(func) # Copies __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 3. Decorators Accessing Arguments

Since `wrapper` receives `*args` and `**kwargs`, it can inspect or modify them.

```python
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("Arguments must be positive!")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def sqrt(x):
    return x ** 0.5
```

---

## 4. Decorators Accepting Arguments

If the decorator *itself* needs arguments (e.g., `@repeat(times=3)`), you need **three levels** of nested functions.
1.  Outer: Accepts decorator arguments.
2.  Middle: Accepts the function.
3.  Inner: The wrapper.

```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello {name}")
```

---

## 5. Class-Based Decorators

You can use a **Class** as a decorator by implementing `__call__`. This is useful for **stateful decorators**.

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def do_something():
    pass
```
*Note*: Using classes to decorate **methods** in a class can be tricky because `self` generally refers to the `CountCalls` instance, not the instance of the class owning the method. Descriptors are often needed to solve this.

---

## 6. Decorating Classes

You can decorate an entire class. The decorator receives the class object, modifies it (or replaces it), and returns it.

```python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Connected")
```

---

## 7. Advanced: "Optional" Arguments

Creating a decorator that works BOTH as `@my_dec` AND `@my_dec(arg=1)` is a common expert pattern.

```python
def smart_decorator(func=None, *, factor=1):
    # Case 1: Called as @smart_decorator(factor=2)
    # func is None. We return a partial decorator.
    if func is None:
        return lambda f: smart_decorator(f, factor=factor)

    # Case 2: Called as @smart_decorator
    # func is the actual function.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Factor is {factor}")
        return func(*args, **kwargs)
    return wrapper

@smart_decorator
def foo(): pass

@smart_decorator(factor=10)
def bar(): pass
```

---

## 8. Expert Interview Questions

### Q1: What is the execution order of stacked decorators?
```python
@dec1
@dec2
def func(): pass
```
**Application Order**: Bottom-up. `dec2` is applied first, then `dec1`.
Effective code: `func = dec1(dec2(func))`

**Execution Order**: Top-down (usually). The wrapper returned by `dec1` executes first, calls `dec2`'s wrapper, which calls `func`.

### Q2: How do you decorate a method inside a class?
It's the same as a function, but remember the first argument in `*args` will be `self`.

### Q3: What is `functools.lru_cache`?
It is a built-in decorator that memoizes (caches) the result of a function based on arguments. It uses a naive hash map approach.

### Q4: Can a decorator modify the function signature?
Yes. A decorator can take `func(a, b)` and return a wrapper accepting `wrapper(a, b, c)`. However, tools like `inspect.signature` might get confused unless you use advanced tools (like the `decorator` library) to fix the signature metadata.
