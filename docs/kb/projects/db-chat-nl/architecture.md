# Architecture

## System Design

### Architecture Pattern

**Layered 3-Tier Architecture**

```
┌─────────────────────────────────────────────────────────┐
│  Frontend Layer (React + TypeScript)                    │
│  - Chat UI, Auth UI, Schema Viewer, Admin Panel        │
│  - SSE client for streaming responses                   │
│  - Local state (useChat, useAuth hooks)                │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/SSE
                   │ (JSON, Server-Sent Events)
┌──────────────────▼──────────────────────────────────────┐
│  API Layer (FastAPI)                                     │
│  - REST endpoints: /chat, /auth, /conversations         │
│  - Streaming endpoint: /chat/stream (SSE)               │
│  - Dependency injection for services                    │
│  - JWT authentication middleware                         │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  Service Layer (Business Logic)                         │
│  - LLMService: Claude API with Tool Use                │
│  - DatabaseService: DuckDB, PostgreSQL, Azure SQL       │
│  - AuthService: JWT tokens, password hashing           │
│  - AppDataService: Conversation persistence             │
│  - QueryIntelligence: Caching, few-shot learning       │
└─────────────────────────────────────────────────────────┘
```

**Evidence**: main.py:1-180 (FastAPI app initialization), App.tsx:1-200 (React router), services/ directory structure

---

## Core Architectural Decisions

### 1. Agentic Tool Use Pattern

**Decision**: Use Claude's Tool Use API to give the AI autonomous control over SQL execution and retry logic.

**Rationale**:
- Claude can execute queries, see errors, and fix them automatically (self-healing)
- Reduces prompt complexity - no need to engineer SQL extraction from text
- Handles edge cases (syntax errors, typos) without custom error handlers
- Supports multi-step workflows (discovery query -> clarification -> final query)

**Implementation**:
```python
SQL_TOOLS = [
    {
        "name": "execute_sql",
        "description": "Execute a SQL query against the database and return results",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "reasoning": {"type": "string"}
            }
        }
    },
    {
        "name": "ask_clarification",
        "description": "Ask the user to clarify when multiple matches exist",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
]
```

**Evidence**: llm.py:97-139 (tool definitions), llm.py:707-1054 (agentic streaming loop with auto-retry)

---

### 2. Server-Sent Events (SSE) for Streaming

**Decision**: Use SSE instead of WebSockets for real-time AI response streaming.

**Rationale**:
- Simpler protocol than WebSockets (HTTP-based, no handshake)
- One-way communication sufficient (server → client)
- Better compatibility with proxies and load balancers
- Automatic reconnection in browsers
- Works with standard HTTP infrastructure

**Implementation**:
```python
def generate_events():
    for event in llm_service.process_with_tools_streaming(...):
        yield f"data: {json.dumps(event)}\n\n"

return StreamingResponse(
    generate_events(),
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"
    }
)
```

**Frontend handling**:
```typescript
const eventSource = new EventSource(url);
eventSource.onmessage = (e) => {
  const event = JSON.parse(e.data);
  handleStreamEvent(event);
};
```

**Evidence**: routes.py:93-218 (SSE endpoint), api.ts:120-200 (SSE client), useChat.ts:90-326 (event handling)

---

### 3. Multi-Database Abstraction

**Decision**: Abstract base class `BaseDatabaseService` with concrete implementations for DuckDB, PostgreSQL, Azure SQL.

**Rationale**:
- Single interface for LLM service regardless of database type
- Swap databases without changing API layer
- Database-specific optimizations in each implementation (e.g., LIMIT vs TOP)
- Easier testing with mock implementations

**Interface**:
```python
class BaseDatabaseService(ABC):
    @abstractmethod
    def get_schema(self, refresh: bool = False) -> DatabaseSchema:
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> QueryResult:
        pass

    @property
    @abstractmethod
    def db_type(self) -> str:
        pass
```

