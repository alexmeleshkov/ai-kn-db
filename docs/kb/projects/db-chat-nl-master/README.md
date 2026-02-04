# Database Chat NL (Master)

A natural language to SQL chat application that enables users to query PostgreSQL databases using conversational language. Built with Claude API for AI-powered query generation, featuring real-time streaming responses, automatic chart visualization, and a comprehensive learning system that improves query accuracy over time. The application includes JWT authentication, conversation persistence, admin panel, and specialized support for domain-specific databases (e.g., Ipswich Town FC fan data).

## Quick Facts

- **Status**: reference
- **Stack**: React 18 + TypeScript + FastAPI + PostgreSQL
- **Architecture**: Layered - SPA frontend, RESTful backend with service layer, PostgreSQL persistence
- **Deployment**: Docker-based with Vite frontend build

## Core Capabilities

1. **JWT Authentication** - Secure user login with JWT tokens and bcrypt password hashing
2. **Natural Language to SQL** - AI-powered query generation using Claude API with Tool Use and extended thinking
3. **Real-Time Chat** - Interactive chat interface with SSE streaming, clarification requests, and conversation history
4. **Schema Introspection** - Dynamic database schema discovery and metadata extraction for PostgreSQL and Azure SQL
5. **Query Validation** - Schema-based SQL validation with error context generation and retry suggestions
6. **Learning Store** - Persistent storage of successful query patterns with similarity-based retrieval for few-shot learning
7. **Data Visualization** - Automatic chart generation (bar/line/pie) for query results with Ipswich Town color palette
8. **Admin Panel** - Admin interface for viewing all user conversations with read-only access
9. **Query Intelligence** - LRU caching, error analysis, and context-aware query suggestions
10. **Data Streaming** - Server-Sent Events (SSE) for real-time responses with heartbeat polling to prevent timeouts

## Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd db-chat-nl-master

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Configure environment
cp .env.example .env
# Required variables:
#   ANTHROPIC_API_KEY - Your Claude API key
#   DATABASE_URL - PostgreSQL connection string
#   JWT_SECRET - Secret for JWT signing
#   POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE
#   ADMIN_API_KEY - For admin panel access

# Run with Docker
docker-compose up

# Or run separately:
# Backend: python -m uvicorn app.main:app --reload --port 8000
# Frontend: npm run dev
```

**Access**: http://localhost:5173 (frontend) | http://localhost:8000 (backend) | http://localhost:8000/docs (API docs)

## Documentation

- **meta.yaml** - Project metadata, capabilities (10), technologies (9), run commands
- **features.md** - Links to 10 feature documentation files (jwt-authentication, natural-language-sql, etc.)
- **tech.md** - Links to 10 technology documentation files (fastapi, anthropic-claude, postgresql, etc.)
- **architecture.md** - System design, architectural patterns, file structure, component relationships
- **deployment.md** - Environment variables, build commands, deployment configuration
- **uiDescription.md** - UI structure, component hierarchy, Ipswich Town branding
- **custom-modules.md** - Project-specific implementation patterns

## Key Features

- **Extended Thinking** - Claude API extended thinking mode with real-time thought preview in UI
- **Clarification Requests** - AI can ask for clarification with multiple-choice options when queries are ambiguous
- **Few-Shot Learning** - 20+ pre-loaded Ipswich Town FC examples plus similarity-based retrieval of past successful queries
- **Query History** - localStorage persistence with deduplication and 50-item limit
- **Context-Aware Suggestions** - Auto-complete suggestions based on schema, history, and input
- **JSON Upload** - Upload JSON files to create database tables dynamically
- **S3 Integration** - List and load files from AWS S3 buckets
- **CSV Export** - Export query results to CSV with proper escaping
- **Progress Indicators** - Time-based progress messages and "Try simpler question" button for long queries
- **Heartbeat Polling** - 15-second heartbeat during SQL execution to prevent Heroku 55-second timeout
- **Responsive Design** - Mobile-friendly layout with breakpoint at 768px
- **Ipswich Town Branding** - Custom color scheme (#0E4C92 blue, #FFFFFF white, #D4AF37 gold) throughout UI

---

*This KB entry follows the Universal KB Standard for 1:1 project generation.*
