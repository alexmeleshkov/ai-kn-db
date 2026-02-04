# Database Chat with Natural Language (v2)

A chat interface for querying databases using natural language powered by Anthropic Claude. Users can ask questions in plain English and the system translates them to SQL, executes queries, and presents results with visualizations. Supports multiple database types (PostgreSQL, Azure SQL, DuckDB) with intelligent query learning and caching.

## Quick Facts

- **Status**: reference
- **Stack**: React 18 + TypeScript + FastAPI + PostgreSQL + Claude API
- **Architecture**: Layered monolith with service layer architecture
- **Deployment**: Docker Compose with multi-stage builds

## Core Capabilities

1. **User Authentication** - JWT-based authentication with bcrypt password hashing, registration, and login
2. **Natural Language to SQL** - Anthropic Claude with Tool Use for agentic SQL generation from conversational input
3. **Real-time Streaming** - Server-Sent Events (SSE) for streaming LLM responses and query execution updates
4. **Data Visualization** - Interactive charts (bar, line, pie) using Recharts for query results
5. **Multi-Database Support** - Connect to PostgreSQL, Azure SQL Server (with SOCKS proxy), and DuckDB (with S3 integration)
6. **Query Learning System** - Automatically learns successful query patterns with usage tracking and LRU eviction (max 100 per database)
7. **Conversation Management** - Full CRUD operations with PostgreSQL persistence and dual storage (in-memory for LLM context)
8. **Admin Dashboard** - Cross-user conversation viewing and user management for administrators
9. **File Upload & S3 Integration** - Upload JSON files to DuckDB or load from S3 buckets
10. **Schema Introspection** - Dynamic database schema discovery with table relationships and sample data for LLM context
11. **Autocomplete Suggestions** - Input autocomplete for table names, column names, and query templates
12. **Markdown Rendering** - Rich message formatting with code highlighting and table rendering

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd db-chat-nl-v2

# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Required variables:
#   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
#   JWT_SECRET=your-secret-key
#   ANTHROPIC_API_KEY=sk-ant-...
#   CORS_ORIGINS=http://localhost:5173

# Run with Docker Compose
docker-compose up

# Or run manually:
# Terminal 1 - PostgreSQL
docker-compose up -d postgres

# Terminal 2 - Backend
cd backend
python -m app.main

# Terminal 3 - Frontend
cd frontend
npm run dev
```

**Access**: [http://localhost:5173](http://localhost:5173) (frontend) | [http://localhost:8000](http://localhost:8000) (backend)

## Key Features

### Intelligent SQL Generation
- Uses Claude's Tool Use API for agentic SQL generation
- Learns from successful queries and reuses patterns
- Provides few-shot examples for domain-specific data (Ipswich Town FC sample)
- Validates queries before execution
- Caches results for identical questions

### Dual Conversation Storage
- **PostgreSQL**: Durable persistence for user conversations and messages
- **In-memory**: Fast LRU-based conversation store for LLM context (max 10 messages)
- Automatic conversation creation from first message
- Auto-generated titles from first 50 characters

### Multi-Database Architecture
- **DuckDB**: Local JSON querying with S3 support for analytics
- **PostgreSQL**: RDS connections for production databases
- **Azure SQL**: Business data access with SOCKS proxy support for secure networks
- Abstract base class for consistent database service interface

### Security & Authentication
- JWT stateless authentication (1-week expiration)
- Bcrypt password hashing with automatic salt generation
- Role-based access control (admin flag)
- CORS configuration for frontend origins
- User-scoped data access (conversations, messages)

### Admin Features
- View all conversations across all users
- View conversation details with messages
- User management with conversation counts
- Clear learned query cache by database

## Documentation

- **meta.yaml** - Project metadata, capabilities, technology stack, run commands
- **modules.md** - Complete code patterns with all 47 files documented
- **tech.md** - Technology stack details with versions and dependencies
- **architecture.md** - System design, layers, data flow, and architectural patterns
- **deployment.md** - Docker configuration, environment variables, and deployment steps
- **uiDescription.md** - UI structure, components, and user interactions

---

*This KB entry was generated from a complete repository scan with 47 files extracted across backend and frontend.*
