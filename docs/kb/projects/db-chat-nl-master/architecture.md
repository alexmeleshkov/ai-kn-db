# Architecture

> **Purpose**: Document WHY behind architectural choices and system design.
> Focus on decisions that inform structural patterns during generation.

## Architecture Pattern

**Pattern**: Layered Architecture (Three-Tier: Frontend + Backend + Database)

**Why chosen**:
- Clear separation of concerns between presentation (React), business logic (FastAPI services), and data persistence (PostgreSQL)
- Enables independent scaling of frontend and backend
- Service layer provides reusable business logic abstractions
- Facilitates testing with clear boundaries between layers

**Trade-offs**:
- ✅ Clear boundaries make codebase easy to navigate and maintain
- ✅ Service layer enables code reuse across multiple API endpoints
- ✅ Easy to add new features by extending service layer
- ⚠️ Some operations require coordination across multiple layers
- ⚠️ Not horizontally scalable without additional infrastructure (single PostgreSQL instance)

---

## Project Structure

### Directory Tree

```
db-chat-nl-master/
├── backend/
│   └── app/
│       ├── api/                 # FastAPI route handlers
│       │   ├── admin_routes.py
│       │   ├── auth_routes.py
│       │   ├── conversation_routes.py
│       │   ├── routes.py
│       │   └── __init__.py
│       ├── models/              # SQLAlchemy ORM models
│       │   ├── database.py
│       │   └── __init__.py
│       ├── schemas/             # Pydantic request/response schemas
│       │   ├── chat.py
│       │   └── __init__.py
│       └── services/            # Business logic services
│           ├── app_data.py
│           ├── auth.py
│           ├── chat.py
│           ├── conversations.py
│           ├── database.py
│           ├── database_azure.py
│           ├── database_base.py
│           ├── database_pg.py
│           ├── ipswich_examples.py
│           ├── learning_store.py
│           ├── llm.py
│           ├── query_intelligence.py
│           ├── tasks.py
│           └── __init__.py
├── frontend/
│   └── src/
│       ├── components/          # React UI components
│       │   ├── AdminConversationViewer.tsx
│       │   ├── AuthPage.tsx
│       │   ├── ChatContainer.tsx
│       │   ├── ChatInput.tsx
│       │   ├── ChatMessage.tsx
│       │   ├── DatabaseInfo.tsx
│       │   ├── DataViewer.tsx
│       │   ├── QueryChart.tsx
│       │   ├── QueryHistory.tsx
│       │   └── SidebarTabs.tsx
│       ├── hooks/               # Custom React hooks
│       │   ├── useChat.ts
│       │   ├── useQueryHistory.ts
│       │   └── useSuggestions.ts
│       └── styles/              # CSS stylesheets
│           └── index.css
└── docker-compose.yml           # Multi-container orchestration
```

### Folder Organization

**backend/app/api** (`backend/app/api/`):
- **Purpose**: FastAPI route handlers (controllers) that receive HTTP requests and delegate to services
- **Key files**: auth_routes.py (JWT authentication), routes.py (chat endpoint with SSE), conversation_routes.py (CRUD), admin_routes.py (admin panel)
- **File patterns**: `*_routes.py` for endpoint definitions

**backend/app/models** (`backend/app/models/`):
- **Purpose**: SQLAlchemy ORM models for database schema
- **Key entities**: User (authentication), Conversation (chat sessions), ConversationMessage (individual messages)
- **File patterns**: `database.py` contains all models

**backend/app/schemas** (`backend/app/schemas/`):
- **Purpose**: Pydantic schemas for request/response validation and serialization
- **Key files**: chat.py (ChatRequest, ChatResponse, StreamEvent, TableSchema, ColumnSchema)
- **File patterns**: `*.py` for schema definitions grouped by domain

**backend/app/services** (`backend/app/services/`):
- **Purpose**: Business logic layer with reusable service classes
- **Key subdirectories**: Database services (database*.py), AI services (llm.py, chat.py), intelligence services (learning_store.py, query_intelligence.py)
- **File patterns**: `*.py` service files, abstract base classes (database_base.py), concrete implementations (database_pg.py, database_azure.py)

**frontend/src/components** (`frontend/src/components/`):
- **Purpose**: React UI components for chat interface, admin panel, data visualization
- **Key components**: ChatContainer (main UI), ChatMessage (message rendering), QueryChart (Chart.js visualization), AuthPage (login)
- **File patterns**: `*.tsx` for React components with TypeScript

