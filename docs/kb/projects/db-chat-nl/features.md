# Features: ITFC Analysis

## Core Features

### 1. Natural Language to SQL Conversion
**Description**: Translates English questions into SQL queries using Claude AI

**Capabilities**:
- Simple queries (COUNT, SELECT)
- Complex queries (JOINs, aggregations, GROUP BY)
- Extended thinking for multi-step reasoning (5000 token budget)
- Query validation before execution
- Automatic retry with corrections (max 15 iterations)

**Example Questions**:
- "How many fans are there?"
- "Show me memberships by country"
- "What are the top 10 communication sources?"
- "Count fans with email permission"

### 2. Chat Interface
**Description**: Interactive chat interface with message history

**Capabilities**:
- Real-time SSE streaming responses
- Markdown rendering for formatted responses
- Message history within conversation
- Loading states and error handling
- Heartbeat mechanism to prevent timeout

### 3. Query Result Visualization
**Description**: Display query results as tables and charts

**Capabilities**:
- Tabular display with scrolling
- CSV export functionality
- Automatic chart generation for numeric results
- Chart.js integration (bar, line, pie charts)
- Responsive layout

### 4. Authentication & Authorization
**Description**: Self-hosted JWT-based authentication

**Capabilities**:
- User registration with email/password
- Login with JWT token generation (7-day expiration)
- Password visibility toggle
- Token stored in localStorage
- Protected API routes
- bcrypt password hashing (12 rounds)

### 5. Conversation History
**Description**: Persistent storage of chat conversations

**Capabilities**:
- List all user conversations
- Load conversation with full message history
- Delete conversations
- Conversation titles (auto-generated or manual)
- Search/filter conversations

### 6. Database Schema Viewer
**Description**: Browse database tables and columns

**Capabilities**:
- View all tables in database
- View column names and data types
- Schema caching for performance
- Manual schema refresh
- Collapsible table view

### 7. Universal Learning System
**Description**: Learns from successful SQL queries to improve accuracy

**Capabilities**:
- Store successful question-SQL pairs
- Retrieve similar queries for new questions
- Auto-cleanup (max 100 queries per database)
- Database-specific learning
- Error pattern tracking

**Sources**: ARCHITECTURE.md:L249-L274

### 8. Ipswich-Specific Examples
**Description**: Few-shot examples for common Ipswich fan data queries

**Capabilities**:
- Static examples for fan counts, memberships, permissions
- Column name glossary (prefixed columns like [fan.id])
- Domain-specific query patterns
- Examples included in LLM prompt

### 9. Admin Features
**Description**: Administrative capabilities for oversight

**Capabilities**:
- View all conversations across users
- Monitor query patterns
- System health checks

## Technical Features

### SSE Streaming
- Server-Sent Events for real-time responses
- Heartbeat messages to prevent Heroku timeout
- Graceful connection handling

### Query Intelligence
- SQL syntax validation
- Query optimization hints
- Result row limiting (max 1000)
- Timeout handling (30s default)

### Database Adapters
- Pluggable database backends (Azure SQL, PostgreSQL, DuckDB)
- Connection pooling
- Schema introspection
- Read-only query enforcement

### Docker Support
- docker-compose configuration
- Separate frontend/backend containers
- Health checks
- Non-root user execution

## Planned/Missing Features

### Not Yet Implemented
- API documentation (Swagger/OpenAPI)
- Query result pagination
- Multi-tenant support
- Role-based access control (RBAC)
- Query scheduling/automation
- Email notifications
- Mobile responsive optimization
- Dark mode
- Query templates/saved queries
- Data export formats (Excel, JSON)

### Testing Gaps
- No frontend unit tests
- No integration tests
- No E2E tests
- No load/performance tests
