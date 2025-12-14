# Deep Dive: Beautiful Soup (`bs4`)

Beautiful Soup is a library for pulling data out of HTML and XML files. It sits on top of an HTML parser (like lxml or html.parser) and provides Pythonic idioms for iterating, searching, and modifying the parse tree.

---

## 1. Parser Wars: `lxml` vs `html.parser`

Beautiful Soup does not parse HTML itself; it uses a backend.

| Parser | Speed | Lenient? | Dependency |
| :--- | :--- | :--- | :--- |
| `lxml` | **Very Fast** | Yes | C library (pip install lxml) |
| `html.parser` | Moderate | Yes | Standard Library (Zero dep) |
| `html5lib` | Slow | **Extremely** | External (Pure Python) |

```python
from bs4 import BeautifulSoup

html_doc = "<html><p>Broken HTML..."
# Always specify the parser explicitly to avoid warning/ambiguity
soup = BeautifulSoup(html_doc, 'lxml')
```

---

## 2. Searching the Tree (`find` vs `select`)

### `find()` / `find_all()`
The classic BS4 API. Good for specific attributes.

```python
# Find first <div> with specific class
soup.find('div', class_='content')

# Find by custom attribute
soup.find(attrs={"data-id": "123"})
```

### `select()` (CSS Selectors)
Often more powerful and concise for modern web scraping. Supports nested selectors.

```python
# Find all <a> tags inside <div class='menu'>
links = soup.select('div.menu > a')
```

---

## 3. Navigating the Tree

You can move sideways and up, not just down.
*   `.parent`: Go up.
*   `.next_sibling` / `.previous_sibling`: Move sideways (be careful of whitespace nodes!).

**Performance Tip**: `SoupStrainer`
If you only need a tiny part of a massive document, parse *only* that part to save memory.

```python
from bs4 import SoupStrainer

# Only parse <a> tags, ignore the rest of the 5MB HTML
only_a_tags = SoupStrainer("a")
soup = BeautifulSoup(html_doc, "lxml", parse_only=only_a_tags)
```