**frontend/src/hooks** (`frontend/src/hooks/`):
- **Purpose**: Custom React hooks for state management and side effects
- **Key hooks**: useChat (SSE streaming, tool use tracking), useQueryHistory (localStorage persistence), useSuggestions (auto-complete)
- **File patterns**: `use*.ts` for custom hooks

### File Naming Conventions

- **Route handlers**: `*_routes.py` - FastAPI endpoint definitions (e.g., `auth_routes.py`, `admin_routes.py`)
- **Services**: `*.py` - Business logic services (e.g., `chat.py`, `llm.py`, `auth.py`)
- **Components**: `*.tsx` - React components with TypeScript (e.g., `ChatContainer.tsx`, `QueryChart.tsx`)
- **Hooks**: `use*.ts` - Custom React hooks (e.g., `useChat.ts`, `useQueryHistory.ts`)
- **Models**: `database.py` - SQLAlchemy ORM models

**Special files**:
- `database_base.py`: Abstract base class defining database service interface
- `app_data.py`: Singleton pattern for global state (database service instance)
- `__init__.py`: Module initialization files (export main classes)
- `index.css`: Complete stylesheet with Ipswich Town branding (3049 lines)

---

## System Components

### High-Level Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (React)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ChatContainer│  │   AuthPage   │  │  SidebarTabs │      │
│  │   useChat    │  │              │  │  AdminViewer │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │ HTTP/SSE                        │
└────────────────────────────┼─────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  API Routes  │  │   Services   │  │   Models     │      │
│  │ routes.py    │─▶│ ChatService  │─▶│ User         │      │
│  │ auth_routes  │  │ LLMService   │  │ Conversation │      │
│  │ admin_routes │  │ AuthService  │  │ Message      │      │
│  └──────────────┘  └──────┬───────┘  └──────┬───────┘      │
│                            │                  │              │
│                            │ Query            │ ORM          │
└────────────────────────────┼──────────────────┼──────────────┘
                             │                  │
                             ▼                  ▼
                    ┌─────────────────┐  ┌─────────────┐
                    │  Claude API     │  │ PostgreSQL  │
                    │  (Anthropic)    │  │             │
                    └─────────────────┘  └─────────────┘
```

---

### Frontend (React + TypeScript)

**Responsibility**: User interface, event handling, state management, SSE streaming reception

**Key subsystems**:
- **Components**: UI rendering (ChatContainer, ChatMessage, QueryChart, AuthPage, SidebarTabs)
- **Hooks**: State management (useChat for SSE, useQueryHistory for localStorage, useSuggestions for auto-complete)
- **Styling**: CSS with Ipswich Town branding (#0E4C92 blue, #FFFFFF white, #D4AF37 gold)

**Technologies**: React 18 (hooks), TypeScript, Chart.js, react-markdown, Vite

---

### Backend (FastAPI + Service Layer)

**Responsibility**: Business logic, API endpoints, database operations, AI integration

**Key layers**:
1. **API Layer** (`app/api`): FastAPI route handlers (routes.py, auth_routes.py, conversation_routes.py, admin_routes.py)
2. **Service Layer** (`app/services`): Business logic (ChatService, LLMService, AuthService, DatabaseService, LearningStore)
3. **Data Layer** (`app/models`): SQLAlchemy ORM models (User, Conversation, ConversationMessage)

**Technologies**: FastAPI, SQLAlchemy, psycopg2, PyJWT, bcrypt, Anthropic Python SDK

---

### Database (PostgreSQL)

**Responsibility**: Persistent storage for users, conversations, messages, learned queries

**Design approach**: Relational database with foreign key constraints

**Key entities**:
- **User**: id, email, hashed_password, is_admin, created_at (JWT authentication)
- **Conversation**: id, user_id, title, created_at, updated_at (chat sessions)
- **ConversationMessage**: id, conversation_id, role, content, created_at (individual messages)
- **LearnedQuery**: database_id, database_type, question, sql_query, execution_time_ms, row_count, usage_count (learning store)

---

## Communication Patterns

### Frontend ↔ Backend

**Protocol**: HTTP (REST) + Server-Sent Events (SSE)

**Patterns**:
1. **REST for CRUD operations**: GET /conversations, POST /register, DELETE /conversations/{id}
2. **SSE for streaming**: POST /chat streams multiple event types (text, thinking, tool_start, tool_result, done)
3. **JWT for authentication**: Bearer token in Authorization header

**Why this approach**:
- SSE enables real-time streaming without WebSocket complexity (unidirectional backend→frontend sufficient)
- REST provides simple, stateless API for CRUD operations
- JWT enables stateless authentication (no server-side session storage)

---

### Backend ↔ Claude API

**Protocol**: HTTPS with streaming

**Patterns**:
- **Tool Use**: Claude autonomously decides when to call execute_sql and ask_clarification tools
- **Extended Thinking**: Optional extended thinking mode with configurable budget (full on first iteration, 1/4 on retries)
- **Streaming**: client.messages.stream() yields events (thinking, text, tool_use)

**Why this approach**:
- Tool Use enables agentic behavior (Claude decides SQL execution timing and error recovery)
- Extended thinking improves query accuracy for complex questions
- Streaming provides real-time feedback to users

---

### Backend ↔ PostgreSQL

**Protocol**: TCP connection pooling (psycopg2.pool.SimpleConnectionPool)

**Patterns**:
- **ORM for app data**: SQLAlchemy models for User, Conversation, ConversationMessage
- **Raw SQL for user databases**: Direct psycopg2 connections for querying user-provided databases
- **Connection pooling**: Reuse connections to avoid overhead (5 min connections, 20 max connections)
- **Query timeout**: 30-second timeout on execute_query to prevent long-running queries

---

## Data Architecture

### User Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Conversation Table

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ConversationMessage Table

```sql
CREATE TABLE conversation_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### LearnedQuery Table

