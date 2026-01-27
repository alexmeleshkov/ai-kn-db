# Repository Scan Snippets

## Directory Tree
```
./.gitignore
./ARCHITECTURE.md
./EVAL_CONTEXT.md
./Procfile
./README.md
./backend/.env.example
./backend/.gitignore
./backend/Dockerfile
./backend/Procfile
./backend/Q001.csv
./backend/app/__init__.py
./backend/app/api/__init__.py
./backend/app/api/admin_routes.py
./backend/app/api/auth_routes.py
./backend/app/api/conversation_routes.py
./backend/app/api/routes.py
./backend/app/core/__init__.py
./backend/app/core/config.py
./backend/app/core/logging.py
./backend/app/main.py
./backend/app/models/__init__.py
./backend/app/models/database.py
./backend/app/schemas/__init__.py
./backend/app/schemas/chat.py
./backend/app/services/__init__.py
./backend/app/services/app_data.py
./backend/app/services/auth.py
./backend/app/services/chat.py
./backend/app/services/conversations.py
./backend/app/services/database.py
./backend/app/services/database_azure.py
./backend/app/services/database_base.py
./backend/app/services/database_pg.py
./backend/app/services/ipswich_examples.py
./backend/app/services/learning_store.py
./backend/app/services/llm.py
./backend/app/services/query_intelligence.py
./backend/app/services/tasks.py
./backend/azure_schema.json
./backend/pytest.ini
./backend/requirements.txt
./backend/runtime.txt
./backend/scripts/add_indexes.sql
./backend/scripts/benchmark_dbs.py
./backend/scripts/continue_import.py
./backend/scripts/convert_json_to_parquet.py
./backend/scripts/convert_to_parquet.py
./backend/scripts/get_azure_schema.py
./backend/scripts/import_to_rds.py
./backend/scripts/migrate_from_supabase.py
./backend/scripts/quick_test.py
./backend/scripts/rds_schema.sql
./backend/scripts/supabase_schema.sql
./backend/scripts/test_chat.py
./backend/scripts/test_ipswich_live.py
./backend/static/assets/index-D0wYA8kv.css
./backend/static/assets/index-DqSzUETL.js
./backend/static/favicon.svg
./backend/static/index.html
./backend/test_results.json
./backend/tests/__init__.py
./backend/tests/test_api.py
./build.sh
./docker-compose.yml
./frontend/Dockerfile
./frontend/index.html
./frontend/nginx.conf
./frontend/package-lock.json
./frontend/package.json
./frontend/public/favicon.svg
./frontend/src/App.tsx
./frontend/src/components/AdminConversationViewer.tsx
./frontend/src/components/AuthPage.tsx
./frontend/src/components/ChatContainer.tsx
./frontend/src/components/ChatInput.tsx
./frontend/src/components/ChatMessage.tsx
./frontend/src/components/DataViewer.tsx
./frontend/src/components/DatabaseInfo.tsx
./frontend/src/components/QueryChart.tsx
./frontend/src/components/QueryHistory.tsx
./frontend/src/components/SidebarTabs.tsx
./frontend/src/hooks/useAuth.tsx
./frontend/src/hooks/useChat.ts
./frontend/src/hooks/useQueryHistory.ts
./frontend/src/hooks/useSuggestions.ts
./frontend/src/main.tsx
./frontend/src/services/api.ts
./frontend/src/styles/index.css
./frontend/src/types/chat.ts
./frontend/tsconfig.json
./frontend/tsconfig.node.json
./frontend/vite.config.ts
./requirements.txt
./runtime.txt
```

## Extension Statistics
```
     40 py
     13 tsx
      6 ts
      6 json
      4 txt
      3 sql
      3 md
      2 svg
      2 html
      2 gitignore
      2 css
      1 yml
      1 sh
      1 js
      1 ini
      1 example
      1 csv
      1 conf
```


## File: ./ARCHITECTURE.md
```
# DB Chat NL — Architecture

## Overview

Natural language interface for querying fan databases using AI.

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                    (React + TypeScript)                      │
│              Login │ Chat │ History │ Schema View            │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────▼────────────────────────────────┐
│                         Backend                              │
│                    (FastAPI + Python)                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Database   │  │  RDS App DB  │  │   Claude API     │   │
│  │  (Adapter)   │  │ (Auth+Data)  │  │   (LLM)          │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────┘   │
└─────────┼─────────────────┼─────────────────────────────────┘
          │                 │
    ┌─────▼─────┐    ┌──────▼──────┐
    │ Azure SQL │    │  AWS RDS    │
    │ (Ipswich) │    │ PostgreSQL  │
    │   Live    │    │ (App Data)  │
    └───────────┘    └─────────────┘
```

