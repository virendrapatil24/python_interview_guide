
import dis

def safe_operation():
    # Appending to a list is robust because the GIL protects the C-level function call
    l = []
    l.append(1)

def unsafe_operation():
    # Accessing global state with += is NOT atomic 
    global x
    x += 1

print("--- Bytecode for list.append (Thread-Safeish) ---")
# You will see LOAD_METHOD, CALL_METHOD. The CALL_METHOD executes C code,
# and the GIL is held during that C execution (unless explicitly released).
dis.dis(safe_operation)

print("\n--- Bytecode for x += 1 (Race Condition prone) ---")
# You will clearly see 3 distinct steps:
# 1. LOAD_GLOBAL (read x)
# 2. LOAD_CONST (load 1)
# 3. INPLACE_ADD (add them)
# 4. STORE_GLOBAL (write back)
# A thread switch can happen between 1 and 4!
dis.dis(unsafe_operation)
