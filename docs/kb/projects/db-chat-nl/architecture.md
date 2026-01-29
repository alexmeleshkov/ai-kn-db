# Architecture

## Architecture Pattern
**Pattern**: Layered Monolith with separate frontend/backend

**Rationale**:
- Simplicity for MVP (single deployment)
- Clear separation of concerns (UI, API, data)
- Easy to understand and modify

**Trade-offs**:
- [+] Simple deployment, easy debugging
- [-] Scaling requires whole-app scaling

## System Components

Frontend (React + TypeScript)
    |
    v HTTPS/SSE
Backend (FastAPI + Python)
    |
    v
Databases (RDS PostgreSQL + Azure SQL)
External Services (Claude API)

### Frontend Layer
- Auth: Login/register, token management
- Chat: Message display, SSE streaming
- Visualizations: Chart.js components
- Schema Viewer: Database explorer

### Backend Layer
1. API Layer: FastAPI routes
2. Service Layer: Business logic
3. Data Layer: Database models

### Data Layer
- AWS RDS PostgreSQL: App data
- Azure SQL Server: Client data (read-only)

## Communication Patterns

### Frontend <-> Backend
- REST API: Auth, conversations
- SSE Streaming: Real-time chat
- JWT Bearer tokens

### Backend <-> Claude API
- Tool Use: Agentic workflow
- Extended Thinking: Complex queries
- Streaming responses

## Design Decisions

### Decision 1: Self-Hosted JWT Auth
**Choice**: PyJWT + bcrypt

**Rationale**: Cost savings, full control, no vendor lock-in

### Decision 2: SSE vs WebSockets
**Choice**: Server-Sent Events

**Rationale**: One-way sufficient, simpler, automatic reconnection

### Decision 3: Dual Database Architecture  
**Choice**: RDS (app) + Azure SQL (client)

**Rationale**: Security isolation, client data cannot migrate
