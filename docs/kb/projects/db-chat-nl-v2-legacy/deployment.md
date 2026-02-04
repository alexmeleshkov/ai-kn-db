# Deployment & Operations

> **Purpose**: Document exact commands to build, run, test, and deploy.
> This enables README generation and smoke test implementation.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for application + database

### Required Software
- **Node.js** - 18.0.0 or higher
- **Python** - 3.11 or higher
- **PostgreSQL** - 14 or higher (or use Docker)
- **Docker** - 24.0+ (optional, recommended for database)
- **Docker Compose** - 2.0+ (optional)

### Required Credentials
- **Anthropic API Key** - Required for Claude API access. Get from: https://console.anthropic.com/
- **PostgreSQL Database** - For application data (conversations, users, learned queries)
- **AWS S3 Credentials** - Optional, for S3 file storage. Get from: AWS Console → IAM
- **Azure SQL Credentials** - Optional, for Azure SQL querying. Get from: Azure Portal

---

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd db-chat-nl-v2
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Setup

**Option A: Docker (Recommended)**
```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Wait for PostgreSQL to be ready (about 5 seconds)
```

**Option B: Local PostgreSQL**
```bash
# Create database
createdb db_chat_nl

# Run schema migrations
psql db_chat_nl < backend/schema.sql
```

### 5. Environment Configuration

> **IMPORTANT**: This project requires several environment variables for configuration.

Create `.env` files for backend and frontend:

```bash
# Backend environment
cp backend/.env.example backend/.env

# Frontend environment (if needed)
cp frontend/.env.example frontend/.env
```

**Backend Environment Variables** (`backend/.env`):

| Variable | Required | Default | Description | Where to Get |
|----------|----------|---------|-------------|--------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | - | Claude API key for LLM | Anthropic Console |
| `DATABASE_URL` | ✅ Yes | - | PostgreSQL connection for app data | `postgresql://user:pass@localhost:5432/dbname` |
| `JWT_SECRET` | ✅ Yes | - | Secret for JWT token signing | Generate with `openssl rand -hex 32` |
| `CORS_ORIGINS` | ⚠️ Optional | `*` | Allowed CORS origins | `http://localhost:5173` for dev |
| `ANTHROPIC_MODEL` | ⚠️ Optional | `claude-opus-4-20250514` | Claude model to use | - |
| `ANTHROPIC_MAX_TOKENS` | ⚠️ Optional | `16000` | Max tokens in response | - |
| `ENABLE_EXTENDED_THINKING` | ⚠️ Optional | `true` | Enable extended thinking | - |
| `THINKING_BUDGET_TOKENS` | ⚠️ Optional | `5000` | Tokens for thinking | - |
| `DB_MODE` | ⚠️ Optional | `duckdb` | Database mode: duckdb, postgres, azure | - |
| `DUCKDB_IN_MEMORY` | ⚠️ Optional | `false` | Use in-memory DuckDB | - |
| `POSTGRES_HOST` | ⚠️ Optional | - | PostgreSQL RDS host (for db_mode=postgres) | - |
| `POSTGRES_PORT` | ⚠️ Optional | `5432` | PostgreSQL RDS port | - |
| `POSTGRES_USER` | ⚠️ Optional | - | PostgreSQL RDS username | - |
| `POSTGRES_PASSWORD` | ⚠️ Optional | - | PostgreSQL RDS password | - |
| `POSTGRES_DATABASE` | ⚠️ Optional | - | PostgreSQL RDS database name | - |
| `AZURE_SQL_SERVER` | ⚠️ Optional | - | Azure SQL server (for db_mode=azure) | Azure Portal |
| `AZURE_SQL_DATABASE` | ⚠️ Optional | - | Azure SQL database name | Azure Portal |
| `AZURE_SQL_USER` | ⚠️ Optional | - | Azure SQL username | Azure Portal |
| `AZURE_SQL_PASSWORD` | ⚠️ Optional | - | Azure SQL password | Azure Portal |
| `SOCKS_PROXY` | ⚠️ Optional | - | SOCKS proxy for Azure SQL (host:port) | - |
| `AWS_ACCESS_KEY_ID` | ⚠️ Optional | - | AWS access key for S3 | AWS Console → IAM |
| `AWS_SECRET_ACCESS_KEY` | ⚠️ Optional | - | AWS secret key for S3 | AWS Console → IAM |
| `AWS_REGION` | ⚠️ Optional | `us-east-1` | AWS region for S3 | - |
| `S3_BUCKET` | ⚠️ Optional | - | S3 bucket name for file storage | - |
| `DEBUG` | ⚠️ Optional | `false` | Enable debug logging | - |

