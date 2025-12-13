# Deep Dive: The `json` Module

JSON is the lingua franca of the web. Python's `json` module is easy to start with (`dumps`/`loads`), but optimizing it and handling custom types requires deeper know-how.

---

## 1. Custom Encoders (`default` parameter)

The `json` serializer only handles basic types (dict, list, str, int, float, bool, None). It fails on `datetime`, `set`, or custom objects.

### The Subclassing Approach
Subclass `json.JSONEncoder` and override `default()`.

```python
import json
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # 1. Handle Datetime
        if isinstance(obj, datetime):
            return obj.isoformat()
        # 2. Handle Sets (JSON has no set, use list)
        if isinstance(obj, set):
            return list(obj)
        
        # 3. Let the base class raise TypeError for other non-serializable objects
        return super().default(obj)

data = {
    'time': datetime.now(),
    'tags': {'python', 'json'}
}

print(json.dumps(data, cls=CustomEncoder))
# Output: {"time": "2023-10-27T10:00:00.123456", "tags": ["python", "json"]}
```

---

## 2. Fast Custom Decoding (Hooks)

You can convert JSON strings directly into custom objects *during parsing* using hooks. This is faster than parsing to a dict and then converting.

### `object_hook`
This function is called for **every** JSON object (dict) decoded.

```python
import json

def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and v.endswith('Z') and 'T' in v:
            try:
                # Naive check for ISO format
                dct[k] = datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                pass
    return dct

json_str = '{"updated_at": "2023-10-27T10:00:00Z"}'
result = json.loads(json_str, object_hook=datetime_parser)
print(type(result['updated_at'])) # <class 'datetime.datetime'>
```

---

## 3. `object_pairs_hook` (Duplicate Keys)

Standard `json.loads` uses a dict, so if a JSON has duplicate keys, the *last one wins*.
`{"a": 1, "a": 2}` becomes `{"a": 2}`.

To preserve duplicate keys (or handle parsing order), use `object_pairs_hook`. It receives a list of `(key, value)` tuples.

```python
import json
from collections import OrderedDict

# Enforce order (Pre-Python 3.7 dicts were unordered)
# or handle duplicates
def handle_duplicates(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            print(f"Warning: Duplicate key {k} found!")
        d[k] = v
    return d

data = json.loads('{"a": 1, "a": 2}', object_pairs_hook=handle_duplicates)
# Output: Warning: Duplicate key a found!
```

---

## 4. Performance: Streaming Large Files

If you have a 2GB JSON file, `json.load(f)` reads the whole thing into memory.
You cannot stream a *single* massive JSON object effectively with the standard library (use `ijson` for that).

However, for **Line-Delimited JSON** (NDJSON), streaming is easy:

```python
import json

# Efficiently processing 10GB of log events
with open('large_logs.jsonl', 'r') as f:
    for line in f:
        # One object in memory at a time
        event = json.loads(line) 
        process(event)
```

**Optimization Tip**: `ujson` or `orjson` are 3rd party libraries written in C/Rust that are significantly faster than standard `json`. In high-performance systems, switch to them.

---

## 5. Security: `scan` vs `decode`

`json` is generally safe, but be wary of:
*   **Recursion Depth**: deeply nested JSON can cause stack overflow.
*   **Nan/Infinity**: Python allows `NaN` in JSON by default (which violates the spec). Use `allow_nan=False` to strictly adhere to the standard.

```python
try:
    json.dumps(float('nan'), allow_nan=False)
except ValueError:
    print("NaN not allowed in strict JSON")
```
