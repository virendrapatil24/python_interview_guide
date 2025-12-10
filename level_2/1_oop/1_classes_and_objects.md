# Python Classes and Objects: An Interview Deep Dive

Object-Oriented Programming (OOP) is a fundamental paradigm in Python. Understanding classes and objects is essential for writing scalable, organized, and reusable code. This guide covers the core concepts from basic to advanced, focusing on common interview topics.

---

## 1. Introduction: Classes and Objects

- **Class:** A blueprint or template for creating objects. It defines a set of attributes (data) and methods (functions) that the created objects will have.
- **Object (Instance):** A specific instance of a class. It has its own state (values for its attributes) and can perform actions using its methods.

Think of a `Car` class as the blueprint. It defines that a car has attributes like `color` and `model`, and methods like `start_engine()`. An individual car, like a "red Tesla Model S", is an object (an instance) of the `Car` class.

---

## 2. Defining a Class and Creating Objects

### The `__init__` Method and `self`

- The `class` keyword is used to define a class.
- The `__init__` method is a special "dunder" (double underscore) method called a **constructor**. It's automatically called when you create a new object to initialize its attributes.
- The `self` parameter is a reference to the current instance of the class. It's used to access variables that belong to the class. It must be the first parameter of any instance method.

```python
# Define the blueprint (Class)
class Dog:
    # This is the constructor
    def __init__(self, name, age):
        # These are instance attributes
        self.name = name
        self.age = age
        print(f"Dog named {self.name} was created.")

    # This is an instance method
    def bark(self):
        return f"{self.name} says Woof!"

# Create instances of the class (Objects)
dog1 = Dog("Buddy", 4)
dog2 = Dog("Lucy", 2)

# Access attributes and call methods
print(f"{dog1.name} is {dog1.age} years old.") # Buddy is 4 years old.
print(dog2.bark()) # Lucy says Woof!
```

---

## 3. Common Interview Questions

1.  **Q: What is `self`?**

    - **A:** `self` represents the instance of the class. It allows you to access the attributes and methods of the class in Python. It is the first argument passed to instance methods.

---

## 4. Next Steps: Deep Dive

Now that you understand the basics, dive deeper into:

- [**Attributes and Methods**](./2_attributes_and_methods.md): Learn about `self`, `@classmethod`, `@staticmethod`, and Magic Methods.
- **The 4 Pillars of OOP**:
    - [Encapsulation](./3_encapsulation.md)
    - [Inheritance](./4_inheritance.md)
    - [Polymorphism](./5_polymorphism.md)
    - [Abstraction](./6_abstraction.md)
