# KB Scan Report: db-chat-nl

**Generated**: 2026-01-28T22:40:05.832729Z
**Extraction Coverage**: 100%
**Repository**: C:\work\db-chat-nl-master

---

## 1. Repository Identity

- **Path**: C:\work\db-chat-nl-master
- **Git Remote**: Not detected
- **Extractor Version**: 1.0.0
- **Scan Duration**: 1s

## 2. Architecture Overview

**Pattern**: layered

### Subsystems

1. **backend/api** (api layer)
   - **Purpose**: Handles HTTP endpoints and request routing (5 files)
   - **Technologies**: FastAPI
   - **Key Exports**: router
   - **Files**: admin_routes.py, auth_routes.py, conversation_routes.py, routes.py

2. **backend/services** (service layer)
   - **Purpose**: Contains business logic and application services (14 files)
   - **Technologies**: Python
   - **Key Exports**: LLMService, ChatService, DatabaseService
   - **Files**: app_data.py, auth.py, chat.py, conversations.py, database.py, llm.py, learning_store.py

3. **backend/models** (database layer)
   - **Purpose**: Manages database models and data access (2 files)
   - **Key Exports**: DatabaseSchema
   - **Files**: database.py

4. **frontend/components** (component layer)
   - **Purpose**: Contains UI components (10 files)
   - **Technologies**: React
   - **Files**: AdminConversationViewer.tsx, AuthPage.tsx, ChatContainer.tsx, ChatInput.tsx, ChatMessage.tsx, DatabaseInfo.tsx, DataViewer.tsx, QueryChart.tsx, QueryHistory.tsx, SidebarTabs.tsx

5. **frontend/hooks** (hook layer)
   - **Purpose**: Provides React hooks for state management (4 files)
   - **Technologies**: React
   - **Files**: useChat.ts, useQueryHistory.ts, useSuggestions.ts, useAuth.tsx

6. **frontend/services** (service layer)
   - **Purpose**: Contains business logic and application services (1 files)
   - **Files**: api.ts

### Communication Patterns

- **backend/app → backend/api**: Import-based communication (imports from ..services.auth)
- **backend/tests → backend/api**: Import-based communication (imports from app.main)
- **frontend/components → frontend/services**: Import-based communication (imports from ../services/api)
- **frontend/components → frontend/hooks**: Import-based communication (imports from ../hooks/useAuth)
- **frontend/components → frontend/types**: Import-based communication (imports from ../types/chat)
- **frontend/hooks → frontend/types**: Import-based communication (imports from ../types/chat)
- **frontend/hooks → frontend/services**: Import-based communication (imports from ../services/api)
- **frontend/services → frontend/types**: Import-based communication (imports from ../types/chat)

## 3. External Interfaces

### HTTP REST APIs

#### Admin API (/admin)
- **GET /admin/conversations** - Get all conversations from all users (admin only) [Auth Required]
- **GET /admin/conversations/{conversation_id}** - Get a specific conversation with all messages (admin only) [Auth Required]
- **GET /admin/users** - Get all users (admin only) [Auth Required]

#### Authentication API (/auth)
- **POST /auth/register** - Register a new user [Auth Required]
  - Request: email (EmailStr), password (str)
  - Response: user (dict), access_token (str)
- **POST /auth/login** - Login with email and password [Auth Required]
  - Request: email (EmailStr), password (str)
  - Response: user (dict), access_token (str)
- **POST /auth/logout** - Logout current user [Auth Required]
  - Response: message (str)
- **GET /auth/me** - Get current authenticated user info [Auth Required]
  - Response: id (str), email (str), is_admin (bool)
- **GET /auth/status** - Check if authentication service is available [Auth Required]

#### Conversations API (/conversations)
- **GET /conversations** - Get all conversations for the current user [Auth Required]
  - Response: conversations (List[ConversationModel])
- **POST /conversations** - Create a new conversation [Auth Required]
  - Request: title (Optional[str], default: "New Chat")
  - Response: id (str), title (str), created_at (str), updated_at (str)
- **GET /conversations/{conversation_id}** - Get a specific conversation with all messages [Auth Required]
- **PATCH /conversations/{conversation_id}** - Update conversation title [Auth Required]
  - Request: title (str)
  - Response: message (str)
