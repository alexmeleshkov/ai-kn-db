# Pattern Candidates from db-chat-nl

This document contains pattern candidates extracted from the db-chat-nl project.

## Pattern: Natural Language to SQL with Extended Thinking

**Context**: Converting natural language questions to SQL queries for fan databases

**Implementation Observations**:
- Uses Claude Opus 4 with extended thinking (5000 token budget)
- Tool-based execution: `execute_sql`, `ask_clarification`
- Query validation and retry mechanism (max 15 iterations)
- SSE streaming with heartbeat for long-running queries
- Ipswich-specific few-shot examples and glossary

**Key Files**:
- `backend/app/services/llm.py`
- `backend/app/services/chat.py`
- `backend/app/services/query_intelligence.py`

**Evidence**: ARCHITECTURE.md:L206-L214 (Claude Opus 4 configuration), README.md:L338-L346 (Extended Thinking feature)

**Potential Reuse**: Any NL-to-SQL application requiring complex multi-step reasoning

---

## Pattern: Universal Learning System

**Context**: Learning from successful SQL queries to improve future accuracy

**Implementation Observations**:
- Stores successful queries per database in PostgreSQL
- Includes queries in LLM prompt as few-shot examples
- Tracks error patterns to avoid repeating mistakes
- Auto-cleanup keeps max 100 queries per database
- Database-specific static examples for common patterns

**Key Files**:
- `backend/app/services/learning_store.py`
- `backend/scripts/supabase_schema.sql` (learned_queries table)

**Schema**:
```sql
learned_queries (
  question TEXT,
  sql TEXT,
  database_name TEXT,
  success BOOLEAN,
  error_message TEXT
)
```

**Evidence**: ARCHITECTURE.md:L249-L274 (Universal Learning System description)

**Potential Reuse**: Any LLM-powered system that needs to learn from past interactions

---

## Pattern: Database Adapter with Multi-Backend Support

**Context**: Supporting multiple database backends (Azure SQL, PostgreSQL, DuckDB)

**Implementation Observations**:
- Abstract base class `DatabaseBase`
- Concrete implementations: `AzureSQLDatabaseService`, `PostgresDatabaseService`, `DatabaseService` (DuckDB)
- Mode selection via environment variable `DB_MODE`
- Lazy schema loading to avoid slow startup
- Connection pooling for app data (RDS PostgreSQL)

**Key Files**:
- `backend/app/services/database_base.py`
- `backend/app/services/database_azure.py`
- `backend/app/services/database_pg.py`
- `backend/app/services/database.py`

**Evidence**: backend/app/main.py:L676-L683 (database service initialization with mode selection)

**Potential Reuse**: Applications needing to support multiple database backends

---

## Pattern: SSE Streaming with Heroku Timeout Handling

**Context**: Streaming LLM responses via Server-Sent Events while handling Heroku's 55s timeout

**Implementation Observations**:
- Sends periodic heartbeat events to keep connection alive
- Streams thinking process, tool calls, and final responses
- Error handling with graceful degradation
- Event types: `heartbeat`, `thinking`, `tool_call`, `response`, `error`, `done`

**Key Files**:
- `backend/app/services/chat.py`
- `backend/app/api/routes.py` (SSE endpoint)

**Evidence**: ARCHITECTURE.md:L212 (SSE streaming with heartbeat for Heroku 55s timeout)

**Potential Reuse**: Any LLM streaming application on platforms with connection timeouts

---

## Pattern: Self-Hosted JWT Authentication

**Context**: User authentication without third-party services (replaced Supabase Auth)

**Implementation Observations**:
- bcrypt for password hashing
- PyJWT for token generation (HS256 algorithm)
- 7-day token expiration
- Token stored in localStorage (frontend)
- Bearer token authentication in API requests
- Dedicated auth endpoints: register, login, logout, me, status

**Key Files**:
- `backend/app/services/auth.py`
- `backend/app/api/auth_routes.py`
- `frontend/src/hooks/useAuth.tsx`

**Schema**:
```sql
app_users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE,
  password_hash TEXT,
  created_at TIMESTAMP
)
```

**Evidence**: ARCHITECTURE.md:L217-L247 (JWT-Based Auth section with authentication flow)

**Potential Reuse**: Any application needing simple JWT-based auth

---

## Pattern: React Hooks for API State Management

**Context**: Managing API state and side effects in React components

**Implementation Observations**:
- Custom hooks: `useAuth`, `useChat`, `useQueryHistory`, `useSuggestions`
- Centralized API client: `services/api.ts`
- JWT token injection in API requests
- Error handling with user feedback
- Loading states for async operations