## Components

### 1. Frontend (React)
- **Location**: `/frontend`
- **Tech**: React 18, TypeScript, Vite
- **Features**:
  - Chat interface with streaming responses
  - User authentication (JWT-based)
  - Show/hide password toggle
  - Chat history sidebar
  - Database schema viewer
  - Query results with charts

### 2. Backend (FastAPI)
- **Location**: `/backend`
- **Tech**: Python 3.11, FastAPI, Uvicorn
- **Features**:
  - REST API endpoints
  - SSE streaming for chat responses
  - JWT authentication (bcrypt + PyJWT)
  - Azure SQL for Ipswich data queries
  - RDS PostgreSQL for app data

### 3. Data Layer

#### Database Architecture
| Database | Purpose | Location |
|----------|---------|----------|
| Azure SQL Server | Ipswich fan data (live) | `sql-sa-directsql-prod-001.database.windows.net` |
| AWS RDS PostgreSQL | App data (users, chats, learning) | `fan-data-db.cbpdozebsgdg.us-east-1.rds.amazonaws.com` |

#### Ipswich Data (Azure SQL Server - Live)
- **Server**: `sql-sa-directsql-prod-001.database.windows.net`
- **Database**: `IpswichTown_cdm`
- **Tables**: 13 (fan, communication, fan_attribute, etc.)
- **Rows**: 11M+ in communication table alone
- **Access**: Read-only, requires IP whitelist
- **Note**: Uses prefixed column names (e.g., `communication.fan_id`)

#### App Data (AWS RDS PostgreSQL)
- **Instance**: `fan-data-db.cbpdozebsgdg.us-east-1.rds.amazonaws.com`
- **Database**: `fandata`
- **Tables**:
  - `app_users` — User accounts (email, password_hash)
  - `conversations` — Chat sessions
  - `messages` — Chat messages
  - `learned_queries` — SQL learning system
- **Auth**: JWT tokens (7-day expiration)

### 4. AI Layer (Claude)
- **Model**: Claude Opus 4 (`claude-opus-4-20250514`)
- **Features**:
  - Natural language to SQL translation
  - Extended thinking for complex queries (5000 token budget)
  - Agentic tool use: `execute_sql`, `ask_clarification`
  - Query validation and retry (max 15 iterations)
  - SSE streaming with heartbeat (for Heroku 55s timeout)
  - Universal Learning System (learns from successful queries)
  - Ipswich-specific few-shot examples and glossary

## Authentication

### JWT-Based Auth (Self-Hosted)
Replaced Supabase Auth with self-hosted JWT solution:

```
User Login/Register
    │
    ▼
Backend validates credentials (bcrypt)
    │
    ▼
JWT Token generated (PyJWT, HS256)
    │
    ▼
Token stored in localStorage (7 days)
    │
    ▼
Token sent with API requests (Bearer)
    │
    ▼
Backend validates token signature
```

### Auth Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login user |
| POST | `/api/v1/auth/logout` | Logout user |
| GET | `/api/v1/auth/me` | Get current user |
| GET | `/api/v1/auth/status` | Check auth service status |

## Universal Learning System

The system learns from successful SQL queries to improve future accuracy:

```
User Question
    │
    ▼
Check learned_queries for similar questions
    │
    ▼
Include successful examples in LLM prompt
    │
    ▼
Generate SQL with few-shot learning
    │
    ▼
If successful, store query for future reference
```

**Features:**
- Stores successful queries per database
- Tracks error patterns to avoid repeating mistakes
- Auto-cleanup keeps max 100 queries per database
- Ipswich-specific static examples for common patterns

## API Endpoints

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Send message (async) |
| POST | `/api/v1/chat/stream` | Send message (SSE streaming) |

### Conversations (requires auth)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/conversations` | List user's conversations |
| POST | `/api/v1/conversations` | Create new conversation |
| GET | `/api/v1/conversations/{id}` | Get conversation with messages |
| PATCH | `/api/v1/conversations/{id}` | Update conversation title |
| DELETE | `/api/v1/conversations/{id}` | Delete conversation |

### Database
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/database/schema` | Get database schema |
| POST | `/api/v1/database/refresh-schema` | Refresh schema cache |

## Environment Variables

### Backend (.env / Heroku Config)
```bash
# Database mode
DB_MODE=azure

# Claude AI
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-opus-4-20250514