**Implementations**:
- `DatabaseService` - DuckDB for JSON files
- `PostgresDatabaseService` - PostgreSQL/RDS
- `AzureSQLDatabaseService` - Azure SQL Server with SOCKS proxy support

**Evidence**: database_base.py:13-80 (abstract base), database.py:52-708 (DuckDB impl), database_pg.py:35-311 (PostgreSQL impl), database_azure.py:40-418 (Azure impl)

---

### 4. Conversation Dual Storage

**Decision**: Store conversations in both PostgreSQL (persistent) and in-memory (LLM context).

**Rationale**:
- **PostgreSQL**: Long-term storage, user authentication required, survives restarts
- **In-memory**: Fast access for LLM context, works without auth, suitable for guest users
- Graceful degradation: If PostgreSQL unavailable, in-memory store continues working

**Flow**:
```
User sends message
  ↓
IF authenticated:
  ├─ Save to PostgreSQL (AppDataService)
  └─ Get conversation_id from PostgreSQL
ENDIF
  ↓
Save to in-memory store (ConversationStore)
  ↓
Get recent history from in-memory for LLM context
  ↓
After AI response:
  ├─ Save to PostgreSQL (if authenticated)
  └─ Save to in-memory store
```

**Evidence**: routes.py:112-144 (dual storage logic), conversations.py:82-139 (in-memory store), app_data.py:50-230 (PostgreSQL storage)

---

### 5. Query Intelligence System

**Decision**: Implement progressive intelligence with caching, few-shot learning, and error pattern detection.

**Components**:

#### a) Query Cache (LRU)
- Cache recent query results by question + schema hash
- Instant responses for repeated questions
- LRU eviction prevents memory bloat

#### b) Few-Shot Learning Store
- Database-specific example storage (e.g., Ipswich Town FC queries)
- Learned queries from successful executions
- Weighted similarity matching for context injection

#### c) Query Validator
- Pre-execution schema validation (table/column existence)
- Error context generation for better AI retries
- Detects typos and suggests alternatives

**Evidence**: query_intelligence.py:32-444 (QueryCache, FewShotStore, QueryValidator), learning_store.py:22-447 (persistent learning), ipswich_examples.py:17-411 (domain-specific glossary)

---

## Data Flow

### Chat Message Flow

```
1. User types question → ChatInput.tsx

2. Frontend (useChat hook):
   - Add user message to local state
   - Initialize SSE connection to /chat/stream
   - Set streaming state (progress indicators)

3. Backend (/chat/stream endpoint):
   - Authenticate user (optional, JWT from header)
   - Create/retrieve PostgreSQL conversation
   - Save user message to PostgreSQL
   - Get in-memory conversation for LLM history

4. LLMService (streaming):
   - Build system prompt with schema + few-shot examples
   - Call Claude API with Tool Use (streaming)
   - FOR EACH event from Claude:
     ├─ Extended Thinking → yield thinking event
     ├─ Text chunk → yield text event
     ├─ Tool Use (execute_sql):
     │   ├─ Validate query (syntax, schema)
     │   ├─ Execute SQL (with heartbeat for long queries)
     │   ├─ IF error → yield error, let Claude retry
     │   └─ IF success → yield result, continue
     └─ Done → yield final event with conversation_id

5. Frontend (SSE event handler):
   - thinking_start → show "Thinking deeply..."
   - thinking → append to thinking text
   - text → append to currentText
   - tool_start → show "Executing query..."
   - tool_result → track executed queries
   - clarification_needed → show option buttons
   - done → add assistant message, save queries

6. Persistence:
   - Save assistant message to PostgreSQL
   - Save to in-memory conversation
   - Learn successful query (FewShotStore)
```

**Evidence**: ChatContainer.tsx:88-353 (frontend flow), useChat.ts:91-326 (SSE handling), routes.py:93-218 (backend SSE), llm.py:707-1054 (streaming loop)

---

## Security Architecture

### Authentication Flow

