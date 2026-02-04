# Technology Stack

> **Purpose**: Document technologies used and WHY they were chosen.
> Focus on decisions that inform package generation and stack understanding.

## Stack Summary

**Architecture**: Layered monolith with service layer architecture
**Deployment**: Docker Compose with multi-stage builds

---

## Backend Stack

### Core Framework
**FastAPI (Python 3.11+)**

**Why chosen**:
- Async/await support for concurrent request handling
- Automatic OpenAPI documentation generation
- Built-in dependency injection for service layer
- Fast performance (comparable to Node.js and Go)
- Type hints with Pydantic for request/response validation
- Native Server-Sent Events (SSE) support for streaming

**Key features used**:
- `@router` decorators for route organization
- `Depends()` for dependency injection (auth, services)
- `StreamingResponse` for SSE streaming
- `HTTPException` for structured error handling
- Pydantic `BaseModel` for schemas
- Lifespan context manager for startup/shutdown
- CORS middleware for frontend integration
- Static file serving for SPA deployment

---

### Databases

**PostgreSQL 14+ (Application Data)**

**Why chosen**:
- Mature, reliable ACID-compliant RDBMS
- Strong JSONB support for metadata storage
- Excellent connection pooling with psycopg2
- Wide deployment support (RDS, Docker, managed services)
- Native UUID type for primary keys

**ORM/Query Tool**: Raw SQL with psycopg2
- Migrations: Manual SQL scripts (lightweight for KB reference)
- Connection pooling: Yes, ThreadedConnectionPool (1-5 connections)

**Use cases**:
- User authentication (app_users table)
- Conversation and message persistence
- Learned query storage with usage tracking

---

**DuckDB (Local Analytics)**

**Why chosen**:
- Embedded analytics database (no separate server)
- Excellent JSON file querying with automatic schema inference
- S3 integration for cloud data access
- Fast columnar storage for analytics workloads
- In-memory or file-based modes

**Use cases**:
- Local JSON file querying
- S3 data lake querying
- Development/prototyping without external database

---

**Azure SQL Server (Business Data - Optional)**

**Why chosen**:
- Enterprise Microsoft SQL Server compatibility
- Secure access via SOCKS proxy for corporate networks
- Windows authentication support
- Integration with existing Azure infrastructure

**Library**: pytds (pure Python TDS protocol)
- SOCKS proxy support for secure networks
- Connection string authentication

---

### AI/ML Service
**Anthropic Claude API**

**Model**: claude-opus-4-20250514

**Why chosen**:
- Industry-leading natural language understanding
- Tool Use (function calling) for agentic SQL generation
- Extended thinking for complex query planning
- Large context window for schema + examples + conversation
- Reliable structured outputs for SQL queries

**Libraries**:
- `anthropic` - Official Python SDK
- Extended thinking enabled with 5000 token budget
- Streaming responses for real-time UX

**Fallback**: None (required service for core functionality)

---

### Authentication
**JWT (JSON Web Tokens) with bcrypt**

**Libraries**:
- `PyJWT` - JWT token creation and verification
- `bcrypt` - Password hashing with automatic salt generation

**Security measures**:
- Bcrypt password hashing (computationally expensive to prevent brute force)
- JWT with HS256 algorithm (HMAC with SHA-256)
- 1-week token expiration (configurable)
- Email normalization (lowercase) for case-insensitive lookup
- Timing attack protection with bcrypt.checkpw
- Admin role flag for privileged operations
- Stateless authentication (no server-side sessions)

---

### External Services

**AWS S3 (Optional)**
- **Library**: boto3 (AWS SDK for Python)
- **Purpose**: JSON file storage and loading into DuckDB
- **Fallback**: App works without S3 (local files only)

---

### Other Backend Dependencies

**psycopg2** - PostgreSQL database adapter with connection pooling

**pydantic** - Data validation and settings management with type hints

**pydantic-settings** - Environment variable loading for configuration

**boto3** - AWS S3 client for file operations

**pytds** - Pure Python TDS protocol for Azure SQL Server

**python-dotenv** - Load environment variables from .env file

**uvicorn** - ASGI server for running FastAPI application

---

## Frontend Stack

