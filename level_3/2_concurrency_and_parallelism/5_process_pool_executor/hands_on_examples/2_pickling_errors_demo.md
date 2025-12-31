# Hands-on: Pickling Errors (The Lambda Trap)

This script demonstrates the most common crash in `ProcessPool` usage: implementing unpicklable functions.

## The Scenario
We try to submit a `lambda` function to the pool. This works in `ThreadPool` but crashes in `ProcessPool`.

## Code

```python
from concurrent.futures import ProcessPoolExecutor
import logging

# Configure logger to see internal errors if possible
logging.basicConfig(level=logging.ERROR)

def good_function(x):
    return x * 2

def run_bad_example():
    print("\n--- Attempting Lambda (Will Fail) ---")
    try:
        with ProcessPoolExecutor() as executor:
            # ERROR: Lambdas are not picklable!
            results = executor.map(lambda x: x * 2, [1, 2, 3])
            print(list(results))
    except Exception as e:
        print(f"Caught Expected Error: {e}")

def run_good_example():
    print("\n--- Attempting Top-Level Function (Will Work) ---")
    with ProcessPoolExecutor() as executor:
        results = executor.map(good_function, [1, 2, 3])
        print(f"Success: {list(results)}")

if __name__ == "__main__":
    # Note: On Windows/Mac, the error might appear in the *worker* process 
    # and re-raised in the parent.
    try:
        run_bad_example()
    except Exception as e:
        print(f"Main caught: {e}")
        
    run_good_example()
```

## Key Takeaways
1.  **AttributeError/PickleError**: You will typically see `"Can't pickle <function <lambda> ...>"`.
2.  **Top-Level Requirement**: Always define worker functions at the module level, not nested inside `main()` or other functions.
