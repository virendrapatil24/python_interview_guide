# Inheritance in Python

## Inheritance

A mechanism where a new class (child/subclass) inherits attributes and methods from an existing class (parent/superclass). This promotes code reuse.

```python
class Animal:
    def speak(self):
        return "Some generic animal sound"

# Dog inherits from Animal
class Dog(Animal):
    # Overriding the parent method
    def speak(self):
        return "Woof!"

    def wag_tail(self):
        return "Tail wagging"

# Another derived class
class Cat(Animal):
    def meow(self):
        return f"{self.name} says: Meow!"

my_dog = Dog()
print(my_dog.speak()) # Woof! (overridden method)
print(my_dog.wag_tail()) # wag_tail() is specific to Dog

my_cat = Cat()
print(my_cat.speak()) # Meow! (overridden method)
print(my_cat.meow()) # meow() is specific to Cat
```


### Using `super()`

The `super()` function is used to give access to methods and properties of a parent or sibling class. Reference the `super` function to call a method from the parent class.

This is most commonly used in the `__init__` method to initialize the parent class's attributes while adding new ones in the child class.

#### Example: Extending `__init__`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def work(self):
        return f"{self.name} is working."

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        # Call the parent class's constructor to handle name and salary
        super().__init__(name, salary)
        # Initialize the new attribute specific to Manager
        self.team_size = team_size

    # Extending a parent method
    def work(self):
        # Get the result from the parent method
        base_work = super().work()
        return f"{base_work} Managing a team of {self.team_size}."

# Usage
mgr = Manager("Alice", 90000, 5)
print(mgr.name)      # Output: Alice (Initialized by Employee)
print(mgr.team_size) # Output: 5 (Initialized by Manager)
print(mgr.work())    # Output: Alice is working. Managing a team of 5.
```

## Common Interview Questions

**Q: What is inheritance? Explain `super()`.**

- **A:** Inheritance allows a class (child) to inherit properties from another class (parent). `super()` is a built-in function that allows the child class to call methods from its parent class, which is especially useful for extending `__init__` or other overridden methods.