- **DELETE /conversations/{conversation_id}** - Delete a conversation and all its messages [Auth Required]
  - Response: message (str)
- **GET /conversations/{conversation_id}/messages** - Get all messages for a conversation [Auth Required]

#### Main API
- **GET /health** - Health check endpoint [No Auth]
- **POST /chat** - Send a chat message and receive a response [No Auth]
- **POST /chat/stream** - Stream a chat response using Server-Sent Events (SSE) [No Auth]
- **GET /tasks/{task_id}** - Check the status of a background task [No Auth]
- **GET /database/info** - Get information about the connected database [No Auth]
- **GET /database/schema** - Get the full database schema [No Auth]
- **POST /database/refresh-schema** - Refresh the cached database schema [No Auth]
- **GET /database/tables** - Get list of all loaded tables [No Auth]
- **POST /database/upload** - Upload a JSON file to be queried [No Auth]
- **DELETE /database/tables/{table_name}** - Remove a loaded table [No Auth]
- **GET /s3/files** - List JSON files in S3 bucket [No Auth]
- **POST /s3/upload** - Upload JSON file to S3 bucket [No Auth]
- **POST /s3/load** - Load JSON file from S3 into DuckDB [No Auth]
  - Request: s3_path (str), table_name (Optional[str])
- **POST /database/connect** - Connect to a remote PostgreSQL database [No Auth]
  - Request: host (str), port (int), database (str), username (str), password (str)
- **GET /database/connections** - List available database connection options [No Auth]
- **POST /admin/clear-learning-cache** - Clear the learned queries cache for the current database [No Auth]

**Total Operations**: 30

### Streaming Interfaces

#### Server-Sent Events (SSE)
- **POST /chat/stream** - SSE streaming endpoint for chat responses
  - Message Format:
    - type (string, required) - Message type discriminator
    - content (varies, required) - Message content varies by type

## 4. UI Structure

**Routing Framework**: none
**Auth Pattern**: context

### Screens

1. **App** (frontend\src\App.tsx)
   - Purpose: Ipswich Town Fan Data Insights
   - Auth Required: Yes
   - States: loading
   - Sub-components: ViewMode, SidebarTabs, AdminConversationViewer, ChatContainer, AuthPage, TableSchema, AppContent, AuthProvider, DataViewer, AuthWrapper

2. **AppContent** (frontend\src\App.tsx)
   - Purpose: Ipswich Town Fan Data Insights
   - Auth Required: Yes
   - States: loading
   - Sub-components: ViewMode, SidebarTabs, AdminConversationViewer, ChatContainer, AuthPage, TableSchema, AppContent, AuthProvider, DataViewer, AuthWrapper

3. **AuthWrapper** (frontend\src\App.tsx)
   - Purpose: Ipswich Town Fan Data Insights
   - Auth Required: Yes
   - States: loading
   - Sub-components: ViewMode, SidebarTabs, AdminConversationViewer, ChatContainer, AuthPage, TableSchema, AppContent, AuthProvider, DataViewer, AuthWrapper

4. **AdminConversationViewer** (frontend\src\components\AdminConversationViewer.tsx)
   - Purpose: Admin Conversation Viewer - Read-only view of any conversation for admins
   - Auth Required: No
   - States: empty, loading, error
   - Sub-components: AdminConversationWithMessages

5. **AuthPage** (frontend\src\components\AuthPage.tsx)
   - Purpose: Authentication page with login and registration forms
   - Auth Required: Yes
   - States: loading, error

6. **ChatContainer** (frontend\src\components\ChatContainer.tsx)
   - Purpose: Main chat container component with streaming support
   - Auth Required: No
   - States: success, loading, error, empty
   - Sub-components: ChatMessage, ChatInput

7. **ChatInput** (frontend\src\components\ChatInput.tsx)
   - Purpose: Component for the chat input field with suggestions
   - Auth Required: No

8. **ChatMessage** (frontend\src\components\ChatMessage.tsx)
   - Purpose: Component for rendering a single chat message
   - Auth Required: No
   - States: success, error
   - Sub-components: QueryChart, QueryResultDisplay, ReactMarkdown

