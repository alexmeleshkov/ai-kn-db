# Technology Stack

> **Purpose**: Document technologies used and WHY they were chosen.
> Focus on decisions that inform package generation and stack understanding.

## Stack Summary

**Architecture**: Layered Monolith (API → Services → Database)
**Deployment**: Docker Compose (local), Heroku (production)

---

## Backend Stack

### Core Framework
**FastAPI 0.109.0+**

**Why chosen**:
- Modern Python web framework with automatic API documentation
- Native async/await support for concurrent operations
- Dependency injection system simplifies service management
- Built-in Pydantic validation for type safety
- SSE (Server-Sent Events) support for streaming responses
- High performance comparable to Node.js and Go

**Key features used**:
- StreamingResponse for SSE chat streaming
- Dependency injection for service access (Depends pattern)
- Background tasks for long-running operations
- Automatic OpenAPI/Swagger documentation
- Request validation with Pydantic models

---

### Database

**PostgreSQL 14+ (AWS RDS)**

**Why chosen**:
- Production-ready relational database with ACID guarantees
- Connection pooling for concurrent users (psycopg2)
- JSON column support for flexible metadata storage
- Strong authentication and user management
- Mature ecosystem and excellent AWS integration

**ORM/Query Tool**: Raw SQL with psycopg2 (no ORM)
- Migrations: Manual SQL scripts (backend/scripts/*_schema.sql)
- Connection pooling: Yes, psycopg2.pool.SimpleConnectionPool

**Azure SQL Server (Live Data)**

**Why chosen**:
- Ipswich Town FC fan database hosted on Azure
- Microsoft SQL Server T-SQL dialect
- Firewall requires static IP (QuotaGuard proxy)

**Query Tool**: python-tds (pure Python, SOCKS-compatible)

**DuckDB 1.0+ (Local/JSON)**

**Why chosen**:
- In-memory SQL for JSON file querying
- Zero configuration for development
- S3 integration for cloud data
- Parquet support for efficient columnar storage
- Perfect for data exploration without database setup

---

### Authentication
**JWT (JSON Web Tokens) + bcrypt**

**Libraries**:
- `PyJWT>=2.8.0` - JWT token creation and verification
- `bcrypt>=4.1.0` - Password hashing with automatic salt generation

**Security measures**:
- HS256 algorithm for token signing
- 1-week token expiration
- bcrypt with auto-generated salt (CPU-intensive but secure)
- Email case normalization
- Generic error messages (don't reveal if email exists)
- Last login timestamp tracking

---

### AI / LLM Integration
**Anthropic Claude Opus 4**

**Library**: `anthropic>=0.40.0`

**Purpose**: Natural language to SQL conversion with extended thinking

**Features used**:
- Messages API with streaming support
- Tool Use (agentic behavior with execute_sql and ask_clarification tools)
- Extended thinking for complex multi-step reasoning
- Max tokens: 4096
- Thinking budget: full on first try, quarter on retry

**Fallback**: None (Claude is required for core functionality)

---

### External Services

**AWS S3**
- **Library**: `boto3>=1.34.0`
- **Purpose**: JSON/Parquet file storage and direct querying via DuckDB
- **Fallback**: Local file upload mode

**QuotaGuard Static (SOCKS5 Proxy)**
- **Library**: `pysocks>=1.7.0`
- **Purpose**: Static IP for Azure SQL Server firewall
- **Fallback**: Direct connection (for dev/local PostgreSQL)

---

### Other Backend Dependencies

**pydantic[email]>=2.5.0** - Request/response validation with type safety

**uvicorn[standard]>=0.27.0** - ASGI server with WebSocket and SSE support

**psycopg2-binary>=2.9.0** - PostgreSQL connection pooling

**python-tds>=1.15.0** - Pure Python SQL Server driver (SOCKS-compatible)

**python-multipart>=0.0.6** - File upload support

**python-dotenv>=1.0.0** - Environment variable management

**pyopenssl>=24.0.0** - SSL/TLS for Azure SQL

**certifi** - SSL root certificates

---

## Frontend Stack

### Core Framework
**React 18.2.0**

**Why chosen**:
- Mature component-based architecture
- Large ecosystem and community
- Excellent TypeScript support
- Hooks for clean state management
- Server-Side Events (SSE) support via EventSource API

**Key features used**:
- Functional components with hooks (useState, useEffect, useCallback)
- Custom hooks for encapsulated logic (useChat, useAuth, useQueryHistory)
- Conditional rendering for dynamic UI
- Component composition

---

### Language
**TypeScript 5.2.2**

**Why chosen**:
- Type safety prevents runtime errors
- Better IDE support (autocomplete, refactoring)
- Self-documenting code with interfaces
- Catches bugs at compile time
- Gradual adoption (can mix with JavaScript)

**Config settings**:
- Strict mode enabled
- ES2020 target
- JSX: react-jsx

---

### Build Tool
**Vite 5.0.8**

**Why chosen**:
- Lightning-fast hot module replacement (HMR)
- Native ES modules (no bundling in dev)
- Optimized production builds
- Simple configuration
- Better DX than Webpack or Create React App

---

### Styling
**Approach**: CSS with CSS Variables

**Why this approach**:
- No external dependency (built-in browser support)
- CSS variables for theming (dark mode ready)
- Simple and performant
- No build step required

---

### State Management
**React Hooks (useState, useEffect, useCallback)**

**Why this approach**:
- Built-in (no external library needed)
- Sufficient for app complexity
- Custom hooks encapsulate logic
- Context API not needed (props sufficient)

---

### Data Fetching
**Fetch API + EventSource (SSE)**

**Why chosen**:
- Native browser APIs (no external library)
- Fetch for REST API calls
- EventSource for SSE streaming
- Simple and lightweight

---

### Other Frontend Dependencies

**chart.js@^4.5.1** - Canvas-based charts (bar, line, pie)

**react-chartjs-2@^5.3.1** - React wrapper for Chart.js

**react-markdown@^9.0.1** - Markdown rendering for chat messages

**remark-gfm@^4.0.0** - GitHub Flavored Markdown support (tables, strikethrough)

---

## Infrastructure

### Containerization
**Docker Compose**

**Strategy**:
- Separate containers for frontend and backend
- nginx for frontend static serving
- Health checks for backend
- Environment-based configuration

**Services**:
- `backend`: FastAPI on port 8000
- `frontend`: nginx on port 80 (dev: Vite on 5173)

---

### Environment Management
**Approach**: .env files with python-dotenv

**Required variables** (from meta.yaml):
- `ANTHROPIC_API_KEY` - Claude API access (required)
- `ANTHROPIC_MODEL` - Model ID (default: claude-opus-4-20250514)
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DATABASE`, `POSTGRES_USER`, `POSTGRES_PASSWORD` - RDS connection (required)
- `JWT_SECRET` - Token signing key (required)
- `DB_MODE` - Database mode: azure | postgres | duckdb (required)
- `AZURE_SQL_*` - Azure SQL Server credentials (required if DB_MODE=azure)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET` - S3 integration (optional)
- `QUOTAGUARDSTATIC_URL` - SOCKS5 proxy URL for Azure (optional, Heroku add-on)
- `CORS_ORIGINS` - Allowed origins (default: *)
- `MAX_QUERY_RESULTS` - Result limit (default: 1000)
- `QUERY_TIMEOUT` - Query timeout in seconds (default: 30)

---

### Logging
**Backend**: Python logging module with structured logs

**Frontend**: console.log/error for development

---

### Testing

**Backend**:
- Framework: pytest
- Test types: Unit tests for services, integration tests for API routes
- Location: backend/tests/

**Frontend**:
- No tests currently (would use Vitest or Jest)

---

## Security Measures

- JWT authentication with 1-week expiration
- bcrypt password hashing with automatic salt
- Admin authorization via is_admin flag in JWT
- User-scoped data access (conversation ownership verification)
- Read-only SQL queries (SELECT only, block INSERT/UPDATE/DELETE/DROP/etc.)
- Query validation (dangerous keyword detection)
- SQL injection prevention (parameterized queries with %s placeholders)
- CORS configuration for allowed origins
- HTTPS/SSL for all connections (production)
- Environment-based secrets (never commit .env)

---

## Performance Considerations

**Backend**:
- Connection pooling for PostgreSQL (concurrent users)
- Schema caching (refresh only when requested)
- In-memory conversation store with LRU eviction (max 100 conversations)
- S3 views (no data copying, query on-demand)
- Parquet format for S3 (columnar, compressed)
- Automatic LIMIT on queries (prevent huge transfers)
- SSE streaming for low-latency responses
- Background tasks for long-running operations
- Thread pool for async SQL execution with timeout

**Frontend**:
- Vite for fast HMR and optimized builds
- EventSource for streaming responses (low latency)
- Optimistic UI updates (immediate feedback)
- Lazy loading for components (code splitting)
- React.memo for component memoization (prevent unnecessary re-renders)

**Database**:
- Indexed queries (ORDER BY updated_at, created_at, usage_count)
- Row count approximation (pg_class.reltuples, sys.partitions) instead of COUNT(*)
- Automatic cleanup of learned queries (max 100 per database)
- Connection reuse with keepalive checking

---

## Known Limitations

- In-memory conversation store not shared across workers (single-worker only)
- Conversations lost on backend restart (not persisted except in PostgreSQL for authenticated users)
- No user email verification (trust on registration)
- No password reset flow
- Admin key hardcoded in backend (should be environment variable)
- No rate limiting (API can be abused)
- S3 integration requires AWS credentials (not included)
- Azure SQL requires QuotaGuard proxy on Heroku (adds latency and cost)
- DuckDB in-memory mode loses data on restart
- No multi-tenancy (single database shared by all users)

---
