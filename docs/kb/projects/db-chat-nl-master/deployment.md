# Deployment & Operations

> **Purpose**: Document exact commands to build, run, test, and deploy.
> This enables README generation and smoke test implementation.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows (with WSL recommended)
- **Memory**: Minimum 4GB RAM (8GB recommended for development)
- **Disk Space**: 2GB for dependencies and build artifacts

### Required Software
- **Python** - >= 3.11 (for FastAPI backend with asyncio improvements)
- **Node.js** - >= 18.0.0 (for Vite and React 18)
- **PostgreSQL** - >= 14 (for database persistence)
- **Docker** - >= 24.0 (optional, for containerized deployment)

### Required Credentials
- **Anthropic API Key** - Claude API access from https://console.anthropic.com/
- **PostgreSQL Database** - Connection string or individual credentials (host, port, user, password, database)
- **JWT Secret** - Random string for JWT token signing (generate with `openssl rand -hex 32`)
- **Admin API Key** - Secret key for admin panel access (generate with `openssl rand -hex 32`)

---

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repo-url>
cd db-chat-nl-master
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

**Key dependencies**:
- fastapi - ASGI web framework
- uvicorn - ASGI server
- anthropic - Claude API client
- psycopg2-binary - PostgreSQL driver
- sqlalchemy - ORM
- pyjwt - JWT token handling
- bcrypt - Password hashing

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

**Key dependencies**:
- react - UI library
- typescript - Type safety
- vite - Build tool and dev server
- chart.js - Data visualization
- react-markdown - Markdown rendering

### 4. Database Setup
```bash
# Option 1: Local PostgreSQL
createdb db_chat_nl
psql db_chat_nl < schema.sql  # If schema file exists

# Option 2: Docker PostgreSQL
docker run --name db-chat-nl-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=db_chat_nl \
  -p 5432:5432 \
  -d postgres:14
```

**Schema initialization**: Tables (users, conversations, conversation_messages, learned_queries) are created automatically by SQLAlchemy on first run.

### 5. Environment Configuration

> **IMPORTANT**: Document ALL environment variables used in the project.

Create `.env` file in backend root:

```bash
cd backend
cp .env.example .env
# Edit .env with your actual values
```

**Environment Variables**:

