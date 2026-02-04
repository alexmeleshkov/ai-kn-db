# Architecture

> **Purpose**: Document WHY behind architectural choices and system design.
> Focus on decisions that inform structural patterns during generation.

## Architecture Pattern

**Pattern**: Layered Monolith with Service Layer Architecture

**Why chosen**:
- Clear separation of concerns (API → Services → Data)
- Simple deployment (single application, no microservices complexity)
- Easy to understand and maintain for small teams
- Dependency injection enables testability
- Can be split into microservices later if needed

**Trade-offs**:
- ✅ Simple deployment and operation
- ✅ Fast development cycle (no distributed system complexity)
- ✅ All code in one repository
- ✅ Shared database transactions
- ⚠️ Cannot scale individual components independently
- ⚠️ Single point of failure (no redundancy without load balancer)
- ⚠️ All services must use same tech stack

---

## System Components

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   ChatUI     │  │  AdminPanel  │  │  DataViewer  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         └─────────────────┴─────────────────┘                   │
│                           │                                     │
│                    EventSource (SSE)                            │
└───────────────────────────┼─────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                    FastAPI Backend                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              API Layer (routes)                         │   │
│  │  /chat/stream  /conversations  /admin  /database       │   │
│  └─────────────────┬───────────────────────────────────────┘   │
│                    │                                            │
│  ┌─────────────────┴───────────────────────────────────────┐   │
│  │           Service Layer (business logic)                │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │  │   Chat   │  │   LLM    │  │ Learning │             │   │
│  │  │ Service  │→ │ Service  │→ │  Store   │             │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘             │   │
│  │       │             │              │                    │   │
│  │  ┌────▼─────┐  ┌───▼────┐  ┌──────▼─────┐             │   │
│  │  │Database  │  │Anthropic│  │  AppData   │             │   │
│  │  │Services  │  │  Claude │  │  Service   │             │   │
│  │  │(DuckDB/  │  │   API   │  │            │             │   │
│  │  │ Postgres/│  └─────────┘  └──────┬─────┘             │   │
│  │  │ Azure)   │                      │                    │   │
│  │  └────┬─────┘                      │                    │   │
│  └───────┼────────────────────────────┼────────────────────┘   │
│          │                            │                        │
│  ┌───────▼────────┐          ┌────────▼─────────┐             │
│  │  Business Data │          │  Application Data│             │
│  │  (PostgreSQL/  │          │   (PostgreSQL)   │             │
│  │   Azure SQL/   │          │  - Users         │             │
│  │   DuckDB+S3)   │          │  - Conversations │             │
│  │                │          │  - Messages      │             │
│  │  - Schema      │          │  - Learned Queries│            │
│  │  - Query Data  │          └──────────────────┘             │
│  └────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### Frontend Component

**Responsibility**: User interface for chat, database querying, and administration

**Key subsystems**:
- **Chat Interface** (`ChatContainer`, `ChatMessage`, `ChatInput`): Real-time chat with SSE streaming
- **Admin Panel** (`AdminConversationViewer`, `SidebarTabs`): Cross-user conversation viewing
- **Data Viewer** (`DataViewer`, `QueryChart`): Table browsing and result visualization
- **Authentication** (`AuthPage`, `AuthContext`): Login/register with JWT tokens
- **Hooks** (`useChat`, `useQueryHistory`, `useSuggestions`): Reusable state management logic

**Technologies**: React 18, TypeScript, EventSource (SSE), Vite, Recharts

---

### Backend API Layer

**Responsibility**: HTTP request handling and routing

**Key layers**:
1. **Main Routes** (`api/routes.py`): Chat streaming, database operations, file uploads, S3 integration
2. **Auth Routes** (`api/auth_routes.py`): Registration, login, token verification
3. **Conversation Routes** (`api/conversation_routes.py`): Conversation CRUD with user scoping
4. **Admin Routes** (`api/admin_routes.py`): Cross-user data access for admins

**Patterns**:
- Dependency injection via FastAPI `Depends()`
- Route groups with `APIRouter` and prefix
- Pydantic models for request/response validation
- HTTPException for error handling

**Technologies**: FastAPI, Pydantic, Uvicorn (ASGI server)

---

### Backend Service Layer

**Responsibility**: Business logic and orchestration

**Design approach**: Service-oriented with single responsibility principle

**Key services**:
- **ChatService** (`services/chat.py`): Orchestrates LLM and database for chat flow
- **LLMService** (`services/llm.py`): Anthropic Claude integration with Tool Use for SQL generation
- **DatabaseServices** (`services/database*.py`): Abstract base class with implementations for DuckDB, PostgreSQL, Azure SQL
- **AppDataService** (`services/app_data.py`): Application data persistence (conversations, messages, learned queries)
- **AuthService** (`services/auth.py`): JWT authentication with bcrypt password hashing
- **LearningStore** (`services/learning_store.py`): Query learning system with semantic similarity
- **ConversationStore** (`services/conversations.py`): In-memory LRU conversation cache for LLM context
- **QueryIntelligence** (`services/query_intelligence.py`): Query validation, caching, example selection
- **TaskManager** (`services/tasks.py`): Background task management for long-running queries

