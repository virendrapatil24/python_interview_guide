# Basic File Handling in Python

File handling (or File I/O) is the process of creating, reading, updating, and deleting files. It's a fundamental skill for any program that needs to persist data or work with external data sources.

---

## 1. The `open()` Function

The core of file handling is the built-in `open()` function, which creates a file object that serves as a link to a file on your system.

### Syntax

`open(file, mode='r', encoding=None)`

- **`file`**: The path to the file you want to open.
- **`mode`**: A string specifying how the file should be opened.
- **`encoding`**: The encoding to use for text files (e.g., `'utf-8'`). It's a best practice to always specify this.

### Common File Modes

| Mode  | Description                                                                       |
| :---- | :-------------------------------------------------------------------------------- |
| `'r'` | **Read** (default). Raises an error if the file does not exist.                   |
| `'w'` | **Write**. Creates a new file or **overwrites** an existing one.                  |
| `'a'` | **Append**. Creates a new file or appends to the end of an existing one.          |
| `'x'` | **Exclusive Creation**. Creates a file, but fails if it already exists.           |
| `'+'` | **Update**. Can be added to other modes (`'r+'`, `'w+'`) for reading and writing. |
| `'b'` | **Binary Mode**. For non-text files like images or executables.                   |
| `'t'` | **Text Mode** (default). For text files.                                          |

---

## 2. The `with` Statement (Context Manager)

The recommended way to work with files is using the `with` statement. It automatically and reliably closes the file for you, even if errors occur within the block.

### Syntax

```python
with open('my_file.txt', 'w', encoding='utf-8') as f:
    # Perform file operations here
    f.write("Hello, file!")

# The file is automatically closed here
```

**Why is this better?** Without `with`, you are responsible for calling `f.close()`. If an error happens before `f.close()` is reached, the file might be left open, which can lead to resource leaks or data corruption.

---

## 3. Reading from Files

Once a file is opened in read mode (`'r'`), you have several ways to get its content.

```python
with open('example.txt', 'r', encoding='utf-8') as f:
    # Method 1: Read the entire file into one string (for small files)
    content = f.read()
    print(content)

    # Method 2: Read line by line (memory efficient, best for large files)
    for line in f:
        print(line, end='') # The line already includes a newline

    # Method 3: Read one line at a time
    line1 = f.readline()
    line2 = f.readline()

    # Method 4: Read all lines into a list (for small to medium files)
    all_lines = f.readlines()
```

---

## 4. Writing to Files

To write data, open the file in write (`'w'`) or append (`'a'`) mode.

### `write()`

Writes a single string to the file. It does **not** add a newline character automatically.

```python
# 'w' mode will overwrite the file if it exists
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("This is the first line.\n")
    f.write("This is the second line.")
```

### `writelines()`

Writes a list of strings to the file. Like `write()`, it does **not** add newlines.

```python
lines = ["First line\n", "Second line\n", "Third line\n"]
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
```

---

## 5. Moving the Cursor with `seek()`

A file object has an internal cursor that tracks your position. You can move it with `f.seek(offset)`.

```python
with open('example.txt', 'r') as f:
    content = f.read(5)  # Read first 5 characters
    print(f"Current position: {f.tell()}") # Tell current position

    f.seek(0)  # Go back to the beginning of the file
    content_again = f.read(5)
```

---

## 6. Common Interview Questions

1.  **Q: Why is it important to use the `with open(...) as f:` syntax?**

    - **A:** It's a context manager that guarantees the file will be closed automatically and safely, even if exceptions are raised inside the block. This prevents resource leaks.

2.  **Q: What is the difference between `'w'` and `'a'` modes?**

    - **A:** `'w'` (write) mode overwrites the file if it exists, deleting all previous content. `'a'` (append) mode adds new content to the end of the file without deleting what's already there.

3.  **Q: What's the difference between `read()`, `readline()`, and `readlines()`?**

    - **A:**
      - `read()`: Reads the entire file content into a single string.
      - `readline()`: Reads a single line from the file, including the newline character.
      - `readlines()`: Reads all lines from the file into a list of strings.

4.  **Q: How would you read a large file without loading it all into memory?**

    - **A:** The best way is to iterate over the file object line by line: `for line in f:`. This reads the file one line at a time, which is very memory-efficient.

5.  **Q: What is the purpose of the `encoding` parameter in `open()`?**
    - **A:** It specifies how to decode bytes into characters for text files. Not specifying it can lead to errors or incorrect output because Python might use a system-dependent default encoding that doesn't match the file's actual encoding. `'utf-8'` is a safe and common choice.

---

## 7. Best Practices & Common Pitfalls

- **Best Practice**: Always use the `with` statement for file I/O.
- **Best Practice**: Always specify the `encoding` for text files to avoid platform-dependent behavior.
- **Best Practice**: Close files as soon as you are done with them to free up system resources. The `with` statement handles this for you.
- **Pitfall**: Using `read()` or `readlines()` on very large files can consume a lot of memory and crash your program. Prefer iterating line by line.
- **Pitfall**: Forgetting that `'w'` mode will completely erase the contents of an existing file.
- **Pitfall**: Forgetting that `write()` does not automatically add a newline (`\n`). You must add it manually if you want lines to be separated.