| Variable | Required | Default | Description | Where to Get |
|----------|----------|---------|-------------|--------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | - | Claude API key for NL to SQL generation | Anthropic Console (console.anthropic.com) |
| `DATABASE_URL` | ✅ Yes | - | PostgreSQL connection string (format: postgresql://user:pass@host:port/db) | Your PostgreSQL instance |
| `JWT_SECRET` | ✅ Yes | - | Secret key for JWT token signing | Generate: `openssl rand -hex 32` |
| `POSTGRES_HOST` | ✅ Yes | `localhost` | PostgreSQL server hostname | Your PostgreSQL instance |
| `POSTGRES_PORT` | ✅ Yes | `5432` | PostgreSQL server port | Your PostgreSQL instance |
| `POSTGRES_USER` | ✅ Yes | `postgres` | PostgreSQL username | Your PostgreSQL instance |
| `POSTGRES_PASSWORD` | ✅ Yes | - | PostgreSQL password | Your PostgreSQL instance |
| `POSTGRES_DATABASE` | ✅ Yes | `db_chat_nl` | PostgreSQL database name | Your PostgreSQL instance |
| `ADMIN_API_KEY` | ✅ Yes | - | Secret key for admin panel authentication | Generate: `openssl rand -hex 32` |
| `CORS_ORIGINS` | ⚠️ Optional | `http://localhost:5173` | Allowed CORS origins (comma-separated) | - |
| `DATABASE_TYPE` | ⚠️ Optional | `postgres` | Database type (postgres, azure, duckdb) | - |

**Example `.env` file**:
```bash
# === API Keys & Secrets ===
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
ADMIN_API_KEY=admin-key-a1b2c3d4e5f6g7h8i9j0

# === Database Configuration ===
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/db_chat_nl
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DATABASE=db_chat_nl

# === Application Settings ===
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DATABASE_TYPE=postgres

# === Optional Features ===
# AWS_ACCESS_KEY_ID=your-aws-key  # For S3 file integration
# AWS_SECRET_ACCESS_KEY=your-aws-secret
# AWS_REGION=us-east-1
# AWS_BUCKET_NAME=your-bucket
```

**Security Notes**:
- Never commit `.env` to version control
- `.env` is in `.gitignore`
- Use `.env.example` as template (with no real secrets)
- Rotate keys regularly for production
- Use strong, random values for JWT_SECRET and ADMIN_API_KEY (minimum 32 bytes)

---

## Running the Application

### Development Mode

**Option 1: Run services separately**
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Option 2: Docker Compose**
```bash
docker-compose up
```

**Access**:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs (FastAPI Swagger UI)
- Health Check: http://localhost:8000/health

---

### Production Mode

```bash
# Build frontend
cd frontend
npm run build

# Serve with backend
cd ../backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Production considerations**:
- Use gunicorn or similar ASGI server for production: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
- Serve frontend build (dist/) with nginx or similar
- Enable HTTPS (SSL/TLS certificates)
- Set production CORS_ORIGINS
- Use environment-specific secrets

---

## Building

### Frontend Build
```bash
cd frontend
npm run build
```

**Output**: `frontend/dist/` directory contains:
- `index.html` - Entry point
- `assets/` - JavaScript bundles, CSS, images
- Build optimized for production (minified, tree-shaken)

### Backend Build
```bash
# No build step required for Python
# Dependencies installed via pip install -r requirements.txt
```

### Docker Build
```bash
docker build -t db-chat-nl:latest .
docker-compose build
```

---

## Testing

### Smoke Test
**Purpose**: Verify project builds and runs

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend loads
curl http://localhost:5173
```

**Expected output**:
```json
{"status": "healthy"}
```

### Unit Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

**Note**: Test files not found in scanned code. Test infrastructure needs to be added.

### Integration Tests
```bash
# Not implemented in scanned code
# Recommend adding pytest for backend, Playwright or Cypress for frontend
```

---

## Database Management

### Migrations

**Note**: SQLAlchemy models auto-create tables on first run. For production, use Alembic for migrations.

**Create migration** (with Alembic):
```bash
cd backend
alembic revision --autogenerate -m "Migration description"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback**:
```bash
alembic downgrade -1
```

### Seeding Data

**Admin user creation**:
```bash
# Register first user, then manually set is_admin=True in database
psql db_chat_nl -c "UPDATE users SET is_admin = TRUE WHERE email = 'admin@example.com';"
```

**Ipswich Town FC examples**: Pre-loaded in `backend/app/services/ipswich_examples.py` (20+ examples with glossary)

---

## Deployment

### Heroku

```bash
# Login and create app
heroku login
heroku create db-chat-nl-prod

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your-key
heroku config:set JWT_SECRET=your-secret
heroku config:set ADMIN_API_KEY=your-admin-key

# Deploy
git push heroku main

# Run migrations
heroku run python -m alembic upgrade head

# Open app
heroku open
```

**Heroku considerations**:
- Heartbeat polling (15s) prevents 55s timeout on long queries (evidence: llm.py:HEARTBEAT_INTERVAL=15)
- Use Heroku Postgres addon (automatically sets DATABASE_URL)
- Configure buildpacks: Python + Node.js (for frontend build)

### Docker

```bash
# Build image
docker build -t db-chat-nl:latest .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### AWS / Cloud Platform

```bash
# Build and push to container registry
docker build -t db-chat-nl:latest .
docker tag db-chat-nl:latest your-registry/db-chat-nl:latest
docker push your-registry/db-chat-nl:latest

# Deploy to ECS, EKS, or similar
# Set environment variables in container definition
# Ensure PostgreSQL RDS instance is accessible
# Configure load balancer for HTTPS
```

---

## Monitoring & Maintenance

### Health Checks
```bash
curl http://localhost:8000/health
```

**Expected response**: `{"status": "healthy"}`

**Endpoints to monitor**:
- `/health` - Backend health
- `/` - Frontend loads
- `/docs` - API documentation accessible

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Heroku logs
heroku logs --tail

# Backend logs (if running directly)
# Logs to stdout (use systemd or similar for log management)
```

**Key log patterns**:
- "Learned new query pattern" - Learning store activity
- "Query returned X rows in Y ms" - Successful query execution
- "Query timeout" - Long-running queries (>30s)
- "Heartbeat" - Heartbeat polling during long queries

---

## Troubleshooting

### Issue: "503 Service Unavailable" on auth endpoints
```bash
# Check if AuthService initialized
# Ensure DATABASE_URL and PostgreSQL are accessible
psql $DATABASE_URL -c "SELECT 1;"

# Check backend logs for initialization errors
docker-compose logs backend | grep -i error
```

### Issue: "401 Unauthorized" on admin endpoints
```bash
# Verify JWT_SECRET matches between token creation and verification
# Check user has is_admin=True in database
psql $DATABASE_URL -c "SELECT id, email, is_admin FROM users;"

# Set admin flag manually if needed
psql $DATABASE_URL -c "UPDATE users SET is_admin = TRUE WHERE email = 'admin@example.com';"
```

### Issue: Frontend can't connect to backend
```bash
# Check CORS_ORIGINS includes frontend URL
# Verify backend is running on correct port
curl http://localhost:8000/health

# Check frontend .env file has correct VITE_API_URL
cat frontend/.env
```

### Issue: Claude API errors
```bash
# Verify ANTHROPIC_API_KEY is set and valid
echo $ANTHROPIC_API_KEY

# Check Anthropic API status
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Issue: Query timeout on long-running queries
```bash
# Evidence: 30-second timeout in database_pg.py
# Heartbeat polling prevents Heroku timeout (15s intervals)
# If query genuinely takes >30s, consider:
# 1. Adding indexes to database
# 2. Simplifying query
# 3. Increasing QUERY_TIMEOUT_MS in database service
```

---

## Cleanup

```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes database data)
docker-compose down -v

# Clean npm cache
cd frontend
npm cache clean --force

# Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---