# Azure SQL Server (Ipswich Live Data)
AZURE_SQL_SERVER=sql-sa-directsql-prod-001.database.windows.net
AZURE_SQL_DATABASE=IpswichTown_cdm
AZURE_SQL_USER=ipswichtown-ro
AZURE_SQL_PASSWORD=...

# AWS RDS PostgreSQL (App Data)
POSTGRES_HOST=fan-data-db.cbpdozebsgdg.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DATABASE=fandata
POSTGRES_USER=dbadmin
POSTGRES_PASSWORD=...

# JWT Authentication
JWT_SECRET=<random-32-byte-base64-string>

```

## File: ./README.md
```
# ITFC Analysis

Natural language interface for querying Ipswich Town fan databases. Ask questions in plain English and get answers from your data.

**Live:** https://www.itfcanalysis.com

## Features

- Natural language to SQL conversion using Claude AI (Anthropic)
- Azure SQL Server for live Ipswich fan data queries
- Extended thinking for complex multi-step reasoning
- Self-hosted JWT authentication (bcrypt + PyJWT)
- Chat history persistence (AWS RDS PostgreSQL)
- Real-time SSE streaming responses
- Agentic SQL execution with clarification workflow
- Database schema viewer
- Query results with CSV export

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React 18, TypeScript, Vite |
| Backend | FastAPI, Python 3.11 |
| Fan Data | Azure SQL Server (live) |
| Auth/Chats | AWS RDS PostgreSQL (self-hosted) |
| AI | Claude Opus 4 + Extended Thinking |
| Hosting | Heroku (Standard-2X) |
| Proxy | QuotaGuard Static (SOCKS5) |
| Domain | GoDaddy DNS |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│                    (React + TypeScript)                      │
│              Login | Chat | History | Schema View            │
└────────────────────────────┬────────────────────────────────┘
                             | HTTPS
┌────────────────────────────▼────────────────────────────────┐
│                         Backend                              │
│                    (FastAPI + Python)                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Azure SQL   │  │   AWS RDS    │  │   Claude API     │   │
│  │  (Fan Data)  │  │ (Auth+Chats) │  │ (Opus 4 + Think) │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────┘   │
└─────────┼─────────────────┼─────────────────────────────────┘
          |                 |
    ┌─────▼─────┐    ┌──────▼──────┐
    │Azure SQL  │    │  AWS RDS    │
    │Server     │    │ PostgreSQL  │
    │(Ipswich)  │    │ (App Data)  │
    └───────────┘    └─────────────┘
```

## Performance

| Operation | Time |
|-----------|------|
| Schema loading | ~100-200ms |
| Simple query (COUNT) | ~100-300ms |
| Complex query (JOIN) | ~500-2000ms |
| Extended thinking | ~3-5s |
| Total response | ~5-10s (LLM + thinking) |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Anthropic API key
- Azure SQL Server access (for Ipswich data)
- AWS RDS PostgreSQL (for app data)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run development server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Build & Deploy

```bash
# Build frontend
cd frontend && npm run build

