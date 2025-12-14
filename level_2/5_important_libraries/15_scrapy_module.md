# Deep Dive: Scrapy

Scrapy is an asynchronous web crawling framework. Unlike Beautiful Soup (which just parses), Scrapy manages requests, concurrency, pipelines, and exports.

---

## 1. Asynchronous Architecture (Twisted)

Scrapy is built on **Twisted**, an event-driven networking engine.
*   **Blocking is the Enemy**: If you use `time.sleep()` or a blocking DB call in a parser, you halt the *entire* crawler.
*   **Concurrency**: Scrapy handles multiple requests in parallel (controlled by `CONCURRENT_REQUESTS`).

---

## 2. The Data Flow

1.  **Spider**: Yields `Request` objects.
2.  **Scheduler**: Queues the requests.
3.  **Downloader**: Fetches the internet content (Async).
4.  **Spider**: Parses the `Response` and yields `Item` (data) or new `Request`.
5.  **Item Pipeline**: Processes `Item` (Clean, Validate, Save to DB).

---

## 3. Middleware

You can hook into the request/response lifecycle.
*   **Downloader Middleware**: Global modifications to Requests/Responses (e.g., Rotating User-Agents, Proxy management).
*   **Spider Middleware**: Processing input to spiders.

---

## 4. Avoiding Bans

*   **AutoThrottle**: Automatically adjusts delay based on server load.
*   **Cookies**: Enabled by default (Simulates a session). Disable `COOKIES_ENABLED` for stateless scraping (often harder to track).

```python
# settings.py
DOWNLOAD_DELAY = 1.0 # 1 second delay
RANDOMIZE_DOWNLOAD_DELAY = True
```

---

## 5. Selectors (XPath vs CSS)

Scrapy prefers XPath because it's more powerful (can traverse UP the DOM).

```python
# CSS
response.css('div.product::text').get()

# XPath (Power User)
# "Find link containing text 'Next Page'"
response.xpath('//a[contains(text(), "Next Page")]/@href').get()
```