9. **DatabaseInfo** (frontend\src\components\DatabaseInfo.tsx)
   - Purpose: Component for displaying database schema and file upload
   - Auth Required: No
   - States: loading, error
   - Sub-components: DatabaseSchema, S3File, HealthStatus, Set

10. **DataViewer** (frontend\src\components\DataViewer.tsx)
    - Purpose: Component for viewing table data
    - Auth Required: No
    - States: empty, loading, error
    - Sub-components: QueryResult

11. **QueryChart** (frontend\src\components\QueryChart.tsx)
    - Purpose: Chart component for visualizing query results
    - Auth Required: No
    - Sub-components: Pie, Bar, Line

12. **QueryHistory** (frontend\src\components\QueryHistory.tsx)
    - Purpose: Component for displaying query history in the sidebar
    - Auth Required: No

13. **SidebarTabs** (frontend\src\components\SidebarTabs.tsx)
    - Purpose: Sidebar tabs component with Chats, History, and Admin views
    - Auth Required: Yes
    - States: empty, loading, error
    - Sub-components: AdminConversation, AdminPanel, ChatsList, Conversation

### Navigation Graph

- **App → AuthPage**: Conditional navigation when not_authenticated
- **App → AppContent**: Conditional navigation when authenticated
- **AppContent → AuthPage**: Conditional navigation when not_authenticated
- **AppContent → AppContent**: Conditional navigation when authenticated
- **AuthWrapper → AuthPage**: Conditional navigation when not_authenticated
- **AuthWrapper → AppContent**: Conditional navigation when authenticated

### User Flows

1. **Authentication Flow**: User logs in and accesses protected content
   - Steps: AuthWrapper → AuthPage → App

2. **Main App Flow**: Primary user journey through the application
   - Steps: AdminConversationViewer → ChatContainer → ChatInput

## 5. Data Models

**ORM Frameworks**: pydantic

### Models by Type

#### Pydantic Models (43 total)

**Chat Models:**
- **ChatMessage** (backend\app\schemas\chat.py) - A single chat message
  - Fields: id (UUID), role (MessageRole), content (str), timestamp (datetime), sql_query (Optional[str]), query_result (Optional['QueryResult'])

- **QueryResult** (backend\app\schemas\chat.py) - Result of a SQL query execution
  - Fields: columns (list[str]), rows (list[list[Any]]), row_count (int), execution_time_ms (float), truncated (bool), error (Optional[str])

- **ChatRequest** (backend\app\schemas\chat.py) - Request to send a chat message
  - Fields: message (str, max 2000), conversation_id (Optional[UUID])

- **ChatResponse** (backend\app\schemas\chat.py) - Response from the chat endpoint
  - Fields: conversation_id (UUID), message (ChatMessage), success (bool), error (Optional[str]), task_id (Optional[UUID]), is_async (bool)

- **TaskStatusResponse** (backend\app\schemas\chat.py) - Response for task status check
  - Fields: task_id (UUID), status (str), progress (int), result (Optional[ChatResponse]), error (Optional[str])

- **ConversationHistory** (backend\app\schemas\chat.py) - Full conversation history
  - Fields: conversation_id (UUID), messages (list[ChatMessage]), created_at (datetime), updated_at (datetime)

**Authentication Models:**
- **UserRegister** (backend\app\schemas\user.py) - User registration schema
  - Fields: email (EmailStr), password (str)

- **UserLogin** (backend\app\schemas\user.py) - User login schema
  - Fields: email (EmailStr), password (str)

- **UserResponse** (backend\app\schemas\user.py) - User response schema
  - Fields: id (str), email (str), is_admin (bool)

- **Token** (backend\app\schemas\user.py) - JWT token response
  - Fields: access_token (str), token_type (str)

**Database Models:**
- **TableSchema** (backend\app\models\database.py) - Database table schema
  - Fields: name (str), columns (List[ColumnSchema])

- **ColumnSchema** (backend\app\models\database.py) - Database column schema
  - Fields: name (str), type (str), nullable (bool), primary_key (bool), foreign_key (Optional[str])

