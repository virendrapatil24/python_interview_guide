# Python Numbers: A Comprehensive Guide

## 1. Basic Number Types

### Integer (int)

- Whole numbers without decimal points
- No size limitation in Python 3.x (limited only by available memory)
- Examples: `0`, `-17`, `1000000`

```python
x = 10
y = -3456
big_num = 123456789012345678901234567890  # No overflow!
```

### Float (float)

- Numbers with decimal points
- Follows IEEE-754 double-precision format
- Approximately 15-17 digits of precision
- Examples: `3.14`, `-0.001`, `2.0`

```python
x = 3.14
y = -0.001
z = 2.0  # This is a float, not an int
```

### Complex Numbers (complex)

- Numbers with real and imaginary parts
- Written as `x + yj` where x is real and y is imaginary
- Examples: `3+4j`, `2-1j`, `1j`

```python
z1 = 3 + 4j
z2 = complex(2, -1)  # Another way to create complex numbers
```

## 2. Number Operations and Properties

### Basic Operations

```python
# Addition
result = 5 + 3  # 8

# Subtraction
result = 5 - 3  # 2

# Multiplication
result = 5 * 3  # 15

# Division (always returns float)
result = 5 / 3  # 1.6666666666666667

# Floor Division
result = 5 // 3  # 1

# Modulus (remainder)
result = 5 % 3  # 2

# Power
result = 5 ** 3  # 125
```

### Type Conversion

```python
# Int to Float
float(5)  # 5.0

# Float to Int (truncates decimal part)
int(5.7)  # 5

# String to Number
int("123")  # 123
float("3.14")  # 3.14
```

## 3. Advanced Concepts and Interview Questions

### 1. Float Precision Issues

```python
# Famous floating-point precision example
0.1 + 0.2 == 0.3  # False!
print(0.1 + 0.2)  # 0.30000000000000004
```

**Interview Question:** Why does `0.1 + 0.2 != 0.3` in Python?
**Answer:** This is due to how floating-point numbers are stored in binary format. Not all decimal numbers can be represented exactly in binary, leading to small rounding errors.

### 2. Integer Division

```python
# Python 2 vs Python 3 division
5 / 2   # Python 3: 2.5
5 // 2  # Both: 2
```

**Interview Question:** What's the difference between `/` and `//` operators?
**Answer:** `/` performs true division (always returns float), while `//` performs floor division (rounds down to nearest integer).

### 3. Number System Conversions

```python
# Binary
bin(42)  # '0b101010'

# Octal
oct(42)  # '0o52'

# Hexadecimal
hex(42)  # '0x2a'

# Converting back to integer
int('101010', 2)  # 42 (binary to int)
int('2a', 16)    # 42 (hex to int)
```

### 4. Memory and Identity

```python
# Integer caching
a = 256
b = 256
print(a is b)  # True

c = 257
d = 257
print(c is d)  # False (usually)
```

**Interview Question:** Why does `is` operator behave differently for different integers?
**Answer:** Python caches small integers (-5 to 256 by default) for efficiency. Larger integers are created as new objects.

## 4. Advanced Topics and Tricks

### 1. Decimal Module

```python
from decimal import Decimal

# Exact decimal arithmetic
print(Decimal('0.1') + Decimal('0.2'))  # 0.3 exactly
```

### 2. Numerical Limits

```python
import sys

print(sys.float_info.max)  # Maximum float value
print(sys.float_info.min)  # Minimum positive float value
```

### 3. Infinity and NaN

```python
float('inf')   # Positive infinity
float('-inf')  # Negative infinity
float('nan')   # Not a Number
```

## 5. Common Interview Questions and Solutions

1. **Q: How would you swap two numbers without using a temporary variable?**

   ```python
   a, b = 5, 10
   a, b = b, a  # Python's tuple unpacking
   ```

2. **Q: How can you check if a number is a power of 2?**

   ```python
   def is_power_of_two(n):
       return n > 0 and (n & (n - 1)) == 0
   ```

3. **Q: How to handle floating-point comparison safely?**

   ```python
   import math
   def is_close(a, b, rel_tol=1e-09):
       return math.isclose(a, b, rel_tol=rel_tol)
   ```

## 6. Performance Tips

1. **Use Integer Division When Possible**

   - Integer operations are faster than floating-point operations

2. **Use Built-in Functions**

   ```python
   # Faster
   min(1, 2, 3)
   max(1, 2, 3)
   sum([1, 2, 3])

   # Slower
   sorted([1, 2, 3])[0]  # for minimum
   sorted([1, 2, 3])[-1] # for maximum
   ```

3. **Use math module for complex calculations**

   ```python
   import math

   # More efficient than ** operator for large numbers
   math.pow(2, 1000)
   ```

## 7. Best Practices

1. Use `decimal.Decimal` for financial calculations
2. Always use `is_close()` for floating-point comparisons
3. Be aware of integer division vs float division
4. Use appropriate number types for your use case
5. Consider memory implications when working with large numbers

## 8. Common Pitfalls

1. Assuming integer division in Python 3
2. Comparing floating-point numbers directly
3. Not handling overflow in arithmetic operations
4. Ignoring precision requirements in financial calculations
5. Using `is` operator for number comparisons
