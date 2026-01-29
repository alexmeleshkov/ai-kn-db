# Features & Capabilities

## Must-Have Features (MVP)

### 1. User Authentication (JWT + bcrypt)
**Description**: Secure user registration and login

**Implementation**:
- Module: backend/app/services/auth.py, frontend/src/hooks/useAuth.tsx
- Endpoints: POST /api/v1/auth/register, POST /api/v1/auth/login, GET /api/v1/auth/me
- UI: AuthPage.tsx with email/password inputs

**Acceptance Criteria**:
- [x] User can register with email/password
- [x] Passwords hashed with bcrypt (12 rounds)
- [x] JWT token issued on login (7-day expiration)
- [x] Protected routes require valid token

**Priority**: CRITICAL

### 2. Natural Language to SQL
**Description**: Convert user questions to SQL queries using Claude AI

**Implementation**:
- Module: backend/app/services/llm.py, backend/app/services/chat.py
- Endpoint: POST /api/v1/chat/stream (SSE)
- Tools: execute_sql, ask_clarification

**Acceptance Criteria**:
- [x] Natural language converted to SQL
- [x] Extended thinking for complex queries (5000 tokens)
- [x] Query validation before execution
- [x] Streaming responses with heartbeat

**Priority**: CRITICAL

### 3. Chat History Persistence
**Description**: Save conversations for later retrieval

**Implementation**:
- Module: backend/app/services/app_data.py, conversations.py
- Endpoints: GET /api/v1/conversations, GET /api/v1/conversations/{id}
- Database: conversations, messages tables

**Acceptance Criteria**:
- [x] Conversations stored per user
- [x] Messages include role, content, metadata
- [x] User can load previous conversations

**Priority**: HIGH

### 4. Query Result Visualization
**Description**: Auto-generate charts from query results

**Implementation**:
- Module: frontend/src/components/QueryChart.tsx
- Library: Chart.js with react-chartjs-2
- Chart types: Bar, Line, Pie

**Acceptance Criteria**:
- [x] Numeric data triggers chart generation
- [x] Chart type auto-selected (bar for categorical, line for time series)
- [x] Responsive design

**Priority**: HIGH

### 5. Database Schema Viewer
**Description**: Browse available tables and columns

**Implementation**:
- Module: backend/app/services/database_azure.py
- Endpoint: GET /api/v1/database/schema
- UI: DatabaseInfo.tsx in sidebar

**Acceptance Criteria**:
- [x] Schema loaded from database
- [x] Tables and columns displayed
- [x] Collapsible tree view

**Priority**: MEDIUM

## Nice-to-Have Features

### 6. CSV Export
**Description**: Download query results as CSV

**Implementation**: DataViewer.tsx (CSV generation client-side)
**Priority**: LOW
**Effort**: Low (1-2 hours)

### 7. Admin Panel
**Description**: View all user conversations (admin only)

**Implementation**: AdminConversationViewer.tsx
**Priority**: MEDIUM
**Effort**: Medium (4-6 hours)

## Feature Matrix

| Feature | Priority | Status | Dependencies |
|---------|----------|--------|--------------|
| JWT Auth | CRITICAL | Complete | PyJWT, bcrypt |
| NL to SQL | CRITICAL | Complete | Anthropic API |
| Chat History | HIGH | Complete | PostgreSQL |
| Visualizations | HIGH | Complete | Chart.js |
| Schema Viewer | MEDIUM | Complete | Database driver |
| CSV Export | LOW | Complete | Client-side JS |
| Admin Panel | MEDIUM | Complete | JWT is_admin flag |

## User Flows

### Primary Flow: Query Database
1. User types question: "How many fans are there?"
2. Backend streams SSE events: status -> thinking -> SQL -> results
3. Frontend displays table + auto-generated chart
4. User asks follow-up in same conversation

**Critical Path**: Auth -> Chat -> LLM -> Database -> Visualization

## Non-Functional Requirements

### Performance
- SQL generation: < 3 seconds
- Total response: < 10 seconds (with extended thinking)
- Query timeout: 30 seconds

### Security
- bcrypt hashing (12 rounds)
- JWT expiration (7 days)
- Read-only queries (SELECT only)
- Row limit: 1000 per query

### Usability
- Mobile-responsive (breakpoints: 768px, 1024px)
- Streaming feedback (loading states)
- Error messages user-friendly