### Core Framework
**React 18**

**Why chosen**:
- Virtual DOM for efficient updates during streaming
- Hooks for simple state management (no Redux needed)
- Large ecosystem of components and tools
- Server-Sent Events (EventSource) support in browsers
- Excellent TypeScript integration

**Key features used**:
- Functional components with hooks
- `useState` for local state
- `useEffect` for side effects (API calls, EventSource)
- `useCallback` for memoized callbacks
- `useRef` for EventSource reference
- Context API for auth state
- Custom hooks for reusable logic

---

### Language
**TypeScript 5.0+**

**Why chosen**:
- Type safety catches errors at compile time
- Better IDE autocomplete and refactoring
- Self-documenting interfaces and types
- Prevents common JavaScript bugs (null/undefined)
- Excellent React support

**Config settings**:
- Strict mode enabled for maximum type safety
- ES2020 target for modern browser features
- Path aliases (@/components, @/hooks) for clean imports

---

### Build Tool
**Vite 4.0+**

**Why chosen**:
- Ultra-fast hot module replacement (HMR) during development
- Native ES modules (no bundling in dev)
- Optimized production builds with Rollup
- TypeScript support out of the box
- Simple configuration

**Features used**:
- Dev server with proxy to backend (http://localhost:8000)
- Production build with code splitting
- Asset optimization (CSS, images)
- Environment variable injection

---

### Styling
**Approach**: Vanilla CSS with custom properties (CSS variables)

**Why this approach**:
- No build step overhead (CSS-in-JS adds complexity)
- Design system with CSS variables for consistency
- Easy theming and maintenance
- BEM-style naming for component scoping
- Full control over styling without library constraints
- Lightweight (no runtime CSS-in-JS cost)

**Design system**:
- 30+ CSS custom properties for colors, spacing, radius, transitions
- Ipswich Town FC branding (navy blue primary color)
- Responsive design with media queries
- Animation patterns (spin, pulse, blink, fadeIn, slideUp)

---

### State Management
**React Hooks + Context API**

**Why this approach**:
- No need for Redux (app state is simple)
- useContext for global auth state
- Custom hooks for reusable logic (useChat, useQueryHistory, useSuggestions)
- Local state with useState for component state
- localStorage for persistence (query history)

**State locations**:
- Auth context: User info, isAuthenticated, login/logout
- useChat hook: Messages, streaming state, tool calls
- useQueryHistory hook: Query history with localStorage persistence
- Component state: UI state (tabs, modals, forms)

---

### Data Fetching
**Native fetch API + Server-Sent Events (EventSource)**

**Why chosen**:
- No library needed (fetch is built into browsers)
- EventSource for real-time SSE streaming
- Simple async/await patterns
- Full control over request/response handling

**Patterns used**:
- fetch for standard API calls (GET, POST, DELETE)
- EventSource for streaming chat responses
- JWT token in Authorization header
- Error handling with try/catch
- Loading states during async operations

---

### Other Frontend Dependencies

**react-markdown** - Markdown rendering in chat messages with syntax highlighting

**recharts** - Data visualization (bar, line, pie charts) for query results

**react-dom** - React DOM rendering

---

## Infrastructure

### Containerization
**Docker with Docker Compose**

**Strategy**:
- Multi-stage builds for optimized images
- Separate services for backend, frontend, PostgreSQL
- Development mode with volume mounts for hot reload
- Production mode with built frontend served by backend

**Services** (Docker Compose):
- `postgres` - PostgreSQL 14 for application data
- `backend` - FastAPI application
- `frontend` - React development server (dev) or static build (prod)

**Dockerfile patterns**:
- Backend: Python 3.11-slim base, pip install, uvicorn server
- Frontend: Node 18 base, npm install, vite build, nginx serve

---

### Environment Management
**Approach**: .env files with pydantic-settings

**Required variables**:
- `DATABASE_URL` - PostgreSQL connection string for app data
- `JWT_SECRET` - Secret key for JWT token signing
- `ANTHROPIC_API_KEY` - Claude API key for LLM
- `CORS_ORIGINS` - Allowed CORS origins (default "*" for dev)

**Optional variables**:
- `S3_BUCKET`, `S3_REGION`, `S3_ACCESS_KEY`, `S3_SECRET_KEY` - AWS S3 configuration
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DATABASE` - PostgreSQL RDS configuration
- `AZURE_SQL_HOST`, `AZURE_SQL_DATABASE`, `AZURE_SQL_USERNAME`, `AZURE_SQL_PASSWORD` - Azure SQL configuration
- `SOCKS_PROXY` - SOCKS proxy for Azure SQL (format: host:port)
- `DEBUG` - Enable debug logging

**Environment file locations**:
- Backend: `backend/.env`
- Frontend: `frontend/.env` (VITE_ prefix for Vite variables)

---

### Logging
**Backend**: Python logging module with structured logging

- Log levels: DEBUG, INFO, WARNING, ERROR
- Traceback logging for exceptions
- Request/response logging in development
- Authentication event logging (login, registration)
- Query execution logging (SQL, execution time, row count)

**Frontend**: console.log with error boundaries

- Error logging for failed API calls
- EventSource error logging for streaming failures
- User action logging in development

---

### Testing

**Backend**:
- Framework: pytest (not implemented in scanned codebase)
- Test types: Unit tests for services, integration tests for API routes

**Frontend**:
- Framework: Vitest (not implemented in scanned codebase)
- Test types: Component tests with React Testing Library

**Note**: Testing infrastructure not present in scanned repository (reference project)

---

## Security Measures

- **JWT authentication** with 1-week expiration and HS256 signing
- **Bcrypt password hashing** with automatic salt generation (slow by design)
- **Parameterized SQL queries** in all database services (prevents SQL injection)
- **CORS configuration** with allowed origins (restrict in production)
- **Admin role checking** for privileged operations (user.is_admin flag)
- **User-scoped data access** (users can only see their own conversations)
- **Environment variable protection** (API keys not in code)
- **HTTPS recommended** in production (not enforced in dev)
- **SQL validation** before execution (LLM generates SQL, validated before running)

---

## Performance Considerations

**Backend**:
- Async/await for concurrent request handling
- Connection pooling for PostgreSQL (1-5 connections)
- Schema caching (refresh endpoint for updates)
- Lazy schema loading (avoid slow startup)
- Streaming responses prevent timeout on long queries
- In-memory conversation store (LRU eviction, max 100 conversations)
- Background tasks for async processing (not used heavily)

**Frontend**:
- Vite for fast development and optimized builds
- Code splitting for lazy loading
- EventSource for real-time streaming (no polling)
- localStorage for query history (avoid API calls)
- React virtual DOM for efficient updates
- Memoized callbacks with useCallback

**Database**:
- Connection pooling (psycopg2 ThreadedConnectionPool)
- Indexed columns for fast lookups (user_id, conversation_id, email)
- Pagination for large result sets (limit parameters)
- Sample data limited to 3 rows per table (LLM context)
- Conversation history limited to 10 messages (LLM context)
- Learned query cleanup (max 100 per database, LRU eviction)

---

## Known Limitations

- **No multi-tenancy**: Single-instance deployment, users share database connection pools
- **No rate limiting**: API has no request throttling (add nginx rate limiting in production)
- **No query timeout**: Long-running queries can hang (add database timeout configuration)
- **No result pagination**: Large query results returned in full (could exceed memory)
- **No test coverage**: Reference project has no automated tests
- **No CI/CD**: Manual deployment process
- **No monitoring**: No Prometheus/Grafana/Datadog integration
- **No horizontal scaling**: Single-instance architecture (add load balancer for scaling)
- **LLM dependency**: App requires Claude API (no offline mode)
- **PostgreSQL dependency**: App requires PostgreSQL for persistence (no SQLite fallback)

---

## Version Requirements

**Backend**:
- Python 3.11+
- PostgreSQL 14+
- FastAPI 0.100+
- Anthropic SDK 0.8+

**Frontend**:
- Node.js 18+
- React 18+
- TypeScript 5.0+
- Vite 4.0+

**Infrastructure**:
- Docker 24.0+
- Docker Compose 2.0+

---

*This technology stack is optimized for real-time AI-powered database querying with streaming responses and conversation persistence.*
