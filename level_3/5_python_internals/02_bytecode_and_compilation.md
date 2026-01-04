# Bytecode and Compilation

Python is often called an "interpreted language," but that is a simplification. The reality is that Python is a **bytecode-compiled** language.

---

## 1. The Execution Pipeline

When you run `python myscript.py`, the following happens:

1.  **Lexing/Tokenization**: The source code (text) is broken into tokens (keywords, identifiers, operators).
2.  **Parsing**: Tokens are organized into an Abstract Syntax Tree (AST), representing the logic structure.
3.  **Compilation**: The AST is compiled into **Bytecode**. This is a low-level, platform-independent set of instructions (similar to Assembly).
4.  **Execution**: The **Python Virtual Machine (PVM)** executes this bytecode one instruction at a time.

### Where is the "Interpreter"?
The PVM *is* the interpreter. It is a giant loop that reads a bytecode instruction and executes the corresponding C code.

---

## 2. What are `.pyc` files?

The "Compilation" step (Source -> Bytecode) takes time. To speed up start-up time for subsequent runs, Python saves the compiled bytecode to disk in `__pycache__` directories as `.pyc` files.

*   **Content**: They contain the compiled bytecode, not machine code.
*   **Validity**: Python checks the timestamp of the source file. If the `.py` is newer than the `.pyc`, it recompiles.
*   **Performance**: They **do not** make the program run faster. They only make it **start** faster (skip the compile step).

---

## 3. Disassembling Bytecode (`dis`)

You can view the bytecode using the `dis` module. This is incredibly useful for understanding *exactly* what Python is doing, especially when analyzing atomicity or race conditions.

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

**Typical Output:**
```text
  2           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```
*   `LOAD_FAST`: Pushes a local variable onto the stack.
*   `BINARY_ADD`: Pops two items, adds them, pushes result.
*   `RETURN_VALUE`: Pops item, returns it to caller.

---

## 4. The Python Virtual Machine (PVM)

The PVM is a **stack-based** machine.

*   It doesn't use registers (like x86 CPU).
*   It uses a value stack to hold arguments and results.
*   **Example**: `a + b`
    1.  Push `a` to stack.
    2.  Push `b` to stack.
    3.  Pop both, add them, push result.

This design makes the bytecode simple and portable, though slightly slower than register-based VMs (like LuaJIT or early Android Dalvik).

---

## Summary

*   **Process**: Source Code -> AST -> Bytecode -> PVM -> Machine Code (via C functions).
*   **Bytecode**: Intermediate instructions, stored in `.pyc`.
*   **PVM**: A stack-based interpreter that executes bytecode.

## Interview Checkpoint

**Q: "Is Python compiled or interpreted?"**
*   **Answer**: It is both. Source code is **compiled** to bytecode, which is then **interpreted** by the Python Virtual Machine.

**Q: "Does deleting .pyc files resolve runtime errors?"**
*   **Answer**: Generally no. Use cases where it helps are rare (e.g., corrupted file, timestamp mismatch bugs). It only forces a re-compile on next run.

**Q: "Why is `x += 1` not thread-safe?"**
*   **Answer**: `dis.dis('x += 1')` reveals it is 3 opcodes: `LOAD`, `ADD`, `STORE`. The GIL can switch threads between any of these steps, allowing another thread to change `x` before the `STORE` happens.
