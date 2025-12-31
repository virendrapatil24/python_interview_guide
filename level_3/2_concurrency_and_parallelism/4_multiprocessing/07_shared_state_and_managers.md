# Deep Dive: Shared State (`Value`, `Array`, `Manager`)

Sharing state in `multiprocessing` is tricky because of the isolated memory model.

## 1. Shared Memory (`Value`, `Array`)
These use OS-level shared memory (like `shm` on Linux).

### `Value(typecode, init_value)`
*   **Typecode**: A C-style type character (e.g., `'i'` for signed int, `'d'` for double float).
*   **Locking**: By default, access is synchronized with an internal RLock. You can disable this with `lock=False`.

```python
num = Value('d', 0.0)
with num.get_lock():
    num.value += 1.5
```

### `Array(typecode, sequence)`
*   Fixed-size array of C types.
*   **Limitation**: Very rigid. You cannot grow/shrink it or store Python objects (like strings/lists).

## 2. Server Process (`Manager`)
The `Manager` creates a separate process that holds Python objects. Proxies allow other processes to manipulate them.

```python
manager = multiprocessing.Manager()
shared_list = manager.list()  # Supports append, sort, etc.
shared_dict = manager.dict()
```

### Pros
*   **Flexibility**: You can share Lists, Dicts, Namespaces.
*   **Ease of Use**: Behaves almost like normal Python objects.

### Cons (The Deep Technical Part)
1.  **Performance**: Every operation (e.g., `shared_list.append(1)`) is an IPC call (RPC). It triggers serialization + network/socket transfer + deserialization + execution + response. **It is slow.**
2.  **Memory**: The Manager is a separate process with its own overhead.

### Limitations
*   **Nested Updates**: Managers don't detect changes in nested mutable objects automatically.
    ```python
    d = manager.dict()
    d['nested'] = []
    d['nested'].append(1) # THIS FAILS to update the manager!
    # Fix: Reassign
    temp = d['nested']
    temp.append(1)
    d['nested'] = temp
    ```

## 3. Comparison
| Feature | `Value` / `Array` | `Manager` |
| :--- | :--- | :--- |
| **Speed** | High (Direct Memory) | Low (RPC overhead) |
| **Types** | C-primitives only (int/float) | Complex Python Objects |
| **Safety** | Requires explicit locking | Managed, but slower |
