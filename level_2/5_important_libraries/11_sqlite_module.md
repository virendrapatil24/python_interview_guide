# Deep Dive: The `sqlite3` Module

SQLite is a C-language library that implements a SQL database engine. Python's `sqlite3` module provides a compliant interface (PEP 249) to interact with it. It is serverless and zero-configuration.

---

## 1. Connection and Cursors

*   **Connection**: Represents the database.
*   **Cursor**: The control structure used to traverse and fetch the records of the database.

```python
import sqlite3

# ':memory:' creates a temporary DB in RAM (great for testing)
con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("CREATE TABLE lang(name, first_appeared)")
cur.execute("INSERT INTO lang VALUES (?, ?)", ("C", 1972))
```

---

## 2. Transactions and Context Managers

By default, `sqlite3` opens a transaction implicitly before a DML statement (INSERT/UPDATE/DELETE). You must `commit()` manually.

**Best Practice**: Use the connection as a context manager to auto-commit (or rollback on error).

```python
try:
    with con:
        # Inside this block, a transaction is managed
        con.execute("INSERT INTO lang VALUES (?, ?)", ("Python", 1991))
        # If execution succeeds, con.commit() is called automatically.
except sqlite3.IntegrityError:
    # If error occurs, con.rollback() is called automatically.
    print("Could not insert data")
```

---

## 3. High Performance: `executemany`

Never loop over `execute()` for bulk inserts. It is thousands of times slower.

```python
data = [
    ("Java", 1995),
    ("Go", 2009),
    ("Rust", 2010),
]

# Optimized C-level loop
cur.executemany("INSERT INTO lang VALUES (?, ?)", data)
```

---

## 4. Security: SQL Injection

**NEVER** use string formatting (f-strings) to build SQL queries.
**ALWAYS** use parameterized queries (`?`).

```python
user_input = "' OR 1=1 --"

# VULNERABLE
# Query becomes: SELECT * FROM users WHERE name = '' OR 1=1 --'
cur.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# SECURE
# Driver treats user_input as a literal string value, not SQL code
cur.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

---

## 5. Advanced: Custom Functions and Aggregates

You can attach Python functions to the SQLite engine.

```python
import hashlib

def md5sum(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()

# Register function in SQL
con.create_function("md5", 1, md5sum)

cur.execute("SELECT md5(name) FROM lang LIMIT 1")
print(cur.fetchone())
```
