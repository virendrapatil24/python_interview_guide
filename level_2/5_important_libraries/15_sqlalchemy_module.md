# Deep Dive: SQLAlchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper (ORM). It gives application developers the full power and flexibility of SQL.

---

## 1. The Two Layers: Core vs ORM

SQLAlchemy is actually two libraries in one.

### Core
A Pythonic abstraction over SQL data types and expressions. It is "SQL-like" but database agnostic.
*   Used for: High performance, Schema definition, Bulk operations.
*   Structure: `Engine`, `Connection`, `Table`, `select()`.

### ORM (Object Relational Mapper)
Builds upon Core to map Python classes to database tables.
*   Used for: Domain logic, complex relationships, rapid development.
*   Structure: `Session`, `Model`, `query()`.

---

## 2. The `Session` Lifecycle

The `Session` is the handle to the database conversation. It implements the **Unit of Work** pattern.
*   It tracks changes to objects (Identity Map).
*   It flushes changes to the DB in a transaction when needed.

**Common Mistake**: Sharing a Session across threads.
**Fix**: Use `scoped_session` for thread-local sessions (common in Flask/Web apps).

---

## 3. The N+1 Select Problem

The classic ORM performance killer (Lazy Loading).

```python
# Scenario: Users have Addresses
users = session.query(User).all() # 1 Query
for user in users:
    print(user.address) # N Queries (One per user!)
```

**Solution**: Eager Loading (`joinedload` or `subqueryload`).

```python
from sqlalchemy.orm import joinedload
# Loads User AND Address in 1 BIG query (JOIN)
users = session.query(User).options(joinedload(User.address)).all()
```

---

## 4. Migrations (Alembic)

SQLAlchemy defines the schema in code, but `Alembic` manages changes to the DB over time.
*   Auto-generate migrations: `alembic revision --autogenerate -m "Add column"`
*   Ideally, your models are the "Source of Truth".

---

## 5. Declarative Mapping (Modern Style)

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```
