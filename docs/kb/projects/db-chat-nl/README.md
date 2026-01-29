# Database Chat NL

A natural language chat interface for querying databases powered by Claude AI. Users ask questions in plain English, and Claude generates SQL queries, executes them with automatic retry on errors, and streams back results in real-time. Supports multiple database types (DuckDB for JSON, PostgreSQL, Azure SQL Server) with JWT authentication and conversation persistence.

## Quick Facts

- **Status**: stable
- **Stack**: React 18 + FastAPI + PostgreSQL
- **Architecture**: Layered (3-tier: Frontend -> API -> Services)
- **Deployment**: Docker Compose, Heroku-ready

## Core Capabilities

1. **User Authentication** - JWT-based auth with bcrypt password hashing, protected routes
2. **NL to SQL Generation** - Claude AI converts natural language questions to SQL queries with Tool Use
3. **Real-Time Streaming** - Server-Sent Events (SSE) stream AI responses with live progress indicators
4. **Database Introspection** - Automatic schema discovery for DuckDB, PostgreSQL, and Azure SQL Server
5. **Agentic SQL Execution** - Claude autonomously executes queries, handles errors, and retries with corrections
6. **Conversation Persistence** - Save and load chat conversations with message history in PostgreSQL
7. **Multi-Database Support** - Query JSON files (DuckDB), PostgreSQL (RDS), Azure SQL Server with single interface
8. **Query Intelligence** - Few-shot learning, query caching, error pattern detection, domain-specific glossaries
9. **Admin Panel** - Admin users can view all conversations across all users

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd db-chat-nl-master

# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials:
# - ANTHROPIC_API_KEY (required)
# - DATABASE_URL (PostgreSQL for auth/conversations)
# - JWT_SECRET (for token signing)

# Run with Docker Compose (recommended)
docker-compose up

# Or run separately:
# Backend: cd backend && python -m uvicorn app.main:app --reload
# Frontend: cd frontend && npm run dev
```

**Access**: http://localhost:3000 (frontend) | http://localhost:8000/api/v1 (backend API)

## Documentation

- **meta.yaml** - Project metadata, stack reference, capabilities, run commands
- **modules.md** - All 36 code modules with complete implementation patterns and file structure
- **tech.md** - Technology stack with rationale for each choice
- **architecture.md** - System design, layered architecture, agentic Tool Use pattern
- **deployment.md** - Build, run, test, and deploy commands with Docker configuration
- **uiDescription.md** - Frontend UI structure, components, and user flows

---

*This KB entry follows the Universal KB Standard for 1:1 project generation.*
