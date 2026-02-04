# Custom Modules

This document contains project-specific implementation patterns that are not extracted as reusable features or technology patterns.

---

## Table of Contents

1. [Module Initializers](#module-initializers)
2. [Conversation Service](#conversation-service)
3. [Tasks Service](#tasks-service)
4. [Query Intelligence](#query-intelligence)
5. [Ipswich Examples](#ipswich-examples)

---

## Module Initializers

Several `__init__.py` files serve as module exports:

### backend/app/api/__init__.py
**Purpose**: Empty module initializer for API package

### backend/app/models/__init__.py
**Purpose**: Empty module initializer for models package

### backend/app/schemas/__init__.py
**Purpose**: Exports chat-related Pydantic models

**Exports**:
```python
__all__ = [
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "QueryResult",
    "ConversationHistory",
]
```

### backend/app/services/__init__.py
**Purpose**: Empty module initializer for services package

---

## Conversation Service

**File**: `backend/app/services/conversations.py`

**Purpose**: Wrapper service for conversation operations, delegates to AppDataService

**Interface**:
```python
class ConversationService:
    def __init__(self, app_data_service: AppDataService)
    def create_conversation(self, user_id: str, title: str = "New Chat") -> Optional[dict]
    def get_user_conversations(self, user_id: str) -> list[dict]
    def get_conversation(self, conversation_id: str, user_id: str) -> Optional[dict]
    def delete_conversation(self, conversation_id: str, user_id: str) -> bool
```

**Complete Flow**:
1. Initialize with AppDataService dependency
2. Delegate all operations to app_data_service
3. Provide conversation-focused API (wraps app_data methods)

**All Behaviors**:
- Thin wrapper around AppDataService
- User-scoped access via user_id parameter
- Returns dicts for JSON serialization
- No direct database access (delegates to app_data)

**Dependencies**:
- app_data.AppDataService - database operations

**Module Exports**:
```python
Module Exports (conversations.py):

1. ConversationService class
   - Wrapper service for conversation operations

Usage Pattern:
- conversation_service = ConversationService(app_data_service)
- conversations = conversation_service.get_user_conversations(user_id)
```

---

## Tasks Service

**File**: `backend/app/services/tasks.py`

**Purpose**: Background task manager using ThreadPoolExecutor for async SQL query execution with timeout

**Interface**:
```python
class TaskService:
    def __init__(self, max_workers: int = 5)
    def submit_query(self, query_func: callable, timeout_ms: int = 30000) -> dict
    def shutdown(self)
```

**Complete Flow**:
1. Initialize ThreadPoolExecutor with max_workers
2. submit_query(query_func, timeout_ms):
   - Submit function to thread pool
   - Wait for result with timeout (timeout_ms / 1000 seconds)
   - If timeout: raise TimeoutError
   - If success: return result
   - If exception: raise exception
3. shutdown(): gracefully stop executor (wait=True)

**All Behaviors**:
- Thread pool with configurable max_workers (default 5)
- Query execution with timeout (default 30s)
- Timeout raises TimeoutError (not silent failure)
- Graceful shutdown on app termination
- Concurrent query execution support

**Dependencies**:
- concurrent.futures.ThreadPoolExecutor - async execution
- concurrent.futures.TimeoutError - timeout handling

**Error Handling**:
- TimeoutError if query exceeds timeout_ms
- Exception propagated from query_func
- Logged but not swallowed

**Constants and Configuration**:
- DEFAULT_MAX_WORKERS = 5 - thread pool size
- DEFAULT_TIMEOUT_MS = 30000 - query timeout (30 seconds)

**Module Exports**:
```python
Module Exports (tasks.py):

1. TaskService class
   - Background task manager with thread pool

Usage Pattern:
- task_service = TaskService(max_workers=5)
- result = task_service.submit_query(lambda: db.execute_query(sql), timeout_ms=30000)
```

---

## Query Intelligence

**File**: `backend/app/services/query_intelligence.py`

**Purpose**: Query validation, LRU caching, and error analysis with contextual suggestions

**Interface**:
```python
class QueryValidator:
    @staticmethod
    def validate(sql_query: str) -> tuple[bool, str]
    @staticmethod
    def get_error_context(error: str, sql_query: str) -> str

class QueryCache:
    def __init__(self, max_size: int = 100)
    def get(self, question: str) -> Optional[dict]
    def set(self, question: str, result: dict) -> None
    def clear(self) -> None

class FewShotStore:
    def __init__(self)
    def add_example(self, question: str, sql: str, success: bool, usage_count: int = 1)
    def get_similar(self, question: str, max_examples: int = 3) -> list[dict]
```

**Complete Flow - QueryValidator.validate()**:
1. Convert SQL to uppercase for checking
2. Check for dangerous keywords: UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, INSERT
3. If found: return (False, "Query contains dangerous keyword: {keyword}")
4. If safe: return (True, "")

**Complete Flow - QueryValidator.get_error_context()**:
1. Analyze error message text
2. Match error patterns:
   - "syntax error" → suggest checking commas, quotes, keywords
   - "column" + "does not exist" → extract column name, suggest similar columns
   - "timeout" or "timed out" → suggest adding LIMIT, simplifying joins, using WHERE
   - "division by zero" → suggest checking for NULL/zero values
   - "ambiguous column" → suggest table aliases
3. Return contextual suggestion string

**Complete Flow - QueryCache**:
1. Initialize OrderedDict with max_size
2. get(key):
   - If exists: move to end (LRU), return value
   - If not exists: return None
3. set(key, value):
   - If key exists: update value, move to end
   - If full (len >= max_size): remove first item (least recently used)
   - Add new item at end
4. clear(): empty dict

**Complete Flow - FewShotStore**:
1. add_example(question, sql, success, usage_count):
   - Find if similar example exists (exact match)
   - If exists: increment usage_count
   - If new: add to store with usage_count=1
2. get_similar(question, max_examples):
   - Tokenize input question
   - For each stored example:
     - Calculate similarity score (token overlap + table name matching + usage boost)
   - Sort by score descending
   - Return top N examples

**All Behaviors**:
- Query safety validation (blocks destructive operations)
- Error pattern detection with regex
- Contextual error suggestions
- LRU cache with OrderedDict (O(1) access)
- Few-shot similarity matching with token overlap
- Usage tracking for popular queries

**Algorithm Details - Similarity Matching**:
```
Similarity Score Calculation:
1. Tokenize question: words = question.lower().split()
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

**Constants and Configuration**:
- MAX_CACHE_SIZE = 100 - LRU cache capacity
- DEFAULT_FEW_SHOT_EXAMPLES = 3 - number of similar examples to return

**Module Exports**:
```python
Module Exports (query_intelligence.py):

1. QueryValidator class (static methods)
   - validate(sql_query) -> (bool, str)
   - get_error_context(error, sql_query) -> str

2. QueryCache class
   - LRU cache for query results

3. FewShotStore class
   - Similarity-based example retrieval

Usage Pattern:
- is_valid, error_msg = QueryValidator.validate(sql)
- cache = QueryCache(max_size=100)
- result = cache.get(question)
- cache.set(question, result)
```

---

## Ipswich Examples

**File**: `backend/app/services/ipswich_examples.py`

**Purpose**: Pre-loaded few-shot examples and domain glossary for Ipswich Town FC fan data queries (T-SQL dialect)

**Interface**:
```python
IPSWICH_GLOSSARY: str  # 400+ line glossary
IPSWICH_FEW_SHOT_EXAMPLES: list[dict]  # 20+ examples

def get_ipswich_examples() -> list[dict]
def get_ipswich_glossary() -> str
```

**Complete Flow**:
1. Module loads at import time with constants
2. get_ipswich_examples() returns IPSWICH_FEW_SHOT_EXAMPLES list
3. get_ipswich_glossary() returns IPSWICH_GLOSSARY string
4. Used by LLM service to add context to system prompt

**All Behaviors**:
- Domain glossary explains Ipswich-specific terms (GA tickets, hospitality, ballots, etc.)
- Key table relationships documented (fan, ticket, access tables)
- Critical distinctions clarified (address_country vs GDPR country)
- Clarification patterns (when to ask user for clarification)
- Conversation context examples (remembering previous messages)
- T-SQL syntax examples (TOP N, [brackets], GETDATE(), CAST AS DATE)
- 20+ categorized examples: clarification, segmentation, attendance, conversion, demographics, etc.

**Template Strings**:
```
IPSWICH_GLOSSARY (400+ lines):
## Ipswich Town FC Domain Terms

- **GA tickets** = General Admission tickets
- **Hospitality** = Premium/VIP tickets
- **Ballot** = Ticket allocation lottery
- **Home tickets** = Tickets for home games
- **Away tickets** = Tickets for away games
- **Fan source** = How fan was acquired
- **Activity scale** = Engagement level
... (full glossary 400+ lines)

IPSWICH_FEW_SHOT_EXAMPLES (20+ examples):
[
  {
    "question": "How many fans went to the Coventry game?",
    "workflow": "STEP 1: Run discovery query...",
    "discovery_sql": "SELECT DISTINCT [access.product_opponent_name]...",
    "clarification_options": ["Home game on 2024-08-17", "Away game on 2025-01-01"],
    "final_sql": "SELECT COUNT(DISTINCT [access.fan_id])...",
    "explanation": "Attendance count for specific game",
    "category": "clarification_required"
  },
  ... (20+ examples)
]
```

**Constants and Configuration**:
- IPSWICH_GLOSSARY - 400+ line domain glossary
- IPSWICH_FEW_SHOT_EXAMPLES - 20+ SQL examples with workflows
- Categories: clarification_required, ticket_segmentation, attendance, first_timers, conversion, merchandise, demographics, data_quality, marketing, sales_curve, membership

**Module Exports**:
```python
Module Exports (ipswich_examples.py):

1. IPSWICH_GLOSSARY: str
   - Complete domain glossary

2. IPSWICH_FEW_SHOT_EXAMPLES: list[dict]
   - 20+ SQL examples with workflow instructions

3. get_ipswich_examples() -> list[dict]
4. get_ipswich_glossary() -> str

Usage Pattern:
- from .ipswich_examples import get_ipswich_examples, get_ipswich_glossary
- examples = get_ipswich_examples()  # For system prompt
- glossary = get_ipswich_glossary()  # For domain context
```

---

## Summary

This document contains 5 custom modules specific to the db-chat-nl-master project:

1. **Module Initializers** - Package exports
2. **Conversation Service** - Wrapper for conversation operations
3. **Tasks Service** - Thread pool for async SQL execution
4. **Query Intelligence** - Validation, caching, error analysis
5. **Ipswich Examples** - Domain-specific examples and glossary

These modules are not extracted as reusable patterns because they are either:
- Too simple (empty `__init__.py` files)
- Project-specific wrappers (ConversationService)
- Specialized utilities (TaskService, QueryIntelligence)
- Domain-specific data (Ipswich examples)
