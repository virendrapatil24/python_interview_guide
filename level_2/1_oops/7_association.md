# Association in Python

## Use-A Relationship

Association is a relationship between two separate classes that establishes through their objects. It is known as a **"Use-a"** relationship. In association, the two classes are independent; one class uses the other, but neither owns the other.

### Key Characteristics
1.  **Independence:** Both objects have their own lifecycle. If one is destroyed, the other still exists.
2.  **Multiplicity:** It can be One-to-One, One-to-Many, or Many-to-Many.

### Example: Doctor and Patient
A Doctor treats a Patient, and a Patient consults a Doctor. They interact, but a Doctor isn't *part of* a Patient, nor vice versa.

```python
class Patient:
    def __init__(self, name):
        self.name = name

    def consult(self, doctor):
        print(f"Patient {self.name} is consulting Doctor {doctor.name}")

class Doctor:
    def __init__(self, name):
        self.name = name
    
    def treat(self, patient):
        print(f"Doctor {self.name} is treating Patient {patient.name}")

# Creating Objects independently
p1 = Patient("John")
p2 = Patient("Sarah")

d1 = Doctor("Dr. Smith")
d2 = Doctor("Dr. Who")

# Establishing Association
d1.treat(p1)  # Doctor uses Patient object
p2.consult(d2) # Patient uses Doctor object

# Lifecycle Verification
del d1
print(f"Patient {p1.name} still exists after Doctor is deleted.")
```

### Types of Association
-   **One-to-One:** Example: A User and a Profile.
-   **One-to-Many:** Example: A Teacher and Students.
-   **Many-to-Many:** Example: Students and Courses.