```sql
CREATE TABLE learned_queries (
    id SERIAL PRIMARY KEY,
    database_id VARCHAR(100) NOT NULL,
    database_type VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    execution_time_ms INTEGER,
    row_count INTEGER,
    usage_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- users.email: Unique index for fast email lookup during login
- conversations.user_id: Index for fast user conversation queries
- conversation_messages.conversation_id: Index for fast message retrieval
- learned_queries.(database_id, database_type): Composite index for learning store queries

---

### Data Flow: Natural Language to SQL Query

1. **User input**: User types question in ChatInput, submits to useChat hook
2. **API call**: useChat sends POST /chat with question, conversation_history, database_id
3. **Service orchestration**: ChatService.process_question() coordinates LLM, database, learning store
4. **LLM processing**: LLMService.process_with_tools_streaming() calls Claude API with:
   - Database schema (from DatabaseService.get_schema())
   - Few-shot examples (from LearningStore.get_similar_examples())
   - Domain glossary (from ipswich_examples.py)
   - Tool definitions (execute_sql, ask_clarification)
5. **SSE streaming**: For each Claude event (thinking, text, tool_use), yield StreamEvent to frontend
6. **Tool execution**: If Claude calls execute_sql:
   - Validate query (QueryValidator.validate_against_schema())
   - Execute in thread pool (to allow heartbeat polling)
   - Return results to Claude as tool_result
7. **Learning**: On successful query, store in LearningStore for future few-shot retrieval
8. **Response complete**: Yield "done" event, frontend displays results with optional chart

---

## API Design

### REST API Convention

**Endpoint structure**: `/resource` or `/resource/{id}` with standard HTTP methods

**Response format**:
```json
{
  "data": { ... },
  "message": "Success message"
}
```

**Error format**:
```json
{
  "detail": "Error description"
}
```

**SSE Event format**:
```json
{
  "type": "text|thinking|tool_start|tool_result|done|error",
  "content": "...",
  "query": "...",
  "data": { ... }
}
```

---

### Authentication Flow

1. **Register**: POST /register
   - Input: { email, password }
   - Output: { user: { id, email, is_admin }, token }
2. **Login**: POST /login
   - Input: { email, password }
   - Output: { user: { id, email, is_admin }, token }
3. **Get current user**: GET /me
   - Input: Authorization: Bearer {token}
   - Output: { id, email, is_admin }

---

## Design Decisions

### Decision 1: Server-Sent Events (SSE) over WebSocket

**Context**: Need real-time streaming from backend to frontend for chat responses

**Options considered**:
1. WebSocket (bidirectional, full-duplex)
2. Server-Sent Events (unidirectional, server→client)
3. Long polling (inefficient, high latency)

**Choice**: Server-Sent Events (SSE)

**Rationale**:
- Unidirectional communication sufficient (backend streams to frontend, frontend sends requests via HTTP)
- Simpler than WebSocket (no need for bidirectional protocol)
- Built-in reconnection handling
- Works with standard HTTP/2

**Implications**:
- ✅ Simple implementation with FastAPI StreamingResponse
- ✅ No additional infrastructure (works over HTTP)
- ⚠️ Not suitable for bidirectional real-time communication (but not needed here)

---

### Decision 2: Tool Use Pattern with Claude API

**Context**: Need AI to autonomously execute SQL queries and handle errors

**Options considered**:
1. Single-turn generation (generate SQL, then execute separately)
2. Tool Use pattern (Claude autonomously calls execute_sql tool)

**Choice**: Tool Use pattern with execute_sql and ask_clarification tools

**Rationale**:
- Enables agentic behavior (Claude decides when to execute, retry, or ask for clarification)
- Claude can see query results and iterate (multi-turn reasoning)
- Better error recovery (Claude sees error and generates new query)
- Supports clarification requests (Claude can ask user to disambiguate)

**Implications**:
- ✅ More accurate queries through iterative refinement
- ✅ Better error handling (Claude sees errors and retries)
- ✅ User-friendly clarification requests
- ⚠️ More complex implementation (requires streaming, tool handling, iteration limit)
- ⚠️ Higher token usage (multiple turns, tool results in context)

---

### Decision 3: Learning Store with Similarity Matching

**Context**: Need to improve query accuracy over time

**Options considered**:
1. No learning (rely on Claude's base knowledge)
2. Simple history log (show recent queries)
3. Similarity-based retrieval (weighted keyword matching)

**Choice**: Similarity-based retrieval with weighted keywords and usage tracking

**Rationale**:
- Provides relevant few-shot examples (similar questions → similar SQL)
- Usage tracking prioritizes successful patterns
- Weighted keywords (e.g., 'ballot': 4, 'hospitality': 4) boost domain-specific terms
- Persistent storage enables learning across sessions

**Implications**:
- ✅ Query accuracy improves over time
- ✅ Domain-specific terms get boosted (Ipswich Town FC examples)
- ✅ Usage tracking surfaces best patterns
- ⚠️ Requires PostgreSQL for persistence
- ⚠️ Similarity matching is simple (no embeddings, just keyword overlap)

---

### Decision 4: Factory Pattern for Database Services

**Context**: Need to support multiple database types (PostgreSQL, Azure SQL, DuckDB)

**Options considered**:
1. Single database service with if/else branching
2. Abstract base class with concrete implementations (Factory pattern)

**Choice**: Abstract base class (DatabaseServiceBase) with factory function

**Rationale**:
- Clean abstraction (each database type is separate class)
- Easy to add new database types (create new subclass)
- Factory function (get_database_service()) selects implementation based on config

**Implications**:
- ✅ Clean separation of concerns
- ✅ Easy to extend with new database types
- ✅ Type-safe with abstract methods
- ⚠️ More files (one per database type)

---

### Decision 5: Heartbeat Polling for Long Queries

**Context**: Heroku has 55-second timeout on HTTP responses

**Options considered**:
1. No heartbeat (risk timeout on long queries)
2. Periodic heartbeat events during query execution

**Choice**: 15-second heartbeat with thread pool execution

**Rationale**:
- Heroku 55s timeout requires activity every ~15s
- Thread pool allows SQL to run in background while main thread sends heartbeats
- Heartbeat events keep connection alive

**Implications**:
- ✅ Prevents Heroku timeout on long queries
- ✅ User sees progress (heartbeat events show "Query running...")
- ⚠️ More complex implementation (thread pool, polling with timeout)
- ⚠️ Heroku-specific workaround (not needed on other platforms)

---

## Quality Attributes

### Modularity
**Rating**: High
**Evidence**: Clear service layer separation (LLMService, ChatService, DatabaseService, AuthService), abstract base classes (DatabaseServiceBase), factory pattern (database.py), custom hooks (useChat, useQueryHistory)

### Testability
**Rating**: Medium
**Evidence**: Service layer enables unit testing with mocks, but no test files found in scanned code. Dependency injection used in some services (LLMService accepts database service). Abstract base class enables test doubles for database services.

### Performance
**Rating**: Medium
**Expected**: SSE streaming provides real-time feedback. Connection pooling reduces overhead (5-20 connections). LRU caching for query results. 30-second query timeout prevents runaway queries. No horizontal scaling (single instance). PostgreSQL as bottleneck for concurrent users.

### Security
**Rating**: Medium
**Measures**: JWT authentication with bcrypt password hashing, query validation (SELECT only, dangerous keywords blocked), SQL injection prevention via parameterized queries in some cases, admin role for privileged operations, CORS configuration. Missing: Rate limiting, input sanitization for some endpoints, SQL injection risk in raw query execution.

### Scalability
**Rating**: Low to Medium
**Current capacity**: Single instance (Heroku dyno). PostgreSQL connection pool (5-20 connections). Stateless API (scales horizontally if DB can handle). SSE keeps connections open (limits concurrent users).
**Bottleneck**: PostgreSQL (single instance), SSE connections (one per active chat), Claude API rate limits, no caching layer (Redis).

---
