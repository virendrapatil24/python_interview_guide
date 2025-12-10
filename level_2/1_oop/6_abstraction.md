# Abstraction in Python

## Abstraction

Hiding complex implementation details and showing only the essential features of the object. In Python, this is often achieved by defining classes with clear, public methods for interaction, while keeping the internal workings private.

To enforce abstraction at a class level (ensuring subclasses implement specific methods), Python uses **Abstract Base Classes (ABCs)**.

### Example: Abstract Base Classes

We use the `abc` module to define an abstract base class. Subclasses *must* implement all abstract methods/properties.

```python
from abc import ABC, abstractmethod

# Abstract Base Class
class Animal(ABC):

    @abstractmethod
    def make_sound(self):
        """Subclasses must implement this method"""
        pass

    @abstractmethod
    def move(self):
        """Subclasses must implement this method"""
        pass

# Concrete class
class Dog(Animal):
    def make_sound(self):
        return "Woof!"

    def move(self):
        return "Runs on four legs."

# Concrete class
class Fish(Animal):
    def make_sound(self):
        return "... (silence)"

    def move(self):
        return "Swims in water."

# Usage
# animal = Animal() # TypeError: Can't instantiate abstract class Animal

dog = Dog()
print(f"Dog says: {dog.make_sound()}")
print(f"Dog moves: {dog.move()}")

fish = Fish()
print(f"Fish says: {fish.make_sound()}")
print(f"Fish moves: {fish.move()}")
```

## Common Interview Questions

**Q: What is an Abstract Base Class (ABC)?**
- **A:** An ABC is a class that cannot be instantiated and is used to define a common interface for its subclasses. In Python, we use the `abc` module and the `@abstractmethod` decorator to define them.

**Q: Can you instantiate a class with abstract methods?**
- **A:** No. If you try to create an instance of a class that inherits from an ABC but doesn't implement all its abstract methods, Python will raise a `TypeError` at instantiation time.
