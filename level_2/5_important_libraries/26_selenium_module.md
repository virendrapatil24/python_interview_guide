# Deep Dive: Selenium

Selenium automates browsers. It is primarily used for testing web applications but is also popular for scraping dynamic (JS-heavy) websites.

---

## 1. WebDriver Architecture

Selenium sends commands to a "Driver" executable (e.g., `chromedriver`), which acts as a server to control the actual Browser via internal protocols (DevTools Protocol).

---

## 2. Implicit vs Explicit Waits (Flakiness Killer)

Web pages are asynchronous. Elements don't appear instantly.
*   **Implicit Wait**: "If element not found, poll for X seconds." (Global setting).
*   **Explicit Wait**: "Wait until specific condition (Visible, Clickable) is met." (Recommended).

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Explicit Wait (Best Practice)
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submitDir"))
)
element.click()
```

---

## 3. Headless Mode

Running without a UI. Essential for servers/CI.

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
```

---

## 4. Page Object Model (POM)

A Design Pattern. Create a Class for each page of your app. Methods represent actions.
This decouples "How to find element" from "What the test does".

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_box = (By.ID, "user")
    
    def login(self, user):
        self.driver.find_element(*self.username_box).send_keys(user)
```
