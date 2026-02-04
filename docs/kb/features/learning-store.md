# Learning Store

**Feature ID**: learning.store
**Capability**: learning-store
**Technologies**: postgresql

---

## Overview

Persistent storage for learned SQL query patterns with similarity matching for few-shot learning, usage tracking, and error pattern detection.

**Key characteristics**:
- PostgreSQL-backed storage via AppDataService
- Similarity matching using token overlap and table name matching
- Usage tracking with increment counter
- Error pattern extraction and storage
- Automatic cleanup (maintains max 100 records per database)

---

## File Structure

```
backend/app/
  services/
    learning_store.py      # Learning storage and retrieval
    app_data.py            # PostgreSQL CRUD for learned queries
```

---

## Implementation Patterns

### 1. Learning Store (learning_store.py)

**Purpose**: Manages learned query patterns with similarity-based retrieval

**Interface**:
```python
class LearningStore:
    def __init__(self, database_id: str, database_type: str)
    def add_successful_query(question: str, sql_query: str, execution_time_ms: int, row_count: int)
    def add_failed_pattern(sql_query: str, error: str)
    def get_similar_examples(question: str, max_examples: int = 3) -> list[dict]
    def get_error_patterns() -> list[str]
```

**Similarity Matching Algorithm**:
```
1. Tokenize input question: words = question.lower().split()
2. For each stored query:
   a. Tokenize stored question
   b. Calculate weighted overlap:
      - Common words: +1 point each
      - SQL keywords (select, where, count, group, order): +3 points each
      - Table names matched: +5 points each
   c. Add usage boost: score += log(usage_count + 1)
3. Sort by score descending
4. Return top N (default 3)
```

**Complete Flow - add_successful_query()**:
1. Check if similar query exists via _find_similar_query()
2. If exists and exact match: increment usage counter
3. If new: save to PostgreSQL via app_data.save_learned_query()
4. Trigger cleanup if needed (keep max 100 records)

**Complete Flow - get_similar_examples()**:
1. Load queries from RDS via app_data.get_learned_queries()
2. Apply similarity matching algorithm
3. Return top 3 most similar queries with:
   - question (original user question)
   - sql_query (successful SQL)
   - usage_count (how many times used)
   - execution_time_ms (performance indicator)

**All Behaviors**:
- Deduplication (exact matches increment usage)
- Similarity-based retrieval (not exact match)
- Usage tracking for popularity boost
- Automatic cleanup (max 100 records per database)
- Error pattern extraction (regex-based)
- Success-only retrieval for examples (errors stored separately)

---

### 2. App Data Service - Learned Queries (app_data.py)

**Purpose**: PostgreSQL CRUD operations for learned queries

**Interface**:
```python
def save_learned_query(
    database_id: str,
    database_type: str,
    question: str,
    sql_query: str,
    success: bool = True,
    execution_time_ms: int = None,
    row_count: int = None,
    error_pattern: str = None
) -> Optional[dict]

def get_learned_queries(database_id: str, success_only: bool = True, limit: int = 100) -> list[dict]

def increment_query_usage(query_id: str) -> bool

def clear_learned_queries(database_id: str) -> int
```

**SQL Queries**:
```sql
-- Save learned query
INSERT INTO learned_queries (database_id, database_type, question, sql_query, success, execution_time_ms, row_count, error_pattern, usage_count)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
RETURNING *

-- Get learned queries
SELECT * FROM learned_queries
WHERE database_id = %s AND success = %s
ORDER BY usage_count DESC, created_at DESC
LIMIT %s

-- Increment usage
UPDATE learned_queries SET usage_count = usage_count + 1 WHERE id = %s

-- Cleanup old queries
DELETE FROM learned_queries
WHERE id IN (
  SELECT id FROM learned_queries
  WHERE database_id = %s
  ORDER BY usage_count DESC, created_at DESC
  OFFSET %s
)
```

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Few-shot learning for NL-to-SQL

---

## Related Technologies

- **[PostgreSQL](../technologies/postgresql.md)** - Persistent storage