**Key Files**:
- `frontend/src/hooks/useAuth.tsx`
- `frontend/src/hooks/useChat.ts`
- `frontend/src/hooks/useQueryHistory.ts`
- `frontend/src/hooks/useSuggestions.ts`
- `frontend/src/services/api.ts`

**Evidence**: frontend/src/App.tsx:L850-L887 (custom hooks usage), tree.txt showing frontend/src/hooks structure

**Potential Reuse**: React applications with API-heavy interactions

---

## Pattern: FastAPI Service Initialization in Lifespan

**Context**: Initializing database connections and services at application startup

**Implementation Observations**:
- Uses FastAPI lifespan context manager
- Initializes connection pools (psycopg2 ThreadedConnectionPool)
- Stores services in `app.state` for access in routes
- Graceful shutdown with connection pool cleanup
- Lazy schema loading to avoid slow startup
- Conditional service initialization based on environment

**Key Files**:
- `backend/app/main.py` (lifespan function)

**Evidence**: backend/app/main.py:L638-L713 (lifespan context manager implementation)

**Potential Reuse**: FastAPI applications with stateful services

---

## Pattern: Domain-Specific LLM Examples (Ipswich Football)

**Context**: Providing domain-specific context to LLM for better SQL generation

**Implementation Observations**:
- Static few-shot examples in `ipswich_examples.py`
- Domain glossary (e.g., "STM" = Season Ticket Member)
- Common query patterns (count fans, memberships by country, etc.)
- Column name mappings (prefixed columns like `[fan.id]`)

**Key Files**:
- `backend/app/services/ipswich_examples.py`

**Potential Reuse**: Domain-specific NL-to-SQL applications

---

## Pattern: Query Results with Chart Visualization

**Context**: Displaying query results as tables and charts

**Implementation Observations**:
- Chart.js with react-chartjs-2
- Auto-detect numeric columns for chart generation
- Bar and line chart support
- CSV export functionality
- Markdown rendering for text responses

**Key Files**:
- `frontend/src/components/QueryChart.tsx`
- `frontend/src/components/DataViewer.tsx`

**Dependencies**:
- chart.js ^4.5.1
- react-chartjs-2 ^5.3.1
- react-markdown ^9.0.1

**Evidence**: frontend/package.json:L820-L826 (dependencies list)

**Potential Reuse**: Data visualization in query result interfaces

---

## Pattern: Dual Database Architecture (Business Data + App Data)

**Context**: Separating business data (queried) from application data (auth, history)

**Implementation Observations**:
- Business data: Azure SQL Server (read-only, live Ipswich fan data)
- App data: AWS RDS PostgreSQL (users, conversations, learned queries)
- Separate connection management for each database
- IP whitelist required for Azure SQL access
- SOCKS5 proxy (QuotaGuard) for Heroku to Azure connection

**Key Tables (App Data)**:
- `app_users` - User accounts
- `conversations` - Chat sessions
- `messages` - Chat messages
- `learned_queries` - SQL learning system

**Evidence**: ARCHITECTURE.md:L182-L203 (Database Architecture table), backend/.env.example:L533-L561 (environment variables for dual databases)

**Potential Reuse**: Applications that query external read-only databases while maintaining internal state

---

## Conventions Observed

### Code Organization
- **Backend**: Layered architecture (api, core, models, schemas, services)
- **Frontend**: Component-based with custom hooks for state management
- **Scripts**: Separate directory for maintenance scripts (migrations, imports, testing)

### Naming Conventions
- Python: snake_case for functions, PascalCase for classes
- TypeScript: camelCase for functions/variables, PascalCase for components/types
- Database tables: snake_case
- API endpoints: kebab-case with versioning (`/api/v1/`)

### Error Handling
- Backend: Try-catch with logging and graceful error responses
- Frontend: Error state in hooks with user-friendly messages
- LLM: Retry mechanism with clarification workflow

### Testing
- pytest for backend API tests
- Manual testing scripts in `backend/scripts/`
- Test fixtures in `backend/tests/`

### Documentation
- ARCHITECTURE.md for system overview
- README.md for quick start and deployment
- .env.example for environment variable reference
- Inline docstrings for complex functions

---

## Unknowns / Missing Prerequisites

- QuotaGuard SOCKS5 proxy configuration details
- Heroku deployment configuration (dyno type, add-ons)
- Azure SQL IP whitelisting process
- RDS database initialization scripts (full schema)
- Frontend build optimization settings
- Load testing results and scalability limits
- Claude API rate limits and cost optimization strategies
- Backup and disaster recovery procedures
