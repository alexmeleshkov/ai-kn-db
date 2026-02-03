# Deployment & Operations

> **Purpose**: Document exact commands to build, run, test, and deploy.
> This enables README generation and smoke test implementation.

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL
- **Memory**: 2GB minimum, 4GB recommended
- **Disk Space**: 1GB for dependencies and database

### Required Software
- **Node.js** - >= 18.0.0 (for frontend build)
- **Python** - >= 3.11 (for backend)
- **Docker** - >= 24.0 (optional, for containerized deployment)
- **PostgreSQL** - >= 14 (or use AWS RDS)

### Required Credentials
- **Anthropic API Key** - Get from https://console.anthropic.com/account/keys
- **PostgreSQL Database** - AWS RDS or local instance
- **Azure SQL Server** (optional) - For Ipswich live data
- **AWS S3** (optional) - For JSON file storage
- **QuotaGuard** (optional) - Heroku add-on for Azure SQL static IP

---

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repo-url>
cd db-chat-nl
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

### 4. Database Setup
```bash
# Option A: Use local PostgreSQL
createdb db_chat_nl
psql db_chat_nl < backend/scripts/rds_schema.sql

# Option B: Use AWS RDS (configure in .env)
```

### 5. Environment Configuration

> **IMPORTANT FOR KB ENTRY CREATORS**: Document ALL environment variables used in the project.

Create `.env` file in `backend/` directory:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your actual values
```

**Environment Variables**:

| Variable | Required | Default | Description | Where to Get |
|----------|----------|---------|-------------|--------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | - | Claude API key for NL→SQL | [Anthropic Console](https://console.anthropic.com/account/keys) |
| `ANTHROPIC_MODEL` | ⚠️ Optional | `claude-opus-4-20250514` | Claude model ID | Use default or check Anthropic docs |
| `POSTGRES_HOST` | ✅ Yes | - | PostgreSQL host for app data | AWS RDS endpoint or localhost |
| `POSTGRES_PORT` | ⚠️ Optional | `5432` | PostgreSQL port | Default 5432 |
| `POSTGRES_DATABASE` | ✅ Yes | - | Database name | Your DB name |
| `POSTGRES_USER` | ✅ Yes | - | DB username | Your DB user |
| `POSTGRES_PASSWORD` | ✅ Yes | - | DB password | Your DB password |
| `JWT_SECRET` | ✅ Yes | - | Token signing key | Generate: `openssl rand -hex 32` |
| `DB_MODE` | ✅ Yes | - | Database mode: `azure`, `postgres`, or `duckdb` | Choose based on query database |
| `AZURE_SQL_SERVER` | ⚠️ If DB_MODE=azure | - | Azure SQL host | Azure portal |
| `AZURE_SQL_DATABASE` | ⚠️ If DB_MODE=azure | - | Azure DB name | Azure portal |
| `AZURE_SQL_USER` | ⚠️ If DB_MODE=azure | - | Azure username | Azure portal |
| `AZURE_SQL_PASSWORD` | ⚠️ If DB_MODE=azure | - | Azure password | Azure portal |
| `AWS_ACCESS_KEY_ID` | ⚠️ Optional | - | AWS access key for S3 | AWS IAM |
| `AWS_SECRET_ACCESS_KEY` | ⚠️ Optional | - | AWS secret key | AWS IAM |
| `AWS_REGION` | ⚠️ Optional | `us-east-1` | AWS region | AWS console |
| `S3_BUCKET` | ⚠️ Optional | - | S3 bucket name | AWS S3 console |
| `QUOTAGUARDSTATIC_URL` | ⚠️ Optional | - | SOCKS5 proxy URL | Heroku add-on |
| `CORS_ORIGINS` | ⚠️ Optional | `*` | Allowed origins (comma-separated) | Use * for dev, specific domain for prod |
| `MAX_QUERY_RESULTS` | ⚠️ Optional | `1000` | Max rows returned | Adjust based on needs |
| `QUERY_TIMEOUT` | ⚠️ Optional | `30` | Query timeout in seconds | Adjust for slow databases |

**Example `.env` file**:
```bash
# === API Keys & Secrets ===
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
ANTHROPIC_MODEL=claude-opus-4-20250514

# === Database Configuration (RDS PostgreSQL for app data) ===
POSTGRES_HOST=mydb.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_DATABASE=db_chat_nl
POSTGRES_USER=admin
POSTGRES_PASSWORD=your-db-password

# === Authentication ===
JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6

