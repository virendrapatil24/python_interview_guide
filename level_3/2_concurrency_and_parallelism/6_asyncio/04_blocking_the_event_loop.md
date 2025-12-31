# Blocking the Event Loop (The Cardinal Sin)

The #1 mistake in Asyncio applications is blocking the loop. Because there is only one thread, if you block it, your entire server allows zero new connections and processes zero responses.

## 1. What Blocks the Loop?
Anything that does not `await` and takes time.

### A. Synchronous I/O
*   `requests.get(...)`
*   `time.sleep(1)`
*   `open(file).read()` (for large files)
*   Standard DB drivers (`psycopg2` without async extension).

### B. Heavy CPU Computation
*   `sum(range(10_000_000))`
*   Image processing
*   Machine Learning model inference
*   Parsing massive JSON/XML files

## 2. How to Detect Blocking?
Enable Debug Mode: `asyncio.run(main(), debug=True)`.
*   The loop measures the duration of every callback.
*   If a callback takes > 100ms, it logs:
    > `Executing <Task...> took 0.150 seconds`

## 3. How to Fix Blocking?

### Method A: Use Async Libraries
Replace blocking libraries with native async ones.
*   `requests` -> `aiohttp` / `httpx`
*   `time.sleep` -> `asyncio.sleep`
*   `psycopg2` -> `asyncpg`

### Method B: Offload to Threads/Processes (`run_in_executor`)
If you CANNOT avoid synchronous code (e.g., legacy library or CPU task), you must run it in a separate thread/process so the Loop thread isn't blocked.

```python
loop = asyncio.get_running_loop()

# For I/O Bound (Reading file, requests)
result = await loop.run_in_executor(None, blocking_func) 

# For CPU Bound (Math, Dataframes)
with ProcessPoolExecutor() as pool:
    result = await loop.run_in_executor(pool, heavy_math_func)
```
This effectively turns a blocking function into an awaitable Future.