**Example `.env` file** (`backend/.env`):
```bash
# === Required Configuration ===
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/db_chat_nl
JWT_SECRET=your-secret-key-here-use-openssl-rand-hex-32

# === Application Settings ===
CORS_ORIGINS=http://localhost:5173
ANTHROPIC_MODEL=claude-opus-4-20250514
ANTHROPIC_MAX_TOKENS=16000
ENABLE_EXTENDED_THINKING=true
THINKING_BUDGET_TOKENS=5000

# === Database Mode (choose one) ===
# Option 1: DuckDB for local JSON files
DB_MODE=duckdb
DUCKDB_IN_MEMORY=false

# Option 2: PostgreSQL for RDS querying
# DB_MODE=postgres
# POSTGRES_HOST=your-rds-host.amazonaws.com
# POSTGRES_PORT=5432
# POSTGRES_USER=your-username
# POSTGRES_PASSWORD=your-password
# POSTGRES_DATABASE=your-database

# Option 3: Azure SQL for business data
# DB_MODE=azure
# AZURE_SQL_SERVER=your-server.database.windows.net
# AZURE_SQL_DATABASE=your-database
# AZURE_SQL_USER=your-username
# AZURE_SQL_PASSWORD=your-password
# SOCKS_PROXY=proxy-host:1080

# === Optional S3 Configuration ===
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_REGION=us-east-1
# S3_BUCKET=your-bucket-name

# === Optional Settings ===
# DEBUG=true
```

**Frontend Environment Variables** (`frontend/.env`):

Frontend primarily uses backend API, minimal environment configuration needed.

```bash
# API endpoint (usually not needed in dev, proxied by Vite)
VITE_API_URL=http://localhost:8000
```

**Security Notes**:
- Never commit `.env` to version control
- `.env` is in `.gitignore`
- Use `.env.example` as template (with no real secrets)
- Rotate keys regularly for production
- Store production secrets in secure vault (AWS Secrets Manager, Azure Key Vault, etc.)

---

## Running the Application

### Development Mode

**Option 1: Docker Compose (Recommended)**
```bash
# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

**Option 2: Run services separately**

Terminal 1 - Database:
```bash
docker-compose up postgres
```

Terminal 2 - Backend:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
# Or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

Access same URLs as Docker Compose option.

---

## Building for Production

### Backend Build
```bash
cd backend

# Build Docker image
docker build -t db-chat-nl-backend:latest .

# Or create distribution package
python -m pip install --upgrade build
python -m build
```

### Frontend Build
```bash
cd frontend

# Build static files
npm run build

# Output in: frontend/dist/
```

### Full Stack Build
```bash
# Build all services
docker-compose build

# Or build specific service
docker-compose build backend
docker-compose build frontend
```

---

## Production Deployment

### Docker Compose Production

**docker-compose.prod.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: db_chat_nl
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - CORS_ORIGINS=${CORS_ORIGINS}
    depends_on:
      - postgres
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  postgres_data:
```

**Deploy**:
```bash
# Set environment variables
export DATABASE_URL="postgresql://user:pass@postgres:5432/db_chat_nl"
export ANTHROPIC_API_KEY="sk-ant-..."
export JWT_SECRET="your-secret"
export CORS_ORIGINS="https://yourdomain.com"

# Start production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

### Cloud Deployment Options

**AWS Deployment**:
1. **ECS/Fargate**: Deploy backend and frontend as separate tasks
2. **RDS PostgreSQL**: Use managed PostgreSQL for application data
3. **CloudFront + S3**: Serve frontend static files
4. **Application Load Balancer**: Route traffic to backend
5. **Secrets Manager**: Store API keys and secrets

**Azure Deployment**:
1. **App Service**: Deploy backend as Python app
2. **Static Web Apps**: Host frontend
3. **Azure Database for PostgreSQL**: Managed database
4. **Azure Key Vault**: Store secrets
5. **Application Gateway**: Load balancing

**DigitalOcean Deployment**:
1. **App Platform**: Deploy backend and frontend
2. **Managed PostgreSQL**: Database hosting
3. **Spaces**: Object storage (S3-compatible)

---

## Database Migrations

**Initial Schema** (`backend/schema.sql`):
```sql
-- Users table
CREATE TABLE IF NOT EXISTS app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

CREATE INDEX idx_app_users_email ON app_users(email);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);

-- Learned queries table
CREATE TABLE IF NOT EXISTS learned_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    database_id VARCHAR(255) NOT NULL,
    database_type VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    execution_time_ms INTEGER,
    row_count INTEGER,
    error_pattern VARCHAR(255),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_learned_queries_database_usage ON learned_queries(database_id, usage_count DESC, last_used_at DESC);
```

**Run migrations**:
```bash
# Development
psql $DATABASE_URL -f backend/schema.sql

