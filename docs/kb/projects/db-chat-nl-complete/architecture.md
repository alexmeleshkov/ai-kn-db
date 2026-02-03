# Architecture

> **Purpose**: Document WHY behind architectural choices and system design.
> Focus on decisions that inform structural patterns during generation.

## Architecture Pattern

**Pattern**: Layered Monolith

**Why chosen**:
- Clear separation of concerns (API → Services → Data)
- Simple deployment model (single application)
- Easy to reason about and debug
- No network overhead between layers
- Good fit for team size and complexity

**Trade-offs**:
- ✅ Simple to develop and deploy
- ✅ Low latency (in-process calls)
- ✅ Easy debugging with single codebase
- ✅ Straightforward transaction management
- ⚠️ Single point of failure (entire app goes down)
- ⚠️ Scaling requires scaling entire app
- ⚠️ Technology lock-in (Python/FastAPI)

---

## System Components

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                    (React + TypeScript)                      │
│              Login | Chat | History | Schema View            │
└────────────────────────────┬────────────────────────────────┘
                             | HTTPS + SSE
┌────────────────────────────▼────────────────────────────────┐
│                         Backend                              │
│                    (FastAPI + Python)                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  API Layer   │  │   Services   │  │   Models         │   │
│  │  (Routes)    │→ │   (Logic)    │→ │   (Schemas)      │   │
│  └──────────────┘  └──────┬───────┘  └──────────────────┘   │
│                            |                                 │
└────────────────────────────┼─────────────────────────────────┘
                             |
      ┌──────────────────────┼──────────────────────┐
      |                      |                      |
┌─────▼─────┐    ┌───────────▼─────┐    ┌──────────▼────────┐
│Azure SQL  │    │  AWS RDS         │    │  Claude API       │
│Server     │    │ PostgreSQL       │    │  (Opus 4)         │
│(Fan Data) │    │ (Auth+Chats)     │    │  + Thinking       │
└───────────┘    └──────────────────┘    └───────────────────┘
```

---

### Component 1: Frontend (React SPA)

**Responsibility**: User interface for chat, authentication, and data visualization

**Key subsystems**:
- **Components** (`src/components/`): UI building blocks (chat, auth, data display)
- **Hooks** (`src/hooks/`): State management and API integration
- **Services** (`src/services/`): API client for backend communication

**Technologies**: React 18, TypeScript, Vite, Chart.js

---

### Component 2: Backend (FastAPI Application)

**Responsibility**: API server orchestrating business logic, authentication, and database access

**Key layers**:
1. **API Routes** (`app/api/`): HTTP endpoints for REST and SSE streaming
2. **Services** (`app/services/`): Business logic (auth, chat, database, LLM)
3. **Models & Schemas** (`app/models/`, `app/schemas/`): Data structures and validation
4. **Core** (`app/core/`): Configuration and logging

---

### Component 3: Data Layer

**Responsibility**: Persistent storage for user data, conversations, and query database

**Design approach**: Multi-database architecture

**Key entities**:
- **app_users** (PostgreSQL): id, email, password_hash, is_admin, created_at, last_login_at
- **conversations** (PostgreSQL): id, user_id, title, created_at, updated_at
- **messages** (PostgreSQL): id, conversation_id, role, content, metadata, created_at
- **learned_queries** (PostgreSQL): id, database_id, question, sql_query, success, usage_count, last_used_at
- **Fan Data** (Azure SQL or DuckDB): Variable schema based on loaded database

---

## Communication Patterns

### Frontend ↔ Backend

**Protocol**: HTTPS + SSE (Server-Sent Events)

**Patterns**:
1. **REST API**: Standard CRUD for conversations, users, database metadata
   - GET /api/v1/conversations (list user's chats)
   - POST /api/v1/auth/login (authenticate)
   - GET /api/v1/database/schema (schema introspection)
2. **SSE Streaming**: Real-time chat responses
   - POST /api/v1/chat/stream (send message, receive streamed response)
   - Event types: thinking, text, tool_start, tool_result, done, error
3. **Authentication**: JWT Bearer token in Authorization header
   - Token obtained from /auth/login
   - Included in all authenticated requests

**Why this approach**:
- REST for CRUD operations (simple, stateless)
- SSE for streaming (low latency, real-time updates, simpler than WebSockets)
- JWT for stateless authentication (scales horizontally, no session storage)

---

### Backend ↔ Databases

**Protocol**: Native database protocols (PostgreSQL wire, TDS, DuckDB in-process)

**Patterns**:
- **Connection Pooling**: psycopg2.pool.SimpleConnectionPool for PostgreSQL
- **Parameterized Queries**: All user input uses %s placeholders (SQL injection prevention)
- **Transaction Management**: Explicit commit/rollback for data consistency
- **Schema Caching**: Fetch once, refresh on demand

---

### Backend ↔ Claude API

**Protocol**: HTTPS with anthropic SDK

**Patterns**:
- **Streaming**: Async generator yields events as they arrive
- **Tool Use**: Claude calls execute_sql and ask_clarification tools autonomously
- **Extended Thinking**: Budget configured for complex reasoning
- **Retry Logic**: Quarter thinking budget on second attempt

---

## Data Architecture

### app_users (PostgreSQL)

```sql
CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);
```

### conversations (PostgreSQL)

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id),
    title VARCHAR(500) DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### messages (PostgreSQL)

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### learned_queries (PostgreSQL)

```sql
CREATE TABLE learned_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    database_id VARCHAR(255) NOT NULL,
    database_type VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    execution_time_ms INTEGER,
    row_count INTEGER,
    error_pattern TEXT,
    usage_count INTEGER DEFAULT 1,
    last_used_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes**:
