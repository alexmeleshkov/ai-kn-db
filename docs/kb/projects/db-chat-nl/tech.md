# Technology Stack

## Frontend

### React 18.2 with TypeScript
- **Purpose**: UI framework for interactive chat interface
- **Key Features Used**: Hooks (useState, useEffect, useCallback), TypeScript strict mode, memo for performance
- **Evidence**: frontend/package.json:11-13, ChatContainer.tsx uses hooks extensively

### Vite 5.0
- **Purpose**: Fast build tool and dev server
- **Key Features Used**: Hot module replacement, TypeScript support, optimized production builds
- **Evidence**: frontend/vite.config.ts:1-13, frontend/package.json:6-7

### React Markdown + remark-gfm
- **Purpose**: Render AI responses with markdown formatting (tables, code blocks)
- **Key Features Used**: GitHub Flavored Markdown support
- **Evidence**: ChatMessage.tsx:6-7, renders formatted SQL and tables

### Chart.js + react-chartjs-2
- **Purpose**: Data visualization for query results
- **Key Features Used**: Bar, line, pie charts with dynamic data
- **Evidence**: QueryChart.tsx:6-32, CHART_COLORS configuration

---

## Backend

### FastAPI 0.109+
- **Purpose**: High-performance Python API framework
- **Key Features Used**: Async routes, dependency injection, Pydantic validation, StreamingResponse for SSE
- **Evidence**: backend/requirements.txt:2, routes.py:93-218 (streaming endpoint)

### Uvicorn (ASGI Server)
- **Purpose**: Production-ready async server for FastAPI
- **Key Features Used**: WebSocket support, graceful shutdown, hot reload (dev)
- **Evidence**: backend/requirements.txt:3, main.py startup

### Pydantic 2.5+ with Email Support
- **Purpose**: Data validation and settings management
- **Key Features Used**: BaseModel for schemas, pydantic-settings for env vars, EmailStr validation
- **Evidence**: backend/requirements.txt:4-5, schemas/chat.py:10-154, core/config.py

---

## AI / LLM

### Anthropic Claude API 0.40+
- **Purpose**: Natural language to SQL generation with agentic Tool Use
- **Key Features Used**:
  - Tool Use (execute_sql, ask_clarification)
  - Streaming API with Server-Sent Events
  - Extended Thinking for complex reasoning
  - Automatic retry on query errors
- **Evidence**: backend/requirements.txt:11, llm.py:97-1054, AGENTIC_SYSTEM_PROMPT with tools

---

## Databases

### DuckDB 1.0+
- **Purpose**: Query JSON files locally without database setup
- **Key Features Used**:
  - `read_json_auto()` for dynamic JSON ingestion
  - S3 integration (`read_parquet()` from S3)
  - In-memory and file-based modes
  - Column name sanitization
- **Evidence**: backend/requirements.txt:8, database.py:14-708, S3 view creation at line 122-237

### PostgreSQL 14+ (via psycopg2)
- **Purpose**: Persistent storage for users, conversations, messages, learned queries
- **Key Features Used**:
  - Connection pooling
  - JSON column type for message metadata
  - Timestamp tracking (created_at, updated_at)
  - Foreign key constraints with CASCADE delete
- **Evidence**: backend/requirements.txt:14, app_data.py:1-658, schema usage throughout

### Azure SQL Server (python-tds)
- **Purpose**: Query live Azure SQL databases (Ipswich Town FC use case)
- **Key Features Used**:
  - Pure Python TDS protocol (no ODBC required)
  - SOCKS proxy support for IP whitelisting
  - T-SQL syntax translation (LIMIT -> TOP)
  - Prefixed column names (`[access.fan_id]`)
- **Evidence**: backend/requirements.txt:21-23, database_azure.py:1-418, SQL syntax conversion at line 255-277

---

## Authentication

### PyJWT 2.8+
- **Purpose**: JSON Web Token generation and verification
- **Key Features Used**: HS256 algorithm, expiration timestamps, token payload extraction
- **Evidence**: backend/requirements.txt:17, auth.py:17-94, create_token and verify_token methods

### bcrypt 4.1+
- **Purpose**: Password hashing with salt
- **Key Features Used**: Password hashing on registration, secure password comparison
- **Evidence**: backend/requirements.txt:18, auth.py:53-62, hash_password and verify_password

---

## Cloud Services

### AWS S3 (boto3 1.34+)
- **Purpose**: Store and query large JSON datasets without local storage
- **Key Features Used**:
  - List objects in bucket
  - Upload files to S3
  - Direct DuckDB queries from S3 (data stays remote)
- **Evidence**: backend/requirements.txt:26, database.py:122-237, routes.py:372-488 (S3 endpoints)

### SOCKS Proxy (PySocks 1.7+)
- **Purpose**: Route Azure SQL traffic through static IP proxy (IP whitelisting)
- **Key Features Used**: SOCKS5 proxy socket creation with authentication
- **Evidence**: backend/requirements.txt:29, database_azure.py:53-92, proxy socket setup

---

## Development Tools

### pytest + pytest-asyncio
- **Purpose**: Test framework for API and service testing
- **Key Features Used**: Async test support, fixtures, httpx integration
- **Evidence**: backend/requirements.txt:36-38, backend/tests/test_api.py

### python-dotenv
- **Purpose**: Load environment variables from .env files
- **Key Features Used**: Automatic .env loading on startup
- **Evidence**: backend/requirements.txt:34, core/config.py uses Settings

### TypeScript 5.2+
- **Purpose**: Type-safe JavaScript for frontend
- **Key Features Used**: Strict mode, interface definitions, type inference
- **Evidence**: frontend/tsconfig.json:2-20, all .ts/.tsx files

---

## Deployment

### Docker + Docker Compose
- **Purpose**: Containerized deployment with multi-service orchestration
- **Key Features Used**:
  - Multi-stage builds for frontend (Vite build -> nginx)
  - Backend healthcheck endpoints
  - Network isolation
  - Environment variable injection
- **Evidence**: docker-compose.yml:1-34, backend/Dockerfile, frontend/Dockerfile

### nginx (frontend serving)
- **Purpose**: Production-ready static file serving
- **Key Features Used**: Single-page app routing, gzip compression, proxy pass to backend
- **Evidence**: frontend/nginx.conf, frontend/Dockerfile:7-11

---

## Key Technology Decisions

1. **DuckDB over traditional RDBMS for JSON**: Enables querying JSON files without database setup, perfect for quick data exploration
2. **FastAPI over Flask/Django**: Async support critical for SSE streaming, automatic OpenAPI docs
3. **Claude Tool Use over prompt engineering**: Agentic approach allows Claude to autonomously execute and retry queries
4. **Server-Sent Events over WebSockets**: Simpler for one-way streaming, better browser compatibility
5. **JWT over session cookies**: Stateless authentication works across distributed deployments
6. **PostgreSQL for persistence over Supabase**: Self-hosted solution after Supabase migration, full control
7. **Extended Thinking for complex queries**: Improves accuracy on multi-step SQL generation
8. **Chart.js over D3.js**: Simpler API for standard chart types, smaller bundle size
