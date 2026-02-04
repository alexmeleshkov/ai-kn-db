# Natural Language to SQL

**Feature ID**: natural-language.nl-to-sql
**Capability**: natural-language-sql
**Technologies**: anthropic-claude, postgresql, fastapi, react-hooks, sse

---

## Overview

AI-powered natural language to SQL conversion using Claude API with Tool Use pattern, extended thinking, streaming responses, and few-shot learning. Converts user questions into SQL queries with semantic understanding, error recovery, and clarification requests.

**Key characteristics**:
- Claude API streaming with extended thinking mode
- Tool Use pattern for SQL execution and clarification
- Few-shot learning with similarity-based example retrieval
- Error analysis with contextual suggestions
- Query validation before execution
- Heartbeat polling during long queries (prevents 55s Heroku timeout)
- Conversational memory with conversation_id persistence
- Server-Sent Events (SSE) for real-time streaming

---

## File Structure

```
backend/app/
  services/
    llm.py                  # Claude API integration with streaming
    chat.py                 # Chat orchestration service
    learning_store.py       # Few-shot example storage
    query_intelligence.py   # Query validation and error analysis

frontend/src/
  hooks/
    useChat.ts              # Chat state with streaming support
    useSuggestions.ts       # NL query suggestions
```

---

## Implementation Patterns

### 1. LLM Service (llm.py)

**Purpose**: Claude API service with streaming, extended thinking, tool use for SQL execution and clarification, heartbeat polling, and complete system prompt generation.

**Interface**:
```python
class LLMService:
    def __init__(self)
    def stream_nl_to_sql(
        self,
        question: str,
        schema: DatabaseSchema,
        db_service: Any,
        learning_store: LearningStore,
        conversation_history: list[dict] = None,
        max_iterations: int = 5
    ) -> Generator[dict, None, None]
    def _build_system_prompt(...) -> str
    def _build_messages(...) -> list[dict]
    def _handle_tool_use(...) -> dict
```

**Complete Flow**:
1. Build system prompt with schema, glossary, sample data, few-shot examples from learning_store
2. Configure extended thinking (full budget first iteration, 1/4 on retry to speed up)
3. Build messages list with conversation history and current question
4. Stream with anthropic.messages.stream() using claude-3-5-sonnet-20241022
5. For each streaming event:
   - thinking_start: Yield {"type": "thinking_start"}
   - content_block_delta (thinking): Yield {"type": "thinking", "content": delta.delta.thinking}
   - thinking_end: Yield {"type": "thinking_end"}
   - content_block_delta (text): Yield {"type": "text", "content": delta.delta.text}
   - content_block_stop: Process final message for tool use
6. Handle tool use:
   - execute_sql: Validate query, execute in thread pool with timeout, emit heartbeat every 15s, save to learning store on success
   - ask_clarification: Yield clarification request, wait for user selection
7. Recursively call with tool results if tool use occurred (up to max_iterations)
8. Yield {"type": "done", "conversation_id": ...}

**All Behaviors**:
- Extended thinking preview (streaming thought process to UI)
- Tool calls: execute_sql(query), ask_clarification(question, options)
- Heartbeat polling every 15s during SQL execution (prevents Heroku H15 error)
- Query timeout handling with user-friendly messages
- Error context from QueryValidator for failed queries
- Few-shot example selection by similarity matching
- System prompt includes: schema, glossary, sample data, examples, tool definitions
- Recursive tool use pattern (Claude can execute multiple queries)
- Conversation memory via conversation_id
- Token limit: max 4096 output tokens
- Temperature: 1.0 for creative SQL generation

**Dependencies**:
- anthropic - Claude API client for streaming
- concurrent.futures.ThreadPoolExecutor - async SQL execution
- time.sleep() - heartbeat polling during query execution

**Error Handling**:
- SQL timeout: "Query execution timed out. Try adding LIMIT or WHERE clause."
- SQL error: Get contextual suggestions from QueryValidator, include in tool_result
- API errors: Logged and yielded as error events
- Validation errors: Blocked queries (UPDATE, DELETE, DROP) return error without execution

**Template Strings**:
```
SYSTEM_PROMPT_TEMPLATE (1054 lines):
You are a SQL expert helping analyze data. Here is the database schema:
{schema}

Domain terminology:
{glossary}

Sample data:
{sample_data}

Similar past queries:
{few_shot_examples}

Your tools:
- execute_sql: Run SQL queries
- ask_clarification: Ask user for clarification when question is ambiguous

Critical instructions:
- Use tool execute_sql to run queries, not markdown code blocks
- Call ask_clarification if multiple possible interpretations exist
- Remember context from conversation history
```

**Constants and Configuration**:
- MAX_OUTPUT_TOKENS = 4096
- TEMPERATURE = 1.0
- EXTENDED_THINKING_BUDGET = 10000 tokens (first try), 2500 tokens (retry)
- HEARTBEAT_INTERVAL = 15 seconds (prevents Heroku 55s timeout)
- MAX_ITERATIONS = 5 (tool use recursion limit)

---

### 2. Chat Service (chat.py)

**Purpose**: Orchestrates NL-to-SQL conversation flow by integrating LLM service, database service, learning store, and SSE streaming.

**Interface**:
```python
class ChatService:
    def __init__(self, llm_service: LLMService, db_service: DatabaseService, learning_store: LearningStore)
    def stream_chat(
        self,
        question: str,
        conversation_history: list[dict] = None,
        conversation_id: str = None
    ) -> Generator[str, None, None]
```

