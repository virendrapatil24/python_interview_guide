# Python Attributes and Methods

Understanding how Python handles attributes and methods is crucial for mastering OOP.

## 1. Instance vs. Class Variables

This is a very common interview question.

- **Class Variables:** Shared among all instances of a class. They are defined directly inside the class but outside of any methods.
- **Instance Variables:** Unique to each instance. They are defined inside the `__init__` method using `self`.

```python
class Car:
    # Class variable (shared by all Car objects)
    wheels = 4

    def __init__(self, make, model):
        # Instance variables (unique to each object)
        self.make = make
        self.model = model

car1 = Car("Toyota", "Camry")
car2 = Car("Honda", "Civic")

# Both instances share the class variable
print(car1.wheels)  # 4
print(car2.wheels)  # 4

# You can access it via the class itself
print(Car.wheels)   # 4

# Modifying the class variable affects all instances
Car.wheels = 3
print(car1.wheels)  # 3
print(car2.wheels)  # 3
```

## 2. Instance, Class, and Static Methods

### Instance Method

- The most common type. It takes `self` as the first argument and can access/modify instance state.
- Example: `def my_method(self, ...)`

### Class Method

- Marked with a `@classmethod` decorator.
- Takes `cls` (the class itself) as the first argument, not `self`.
- Can access/modify class state (class variables) but not instance state.
- Often used as factory methods to create instances in a specific way.

### Static Method

- Marked with a `@staticmethod` decorator.
- Doesn't take `self` or `cls` as the first argument.
- It's essentially a regular function namespaced within the class. It cannot access class or instance state.
- Used for utility functions that are logically related to the class but don't depend on its state.

### Real-World Interview Example: Employee System

Here is a practical example you can use in an interview to demonstrate *when* to use each type.

```python
class Employee:
    # Class Variable: Common to all employees
    raise_amount = 1.05  # 5% raise

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # Instance Method: modifying the specific instance's data
    def apply_raise(self):
        self.salary = int(self.salary * self.raise_amount)
        return f"{self.name}'s new salary: {self.salary}"

    # Class Method: Alternative Constructor (Factory)
    # Uses 'cls' to create a new instance
    @classmethod
    def from_string(cls, emp_str):
        name, salary = emp_str.split('-')
        return cls(name, int(salary))

    # Static Method: Utility function
    # Logical connection to Employee, but doesn't need specific employee or class data
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6: # Sat or Sun
            return False
        return True

import datetime

# 1. Instance Method Usage
emp_1 = Employee("Alice", 50000)
print(emp_1.apply_raise()) 
# Output: Alice's new salary: 52500

# 2. Class Method Usage (Creating an object from a string)
emp_str_Input = "Bob-60000"
emp_2 = Employee.from_string(emp_str_Input)
print(emp_2.name) 
# Output: Bob

# 3. Static Method Usage (Checking a date)
my_date = datetime.date(2023, 10, 23) # A Monday
print(Employee.is_workday(my_date)) 
# Output: True
```

### Basic Syntax Example

Here is a simple example to see the syntax differences clearly.

```python
class MyClass:
    class_var = "I am a class variable"

    def __init__(self, instance_var):
        self.instance_var = instance_var

    # Instance method
    def instance_method(self):
        return f"Accessing instance var: {self.instance_var}"

    # Class method
    @classmethod
    def class_method(cls):
        return f"Accessing class var: {cls.class_var}"

    # Static method
    @staticmethod
    def static_method(x, y):
        return f"I'm a utility. Result: {x + y}"

obj = MyClass("I am an instance variable")
print(obj.instance_method())
print(MyClass.class_method())
print(MyClass.static_method(5, 3))
```

### Key Differences for Interviews

| Type | Decorator | First Argument | Access | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Instance** | None | `self` | Instance & Class | Modifying object state (e.g., `update_email`) |
| **Class** | `@classmethod` | `cls` | Class Only | Factory methods (e.g., `from_json`) |
| **Static** | `@staticmethod` | None | Neither | Utility functions (e.g., `is_valid_email`) |

## 3. Magic (Dunder) Methods

Special methods with double underscores at the beginning and end of their names. They allow you to emulate the behavior of built-in types.

- `__str__(self)`: Called by `str(obj)` and `print(obj)`. Should return a user-friendly string representation.
- `__repr__(self)`: Called by `repr(obj)`. Should return an unambiguous, official string representation that, ideally, can be used to recreate the object.
- `__len__(self)`: Called by `len(obj)`.
- `__eq__(self, other)`: Called by the equality operator `==`.

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f'"{self.title}" by {self.author}'

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    def __len__(self):
        return self.pages

book = Book("1984", "George Orwell", 328)
print(book)         # Calls __str__: "1984" by George Orwell
print(repr(book))   # Calls __repr__: Book('1984', 'George Orwell', 328)
print(len(book))    # Calls __len__: 328
```

## 4. Common Interview Questions

**Q: What is the difference between a class method, a static method, and an instance method?**

- **A:** **Instance methods** need a class instance and can access the instance through `self`. **Class methods** don't need an instance; they need the class itself and can access it through `cls`. **Static methods** don't need the class or instance and are like regular functions inside the class's namespace.

**Q: What is the difference between `__str__` and `__repr__`?**
- **A:** `__str__` is for creating a readable, user-friendly output. `__repr__` is for creating an unambiguous, official representation of an object, often used for debugging and development. If `__str__` is not defined, `print()` will fall back to using `__repr__`.
