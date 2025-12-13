# Deep Dive: FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

---

## 1. ASGI vs WSGI

FastAPI runs on **ASGI** (Asynchronous Server Gateway Interface), specifically standardizing `async` / `await` support.
*   Allows handling WebSockets.
*   High concurrency (handles thousands of requests/s).
*   Needs an ASGI server like `uvicorn` or `hypercorn`.

---

## 2. Pydantic (Data Validation)

FastAPI relies heavily on **Pydantic**. You define the "shape" of data using classes with Type Hints.
*   **Validation**: Automatically validates incoming JSON against the class schema.
*   **Serialization**: Converts output objects to JSON.
*   **Docs**: Auto-generates OpenAPI (Swagger) schemas.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None
```

---

## 3. Dependency Injection

FastAPI has a powerful DI system.
You can create a "Dependency" (a function) that is executed before the path operation.
*   Code reuse (DB connection logic).
*   Security (OAuth2 authentication).

```python
from fastapi import Depends

async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

---

## 4. Async/Await (Concurrency)

If your endpoint does I/O (DB, Network), verify your library supports `async`.
*   **Good**: `async def` with `await database.fetch_all()`.
*   **Bad**: `async def` with blocking code (e.g., `requests.get`, `time.sleep`). This blocks the **Entire Loop**. If you must block, use `def` (FastAPI runs it in a threadpool).

---

## 5. Background Tasks

FastAPI can handle background tasks (like sending email) after returning a response.

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"notification sent to {email}")
    return {"message": "Notification sent in the background"}
```
