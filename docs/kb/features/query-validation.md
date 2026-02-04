# Query Validation

**Feature ID**: query.validation
**Capability**: query-validation
**Technologies**: postgresql, react-hooks

---

## Overview

SQL query validation and error analysis with contextual suggestions, LRU caching, and query history tracking with localStorage persistence.

**Key characteristics**:
- Query safety validation (blocks dangerous operations)
- Error pattern detection with contextual suggestions
- LRU cache for query results (100-item capacity)
- Query history with deduplication (50-item limit)
- localStorage persistence for history

---

## File Structure

```
backend/app/
  services/
    query_intelligence.py  # Query validation and caching

frontend/src/
  hooks/
    useQueryHistory.ts     # Query history management
```

---

## Implementation Patterns

### 1. Query Validator (query_intelligence.py)

**Purpose**: Validates SQL queries before execution and provides error context

**Interface**:
```python
class QueryValidator:
    @staticmethod
    def validate(sql_query: str) -> tuple[bool, str]
    @staticmethod
    def get_error_context(error: str, sql_query: str) -> str
```

**Validation Rules**:
```python
- Block UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, INSERT (except SELECT)
- Allow SELECT queries only
- Return (False, "Query contains dangerous keyword: UPDATE") if blocked
- Return (True, "") if valid
```

**Error Context Generation**:
```
Error patterns:
- "syntax error" → "Check SQL syntax. Common issues: missing commas, unclosed quotes."
- "column" + "does not exist" → Extract column name, suggest similar columns (Levenshtein distance < 3)
- "timeout" or "timed out" → "Query too complex. Try: 1) Add LIMIT, 2) Simplify joins, 3) Use WHERE to filter"
- "division by zero" → "Check for NULL or zero values in denominator"
- "ambiguous column" → "Specify table alias for column"
```

---

### 2. Query Cache (query_intelligence.py)

**Purpose**: LRU cache for query results to avoid re-execution

**Interface**:
```python
class QueryCache:
    def __init__(self, max_size: int = 100)
    def get(self, question: str) -> Optional[dict]
    def set(self, question: str, result: dict) -> None
    def clear(self) -> None
```

**Algorithm**:
```
LRU Cache Implementation:
1. OrderedDict for O(1) access and LRU ordering
2. get(key): Move to end (most recently used), return value
3. set(key, value):
   - If exists: move to end
   - If full: remove first item (least recently used)
   - Add new item at end
4. max_size = 100 items
```

---

### 3. Query History Hook (useQueryHistory.ts)

**Purpose**: React hook managing query history with localStorage persistence

**Interface**:
```typescript
interface QueryHistoryItem {
  id: string;
  question: string;
  timestamp: string;
  successful: boolean;
}

export function useQueryHistory(): {
  history: QueryHistoryItem[];
  addToHistory: (question: string, successful: boolean) => void;
  removeFromHistory: (id: string) => void;
  clearHistory: () => void;
}
```

**Complete Flow**:
1. Initialize from localStorage (key: 'db-chat-query-history')
2. addToHistory(question, successful):
   - Check if question already exists (case-insensitive)
   - If exists: move to top, update timestamp
   - If new: add to top with UUID
   - Limit to 50 items (slice(0, 50))
   - Save to localStorage
3. removeFromHistory(id): filter out item, save
4. clearHistory(): set to [], save

**All Behaviors**:
- localStorage persistence (survives page reload)
- Deduplication (case-insensitive matching)
- Most recent first ordering
- 50-item limit
- Success/failure tracking
- Automatic save on every change via useEffect

**Error Handling**:
- localStorage.getItem failure: return empty array
- localStorage.setItem failure: log error, don't block
- JSON.parse failure: return empty array

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Query safety and history

---

## Related Technologies

- **[PostgreSQL](../technologies/postgresql.md)** - Query execution
- **[React Hooks](../technologies/react-hooks.md)** - Frontend state management
