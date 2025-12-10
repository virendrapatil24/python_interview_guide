# Encapsulation in Python

## Encapsulation

Bundling data (attributes) and methods that operate on the data into a single unit (a class). It restricts direct access to some of an object's components.

- **Public:** Accessible from anywhere (e.g., `my_var`).
- **Protected:** By convention, prefixed with a single underscore (e.g., `_my_var`). Should not be accessed from outside the class, but it's not enforced by Python.
- **Private:** Prefixed with a double underscore (e.g., `__my_var`). Python performs **name mangling** on these, making them harder to access from outside (`_ClassName__my_var`).


### Practical Example: Public, Protected, and Private Members

Here is a comprehensive example showing how access modifiers work in Python, including the concept of name mangling.

```python
class Animal:
    def __init__(self, name, species, age):
        self.name = name       # Public: Accessible from anywhere
        self._species = species # Protected: Accessible/modifiable subclass, but conventionally treated as non-public
        self.__age = age       # Private: Not accessible from outside directly

    def speak(self):
        print(f"{self.name} makes a sound.")

    # Protected method
    def _describe_species(self):
        print(f"{self.name} is a {self._species}.")

    # Private method
    def __reveal_age(self):
        print(f"Age of {self.name} is: {self.__age}")

    # Public method to control access to private variable (Getter)
    def get_age(self):
        return self.__age


class Dog(Animal):
    def speak(self):
        print(f"{self.name} barks.")

    def show_details(self):
        print("--- Dog Details ---")
        # 1. Public Access
        print(f"Name (Public): {self.name}")

        # 2. Protected Access (Allowed in subclass)
        print(f"Species (Protected): {self._species}")

        # 3. Private Access via Public Getter
        print(f"Age (Private via Getter): {self.get_age()}")

        # 4. Protected Method Access
        self._describe_species()

        # 5. Direct Private Access (Will Fail)
        # self.__reveal_age() # AttributeError: 'Dog' object has no attribute '_Dog__reveal_age'

        # 6. Name Mangling (Technically possible, but bad practice)
        print("Accessing private method via name mangling:")
        self._Animal__reveal_age()


# Usage
dog = Dog("Koko", "Golden Retriever", "5")
dog.speak()
dog.show_details()
```

## Common Interview Questions

**Q: What is name mangling in Python?**

- **A:** It's a mechanism Python uses for "private" attributes. If you have an attribute named `__my_attr` in a class `MyClass`, Python internally renames it to `_MyClass__my_attr` to avoid accidental name clashes in subclasses.
