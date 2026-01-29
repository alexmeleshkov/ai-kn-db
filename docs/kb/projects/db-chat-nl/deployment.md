# Deployment & Operations

## Prerequisites

### Required Software
- **Python** 3.11+
- **Node.js** 20+
- **PostgreSQL** 14+ (local or AWS RDS)
- **Docker** (optional, for containerized deployment)

### Required Credentials
- **Anthropic API key**: Get from https://console.anthropic.com
- **PostgreSQL connection**: AWS RDS or local instance
- **Azure SQL** (optional): For specific client data

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd db-chat-nl-master
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scriptsctivate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Setup
```bash
# Using Docker
docker run -d --name postgres-db -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:14

# Or local PostgreSQL
createdb fandata
psql fandata < backend/scripts/rds_schema.sql
```

### 5. Environment Configuration
```bash
cp backend/.env.example backend/.env
# Edit .env with your values:
# ANTHROPIC_API_KEY=sk-ant-...
# POSTGRES_HOST=localhost
# POSTGRES_DATABASE=fandata
# JWT_SECRET=<generate-random-32-bytes>
```

## Running the Application

### Development Mode
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Access at: http://localhost:5173

### Using Docker Compose
```bash
docker-compose up
```

## Building

### Frontend Build
```bash
cd frontend
npm run build
# Output: dist/
```

### Backend Build (for Heroku)
```bash
cd frontend && npm run build
cp -r dist/* ../backend/static/
cd ../backend
git add -A && git commit -m "Deploy" && git push heroku master
```

## Testing

### Smoke Test
```bash
# Backend health check
curl http://localhost:8000/api/v1/health

# Frontend build
cd frontend && npm run build
```

### Unit Tests
```bash
cd backend
pytest tests/
```

## Deployment Platforms

### Heroku Deployment
```bash
# Login
heroku login

# Create app
heroku create db-chat-nl-app

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-...
heroku config:set JWT_SECRET=...
heroku config:set POSTGRES_HOST=<rds-host>

# Deploy
cd backend
git push heroku master

# View logs
heroku logs --tail
```

### Docker Deployment
```bash
# Build
docker build -t db-chat-nl:latest backend/

# Run
docker run -d -p 8000:8000 --env-file backend/.env db-chat-nl:latest
```

## Environment Variables

Required variables for backend/.env:
```bash
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-opus-4-20250514
DB_MODE=postgres  # or azure
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=fandata
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
JWT_SECRET=<random-32-byte-hex>
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

## Monitoring & Maintenance

### Health Checks
```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status":"healthy"}
```

### Logs
```bash
# Heroku
heroku logs --tail -a db-chat-nl-app

# Docker
docker logs -f <container-id>
```

## Troubleshooting

**Port 8000 already in use**:
```bash
lsof -i :8000  # Find process
kill -9 <PID>
```

**CORS error**:
Check CORS_ORIGINS in .env includes frontend URL

**Database connection fails**:
Verify POSTGRES_HOST and credentials in .env
```bash
psql -h localhost -U postgres -d fandata  # Test connection
```
