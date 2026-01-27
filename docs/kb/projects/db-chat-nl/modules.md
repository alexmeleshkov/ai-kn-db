# Modules: ITFC Analysis

## Backend Modules

### API Routes (`backend/app/api/`)

#### `routes.py`
Main API endpoints for chat and database operations
- `POST /api/v1/chat/stream` - SSE streaming chat endpoint
- `GET /api/v1/health` - Health check
- `GET /api/v1/database/schema` - Get database schema
- `POST /api/v1/database/refresh-schema` - Refresh schema cache

#### `auth_routes.py`
Authentication endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/status` - Check auth service status

#### `conversation_routes.py`
Conversation management
- `GET /api/v1/conversations` - List user conversations
- `POST /api/v1/conversations` - Create new conversation
- `GET /api/v1/conversations/{id}` - Get conversation with messages
- `PATCH /api/v1/conversations/{id}` - Update conversation title
- `DELETE /api/v1/conversations/{id}` - Delete conversation

#### `admin_routes.py`
Admin-only endpoints
- Admin conversation viewer
- System monitoring

### Core (`backend/app/core/`)

#### `config.py`
Application configuration and settings
- Environment variable loading
- Pydantic settings validation
- Database connection strings
- API keys and secrets

#### `logging.py`
Centralized logging configuration
- Structured logging
- Log levels
- Output formatting

### Services (`backend/app/services/`)

#### `database_base.py`
Abstract base class for database adapters
- `get_schema()` - Introspect database schema
- `execute_query()` - Execute SQL and return results
- Connection management interface

#### `database_azure.py`
Azure SQL Server implementation
- python-tds connection
- SOCKS5 proxy support (QuotaGuard)
- Schema caching
- Query execution with timeout
- Prefixed column name handling

#### `database_pg.py`
PostgreSQL implementation
- psycopg2 connection pooling
- Schema introspection
- Query execution
- Error handling

#### `app_data.py`
RDS PostgreSQL app data service
- User management (CRUD)
- Conversation persistence
- Message storage
- Learned query storage
- Connection pooling

#### `auth.py`
JWT authentication service
- Password hashing with bcrypt (12 rounds)
- JWT token generation (HS256, 7-day expiration)
- Token validation and decoding
- User registration and login logic

**Sources**: ARCHITECTURE.md:L217-L238

#### `llm.py`
Claude AI integration
- Anthropic SDK client
- Extended thinking support (5000 token budget)
- Tool use implementation (execute_sql, ask_clarification)
- Streaming message handling
- Error recovery and retry logic (max 15 iterations)

**Sources**: ARCHITECTURE.md:L206-L214

#### `chat.py`
Chat orchestration service
- User question processing
- Schema loading and caching
- Learned query retrieval
- Prompt construction
- SSE response streaming
- Conversation and message persistence
- Heartbeat mechanism

#### `learning_store.py`
Universal learning system
- Store successful question-SQL pairs
- Retrieve similar queries
- Database-specific storage
- Auto-cleanup (max 100 per DB)
- Error pattern tracking

#### `ipswich_examples.py`
Static few-shot examples
- Common Ipswich fan database queries
- Column name glossary
- Domain-specific patterns
- Example question-SQL pairs

#### `query_intelligence.py`
Query validation and optimization
- SQL syntax validation
- Query safety checks (SELECT only)
- Result row limiting
- Optimization hints

#### `conversations.py`
Conversation management logic
- Create, read, update, delete conversations
- List user conversations
- Title generation

#### `tasks.py`
Background task management
- Async task handling
- Long-running operations

### Models (`backend/app/models/`)

#### `database.py`
Database model definitions
- ORM models (if using SQLAlchemy)
- Database table schemas

### Schemas (`backend/app/schemas/`)

#### `chat.py`
Pydantic schemas for API validation
- `ChatRequest` - User question input
- `ChatResponse` - LLM response output
- `QueryResult` - SQL query results
- `Message` - Chat message structure
- `Conversation` - Conversation structure

## Frontend Modules

### Components (`frontend/src/components/`)

#### `AuthPage.tsx`
Login and registration UI
- Email/password form
- Show/hide password toggle
- Error display
- Registration/login mode switching

#### `ChatContainer.tsx`
Main chat interface container
- Message list rendering
- Auto-scroll to bottom
- Loading states
- Error handling

#### `ChatInput.tsx`
User input field
- Text area with auto-resize
- Submit button
- Enter key handling
- Character count (optional)

#### `ChatMessage.tsx`
Individual message display
- Markdown rendering (react-markdown)
- User vs assistant styling
- Timestamp display
- Code block syntax highlighting

#### `SidebarTabs.tsx`
Sidebar with history and schema tabs
- Tab switching
- Conversation list
- Schema viewer toggle

#### `QueryHistory.tsx`
Conversation history list
- List all conversations
- Click to load conversation
- Delete conversation button
- Conversation title display

#### `DatabaseInfo.tsx`
Database schema viewer
- Table list
- Column details (name, type)
- Collapsible sections
- Refresh schema button

#### `DataViewer.tsx`
Query results table display
- Scrollable table
- Column headers
- Row data
- CSV export button

#### `QueryChart.tsx`
Chart.js visualizations
- Bar, line, pie charts
- Automatic chart type selection
- Responsive sizing
- Legend and labels

#### `AdminConversationViewer.tsx`
Admin view of all conversations
- System-wide conversation list
- User filtering
- Conversation inspection

### Hooks (`frontend/src/hooks/`)

#### `useAuth.tsx`
Authentication context and hooks
- Login/logout functions
- Current user state
- Token management (localStorage)
- Protected route logic
- AuthContext provider

#### `useChat.ts`
Chat state management
- Send message function
- SSE connection handling
- Message history state
- Loading and error states
- Conversation management

#### `useQueryHistory.ts`
Conversation history management
- Fetch conversations
- Load conversation messages
- Delete conversation
- Conversation list state

#### `useSuggestions.ts`
Query suggestions
- Example question display
- Quick action buttons
- Suggestion selection

### Services (`frontend/src/services/`)

#### `api.ts`
API client for backend communication
- Axios/fetch configuration
- Request/response interceptors
- JWT token attachment
- Error handling
- Endpoint wrappers

### Types (`frontend/src/types/`)

#### `chat.ts`
TypeScript type definitions
- Message interface
- Conversation interface
- User interface
- QueryResult interface
- API response types

### Styles (`frontend/src/styles/`)

#### `index.css`
Global styles
- CSS variables
- Component styles
- Responsive breakpoints
- Utility classes

## Scripts (`backend/scripts/`)

### `rds_schema.sql`
RDS PostgreSQL schema definition
- `app_users` table
- `conversations` table
- `messages` table
- `learned_queries` table
- Indexes and constraints

### `supabase_schema.sql`
Legacy Supabase schema (deprecated)

### `migrate_from_supabase.py`
Migration script from Supabase to RDS

### `benchmark_dbs.py`
Database performance benchmarking

### `test_chat.py`
Chat API testing script

### `test_ipswich_live.py`
Ipswich database connection test

## Configuration Files

### `backend/requirements.txt`
Python dependencies

### `frontend/package.json`
Node.js dependencies and scripts

### `docker-compose.yml`
Docker multi-container orchestration

### `backend/Dockerfile`
Backend container definition

### `frontend/Dockerfile`
Frontend container definition

### `build.sh`
Production build script

### `backend/Procfile`
Heroku deployment configuration

### `backend/.env.example`
Environment variable template