---

### Data Layer

**Responsibility**: Data persistence and retrieval

**Design approach**: Dual database architecture

**Key entities**:
- **Application Data (PostgreSQL)**:
  - `app_users`: User credentials and metadata (id, email, password_hash, is_admin)
  - `conversations`: User conversations (id, user_id, title, created_at, updated_at)
  - `messages`: Conversation messages (id, conversation_id, role, content, metadata, created_at)
  - `learned_queries`: Successful SQL patterns (id, database_id, question, sql_query, usage_count, last_used_at)

- **Business Data (PostgreSQL/Azure SQL/DuckDB)**:
  - Dynamic schema based on connected database
  - Introspected at runtime for LLM context
  - Sample data (3 rows per table) provided to LLM

**Indexes**:
- `app_users.email`: Fast user lookup during login
- `conversations.user_id, updated_at`: User's recent conversations
- `messages.conversation_id, created_at`: Chronological message retrieval
- `learned_queries.database_id, usage_count, last_used_at`: LRU query retrieval

---

## Communication Patterns

### Frontend ↔ Backend

**Protocol**: HTTP/HTTPS with Server-Sent Events (SSE)

**Patterns**:
1. **Standard API Calls**: REST-style with JSON
   - Authentication: JWT Bearer token in `Authorization` header
   - CRUD operations: GET, POST, PATCH, DELETE
   - Pydantic validation on request/response
   - Error responses: JSON with `detail` field

2. **Streaming Chat**: Server-Sent Events (EventSource)
   - Endpoint: `POST /chat/stream`
   - Optional authentication (works without auth)
   - Event types: `text`, `thinking`, `tool_start`, `tool_result`, `done`, `error`
   - Events format: `data: {JSON}\n\n`
   - Client: EventSource API, server: FastAPI StreamingResponse

3. **File Uploads**: Multipart form data
   - JSON files uploaded to `/database/upload`
   - Stored in backend, loaded into DuckDB

**Why this approach**:
- SSE provides real-time streaming without WebSocket complexity
- JWT tokens are stateless and scale horizontally
- REST conventions are well-understood and widely supported
- Pydantic provides automatic validation and documentation

---

### Backend ↔ Anthropic Claude

**Protocol**: HTTPS with streaming

**Patterns**:
- Streaming API with `stream=True`
- Tool Use (function calling) for agentic behavior
- System prompt with schema, examples, guidelines
- Message history for conversation context
- Extended thinking for complex queries (5000 token budget)

**Flow**:
1. Build system prompt with database schema and few-shot examples
2. Send user message with conversation history
3. Stream events: text delta, thinking, tool calls
4. For tool calls: execute SQL, return results to Claude
5. Continue streaming until final response

---

### Backend ↔ Databases

**Protocol**: Database-specific (psycopg2, pytds, DuckDB API)

**Patterns**:
- Connection pooling for PostgreSQL (ThreadedConnectionPool)
- Parameterized queries for SQL injection prevention
- Schema caching with refresh endpoint
- Lazy loading to avoid slow startup
- Sample data retrieval (3 rows per table) for LLM context

**Why this approach**:
- Connection pooling improves performance
- Parameterized queries prevent SQL injection
- Schema caching reduces database load
- Sample data helps LLM understand data patterns

---

## Data Architecture

### app_users Table

```sql
CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    INDEX idx_email (email)
);
```

### conversations Table

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_updated (user_id, updated_at DESC)
);
```

### messages Table

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_conversation_created (conversation_id, created_at ASC)
);
```

