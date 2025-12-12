# Aggregation in Python

## Has-A Relationship (Weak Association)

Aggregation is a specialized form of association. It represents a **"Has-a"** relationship where a "Parent" object contains a "Child" object, but the child can exist independently of the parent. This is often called a **Weak Association**.

### Key Characteristics
1.  **Independence:** The child object is created *outside* the parent and passed in.
2.  **Lifecycle:** If the parent is destroyed, the child object **survives**.

### Example: Department and Teacher
A Department *has* Teachers. However, if the Department closes (is deleted), the Teachers don't cease to exist; they can join another department.

```python
class Teacher:
    def __init__(self, name):
        self.name = name
    
    def teach(self):
        return "Teaching..."

class Department:
    def __init__(self, name, teachers=None):
        self.name = name
        # Teachers are passed in from outside (Aggregation)
        if teachers is None:
            self.teachers = []
        else:
            self.teachers = teachers

    def show_teachers(self):
        print(f"Department: {self.name}")
        for teacher in self.teachers:
            print(f"- {teacher.name}")

    def __del__(self):
        print(f"Department {self.name} is closing.")

# 1. Create independent objects (Teachers)
t1 = Teacher("Mr. Anderson")
t2 = Teacher("Ms. Frizzle")

# 2. Create the container object (Department) and aggregate teachers
dept = Department("Computer Science", [t1, t2])

# 3. Usage
dept.show_teachers()

# 4. Lifecycle Demonstration
del dept # Delete the department
# The teachers still exist!
print(f"Teacher {t1.name} is still here.")
print(f"Teacher {t2.name} is still here.")
```

### Interview Tip
In code, you identify aggregation when objects are passed to the `__init__` method (dependency injection) rather than being created inside it.