**Complete Flow**:
1. Get schema from database service
2. Call llm_service.stream_nl_to_sql() with question, schema, db_service, learning_store, conversation_history
3. For each event from LLM service:
   - Format as SSE: "data: {json}\n\n"
   - Yield to client
4. On completion, persist conversation if needed

**All Behaviors**:
- SSE streaming (text/event-stream content type)
- Event types: thinking_start, thinking, thinking_end, text, tool_start, tool_result, done, error, heartbeat
- Conversation persistence via conversation_id
- Error propagation to client

---

### 3. Learning Store (learning_store.py)

**Purpose**: Persistent storage for successful SQL patterns with similarity matching, usage tracking, and error pattern detection.

**Interface**:
```python
class LearningStore:
    def __init__(self, database_id: str, database_type: str)
    def add_successful_query(question: str, sql_query: str, execution_time_ms: int, row_count: int)
    def get_similar_examples(question: str, max_examples: int = 3) -> list[dict]
    def get_error_patterns() -> list[str]
```

**Similarity Algorithm**:
```
1. Tokenize question: words = question.lower().split()
2. For each stored query:
   a. Tokenize stored question
   b. Calculate weighted overlap:
      - Common words: +1 point each
      - SQL keywords (select, where, count): +3 points each
      - Table names matched: +5 points each
   c. Add usage boost: score += log(usage_count + 1)
3. Sort by score descending
4. Return top N
```

---

### 4. Query Intelligence (query_intelligence.py)

**Purpose**: Query validation, caching, and error analysis with contextual suggestions.

**Interface**:
```python
class QueryValidator:
    def validate(sql_query: str) -> tuple[bool, str]
    def get_error_context(error: str, sql_query: str) -> str

class QueryCache:
    def __init__(max_size: int = 100)
    def get(question: str) -> Optional[dict]
    def set(question: str, result: dict)
```

**Error Patterns**:
```
- "syntax error" → "Check SQL syntax. Common issues: missing commas, unclosed quotes."
- "column does not exist" → Extract column name, find similar columns (Levenshtein < 3), suggest alternatives
- "timeout" → "Query too complex. Try: 1) Add LIMIT, 2) Simplify joins, 3) Use WHERE to filter"
- "division by zero" → "Check for NULL or zero values in denominator"
```

---

### 5. Frontend Chat Hook (useChat.ts)

**Purpose**: React hook managing chat state with SSE streaming, extended thinking preview, tool use tracking, and clarification handling.

**Interface**:
```typescript
interface UseChatResult {
  messages: ChatMessage[];
  streamingState: StreamingState;
  sendUserMessage: (content: string) => Promise<void>;
  selectClarificationOption: (option: string) => void;
  loadConversation: (id: string) => Promise<void>;
  // ... other methods
}

export function useChat(): UseChatResult
```

**Complete Flow**:
1. User calls sendUserMessage(content)
2. Add user message to messages array immediately (optimistic UI)
3. Connect to SSE endpoint: POST /chat with content and conversation_id
4. Process SSE events:
   - thinking_start: Set isThinking=true, show thinking indicator
   - thinking: Append to thinkingText, display in UI
   - text: Append to currentText, display streaming response
   - tool_start: Show "Executing SQL..." with query preview
   - tool_result: Show success/error, display results if available
   - clarification_needed: Show clarification UI with options
   - done: Add assistant message with full text and executed queries
5. Handle clarification: user selects option, call sendUserMessage with selection

**All Behaviors**:
- Real-time SSE streaming with progress indicators
- Extended thinking preview (shows AI reasoning)
- SQL query execution tracking (query text, status, results)
- Clarification UI (multiple-choice questions from AI)
- Elapsed time counter (updates every 100ms)
- Progress stages: connecting → thinking → generating_sql → executing_query → processing_results
- AbortController for stream cancellation
- Conversation memory (conversationId persisted)
- User-friendly error messages (timeout, network, connection)

---

### 6. Query Suggestions (useSuggestions.ts)

**Purpose**: Generate context-aware query suggestions based on schema, history, and user input.

**Interface**:
```typescript
export function useSuggestions(
  tables: TableSchema[],
  history: QueryHistoryItem[],
  input: string
): Suggestion[]
```

**Suggestion Algorithm**:
```
Empty input:
- "How many [table] are there?"
- "Show me all [table]"
- "What is the total [numeric_column]?"
- Top 3 recent history items

Non-empty input:
- Filter history items matching input
- Table name matches → count/show suggestions
- Column name matches → aggregation suggestions
- Keyword detection:
  * "how many" → count queries
  * "show"/"list" → select queries
  * "top"/"best" → top N queries
  * "count"/"group" → group by queries
```

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Main NL-to-SQL chat application

---

## Related Technologies

- **[Claude API](../technologies/anthropic-claude.md)** - AI model for NL understanding
- **[PostgreSQL](../technologies/postgresql.md)** - Database for query execution
- **[SSE](../technologies/sse.md)** - Real-time streaming
- **[FastAPI](../technologies/fastapi.md)** - Backend framework
- **[React Hooks](../technologies/react-hooks.md)** - Frontend state management

---

## Variants

### Variant 1: Claude Tool Use (Current Implementation)
- **When to use**: When you need SQL execution integrated into AI conversation flow
- **Trade-offs**:
  - ✅ Pros: Natural conversation, error recovery, clarification requests, recursive tool use
  - ❌ Cons: Token usage, API latency, requires careful prompt engineering

### Variant 2: Text-to-SQL Model (Alternative)
- **When to use**: When you need faster response or offline capability
- **Trade-offs**:
  - ✅ Pros: Lower latency, no API costs, predictable output
  - ❌ Cons: Less flexible, no conversation memory, limited error recovery