- `idx_conversations_user_updated` on (user_id, updated_at DESC) - Fast user conversation listing
- `idx_messages_conversation_created` on (conversation_id, created_at ASC) - Fast message retrieval
- `idx_learned_queries_db_usage` on (database_id, usage_count DESC, last_used_at DESC) - Fast similarity matching

---

### Data Flow: Chat Message

1. **User sends message**: Frontend POST to /api/v1/chat/stream with message and conversation_id
2. **Authentication**: Backend verifies JWT token, extracts user_id
3. **Persistence**: Save user message to PostgreSQL (conversations + messages tables)
4. **In-Memory Context**: Load last 10 messages from conversation_store for LLM context
5. **Schema Introspection**: Fetch database schema and 3 sample rows per table
6. **LLM Processing**: Stream to Claude with schema, samples, conversation history
7. **Tool Execution**: Claude calls execute_sql tool, backend executes query on target database
8. **Result Streaming**: Stream thinking, text, tool results as SSE events to frontend
9. **Persistence**: Save assistant response to PostgreSQL
10. **Frontend Display**: EventSource receives events, updates UI incrementally

---

## API Design

### REST API Convention

**Endpoint structure**: `/api/v1/<resource>/<action>`

**Response format** (success):
```json
{
  "data": { ... },
  "success": true
}
```

**Error format**:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

**SSE Event format**:
```
data: {"type": "text", "content": "Response text"}

data: {"type": "tool_result", "tool_name": "execute_sql", "result": {...}}

data: {"type": "done"}

```

---

### Key Flow: User Authentication

1. **POST /api/v1/auth/register**: Email + password → bcrypt hash → save to app_users → create JWT → return user + token
   - Input: `{"email": "user@example.com", "password": "secret"}`
   - Output: `{"user": {"id": "...", "email": "..."}, "access_token": "eyJ..."}`
2. **POST /api/v1/auth/login**: Email + password → lookup user → verify bcrypt → update last_login_at → create JWT → return user + token
   - Input: `{"email": "user@example.com", "password": "secret"}`
   - Output: `{"user": {"id": "...", "email": "...", "is_admin": false}, "access_token": "eyJ..."}`
3. **GET /api/v1/auth/me** (with Bearer token): Verify JWT → return user info
   - Header: `Authorization: Bearer eyJ...`
   - Output: `{"id": "...", "email": "...", "is_admin": false}`

---

## Design Decisions

### Decision 1: SSE over WebSockets

**Context**: Need real-time streaming for chat responses without polling

**Options considered**:
1. WebSockets (bidirectional, persistent connection)
2. Server-Sent Events (unidirectional, HTTP-based)
3. Long polling (HTTP-based, simple but inefficient)

**Choice**: Server-Sent Events (SSE)

**Rationale**:
- Simpler than WebSockets (HTTP-based, no special handshake)
- Built-in reconnection handling in EventSource API
- Sufficient for unidirectional streaming (backend → frontend)
- Better firewall/proxy compatibility than WebSockets
- Native browser support without libraries

**Implications**:
- ✅ Simpler implementation and debugging
- ✅ Works through corporate proxies
- ⚠️ Unidirectional only (no client → server streaming)

---

### Decision 2: Dual Conversation Storage (In-Memory + PostgreSQL)

**Context**: Need fast LLM context access but also persistent history

**Options considered**:
1. PostgreSQL only (persistent but slow for LLM context)
2. In-memory only (fast but lost on restart)
3. Dual storage (in-memory + PostgreSQL)

**Choice**: Dual storage with in-memory for LLM context, PostgreSQL for persistence

**Rationale**:
- In-memory provides instant access for LLM prompts (no database roundtrip)
- PostgreSQL ensures history survives restarts
- In-memory has LRU eviction (max 100 conversations, max 50 messages each)
- PostgreSQL saves after each message (authenticated users only)

**Implications**:
- ✅ Fast LLM context retrieval
- ✅ Persistent history across restarts
- ⚠️ Complexity of maintaining two stores
- ⚠️ Memory usage for 100 conversations

---

### Decision 3: Multi-Database Support via Abstract Base Class

**Context**: Need to support PostgreSQL, Azure SQL, and DuckDB with different connectors

**Options considered**:
1. Single database class with if/else branches
2. Abstract base class with concrete implementations
3. Separate services with no shared interface

**Choice**: Abstract base class (BaseDatabaseService) with concrete implementations

**Rationale**:
- Polymorphism allows LLM service to work with any database
- Each implementation handles dialect-specific logic (T-SQL vs PostgreSQL)
- Shared validation logic in base class (query safety)
- Easy to add new database types

**Implications**:
- ✅ Clean separation of concerns
- ✅ Reusable LLM/chat logic
- ⚠️ More files to maintain

---

## Quality Attributes

### Modularity
**Rating**: High
**Evidence**: Clear layer separation, dependency injection, abstract interfaces for databases

### Testability
**Rating**: Medium
**Evidence**: Services use dependency injection (can mock), but some global state (conversation_store singleton)

### Performance
**Rating**: Medium-High
**Expected**: Sub-second for simple queries, 5-10s for complex queries with extended thinking

### Security
**Rating**: Medium
**Measures**: JWT auth, bcrypt hashing, parameterized queries, read-only SQL, but no rate limiting or email verification

### Scalability
**Rating**: Low-Medium
**Current capacity**: Single worker (in-memory state), PostgreSQL can handle hundreds of concurrent users
**Bottleneck**: In-memory conversation store not shared across workers, Claude API rate limits

---
