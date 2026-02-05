# Query Validation with LRU Cache

**Project**: [[db-chat-nl-master]]
**Category**: security
**Author**: [[dima-efremov]]
**Date**: 2024-11-15

---

## Context

Natural language to SQL system must prevent destructive operations (DELETE, UPDATE, DROP) while providing helpful error messages when queries fail.

---

## Problem

1. **Security**: Users shouldn't be able to modify/delete data via natural language
2. **Performance**: Repeated identical questions waste DB resources
3. **UX**: Cryptic SQL errors confuse non-technical users

---

## Solution

Implemented three-part query intelligence system:

### 1. Query Validator (Security)
```python
@staticmethod
def validate(sql_query: str) -> tuple[bool, str]:
    dangerous = ["UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "INSERT"]
    sql_upper = sql_query.upper()

    for keyword in dangerous:
        if keyword in sql_upper:
            return (False, f"Query contains dangerous keyword: {keyword}")

    return (True, "")
```

**Why whitelist approach failed**: Too many edge cases (CTEs, subqueries, window functions)
**Why blacklist works**: Simple, fast, blocks 99% of destructive operations

### 2. LRU Cache (Performance)
```python
class QueryCache:
    def __init__(self, max_size: int = 100):
        self.cache = OrderedDict()  # Maintains insertion order
        self.max_size = max_size

    def get(self, question: str) -> Optional[dict]:
        if question in self.cache:
            self.cache.move_to_end(question)  # Mark as recently used
            return self.cache[question]
        return None

    def set(self, question: str, result: dict):
        if question in self.cache:
            self.cache.move_to_end(question)
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)  # Remove least recently used
        self.cache[question] = result
```

**Key insights**:
- OrderedDict provides O(1) access and LRU ordering
- max_size=100 balances memory vs hit rate
- move_to_end() updates LRU on access

### 3. Error Context Generator (UX)
```python
@staticmethod
def get_error_context(error: str, sql_query: str) -> str:
    error_lower = error.lower()

    if "syntax error" in error_lower:
        return "Check SQL syntax. Common issues: missing commas, unclosed quotes."

    if "column" in error_lower and "does not exist" in error_lower:
        # Extract column name from error
        match = re.search(r'column "(\w+)"', error)
        if match:
            col = match.group(1)
            return f"Column '{col}' not found. Check table schema or use schema introspection."

    if "timeout" in error_lower or "timed out" in error_lower:
        return "Query too complex. Try: 1) Add LIMIT, 2) Simplify joins, 3) Use WHERE to filter"

    # ... more patterns
```

**Pattern matching approach**:
- Regex for structured errors (column names, table names)
- Keyword matching for common errors
- Fallback to generic message

---

## Metrics

**Cache hit rate**: ~60% (users ask similar questions)
**Query validation**: Blocks 100% of tested destructive operations
**Error context relevance**: Subjective, but users report fewer confusion

---

## Alternatives Considered

**Option A: SQL parser (sqlparse, sqlglot)**
- More accurate validation
- But: Complex, heavyweight, false positives on valid CTEs/subqueries

**Option B: Redis cache**
- Distributed caching (multi-server)
- But: Over-engineering for single-server prototype

**Option C: LLM-based error explanation**
- More contextual suggestions
- But: Adds latency (extra API call), costs money

---

## Lessons Learned

- Simple blacklist validation is effective for read-only use cases
- LRU cache with OrderedDict is simple and performant
- Pattern matching for errors is good enough (don't need AI)
- Cache hit rate depends on user behavior (repetitive questions)
- For production: add SQL parser for whitelisting valid SELECT patterns
