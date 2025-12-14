# Deep Dive: The `re` Module (Regex)

Regular Expressions (Regex) are a powerful tool for matching patterns in text. Python's `re` module provides full support for Perl-like regular expressions.

---

## 1. common Methods (The Daily Drivers)

Here are the functions you will use 90% of the time.

### `re.match` vs `re.search`
This is the most common interview question.
*   **`match()`**: Checks for a match only at the **beginning** of the string.
*   **`search()`**: Scans through the **entire string** looking for the first location where the pattern produces a match.

```python
import re

text = "Hello Python World"

# Match checks start of string
print(re.match(r"Python", text))  # None (starts with Hello)
print(re.match(r"Hello", text))   # <re.Match object>

# Search scans everywhere
print(re.search(r"Python", text)) # <re.Match object>
```

### `re.findall` vs `re.finditer`
*   **`findall()`**: Returns a **list** of all non-overlapping matches.
*   **`finditer()`**: Returns an **iterator** yielding match objects. (Better for memory).

```python
text = "id=123, id=456, id=789"
ids = re.findall(r"\d+", text)
print(ids) # ['123', '456', '789']
```

### `re.sub` (Search and Replace)
Replaces the occurrences of the pattern with a replacement string.

```python
text = "Contact: 123-456-7890"
# Mask the digits
masked = re.sub(r"\d", "X", text)
print(masked) # Contact: XXX-XXX-XXXX
```

### `re.split`
Split string by the occurrences of the pattern.

```python
text = "apple, orange; banana: grape"
# Split by comma, semicolon, or colon (and optional space)
fruits = re.split(r"[,;:]\s*", text)
print(fruits) # ['apple', 'orange', 'banana', 'grape']
```

---

## 2. Engine Internals: The Backtracking NFA

Python uses a **Backtracking NFA** (Non-Deterministic Finite Automaton) engine.
*   **Mechanism**: It tries a path, and if it fails, it "backtracks" (rewinds) to try another alternative.
*   **Implication**: In worst-case scenarios, the checking time can be **Exponential** relative to the input string length.

---

## 3. The Danger: Catastrophic Backtracking (ReDoS)

**ReDoS** (Regular Expression Denial of Service) occurs when a regex takes years to compute on a relatively short string.

### The Trap
Pattern: `(a+)+$` on string `aaaaaaaaaaaaaaaaaaaa!`.
*   The engine tries to match the `a+` inside.
*   Then it tries to match the outer `+`.
*   When it hits the `!`, it fails and backtracks to try every possible combination of splitting the `a`'s between the inner and outer groups.

### The Solution: Atomic Grouping (Simulated)
Python `re` (before 3.11) did not support true Atomic Groups `(?>...)` natively (the `regex` module does). However, you can simulate it with lookaheads.

**Trick**: `(?=(...))\1`
This matches `...` in a lookahead (which is atomic-ish) and then consumes it with a backreference.

```python
import re
import time

# Bad: Infinite backtracking
bad_pattern = re.compile(r"(a+)+$")

# Safe: Atomic simulation (or just fixing the logic to r"a+$")
safe_pattern = re.compile(r"(?=(a+))\1$")

text = "a" * 30 + "!"

start = time.time()
try:
    # safe_pattern.match(text) # Fast
    pass
except Exception:
    pass
print("Finished")
```

---

## 4. Advanced Patterns: Lookarounds

Lookarounds allow you to match a position based on what is ahead or behind it, **without consuming characters**.

### Positive Lookahead `(?=...)`
"Match X only if followed by Y": `X(?=Y)`

```python
import re

text = "IsaacAsimov IsaacNewton"
# Match 'Isaac' only if followed by 'Newton'
pattern = r"Isaac(?=Newton)"
matches = re.findall(pattern, text)
print(matches) # ['Isaac'] (The first one is skipped)
```

### Negative Lookbehind `(?<!...)`
"Match Y only if NOT preceded by X": `(?<!X)Y`

```python
text = "100 USD 500 EUR"
# Match numbers NOT preceded by space (beginning of string)
# Actually, let's match 'USD' not preceded by '100 '
pattern = r"(?<!100 )USD"
print(re.search(pattern, text)) # None
```

---

## 5. Named Groups and Backreferences

Naming groups makes complex regex readable and allows referencing repeats.

### `(?P<name>...)`
```python
import re

log_line = "ERROR [2023-01-01]: Connection failed"
pattern = r"(?P<level>[A-Z]+) \[(?P<date>[\d-]+)\]: (?P<msg>.+)"

match = re.search(pattern, log_line)
if match:
    print(match.group('level')) # ERROR
    print(match.group('date'))  # 2023-01-01
```

### Backreferences `\1` or `(?P=name)`
Matching the **same text** identified by a previous capture group.

```python
# Match HTML tags: <b>Bold</b>
# <([a-z]+)> matches start tag
# .*? lazily matches content
# </\1> matches the closing tag with SAME name as group 1
pattern = r"<([a-z]+)>.*?</\1>"

text = "<b>Bold</b> <i>Italic</i>"
print(re.findall(pattern, text)) # ['b', 'i']
```

---

## 6. Performance Flags: `re.VERBOSE` and `re.compile`

Always use `re.VERBOSE` for complex regex. It ignores whitespace and comments inside the pattern.

```python
email_pattern = re.compile(r"""
    ^                   # Start of string
    [a-zA-Z0-9_.+-]+    # Username
    @                   # Separator
    [a-zA-Z0-9-]+       # Domain
    \.[a-zA-Z0-9-.]+    # TLD
    $                   # End of string
""", re.VERBOSE)
```

**Pre-compilation**: `re.compile()` caches the state machine. If you use a regex inside a loop, always compile it outside the loop.