```
1. User registers/logs in → /auth/register or /auth/login
   ↓
2. AuthService:
   - Hash password with bcrypt (12 rounds, auto-salted)
   - Store user in PostgreSQL (app_users table)
   - Generate JWT token (HS256, 7-day expiration)
   ↓
3. Return JWT to frontend
   ↓
4. Frontend stores JWT in localStorage
   ↓
5. All API requests include header:
   Authorization: Bearer <jwt>
   ↓
6. Backend verifies JWT on protected routes:
   - Extract token from header
   - Decode and validate signature
   - Check expiration timestamp
   - Return user payload (id, email, is_admin)
```

**Protected Routes**:
- `/conversations/*` - User's own conversations only
- `/admin/*` - Admin users only (is_admin=true check)

**Evidence**: auth.py:27-246 (JWT generation/verification), auth_routes.py:48-77 (get_current_user dependency), admin_routes.py:25-46 (require_admin)

---

## Deployment Architecture

### Docker Compose Setup

```yaml
services:
  backend:
    - FastAPI app on port 8000
    - Health check: /api/v1/health
    - Environment: .env file injection
    - Restart policy: unless-stopped

  frontend:
    - Vite build → nginx on port 80
    - Depends on backend (waits for startup)
    - Proxy API requests to backend:8000
```

**Production Deployment** (Heroku):
- Backend: Gunicorn + Uvicorn workers
- Frontend: Static build served by backend
- PostgreSQL: Heroku Postgres add-on
- Environment variables via Heroku config vars

**Evidence**: docker-compose.yml:1-34, backend/Dockerfile, frontend/Dockerfile, frontend/nginx.conf

---

## Error Handling

### Multi-Layer Error Strategy

**Layer 1: Frontend Validation**
- Input sanitization (XSS prevention)
- Empty message rejection
- Maximum length enforcement (2000 chars)

**Layer 2: API Validation**
- Pydantic schema validation
- JWT authentication check
- Rate limiting (future enhancement)

**Layer 3: Service Layer**
- SQL query validation (SELECT only)
- Dangerous keyword detection
- Schema validation (table/column existence)

**Layer 4: Agentic Retry**
- Claude sees SQL errors and retries automatically
- Error context includes schema and suggestions
- Maximum 15 iterations per question

**Layer 5: User-Friendly Messages**
- Timeout errors → "Try a more specific question"
- Network errors → "Connection interrupted, please retry"
- Generic errors → Detailed error message with retry button

**Evidence**: schemas/chat.py:98-131 (request validation), database_base.py:55-79 (query validation), llm.py:707-1054 (agentic retry loop), useChat.ts:269-326 (error handling)

---

## Scalability Considerations

### Current Architecture

- **Single-process**: One FastAPI worker (Heroku free tier)
- **In-memory conversation store**: Lost on restart
- **No caching layer**: Direct database queries

### Future Enhancements

1. **Horizontal Scaling**:
   - Add Redis for conversation store
   - Session-based routing or sticky sessions

2. **Database Optimization**:
   - Read replicas for heavy query load
   - Connection pooling (already implemented)
   - Query result caching in Redis

3. **AI Performance**:
   - Parallel query execution for independent queries
   - Prompt caching (Claude API feature)
   - Response streaming with backpressure handling

**Evidence**: conversations.py:82-139 (in-memory store with LRU eviction), query_intelligence.py:32-66 (query cache ready for Redis backend)

---

## Key Patterns

### 1. Dependency Injection (FastAPI)
Services injected via `app.state` and `Depends()` for testability.

### 2. Observer Pattern (SSE Streaming)
Frontend subscribes to SSE events, reacts to each event type.

### 3. Strategy Pattern (Database Abstraction)
Swap database implementations without changing service interface.

### 4. Repository Pattern (AppDataService)
Abstract database operations for conversations, messages, users.

### 5. Template Method (BaseDatabaseService)
Define common query validation, let subclasses implement execute_query.

**Evidence**: Throughout codebase - main.py:60-120 (DI setup), database_base.py (Strategy + Template), app_data.py (Repository), routes.py:93-218 (Observer)
