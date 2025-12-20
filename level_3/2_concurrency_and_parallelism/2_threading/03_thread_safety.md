# Thread-Safe vs. Non-Thread-Safe Operations

Determining which operations are "atomic" (thread-safe) and which are not is the most critical skill in writing correct threaded code.

## 1. What makes an operation Atomic?

An operation is **atomic** if it appears to the rest of the system as an instantaneous action. It either happens completely, or not at all. No other thread can see an intermediate state or interrupt it halfway.

**The GIL Guarantee**: The GIL ensures that a single **Bytecode** instruction is atomic. It does NOT ensure that a single line of Python code is atomic (because one line can compile to many bytecodes).

---

## 2. Safe Operations (Atomic)

In general, operations that execute as a single bytecode or a single C-function call on built-in types (list, dict, set) are atomic.

**Examples of Thread-Safe implementation in CPython:**

1.  **Reading Variables**:
    *   `x = y` (Assignment)
    *   `x.y` (Attribute access)

2.  **List Operations**:
    *   `L.append(x)`
    *   `L.extend(y)`
    *   `x = L[i]`
    *   `x = L.pop()`
    *   `L.sort()`

3.  **Dictionary Operations**:
    *   `x = D[key]`
    *   `D[key] = x`
    *   `D.update(D2)`
    *   `D.pop(key)`

**Why?**
Because the underlying C implementation of `list.append` does not release the GIL while appending. It finishes the job in one go. You generally don't need a lock to `append` to a list shared by many threads.

---

## 3. Unsafe Operations (Non-Atomic)

Any operation that involves a "Read-Modify-Write" cycle is NOT safe because the GIL can switch threads between the 'Read' and the 'Write'.

**The Classic Trap: `+=`**

```python
n = 0
# Thread 1
n += 1 
```

**Under the hood (Bytecode):**
1.  `LOAD_GLOBAL n` (Read 0)
2.  `LOAD_CONST 1` (Load 1)
3.  `INPLACE_ADD` (Compute 1)
4.  **<-- DANGER ZONE: Context Switch can happen here -->**
5.  `STORE_GLOBAL n` (Write 1)

If Thread B runs inside the Danger Zone, it reads the *old* value of `n`, and you lose data.

**Other Unsafe Examples**:
-   `x = x + 1`
-   `done = not done` (Read bool, invert, write back)
-   `if x in my_list: my_list.remove(x)` (Check and Remove are separate—x might vanish in between!)

---

## 4. Proving it with `dis`

You can use the `dis` module to verify safety.

```python
import dis

def safe():
    l.append(1)

def unsafe():
    x[0] += 1

dis.dis(safe)
# ...
# LOAD_METHOD (append)
# CALL_METHOD <-- Single Opcode does the work. Atomic.
# ...

dis.dis(unsafe)
# ...
# INPLACE_ADD
# STORE_SUBSCR <-- Separate Opcodes. Switch possible in between.
```

---

## 5. Global vs Local State

-   **Thread-Local Data**: Variables defined inside a function start as local to that function's stack frame. They are typically safe because other threads can't see them (unless you explicitly pass them out).
-   **Shared Data** (Globals, Class Attributes, Passed Arguments): These are the danger zones requiring Locks.

## Summary

| Operation | Atomic? | Needs Lock? |
| :--- | :--- | :--- |
| `L.append(x)` | YES | No |
| `D[k] = v` | YES | No |
| `x = 5` | YES | No |
| `x = x + 1` | NO | **YES** |
| `x += 1` | NO | **YES** |
| `dict.setdefault` | YES | No |
| `JSON dump` | NO | YES |

**Rule of Thumb**: Even if you think it's atomic, if logic depends on *multiple* steps (Check if Key exists, THEN add value), put a Lock around it. "Check-Then-Act" is rarely atomic.