# Copy to backend static
cp -r dist/* ../backend/static/

# Deploy to Heroku (from backend folder)
cd ../backend
git add -A && git commit -m "Deploy" && git push heroku master
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `ANTHROPIC_MODEL` | Claude model (default: claude-opus-4-20250514) |
| `DB_MODE` | Database mode: `azure`, `postgres`, or `duckdb` |
| `AZURE_SQL_SERVER` | Azure SQL Server host |
| `AZURE_SQL_DATABASE` | Azure SQL database name |
| `AZURE_SQL_USER` | Azure SQL username |
| `AZURE_SQL_PASSWORD` | Azure SQL password |
| `POSTGRES_HOST` | RDS PostgreSQL host (for app data) |
| `POSTGRES_PORT` | RDS PostgreSQL port (default: 5432) |
| `POSTGRES_DATABASE` | RDS database name |
| `POSTGRES_USER` | RDS username |
| `POSTGRES_PASSWORD` | RDS password |
| `JWT_SECRET` | Secret key for JWT token signing |
| `QUOTAGUARDSTATIC_URL` | QuotaGuard SOCKS5 proxy URL (Heroku add-on) |

## Database Tables (Azure SQL - Ipswich Live)

| Table | Description |
|-------|-------------|
| fan | Fan profiles (address, contact info) |
| fan_attribute | Fan attributes and preferences |
| communication | Email/SMS communications |
| ticket | Ticket purchases and allocations |
| access | Stadium entry scans (attendance) |
| fan_permission_source | Permission sources |
| fan_permission | Marketing permissions |
| fan_source | How fans discovered the club |
| merchandise_sale | Merchandise purchases |
| membership | Membership records |
| fan_gdpr | GDPR compliance data |
| hospitality | Hospitality bookings |
| ballot | Ticket ballot entries |

**Note:** Column names use prefixes (e.g., `[fan.id]`, `[ticket.fan_id_beneficiary]`)

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Login user |
| GET | `/api/v1/auth/me` | Get current user |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/stream` | Send message (SSE streaming) |

### Conversations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/conversations` | List user's conversations |
| GET | `/api/v1/conversations/{id}` | Get conversation with messages |
| DELETE | `/api/v1/conversations/{id}` | Delete conversation |

### Database
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/database/schema` | Get database schema |

## Usage Examples

Ask questions like:
- "How many fans are there?"
- "Show me memberships by country"
- "What are the top 10 communication sources?"
- "Count fans with email permission"

## Project Structure

```
db-chat-nl/
```

## File: ./backend/.env.example
```
# Application Settings
APP_NAME=ITFC Analysis
DEBUG=false

# Anthropic Claude Configuration
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
ANTHROPIC_MODEL=claude-opus-4-20250514

# AWS S3 (Fan Data Storage)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_REGION=us-east-1
S3_BUCKET=fan-data-json-db

# Supabase (Auth + Chat History)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# DuckDB Settings
DUCKDB_IN_MEMORY=true

# Query Settings
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30

# CORS (comma-separated list, use * for same-origin)
CORS_ORIGINS=*
```

## File: ./backend/Dockerfile
```
# Backend Dockerfile
FROM python:3.11-slim

# Install ODBC driver dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## File: ./backend/app/main.py
```
"""
Main FastAPI application entry point.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .api import routes
from .api import auth_routes
from .api import conversation_routes
from .api import admin_routes
from .core.config import get_settings
from .core.logging import setup_logging
from .services.database import DatabaseService
from .services.database_pg import PostgresDatabaseService
from .services.database_azure import AzureSQLDatabaseService
from .services.llm import LLMService
from .services.chat import ChatService

# Optional: RDS app data services
try:
    import psycopg2
    from psycopg2 import pool
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initialize services once at startup.
    """
    logger = setup_logging()
    settings = get_settings()

    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    # Initialize RDS connection pool for app data (auth, conversations, learning)
    app_db_pool = None
    if PSYCOPG2_AVAILABLE and settings.postgres_host:
        try:
            app_db_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                host=settings.postgres_host,
                port=settings.postgres_port,
                user=settings.postgres_user,
                password=settings.postgres_password,
                database=settings.postgres_database
            )
            logger.info(f"RDS connection pool initialized: {settings.postgres_host}")

            # Initialize app data services
            from .services.app_data import init_app_data_service
            from .services.auth import init_auth_service

            init_app_data_service(app_db_pool)
            init_auth_service(app_db_pool)
            logger.info("App data and auth services initialized")
        except Exception as e:
            logger.warning(f"RDS connection failed: {e} - auth/conversations disabled")
            app_db_pool = None
    else:
        logger.info("RDS not configured - auth/conversations using local storage")

    # Initialize database service based on mode (for querying business data)
    logger.info(f"Initializing database service (mode: {settings.db_mode})...")
    if settings.db_mode == "azure":
        db_service = AzureSQLDatabaseService()
    elif settings.db_mode == "postgres":
        db_service = PostgresDatabaseService()
    else:
        db_service = DatabaseService()

    if db_service.test_connection():
        logger.info("Database connection successful")
        # Schema will be loaded lazily on first request to avoid slow S3 queries at startup
        logger.info(f"Schema will be loaded lazily (found {len(db_service._loaded_tables)} tables)")
    else:
        logger.warning("Database connection failed")

    logger.info("Initializing LLM service...")
    llm_service = LLMService()

    logger.info("Initializing chat service...")
    chat_service = ChatService(db_service, llm_service)

    # Store services in app state for access in routes
    app.state.db_service = db_service
    app.state.llm_service = llm_service
    app.state.chat_service = chat_service
    app.state.app_db_pool = app_db_pool

    logger.info("All services initialized")

    yield

    # Shutdown
    logger.info("Shutting down application")
    if app_db_pool:
        app_db_pool.closeall()
        logger.info("RDS connection pool closed")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Natural language interface for querying databases",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(routes.router, prefix=settings.api_prefix)
    app.include_router(auth_routes.router, prefix=settings.api_prefix)
    app.include_router(conversation_routes.router, prefix=settings.api_prefix)
    app.include_router(admin_routes.router, prefix=settings.api_prefix)

    # Serve frontend static files in production
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            """Serve the SPA for all non-API routes."""
            # Don't intercept API routes
            if full_path.startswith("api/"):
                return {"error": "Not found"}

            index_file = static_dir / "index.html"
            if index_file.exists():
                return FileResponse(index_file)
            return {"error": "Frontend not built"}

    return app


# Create application instance
app = create_app()
```

## File: ./docker-compose.yml
```
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    environment:
      - DEBUG=false
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped

networks:
  default:
    name: db-chat-nl-network
```

## File: ./frontend/package.json
```
{
  "name": "db-chat-nl-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "chart.js": "^4.5.1",
    "react": "^18.2.0",
    "react-chartjs-2": "^5.3.1",
    "react-dom": "^18.2.0",
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
```

## File: ./frontend/src/App.tsx
```
/**
 * Ipswich Town Fan Data Insights
 */

