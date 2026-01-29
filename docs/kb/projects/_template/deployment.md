# Deployment & Operations

> **Purpose**: Document exact commands to build, run, test, and deploy the project.
> This file enables generation of README.md and smoke test scripts.

## Prerequisites

### System Requirements
- **Operating System**: [e.g., Linux, macOS, Windows with WSL2]
- **Architecture**: [e.g., x64, ARM64]
- **Memory**: [e.g., Minimum 4GB RAM]
- **Disk Space**: [e.g., 2GB free space]

### Required Software
- **[Tool]** - [Version requirement]
  - Example: **Node.js** - >= 18.0.0
  - Installation: `brew install node` (macOS) or [link to install guide]

- **[Tool]** - [Version requirement]
  - Example: **Python** - >= 3.11
  - Installation: `brew install python@3.11` or [link]

- **[Tool]** - [Version requirement]
  - Example: **Docker** - >= 24.0
  - Installation: [Link to Docker docs]

- **[Tool]** - [Version requirement]
  - Example: **PostgreSQL** - >= 14 (or via Docker)
  - Installation: `docker run -d -p 5432:5432 postgres:14`

### Required Credentials
- **[Service]** - API key required
  - Example: **Anthropic API** - Get key from https://console.anthropic.com
  - Variable name: `ANTHROPIC_API_KEY`

- **[Service]** - Credentials required
  - Example: **Database** - Connection string
  - Variable name: `DATABASE_URL`

---

## Local Development Setup

### 1. Clone & Navigate
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or using Poetry
poetry install

# Verify installation
python --version
pip list
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# Or: yarn install / pnpm install

# Verify installation
node --version
npm --version
npm list --depth=0
```

### 4. Database Setup
```bash
# Option A: Using Docker
docker run -d \
  --name project-db \
  -e POSTGRES_PASSWORD=devpassword \
  -e POSTGRES_USER=devuser \
  -e POSTGRES_DB=projectdb \
  -p 5432:5432 \
  postgres:14

# Option B: Local PostgreSQL
createdb projectdb
psql projectdb < schema.sql  # If schema file exists

# Run migrations (if applicable)
cd backend
alembic upgrade head
# Or: python manage.py migrate
```

### 5. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your values
# Required variables:
# DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/projectdb
# JWT_SECRET=your-secret-key-change-in-production
# ANTHROPIC_API_KEY=sk-ant-...
# CORS_ORIGINS=http://localhost:5173
```

**Environment file template**:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
JWT_SECRET=generate-with-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# External Services
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OPENAI_API_KEY=sk-your-key-here  # If using OpenAI

# Server Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Feature Flags (optional)
ENABLE_ANALYTICS=false
ENABLE_DEBUG_MODE=true
```

---

## Running the Application

### Development Mode

**Option 1: Run services separately**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # If using venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Or: python -m uvicorn app.main:app --reload
# Or: flask run  (if Flask)
# Or: python manage.py runserver  (if Django)

# Terminal 2: Frontend
cd frontend
npm run dev
# Or: yarn dev
# Server runs at http://localhost:5173 (Vite default)
```

**Option 2: Using Docker Compose** (recommended)
```bash
# From project root
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Docker Compose file location**: `docker-compose.yml` (or `docker-compose.dev.yml`)

### Production Mode

**Option 1: Docker Compose**
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d

# Check health
docker-compose ps
curl http://localhost:8000/health
```

**Option 2: Manual production deployment**
```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
# Or: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
cd frontend
npm run build
# Serve dist/ folder with nginx or similar
npx serve -s dist -p 3000
```

---

## Building

### Frontend Build
```bash
cd frontend

# Production build
npm run build
# Output directory: dist/ (or build/)

# Verify build
ls -lh dist/
# Should see index.html, assets/, etc.

# Preview production build locally
npm run preview
```

**Build artifacts**:
- Location: `frontend/dist/`
- Assets: HTML, JS, CSS, images
- Size target: < 2MB uncompressed

### Backend Build
```bash
cd backend

# If using Docker
docker build -t project-backend:latest .

# Verify image
docker images | grep project-backend
docker run --rm project-backend:latest python --version
```

**Docker image**:
- Base image: `python:3.11-slim`
- Size target: < 500MB
- Multi-stage: Yes/No

---

## Testing

### Smoke Test (Critical for Generation)
**Purpose**: Verify the project builds and runs with minimal setup.

```bash
# Run smoke test
npm run smoke
# Or: ./scripts/smoke-test.sh
# Or: python scripts/smoke_test.py

# Expected output:
# ✓ Backend health check: OK
# ✓ Frontend build: OK
# ✓ API responds: OK
# Smoke test passed!
```

