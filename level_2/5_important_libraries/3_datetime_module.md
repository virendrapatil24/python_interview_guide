# Deep Dive: The `datetime` Module

Handling time is notoriously difficult in computer science. The `datetime` module is powerful but filled with traps for the unwary (especially around timezones).

---

## 1. Naive vs. Aware Objects (The #1 Mistake)

A `datetime` object can be one of two types:
1.  **Naive**: Contains no timezone information. It represents "clock time" (e.g., "It is 5:00 PM").
2.  **Aware**: Contains a `tzinfo` object. It represents a specific instant in the universe.

**The Golden Rule**: NEVER mix naive and aware objects. Python will raise a `TypeError` on subtraction or comparison.

### The Modern Way: `zoneinfo` (Python 3.9+)
Before 3.9, you needed the external `pytz` library. Now, the standard library includes IANA time zone support via `zoneinfo`.

```python
from datetime import datetime
from zoneinfo import ZoneInfo # Python 3.9+ standard library

# 1. Capture current time in UTC (Always store UTC in DB!)
now_utc = datetime.now(ZoneInfo("UTC"))
print(f"UTC: {now_utc}") 
# Output: 2023-10-27 10:00:00+00:00

# 2. Convert to User's Local Time (Display only)
user_tz = ZoneInfo("Asia/Kolkata")
now_india = now_utc.astimezone(user_tz)
print(f"India: {now_india}")
# Output: 2023-10-27 15:30:00+05:30

# 3. Arithmetic handles DST transitions automatically
from datetime import timedelta
future = now_india + timedelta(days=1)
```

---

## 2. Monotonic Clocks vs Wall Time

Which function should you use to measure performance?

*   `time.time()`: Returns "Wall Clock" time. **DANGEROUS** for measuring duration. The user can change the system clock, or NTP can adjust it backward, causing negative durations.
*   `time.monotonic()`: A clock that *cannot go backward*. It is not affected by system clock updates. Use this for general timeouts and scheduling.
*   `time.perf_counter()`: The highest resolution monotonic clock available (CPU counter). Use this for **benchmarking**.

```python
import time

# BAD: Measuring execution time
start = time.time()
# ... operation ...
end = time.time()
# If NTP update happens here, (end - start) could be negative!

# GOOD:
start = time.perf_counter()
# ... operation ...
end = time.perf_counter()
print(f"Duration: {end - start:.6f} seconds")
```

---

## 3. Parsing ISO 8601 (Correctly)

`isoformat()` is the industry standard for string serialization.
Older Python versions struggled to parse ISO strings with timezones (like `2023-01-01T12:00:00+05:30`).

### `datetime.fromisoformat()`
In Python 3.7+, `fromisoformat()` can handle the output of `isoformat()`, but it was limited.
In Python 3.11+, it essentially supports any valid ISO 8601 string.

```python
from datetime import datetime

# The "Z" (Zulu/UTC) suffix was historically tricky
iso_string = "2023-10-27T10:00:00Z"

# Python 3.11+ handles the 'Z' automatically
dt = datetime.fromisoformat(iso_string)
print(dt)
# Output: 2023-10-27 10:00:00+00:00
```

---

## 4. `timedelta` and Date Arithmetic

`timedelta` represents a duration.

**Trap**: `timedelta` does not support "months" or "years" because those represent variable durations (28-31 days, 365-366 days).
*   For accurate calendar arithmetic (e.g., "add 1 month"), use `python-dateutil` (external) `relativedelta`.

```python
from datetime import datetime, timedelta

now = datetime.now()
tomorrow = now + timedelta(days=1) # Safe
next_week = now + timedelta(weeks=1) # Safe

# next_month = now + timedelta(months=1) # TypeError! Invalid argument
```

---

## Summary Checklist

| Class/Method | Purpose | Principal Note |
| :--- | :--- | :--- |
| `datetime.timestamp()` | Get POSIX timestamp (float) | Relative to Epoch (1970-1-1). Always implies UTC. |
| `datetime.combine()` | Merge date + time | Useful when date and time come from different widgets/inputs. |
| `dateutil.parser` | Flexible parsing | Use this (external lib) if you need to parse "fuzzy" strings like "Jan 1st, 2023". |
