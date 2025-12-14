# Deep Dive: The `pydantic` Module

Pydantic is the industry standard for **Data Parsing and Validation** in modern Python. While Python's `dataclasses` focus on storing data, Pydantic focuses on *validating* it. It is the backbone of FastAPI, Typer, and many other modern frameworks.

> **Key Concept**: Pydantic parses data, not just validates it. If you say `id: int` and pass `"123"`, Pydantic will coerce it to integer `123`.

---

## 1. The Core: `BaseModel`

To create a schema, subclass `BaseModel` and define attributes with type hints.

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str = "Anonymous"
    tags: list[str] = []

# Happy Path
user = User(id="123", name="Alice", tags=["admin"])
print(user.id)        # 123 (Coerced from string!)
print(type(user.id))  # <class 'int'>

# Validation Error
try:
    User(id="invalid")
except ValidationError as e:
    print(e.json())
```

---

## 2. Field Customization

Use `Field` to add metadata (constraints, defaults, descriptions).

```python
from pydantic import BaseModel, Field, ValidationError

class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    sku: str = Field(min_length=3, max_length=10)

# Valid
p = Product(name="Hammer", price=9.99, sku="HAM-001")

# Handling Validation Errors Gracefully
try:
    Product(name="Hammer", price=-5, sku="HAM")
except ValidationError as e:
    print(" Validation Failed!")
    
    # Iterate over structured error list
    for err in e.errors():
        field = err['loc'][0]   # e.g., 'price'
        # Pydantic auto-generates this message based on the failed constraint (gt=0)
        msg = err['msg']        # e.g., 'Input should be greater than 0'
        print(f" -> Field '{field}': {msg}")
```

**Common Constraints**: `gt`, `lt`, `ge`, `le` (numbers); `min_length`, `max_length`, `pattern` (strings).

---

## 3. Custom Validators (`@field_validator`)

For logic that built-in constraints can't handle.

**V2 Style (Python 3.10+)**:

```python
from pydantic import BaseModel, field_validator

class SignUpRequest(BaseModel):
    password: str
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def match_passwords(cls, v: str, info):
        # Access other fields via info.data dictionary
        if 'password' in info.data and v != info.data['password']:
            raise ValueError("Passwords do not match")
        return v
    
    @field_validator('password')
    @classmethod
    def strong_password(cls, v: str):
        if len(v) < 8 or 'admin' in v:
            raise ValueError("Password too weak")
        return v
```

---

## 4. Derived & Computed Fields (`@computed_field`)

Often you want a field in the output JSON that is calculated from other fields.

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    def area(self) -> float:
        return self.width * self.height

r = Rectangle(width=10, height=5)
print(r.model_dump()) 
# {'width': 10.0, 'height': 5.0, 'area': 50.0}
```

---

## 5. Model Serialization (Dump / Load)

Pydantic V2 introduced highly optimized methods.

*   `model_validate_json(json_str)`: Parse raw JSON string.
*   `model_dump()`: Convert to Python dict.
*   `model_dump_json()`: Convert to JSON string.

```python
json_data = '{"id": 100, "name": "Bob"}'
user = User.model_validate_json(json_data)

# Export
print(user.model_dump(exclude={'tags'})) # {'id': 100, 'name': 'Bob'}
```

---

## 6. Settings Management (`pydantic-settings`)

Pydantic is rarely used just for API types; it is the gold standard for loading environment variables. Note: This is now a separate package `pip install pydantic-settings`.

```python
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    db_url: str
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

# Auto-loads from OS Key or .env file
# export DB_URL=postgres://...
config = AppSettings()
print(config.db_url)
```

---

## 7. Performance: Pydantic V2 (Rust Core)

**Crucial Interview Knowledge**:
Pydantic V2 (released 2023) rewrote the validation core in **Rust**.
*   **Speed**: It is 5-20x faster than Pydantic V1 and other pure-Python validation libraries.
*   **Validation**: It is "Correct by Construction".

---

## 8. Expert Interview Questions

### Q1: What is the difference between `model_validate` and `__init__`?
*   `__init__`: Standard Python initialization. Pydantic hooks into this to run validation when you call `User(id=1)`.
*   `model_validate(obj)`: Used to parse an existing dict/object into the model. Trustworthy for "Parsing".

### Q2: How do you handle circular references in Pydantic?
Use `UpdateForwardRefs` (V1) or `from __future__ import annotations` with string-based type hints (V2). Pydantic resolves them lazily.

### Q3: `mode='before'` vs `mode='after'` validators?
*   `mode='before'`: The validator runs **before** Pydantic tries to parse the type (e.g., converting a raw string to an object).
*   `mode='after'` (Default): Runs **after** Pydantic has validated that the type is correct (e.g., ensuring `age` is positive after ensuring it is an int).

### Q4: Why not just use Python `dataclasses`?
Dataclasses do not validate.
`d = DataClass(x="string")` where `x: int` is perfectly valid Python but creates a bug. Pydantic raises an error immediately. Pydantic also handles JSON serialization/deserialization out of the box.