# === Query Database (choose one mode) ===
DB_MODE=duckdb
# OR for Azure SQL:
# DB_MODE=azure
# AZURE_SQL_SERVER=myserver.database.windows.net
# AZURE_SQL_DATABASE=fan_data
# AZURE_SQL_USER=admin
# AZURE_SQL_PASSWORD=your-password

# === Optional S3 Integration ===
# AWS_ACCESS_KEY_ID=AKIA...
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_REGION=us-east-1
# S3_BUCKET=fan-data-json-db

# === Application Settings ===
CORS_ORIGINS=*
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30
```

**Security Notes**:
- Never commit `.env` to version control
- `.env` is in `.gitignore`
- Use `.env.example` as template (with no real secrets)
- Rotate keys regularly for production
- Use separate keys for dev/staging/production

---

## Running the Application

### Development Mode

**Option 1: Run services separately**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Option 2: Docker Compose**
```bash
# From project root
docker-compose up --build
```

**Access**:
- Frontend: http://localhost:5173 (dev) or http://localhost:3000 (Docker)
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Production Mode

```bash
# Build frontend
cd frontend
npm run build

# Copy to backend static directory
cp -r dist/* ../backend/static/

# Run backend with production server
cd ../backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Building

### Frontend Build
```bash
cd frontend
npm run build
```

**Output**: `frontend/dist/` - Static HTML/CSS/JS files

### Backend Build
```bash
# No build step needed for Python
# But can create requirements.txt with exact versions:
pip freeze > requirements.txt
```

---

## Testing

### Smoke Test
**Purpose**: Verify project builds and runs

```bash
# Backend smoke test
cd backend
python -m pytest tests/ -v

# Frontend smoke test
cd frontend
npm run build
```

**Expected output**:
```
backend/tests/test_api.py::test_health_check PASSED
backend/tests/test_api.py::test_auth_flow PASSED
...
frontend build: ✓ built in 2.34s
```

### Unit Tests
```bash
# Backend
cd backend
source venv/bin/activate
pytest tests/ -v

# Frontend (not implemented)
# cd frontend
# npm test
```

### Integration Tests
```bash
# Backend integration tests
cd backend
pytest tests/test_api.py -v
```

---

## Database Management

### Migrations

**Create schema** (first time setup):
```bash
# PostgreSQL (RDS)
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE -f backend/scripts/rds_schema.sql

# Azure SQL (if using)
# Use backend/scripts/azure_schema.json or SSMS
```

**Schema files**:
- `backend/scripts/rds_schema.sql` - PostgreSQL schema
- `backend/scripts/supabase_schema.sql` - Legacy Supabase schema
- `backend/scripts/azure_schema.json` - Azure SQL schema metadata

**No ORM/migration tool**: Manual SQL scripts only

---

## Deployment

### Heroku

```bash
# From backend directory
cd backend

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0

# Add QuotaGuard (for Azure SQL)
heroku addons:create quotaguardstatic:starter

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your-key
heroku config:set JWT_SECRET=$(openssl rand -hex 32)
heroku config:set DB_MODE=azure
heroku config:set AZURE_SQL_SERVER=your-server
# ... set all required vars

# Deploy
git push heroku master

# Open app
heroku open
```

**Procfile** (already included):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Monitoring & Maintenance

### Health Checks
```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status": "healthy", "database_connected": true}
```

### Logs
```bash
# Local development
# Backend logs in terminal

# Heroku
heroku logs --tail

# Docker
docker-compose logs -f backend
```

---

## Troubleshooting

### Issue: Backend won't start - "ModuleNotFoundError"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Frontend build fails - "Module not found"
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Database connection fails
```bash
# Check PostgreSQL is running
psql -h localhost -U postgres -l

# Verify .env file has correct credentials
cat backend/.env | grep POSTGRES

# Test connection manually
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DATABASE
```

### Issue: "401 Unauthorized" on all authenticated endpoints
```bash
# Check JWT_SECRET is set
echo $JWT_SECRET

# If empty, generate new secret:
openssl rand -hex 32

# Set in .env:
echo "JWT_SECRET=<generated-secret>" >> backend/.env
```

---

## Cleanup

```bash
# Stop Docker containers
docker-compose down

# Remove volumes (WARNING: deletes database data)
docker-compose down -v

# Remove virtual environment
deactivate
rm -rf backend/venv

# Remove node_modules
rm -rf frontend/node_modules

# Remove build artifacts
rm -rf frontend/dist backend/__pycache__ backend/uploads
```

---