import { useState, useCallback, useEffect } from 'react';
import { ChatContainer } from './components/ChatContainer';
import { DataViewer } from './components/DataViewer';
import { SidebarTabs } from './components/SidebarTabs';
import { AuthPage } from './components/AuthPage';
import { AdminConversationViewer } from './components/AdminConversationViewer';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { getDatabaseSchema } from './services/api';
import type { TableSchema } from './types/chat';
import './styles/index.css';

type ViewMode = 'chat' | 'data' | 'admin-view';

function AppContent() {
  const [chatKey, setChatKey] = useState(0);
  const [viewMode, setViewMode] = useState<ViewMode>('chat');
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [tables, setTables] = useState<TableSchema[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const [adminViewConversationId, setAdminViewConversationId] = useState<string | null>(null);

  const { user, logout } = useAuth();

  // Fetch database schema for suggestions
  useEffect(() => {
    getDatabaseSchema()
      .then(schema => setTables(schema.tables))
      .catch(() => setTables([]));
  }, []);

  const handleNewChat = useCallback(() => {
    setChatKey(prev => prev + 1);
    setViewMode('chat');
    setSelectedTable(null);
    setSelectedConversationId(null);
    setAdminViewConversationId(null);
  }, []);

  const handleViewAdminConversation = useCallback((conversationId: string) => {
    setAdminViewConversationId(conversationId);
    setViewMode('admin-view');
  }, []);

  const handleClearChat = useCallback(() => {
    setChatKey(prev => prev + 1);
  }, []);

  const handleCloseDataViewer = useCallback(() => {
    setViewMode('chat');
    setSelectedTable(null);
  }, []);

  const handleSelectConversation = useCallback((conversationId: string) => {
    setSelectedConversationId(conversationId);
    setChatKey(prev => prev + 1);
    setViewMode('chat');
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        {/* Logo / Header */}
        <div className="sidebar-header">
          <div className="logo-circle">IT</div>
          <div className="logo-text">
            <h1>Ipswich Town</h1>
            <p>Fan Data Insights</p>
          </div>
        </div>

        {/* New Chat Button */}
        <button className="new-chat-btn" onClick={handleNewChat}>
          + New Chat
        </button>

        {/* Sidebar Tabs - Chats */}
        <SidebarTabs
          onSelectConversation={handleSelectConversation}
          onViewAdminConversation={handleViewAdminConversation}
          refreshTrigger={chatKey}
        />

        {/* User Menu */}
        {user && (
          <div className="user-menu">
            <div className="user-info">
              <span className="user-email">{user.email}</span>
              <button className="logout-btn" onClick={logout}>
                Logout
              </button>
            </div>
          </div>
        )}
      </aside>

      <main className="main-content">
        {viewMode === 'admin-view' && adminViewConversationId ? (
          <AdminConversationViewer
            conversationId={adminViewConversationId}
            onClose={handleNewChat}
          />
        ) : viewMode === 'data' && selectedTable ? (
          <DataViewer
            tableName={selectedTable}
            onClose={handleCloseDataViewer}
          />
        ) : (
          <ChatContainer
            key={chatKey}
            onClearChat={handleClearChat}
            tables={tables}
            conversationId={selectedConversationId}
          />
        )}
      </main>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AuthWrapper />
    </AuthProvider>
  );
}

function AuthWrapper() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-page">
        <div className="loading-spinner" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage />;
  }

  return <AppContent />;
}

export default App;
```

## File: ./frontend/tsconfig.json
```
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```
