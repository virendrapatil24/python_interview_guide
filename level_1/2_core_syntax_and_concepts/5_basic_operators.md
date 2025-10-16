# Python Operators: In-Depth Summary

## 1. Arithmetic Operators

- Used for mathematical calculations

| Operator | Description         | Example  | Result |
| -------- | ------------------- | -------- | ------ |
| `+`      | Addition            | `2 + 3`  | `5`    |
| `-`      | Subtraction         | `5 - 2`  | `3`    |
| `*`      | Multiplication      | `2 * 3`  | `6`    |
| `/`      | Division            | `5 / 2`  | `2.5`  |
| `//`     | Floor Division      | `5 // 2` | `2`    |
| `%`      | Modulus (remainder) | `5 % 2`  | `1`    |
| `**`     | Exponentiation      | `2 ** 3` | `8`    |

**Interview Tip:** Know the difference between `/` and `//`. `/` always returns float, `//` returns integer (floor).

## 2. Comparison (Relational) Operators

- Used to compare values, return Boolean

| Operator | Description      | Example  | Result |
| -------- | ---------------- | -------- | ------ |
| `==`     | Equal to         | `5 == 5` | `True` |
| `!=`     | Not equal to     | `5 != 3` | `True` |
| `>`      | Greater than     | `5 > 3`  | `True` |
| `<`      | Less than        | `3 < 5`  | `True` |
| `>=`     | Greater or equal | `5 >= 5` | `True` |
| `<=`     | Less or equal    | `3 <= 5` | `True` |

**Interview Tip:** Chained comparisons are allowed: `1 < x < 10`.

## 3. Logical Operators

- Used for Boolean logic

| Operator | Description | Example          | Result  |
| -------- | ----------- | ---------------- | ------- |
| `and`    | Logical AND | `True and False` | `False` |
| `or`     | Logical OR  | `True or False`  | `True`  |
| `not`    | Logical NOT | `not True`       | `False` |

**Interview Tip:** Logical operators use short-circuit evaluation.

## 4. Assignment Operators

- Used to assign values to variables

| Operator | Description         | Example   | Result       |
| -------- | ------------------- | --------- | ------------ |
| `=`      | Assignment          | `x = 5`   | `x = 5`      |
| `+=`     | Add and assign      | `x += 2`  | `x = x + 2`  |
| `-=`     | Subtract and assign | `x -= 2`  | `x = x - 2`  |
| `*=`     | Multiply and assign | `x *= 2`  | `x = x * 2`  |
| `/=`     | Divide and assign   | `x /= 2`  | `x = x / 2`  |
| `//=`    | Floor divide assign | `x //= 2` | `x = x // 2` |
| `%=`     | Modulus and assign  | `x %= 2`  | `x = x % 2`  |
| `**=`    | Exponent and assign | `x **= 2` | `x = x ** 2` |

## 5. Bitwise Operators

- Used for binary operations on integers

| Operator | Description | Example    | Result |
| -------- | ----------- | ---------- | ------ | --- | --- |
| `&`      | Bitwise AND | `5 & 3`    | `1`    |
| `        | `           | Bitwise OR | `5     | 3`  | `7` |
| `^`      | Bitwise XOR | `5 ^ 3`    | `6`    |
| `~`      | Bitwise NOT | `~5`       | `-6`   |
| `<<`     | Left shift  | `5 << 1`   | `10`   |
| `>>`     | Right shift | `5 >> 1`   | `2`    |

**Interview Tip:** Bitwise operations are common in low-level and optimization questions.

## 6. Membership Operators

- Test for membership in a sequence

| Operator | Description       | Example            | Result |
| -------- | ----------------- | ------------------ | ------ |
| `in`     | Value in sequence | `'a' in 'cat'`     | `True` |
| `not in` | Value not in seq  | `'b' not in 'cat'` | `True` |

## 7. Identity Operators

- Test if two objects are the same

| Operator | Description     | Example      | Result       |
| -------- | --------------- | ------------ | ------------ |
| `is`     | Same object     | `a is b`     | `True/False` |
| `is not` | Not same object | `a is not b` | `True/False` |

**Interview Tip:** `is` checks identity, not equality. Use `==` for value comparison.

## 8. Operator Precedence

- Determines the order of evaluation
- Parentheses `()` can override precedence

| Highest to Lowest Precedence |
| ---------------------------- | --- |
| `()` (parentheses)           |
| `**` (exponent)              |
| `+`, `-`, `~` (unary)        |
| `*`, `/`, `//`, `%`          |
| `+`, `-`                     |
| `<<`, `>>`                   |
| `&`                          |
| `^`                          |
| `                            | `   |
| Comparison (`==`, `!=`, etc) |
| `not`                        |
| `and`                        |
| `or`                         |

## 9. Common Interview Questions

1. **Q: What is the result of `True + 2`?**
   - `3` (because `True` is `1`)
2. **Q: How do you swap two variables without a temp variable?**
   - `a, b = b, a`
3. **Q: What does `a is b` mean?**
   - Checks if `a` and `b` are the same object
4. **Q: How do you check if a value is in a list?**
   - `value in my_list`
5. **Q: What is the output of `5 & 3`?**
   - `1` (bitwise AND)

## 10. Best Practices

- Use parentheses to clarify precedence
- Prefer `==` for value comparison, `is` for identity
- Use membership operators for sequence checks
- Use bitwise operators for performance-critical code
- Avoid chaining too many operators in one line for readability

## 11. Common Pitfalls

- Confusing `/` and `//` division
- Using `is` instead of `==` for value comparison
- Forgetting operator precedence
- Misusing bitwise operators on non-integers
- Not handling type errors in mixed-type operations