### learned_queries Table

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
    error_pattern VARCHAR(255),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_database_usage (database_id, usage_count DESC, last_used_at DESC)
);
```

---

### Data Flow: Chat Message Processing

1. **User sends message** → Frontend: User types message, clicks send
2. **Frontend creates EventSource** → POST /chat/stream with message + conversation_id
3. **Backend authenticates** → Extract JWT token, verify user (optional)
4. **Save user message** → AppDataService saves to PostgreSQL (if authenticated)
5. **Get conversation context** → Retrieve last 10 messages from in-memory store
6. **Get database schema** → DatabaseService introspects schema, gets sample data
7. **Build LLM prompt** → System prompt with schema + examples, user message + history
8. **Stream to Claude** → LLMService calls Anthropic API with streaming
9. **Claude generates SQL** → Tool Use: execute_sql with query + explanation
10. **Execute query** → DatabaseService runs parameterized SQL
11. **Return results to Claude** → Tool result with rows, columns, row count, execution time
12. **Claude generates response** → Natural language explanation of results
13. **Save to learning store** → LearningStore saves successful query pattern
14. **Stream to frontend** → SSE events: text, tool_start, tool_result, done
15. **Frontend updates UI** → Append assistant message, display query results, render chart
16. **Save assistant message** → AppDataService saves to PostgreSQL (if authenticated)

---

## API Design

### RESTful Conventions

**Endpoint structure**: `/resource` or `/resource/{id}` with HTTP verbs

**Response format** (success):
```json
{
  "id": "uuid",
  "field1": "value",
  "field2": "value",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error format**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

**Status codes**:
- 200 OK: Successful GET, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing/invalid auth token
- 403 Forbidden: Valid token but insufficient permissions
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server-side error
- 503 Service Unavailable: Required service not initialized

---

### Chat Streaming Flow

1. **Client creates EventSource**:
   ```javascript
   const eventSource = new EventSource('/chat/stream', {
     method: 'POST',
     headers: { 'Authorization': 'Bearer <token>' },
     body: JSON.stringify({ message: '...', conversation_id: '...' })
   });
   ```

2. **Server streams events**:
   ```
   data: {"type": "text", "content": "I'll query the database..."}\n\n
   data: {"type": "tool_start", "tool": "execute_sql", "query": "SELECT ..."}\n\n
   data: {"type": "tool_result", "success": true, "rows": 10, ...}\n\n
   data: {"type": "text", "content": "The results show..."}\n\n
   data: {"type": "done", "conversation_id": "uuid", "queries": [...]}\n\n
   ```

3. **Client processes events**:
   ```javascript
   eventSource.onmessage = (event) => {
     const data = JSON.parse(event.data);
     if (data.type === 'text') {
       appendText(data.content);
     } else if (data.type === 'tool_result') {
       displayQueryResult(data);
     } else if (data.type === 'done') {
       eventSource.close();
     }
   };
   ```

---

## Architectural Decisions

### Why SSE instead of WebSockets?
- **Simpler**: EventSource API is built into browsers, no library needed
- **One-way**: Chat is mostly server → client, don't need bidirectional
- **HTTP-compatible**: Works with standard HTTP proxies and load balancers
- **Reconnection**: EventSource auto-reconnects on connection drop
- **Stateless**: No WebSocket connection state to manage

### Why dual conversation storage?
- **PostgreSQL**: Durable persistence for user conversations
- **In-memory**: Fast LRU cache for LLM context (last 10 messages)
- **Separation**: App data (PostgreSQL) vs LLM context (in-memory)
- **Performance**: In-memory is faster for frequent reads
- **Scalability**: In-memory can be Redis later if needed

### Why service layer instead of direct DB access?
- **Testability**: Services can be mocked in tests
- **Reusability**: Same service used by multiple routes
- **Single responsibility**: Each service has one job
- **Dependency injection**: FastAPI Depends() makes this easy
- **Future migration**: Services can be split into microservices

### Why DuckDB for local querying?
- **Embedded**: No separate database server needed
- **JSON support**: Excellent schema inference for JSON files
- **S3 integration**: Can query S3 data lakes directly
- **Performance**: Columnar storage is fast for analytics
- **Development**: Easy to prototype without external database

### Why learning store?
- **Improve accuracy**: Reuse successful query patterns
- **Reduce cost**: Fewer LLM calls for similar questions
- **Error avoidance**: Track error patterns to prevent repeats
- **Context**: Few-shot examples improve SQL generation
- **Feedback loop**: System gets better over time

---

## Security Architecture

### Authentication Flow

1. **Registration**: User submits email + password
2. **Hash password**: bcrypt with salt (computationally expensive)
3. **Store user**: INSERT into app_users table
4. **Generate JWT**: Payload with user_id, email, is_admin, exp (1 week)
5. **Return token**: Client stores in localStorage

6. **Login**: User submits email + password
7. **Verify password**: bcrypt.checkpw (timing attack protection)
8. **Generate JWT**: Same as registration
9. **Return token**: Client stores in localStorage

10. **Authenticated request**: Client sends JWT in Authorization header
11. **Verify JWT**: Decode and check signature + expiration
12. **Extract user**: Get user_id, email, is_admin from payload
13. **Proceed**: Use user_id for user-scoped operations

### Authorization Patterns

- **User-scoped data**: Conversations filtered by user_id in WHERE clause
- **Admin role**: is_admin flag checked for admin endpoints
- **No cross-user access**: Users can't see other users' data (404 if try)
- **Stateless tokens**: No server-side session storage

---

## Scalability Considerations

**Current limitations** (single-instance):
- Single database connection pool (shared across all users)
- In-memory conversation store (lost on restart)
- No horizontal scaling (one FastAPI process)

**Future scaling path**:
1. **Add Redis**: Replace in-memory store with Redis for shared cache
2. **Add load balancer**: Nginx/HAProxy to distribute traffic
3. **Horizontal scaling**: Run multiple FastAPI instances behind load balancer
4. **Database connection pooling**: PgBouncer for PostgreSQL connection management
5. **Separate services**: Extract LLM service, learning store into microservices
6. **Message queue**: RabbitMQ/Kafka for async task processing
7. **CDN**: CloudFront/Cloudflare for static assets

---

*This architecture prioritizes simplicity and developer productivity while maintaining clear boundaries for future scaling.*