- **DatabaseSchema** (backend\app\models\database.py) - Complete database schema
  - Fields: tables (List[TableSchema]), table_count (int), total_columns (int)

**Conversation Models:**
- **User** (backend\app\models\supabase.py) - Supabase User model
  - Fields: id (str), email (str), created_at (datetime), is_admin (bool)

- **Conversation** (backend\app\models\supabase.py) - Supabase Conversation model
  - Fields: id (str), user_id (str), title (str), created_at (datetime), updated_at (datetime)

- **Message** (backend\app\models\supabase.py) - Supabase Message model
  - Fields: id (str), conversation_id (str), role (str), content (str), sql_query (Optional[str]), query_result (Optional[dict]), created_at (datetime)

## 6. Runtime Configuration

**Config Mechanism**: both (environment variables + config files)

### Configuration Files
- backend\.env.example
- backend\app\core\config.py

### Required Variables (6)

**Database:**
- POSTGRES_HOST - Postgres host
- POSTGRES_PORT - Postgres port
- POSTGRES_DATABASE - Postgres database
- POSTGRES_USER - Postgres user
- POSTGRES_PASSWORD - Postgres password

**API:**
- QUOTAGUARDSTATIC_URL - Quotaguardstatic url

### Optional Variables (15)

**API:**
- ANTHROPIC_API_KEY (default: sk-ant-api03-xxxxx) - Anthropic api key
- SUPABASE_URL (default: https://xxxxx.supabase.co) - Supabase url

**Authentication:**
- AWS_ACCESS_KEY_ID (default: AKIA...) - Aws access key id
- AWS_SECRET_ACCESS_KEY (default: xxxxx) - Aws secret access key
- SUPABASE_ANON_KEY (default: eyJ...) - Supabase anon key
- SUPABASE_SERVICE_ROLE_KEY (default: eyJ...) - Supabase service role key

**Database:**
- DUCKDB_IN_MEMORY (default: 'true') - Duckdb in memory

**General:**
- APP_NAME (default: ITFC Analysis) - App name
- AWS_REGION (default: us-east-1) - Aws region
- MAX_QUERY_RESULTS (default: '1000') - Max query results
- QUERY_TIMEOUT (default: '30') - Query timeout
- CORS_ORIGINS (default: '*') - Cors origins

**LLM:**
- ANTHROPIC_MODEL (default: claude-opus-4-20250514) - Anthropic model

**Logging:**
- DEBUG (default: 'false') - Debug

**Storage:**
- S3_BUCKET (default: fan-data-json-db) - S3 bucket

## 7. Runtime Lifecycle

**Package Managers**: docker, npm, pip
**Docker Support**: yes
**CI/CD**: no

### Commands

#### Install
```bash
pip install -r requirements.txt  # Install Python dependencies
npm install                      # Install Node dependencies
```

#### Development
```bash
# Frontend
npm run dev  # Start development server (frontend)

# Backend
uvicorn app.main:app --reload  # Start FastAPI development server (backend)

# Docker
docker-compose -f docker-compose.yml up      # Start all services
docker-compose -f docker-compose.yml up -d   # Start in detached mode
```

#### Build
```bash
npm run build            # Build for production (frontend)
cd frontend && npm run build  # Build from README
```

#### Lint
```bash
npm run lint  # Lint code (frontend)
```

#### Other
```bash
npm run preview  # Run preview (frontend)
```

## 8. Dependencies

### By Purpose

**AI/LLM:**
- anthropic >=0.40.0 (runtime, pip)

**Authentication:**
- PyJWT >=2.8.0 (runtime, pip)
- bcrypt >=4.1.0 (runtime, pip)

**Database:**
- psycopg2-binary >=2.9.0 (runtime, pip)
- duckdb >=1.0.0 (runtime, pip)

**HTTP/API:**
- fastapi >=0.109.0 (runtime, pip)
- httpx >=0.26.0 (runtime, pip)

**Configuration:**
- python-dotenv >=1.0.0 (runtime, pip)
- pydantic-settings >=2.1.0 (runtime, pip)

**Testing:**
- pytest >=7.4.0 (runtime, pip)
- pytest-asyncio >=0.23.0 (runtime, pip)

**UI (Frontend):**
- react ^18.2.0 (runtime, npm)
- react-dom ^18.2.0 (runtime, npm)
- react-chartjs-2 ^5.3.1 (runtime, npm)
- react-markdown ^9.0.1 (runtime, npm)
- chart.js ^4.5.1 (runtime, npm)
- remark-gfm ^4.0.0 (runtime, npm)

**Build Tools:**
- vite ^5.0.8 (dev, npm)
- typescript ^5.2.2 (dev, npm)
- @vitejs/plugin-react ^4.2.1 (dev, npm)
- @types/react ^18.2.43 (dev, npm)
- @types/react-dom ^18.2.17 (dev, npm)

**Cloud/Storage:**
- boto3 >=1.34.0 (runtime, pip) - AWS S3 integration

**Other:**
- python-tds >=1.15.0 (runtime, pip) - SQL Server connectivity
- pyopenssl >=24.0.0 (runtime, pip)
- certifi * (runtime, pip)
- pysocks >=1.7.0 (runtime, pip) - SOCKS proxy support
- python-multipart >=0.0.6 (runtime, pip) - File upload support

### Key Frameworks
- **Backend**: FastAPI >=0.109.0, Pydantic 2.x
- **Frontend**: React ^18.2.0, Vite ^5.0.8, TypeScript ^5.2.2
- **Database**: DuckDB >=1.0.0, PostgreSQL (psycopg2-binary >=2.9.0)
- **LLM**: Anthropic Claude >=0.40.0

**Total Dependencies**: 45 (40 runtime, 5 dev)

## 9. Capability Mapping

### By Category

**Authentication (auth):**
- auth capability (2 files): auth_routes.py, auth.py
- authpage capability (1 files): AuthPage.tsx

**Core Functionality (core):**
- chat capability (2 files): routes.py, chat.py
- chatcontainer capability (1 files): ChatContainer.tsx
- chatinput capability (1 files): ChatInput.tsx
- chatmessage capability (1 files): ChatMessage.tsx
- usechat capability (1 files): useChat.ts

**Database (database):**
- database capability (6 files): routes.py, database.py, database_azure.py, database_base.py, database_pg.py, database.py (models)
- database_schema capability (1 files): database.py (models)
- databaseinfo capability (1 files): DatabaseInfo.tsx

**Features (feature):**
- users capability (1 files): admin_routes.py
- admin capability (2 files): admin_routes.py, routes.py
- conversations capability (4 files): admin_routes.py, app_data.py, chat.py, conversations.py
- conversation capability (2 files): conversation_routes.py, chat.py
- health capability (1 files): routes.py
- s3 capability (1 files): routes.py
- learning capability (1 files): learning_store.py
- llm capability (1 files): llm.py
- azure capability (1 files): database_azure.py
- ipswich + examples capabilities (1 files): ipswich_examples.py

**UI Components:**
- Multiple UI components mapped to their respective .tsx files in frontend/src/components/

## 10. Extraction Quality Report

✓ **Successful Extractors**: 8/8
✗ **Failed Extractors**: 0/8

**Coverage**: 100%

### Statistics
- Total Operations: 30 REST API endpoints + 1 SSE streaming endpoint
- Total Screens: 13 UI components
- Total Subsystems: 11 architectural layers
- Total Data Models: 43 Pydantic models
- Total Dependencies: 45 packages
- Total Configuration Variables: 21 (6 required, 15 optional)
- Total Commands: 10 lifecycle commands

### Unknowns

- Git remote URL not detected
- Some API endpoints have null response schemas (need manual documentation)
- Auth mechanism marked as "unknown" in external interfaces (likely JWT-based from dependencies)

### Warnings

None - all extractors completed successfully with comprehensive data extraction.

---

## Evidence Files

All data extracted from:
- external_interfaces.yaml (11791 bytes)
- ui_structure.yaml (5542 bytes)
- internal_boundaries.yaml (4959 bytes)
- data_models.yaml (71850 bytes)
- runtime_config.yaml (3972 bytes)
- runtime_lifecycle.yaml (1773 bytes)
- dependencies.yaml (6884 bytes)
- capability_mapping.yaml (12454 bytes)
- extraction_metadata.yaml (metadata file)