**Smoke test implementation** (example):
```bash
#!/bin/bash
# scripts/smoke-test.sh

set -e

echo "Running smoke test..."

# 1. Check backend starts
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 5

# 2. Health check
curl -f http://localhost:8000/health || (kill $BACKEND_PID; exit 1)
echo "✓ Backend health check: OK"

# 3. Check frontend builds
cd ../frontend
npm run build > /dev/null 2>&1
echo "✓ Frontend build: OK"

# 4. Test critical API endpoint
curl -f http://localhost:8000/api/v1/status || (kill $BACKEND_PID; exit 1)
echo "✓ API responds: OK"

# Cleanup
kill $BACKEND_PID

echo "Smoke test passed!"
```

### Unit Tests
```bash
# Backend
cd backend
pytest
# Or: python -m pytest tests/
# Or: python manage.py test

# With coverage
pytest --cov=app --cov-report=html

# Frontend
cd frontend
npm test
# Or: npm run test:unit
```

### Integration Tests
```bash
# Backend integration tests
cd backend
pytest tests/integration/

# Frontend integration tests
cd frontend
npm run test:integration
```

### End-to-End Tests
```bash
# Using Playwright
cd frontend
npx playwright test

# Using Cypress
npm run cypress:run
```

---

## Database Management

### Migrations

**Create migration**:
```bash
cd backend
alembic revision --autogenerate -m "Add user table"
# Or: python manage.py makemigrations
```

**Apply migrations**:
```bash
alembic upgrade head
# Or: python manage.py migrate
```

**Rollback**:
```bash
alembic downgrade -1
# Or: python manage.py migrate <previous_migration>
```

### Seeding Data
```bash
# Run seed script
cd backend
python scripts/seed.py

# Or via management command
python manage.py seed
```

### Backup & Restore
```bash
# Backup
pg_dump -U user dbname > backup.sql
# Or: docker exec project-db pg_dump -U user dbname > backup.sql

# Restore
psql -U user dbname < backup.sql
```

---

## Deployment Platforms

### Heroku
```bash
# Login
heroku login

# Create app
heroku create project-name

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-...
heroku config:set JWT_SECRET=...

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head

# View logs
heroku logs --tail
```

### AWS (EC2 + RDS)
```bash
# 1. Build and push Docker image
docker build -t project:latest .
docker tag project:latest <ECR_URI>:latest
docker push <ECR_URI>:latest

# 2. SSH to EC2 instance
ssh -i key.pem ec2-user@<EC2_IP>

# 3. Pull and run
docker pull <ECR_URI>:latest
docker run -d -p 8000:8000 --env-file .env <ECR_URI>:latest

# 4. Setup nginx reverse proxy
sudo systemctl start nginx
```

### Docker + docker-compose (VPS)
```bash
# 1. Copy files to server
scp -r . user@server:/var/www/project/

# 2. SSH to server
ssh user@server

# 3. Run with docker-compose
cd /var/www/project
docker-compose -f docker-compose.prod.yml up -d

# 4. Setup SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

### Kubernetes (Advanced)
```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/project-backend
```

---

## Monitoring & Maintenance

### Health Checks
```bash
# Backend health endpoint
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}

# Database connection check
curl http://localhost:8000/health/db
# Expected: {"database": "connected"}
```

### Logs
```bash
# Docker Compose logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Specific time range
docker-compose logs --since 30m backend

# Save logs to file
docker-compose logs > app.log
```

### Performance Monitoring
```bash
# Docker stats
docker stats

# System resources
htop
# Or: top

# Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## Troubleshooting

### Common Issues

**Issue**: Backend won't start - "Port 8000 already in use"
```bash
# Find process using port
lsof -i :8000
# Or on Windows: netstat -ano | findstr :8000

# Kill process
kill -9 <PID>
```

**Issue**: Frontend can't connect to backend - CORS error
```bash
# Check CORS_ORIGINS in backend .env
# Ensure frontend URL is included
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Issue**: Database connection fails
```bash
# Check database is running
docker ps | grep postgres
# Or: pg_isready -h localhost -p 5432

# Verify DATABASE_URL format
# postgresql://username:password@host:port/database
```

**Issue**: Environment variables not loading
```bash
# Verify .env file location (should be in backend/ root)
ls -la backend/.env

# Check file is loaded (add to main.py)
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('JWT_SECRET'))  # Should not be None
```

### Debug Mode
```bash
# Backend debug mode
cd backend
export LOG_LEVEL=DEBUG
python -m uvicorn app.main:app --reload

# Frontend debug mode
cd frontend
npm run dev -- --debug
```

---

## Cleanup

### Stop services
```bash
# Docker Compose
docker-compose down

# Docker with volume cleanup
docker-compose down -v

# Kill specific processes
pkill -f uvicorn
pkill -f vite
```

### Remove build artifacts
```bash
# Frontend
rm -rf frontend/dist frontend/node_modules

# Backend
rm -rf backend/venv backend/__pycache__ backend/.pytest_cache

# Database
docker volume rm project_db_data
```

---

## CI/CD Integration

### GitHub Actions (Example)
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run smoke test
        run: ./scripts/smoke-test.sh
```

### GitLab CI (Example)
```yaml
# .gitlab-ci.yml
stages:
  - test
  - deploy

smoke_test:
  stage: test
  script:
    - ./scripts/smoke-test.sh
```

---
