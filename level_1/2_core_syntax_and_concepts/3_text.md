# Python Strings: A Comprehensive Guide

## 1. String Basics

### String Creation

```python
# Single quotes
s1 = 'Hello'

# Double quotes
s2 = "World"

# Triple quotes (multiline)
s3 = '''This is a
multiline string'''

# Raw strings (ignores escape characters)
raw_str = r'C:\Users\name'

# f-strings (Python 3.6+)
name = "Alice"
greeting = f"Hello, {name}!"
```

### String Properties

- Immutable: Once created, cannot be modified
- Sequence type: Can be indexed and sliced
- Unicode by default in Python 3
- Support for escape sequences (`\n`, `\t`, etc.)

## 2. String Operations

### Basic Operations

```python
# Concatenation
str1 = "Hello" + " " + "World"  # "Hello World"

# Repetition
stars = "*" * 3  # "***"

# Length
len("Python")  # 6

# Indexing
text = "Python"
first = text[0]    # 'P'
last = text[-1]    # 'n'

# Slicing
text = "Python"
slice1 = text[1:4]    # 'yth'
slice2 = text[::-1]   # 'nohtyP' (reverse)
slice3 = text[::2]    # 'Pto' (step by 2)
```

### String Methods

```python
# Case operations
text = "Python Programming"
text.upper()       # "PYTHON PROGRAMMING"
text.lower()       # "python programming"
text.title()       # "Python Programming"
text.capitalize()  # "Python programming"
text.swapcase()    # "pYTHON pROGRAMMING"

# Whitespace handling
text = "  python  "
text.strip()       # "python"
text.lstrip()      # "python  "
text.rstrip()      # "  python"

# Searching and replacing
text = "Python is amazing"
text.find("is")        # 7 (returns -1 if not found)
text.index("is")       # 7 (raises ValueError if not found)
text.replace("is", "was")  # "Python was amazing"
text.count("a")        # 2

# Splitting and joining
text = "one,two,three"
words = text.split(",")    # ["one", "two", "three"]
",".join(words)           # "one,two,three"

# Check string properties
"Python".isalpha()     # True
"Python3".isalnum()    # True
"123".isdigit()        # True
"  ".isspace()         # True
"PYTHON".isupper()     # True
"python".islower()     # True
```

## 3. String Formatting

### 1. %-formatting (Old style)

```python
name = "Alice"
age = 25
print("My name is %s and I'm %d years old" % (name, age))

# Common specifiers
# %s - string
# %d - integer
# %f - float
# %.2f - float with 2 decimal places
```

### 2. str.format() Method

```python
# Basic formatting
"Hello, {}!".format("World")

# Positional arguments
"{0} and {1}".format("Alice", "Bob")

# Named arguments
"{name} is {age} years old".format(name="Alice", age=25)

# Format specifiers
"{:.2f}".format(3.14159)  # "3.14"
"{:>10}".format("test")   # "      test" (right align)
"{:^10}".format("test")   # "   test   " (center align)
"{:<10}".format("test")   # "test      " (left align)
```

### 3. f-strings (Python 3.6+)

```python
name = "Alice"
age = 25

# Basic usage
print(f"Name: {name}, Age: {age}")

# Expressions inside brackets
print(f"2 + 2 = {2 + 2}")

# Format specifiers
price = 49.9527
print(f"Price: ${price:.2f}")  # "Price: $49.95"

# Date formatting
from datetime import datetime
now = datetime.now()
print(f"Current time: {now:%Y-%m-%d %H:%M}")

# Debug syntax (Python 3.8+)
x = 10
print(f"{x=}")  # "x=10"
```

## 4. Advanced String Concepts

### String Interning

```python
# Python interns some strings for optimization
a = "hello"
b = "hello"
print(a is b)  # True

# But not all strings are interned
a = "hello!"
b = "hello!"
print(a is b)  # Might be False
```

### Bytes and Encoding

```python
# String to bytes
text = "Hello"
encoded = text.encode('utf-8')  # b'Hello'

# Bytes to string
decoded = encoded.decode('utf-8')  # "Hello"

# Handle encoding errors
text = "Hello 世界"
encoded = text.encode('ascii', errors='ignore')  # b'Hello '
encoded = text.encode('ascii', errors='replace')  # b'Hello ??'
```

## 5. Common Interview Questions

1. **Q: How to reverse a string in Python?**

   ```python
   # Method 1: Slicing
   text = text[::-1]

   # Method 2: Reversed function
   text = "".join(reversed(text))
   ```

2. **Q: Check if string is palindrome?**

   ```python
   def is_palindrome(s):
       s = s.lower()
       return s == s[::-1]
   ```

3. **Q: Count occurrences of each character?**

   ```python
   from collections import Counter

   def char_count(s):
       return Counter(s)
   ```

4. **Q: Remove duplicates from string?**
   ```python
   # Maintain order
   def remove_duplicates(s):
       return "".join(dict.fromkeys(s))
   ```

## 6. Performance Tips

1. **String Concatenation**

```python
# Bad (creates new string each time)
result = ""
for i in range(1000):
    result += str(i)

# Good (uses list and join)
result = "".join(str(i) for i in range(1000))
```

2. **String Comparison**

```python
# More efficient for prefix checking
if text.startswith("prefix"):
    pass

# Less efficient
if text[:6] == "prefix":
    pass
```

## 7. Best Practices

1. Use f-strings for string formatting (Python 3.6+)
2. Use `join()` for string concatenation in loops
3. Use string methods instead of regular expressions for simple cases
4. Be careful with string interning and `is` operator
5. Handle encoding/decoding errors appropriately
6. Use appropriate string methods (`strip()`, `split()`, etc.)
7. Consider memory usage with large strings

## 8. Common Pitfalls

1. Modifying strings (they're immutable)
2. Using `is` for string comparison
3. Inefficient string concatenation in loops
4. Not handling encoding/decoding errors
5. Using indices instead of string methods
6. Forgetting that `find()` returns -1 while `index()` raises exception
7. Not considering Unicode implications
