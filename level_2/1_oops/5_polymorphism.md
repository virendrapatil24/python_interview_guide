# Polymorphism in Python

## Polymorphism

The ability of different objects to respond to the same method call in different ways. In Python, this is often achieved through "duck typing" ("If it walks like a duck and quacks like a duck, it's a duck").

```python
class Animal:
    def speak(self):
        return "Some generic animal sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow"

def make_animal_speak(animal):
    print(animal.speak())

make_animal_speak(Dog()) # Prints "Woof!"
make_animal_speak(Cat()) # Prints "Meow"


# The above code can be  deduce to list of animals (all treated as Animal)
animals = [Dog(), Cat()]

for animal in animals:
    print(animal.speak())
```

## Common Interview Questions

**Q: What is Duck Typing in Python?**
- **A:** It refers to the concept: "If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck." In Python, this means checking for the presence of a given method or attribute at runtime rather than checking for a specific type. If an object implements the required methods (e.g., `speak()`), it can be used regardless of its class inheritance.

**Q: Does Python support method overloading?**
- **A:** Not directly like Java or C++. You cannot define multiple methods with the same name but different signatures in the same class; the later one will overwrite the previous one. However, you can achieve similar behavior using:
    1.  **Default Arguments:** `def add(self, a, b=0):`
    2.  **Variable-length Arguments:** `def add(self, *args):`
    3.  **`@functools.singledispatch`** (for functions)

**Q: What is the difference between Method Overloading and Method Overriding?**
- **A:**
    -   **Overriding:** Redefining a parent class's method in a child class (Runtime Polymorphism).
    -   **Overloading:** Defining multiple methods with the same name but different parameters in the same class (Compile-time Polymorphism - *Not natively supported in Python*).