# Production (via Docker)
docker-compose exec postgres psql -U postgres -d db_chat_nl -f /schema.sql
```

---

## Monitoring & Logging

### Application Logs

**Backend logs**:
```bash
# Development (terminal)
python -m app.main

# Docker
docker-compose logs -f backend

# Production (journald)
journalctl -u db-chat-nl-backend -f
```

**Frontend logs**:
```bash
# Development
npm run dev

# Docker
docker-compose logs -f frontend

# Browser console
# Open DevTools → Console
```

### Health Checks

**Backend health endpoint**:
```bash
curl http://localhost:8000/health

# Response:
# {"status": "healthy", "database_connected": true}
```

**Database connection test**:
```bash
psql $DATABASE_URL -c "SELECT 1;"
```

---

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/
```

**Note**: Test suite not implemented in scanned repository (reference project).

### Frontend Tests

```bash
cd frontend
npm run test
```

**Note**: Test suite not implemented in scanned repository (reference project).

### Manual Testing Checklist

**Authentication**:
- [ ] Register new user
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should fail)
- [ ] Access protected route without token (should fail)
- [ ] Access admin route as non-admin (should fail)

**Chat**:
- [ ] Send message and receive streaming response
- [ ] View query results in table format
- [ ] Download query results as CSV
- [ ] Visualize results in chart (bar, line, pie)
- [ ] Start new conversation
- [ ] Load existing conversation

**Database**:
- [ ] Upload JSON file
- [ ] View loaded tables
- [ ] Browse table data
- [ ] Delete loaded table
- [ ] Connect to PostgreSQL (if configured)
- [ ] Connect to Azure SQL (if configured)

**Admin** (if is_admin=true):
- [ ] View all conversations
- [ ] View specific conversation from another user
- [ ] View all users

---

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError: No module named 'anthropic'`**
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Error: `psycopg2.OperationalError: could not connect to server`**
```bash
# Solution: Start PostgreSQL
docker-compose up -d postgres

# Or check DATABASE_URL is correct
echo $DATABASE_URL
```

**Error: `anthropic.AuthenticationError: Invalid API Key`**
```bash
# Solution: Check ANTHROPIC_API_KEY
echo $ANTHROPIC_API_KEY

# Get new key from https://console.anthropic.com/
```

### Frontend won't start

**Error: `Error: Cannot find module 'react'`**
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Error: `Network error when calling backend API`**
```bash
# Solution: Check backend is running
curl http://localhost:8000/health

# Start backend if not running
cd backend && python -m app.main
```

### Database issues

**Error: `relation "app_users" does not exist`**
```bash
# Solution: Run migrations
psql $DATABASE_URL -f backend/schema.sql
```

**Error: `database "db_chat_nl" does not exist`**
```bash
# Solution: Create database
createdb db_chat_nl
```

---

## Performance Tuning

### Backend

- **Connection pooling**: Adjust `minconn` and `maxconn` in `main.py` (default 1-5)
- **Schema caching**: Use `/database/refresh-schema` to update cached schema
- **Conversation limit**: Adjust `max_conversations` in `conversations.py` (default 100)
- **Query timeout**: Set database timeout in connection string

### Frontend

- **Code splitting**: Already enabled via Vite
- **Lazy loading**: Use React.lazy for large components
- **Caching**: Browser caches static assets (configured in nginx/Dockerfile)

### Database

- **Indexes**: Already created on user_id, conversation_id, email
- **Vacuum**: Run `VACUUM ANALYZE` periodically on PostgreSQL
- **Connection limit**: Set `max_connections` in postgresql.conf

---

## Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240101.sql

# Docker backup
docker-compose exec postgres pg_dump -U postgres db_chat_nl > backup.sql
```

### Application State

- **Conversations**: Stored in PostgreSQL (backed up with database)
- **Learned queries**: Stored in PostgreSQL (backed up with database)
- **In-memory state**: Lost on restart (conversation context, task status)

---

## Security Hardening

### Production Checklist

- [ ] Set strong `JWT_SECRET` (use `openssl rand -hex 32`)
- [ ] Restrict `CORS_ORIGINS` to your domain
- [ ] Use HTTPS (add nginx reverse proxy with SSL)
- [ ] Set `DEBUG=false`
- [ ] Use managed PostgreSQL with SSL (RDS, Azure Database)
- [ ] Store secrets in vault (AWS Secrets Manager, Azure Key Vault)
- [ ] Enable database connection encryption
- [ ] Set up firewall rules (allow only necessary ports)
- [ ] Regular dependency updates (`pip list --outdated`, `npm outdated`)
- [ ] Enable logging and monitoring
- [ ] Set up automated backups
- [ ] Implement rate limiting (nginx `limit_req_zone`)

---

*This deployment guide covers development setup, production deployment, and operational procedures for the DB Chat NL v2 application.*
