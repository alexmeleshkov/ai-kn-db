# Background Task Manager with ThreadPoolExecutor

**Project**: [[db-chat-nl-master]]
**Category**: performance
**Author**: [[dima-efremov]]
**Date**: 2024-11-15

---

## Context

SQL queries can take unpredictable time (seconds to minutes depending on complexity). Running them synchronously would block the FastAPI event loop and freeze the server.

---

## Problem

- Long-running SQL queries block async web server
- Need timeout mechanism (kill queries that take too long)
- Need concurrent query execution (multiple users)
- Need graceful shutdown (don't kill queries mid-execution)

---

## Solution

Created TaskService using ThreadPoolExecutor for CPU-bound query execution:

**Implementation**:
```python
class TaskService:
    def __init__(self, max_workers: int = 5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit_query(self, query_func: callable, timeout_ms: int = 30000) -> dict:
        future = self.executor.submit(query_func)
        try:
            result = future.result(timeout=timeout_ms / 1000)
            return result
        except TimeoutError:
            raise TimeoutError(f"Query exceeded timeout of {timeout_ms}ms")

    def shutdown(self):
        self.executor.shutdown(wait=True)
```

**Key decisions**:
- ThreadPoolExecutor (not ProcessPoolExecutor) - queries are I/O-bound (waiting for DB)
- max_workers=5 - balance between concurrency and resource usage
- timeout_ms configurable - different queries need different timeouts
- TimeoutError raised (not silent failure) - caller decides how to handle

---

## Alternatives Considered

**Option A: asyncio with timeout**
- Problem: psycopg2 is synchronous (blocks event loop)
- Would need asyncpg (different API, migration cost)

**Option B: Celery task queue**
- Problem: Over-engineering (adds Redis dependency, complexity)
- Would make sense for >1000 concurrent users

**Option C: No timeout**
- Problem: Queries could hang forever
- Users would wait indefinitely with no feedback

---

## Trade-offs

**Benefits**:
- Simple (stdlib only, no external dependencies)
- Timeout prevents hung queries
- Concurrent execution (5 workers)
- Graceful shutdown (wait=True)

**Drawbacks**:
- Limited to 5 concurrent queries (acceptable for prototype)
- Thread overhead (small for I/O-bound tasks)
- No retry mechanism (queries fail permanently)
- No progress tracking (user doesn't know query status)

---

## Lessons Learned

- ThreadPoolExecutor is good for I/O-bound tasks in async frameworks
- Always implement timeouts for external operations (DB, API calls)
- max_workers should match expected concurrent load (not too high)
- Graceful shutdown prevents data corruption
- For production: consider Celery or async DB driver (asyncpg)
