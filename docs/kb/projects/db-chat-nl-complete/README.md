# Database Chat NL (Complete)

Natural language interface for querying Ipswich Town fan databases. Ask questions in plain English and get answers from your data using Claude AI with extended thinking, real-time SSE streaming, self-hosted JWT authentication, and persistent chat history.

## Quick Facts

- **Status**: reference
- **Stack**: React 18 + TypeScript + FastAPI + Python 3.11 + PostgreSQL + Azure SQL
- **Architecture**: Layered Monolith (Frontend → Backend API → Services → Database)
- **Deployment**: Docker Compose, Heroku (production)

## Core Capabilities

1. **Natural Language to SQL** - Claude Opus 4 converts user questions to SQL queries with extended thinking for complex reasoning
2. **Real-time Streaming** - Server-Sent Events (SSE) for low-latency chat responses with thinking indicators
3. **JWT Authentication** - Self-hosted authentication with bcrypt password hashing and PyJWT token management
4. **Conversation Persistence** - Chat history stored in PostgreSQL with in-memory LRU caching for LLM context
5. **Multi-Database Support** - PostgreSQL (RDS), Azure SQL Server, and DuckDB with abstract base class pattern
6. **Schema Introspection** - Automatic database schema loading with table/column metadata for LLM context
7. **Few-Shot Learning** - Similarity-based query example retrieval to improve query quality
8. **Agentic Tool Use** - Claude executes SQL and asks clarification questions autonomously
9. **Query Visualization** - Auto-detect chart types (bar, line, pie) or display as tables
10. **Admin Panel** - Cross-user conversation viewer and user management for admins
11. **Query History** - Persistent history with date grouping and re-execution
12. **Extended Thinking** - Claude configured with extended thinking budget for complex multi-step reasoning

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd db-chat-nl

# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials:
#   - ANTHROPIC_API_KEY (required)
#   - POSTGRES_* (required for app data)
#   - AZURE_SQL_* or DB_MODE=duckdb (required for query database)
#   - JWT_SECRET (required for auth)

# Run with Docker Compose
docker-compose up

# Or run separately:
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

**Access**: http://localhost:5173 (frontend) | http://localhost:8000 (backend)

## Documentation

- **meta.yaml** - Project metadata, stack reference, capabilities, run commands
- **modules.md** - Complete code patterns with all 36 tier1 files for 1:1 generation
- **tech.md** - Technology stack with rationale (React, FastAPI, Claude, PostgreSQL, Azure SQL)
- **architecture.md** - Layered architecture with component relationships and data flow
- **deployment.md** - Setup, build, run, and deploy commands with full environment variable list
- **uiDescription.md** - UI structure, component hierarchy, and user flows

---

*This KB entry follows the Universal KB Standard for 1:1 project generation.*
