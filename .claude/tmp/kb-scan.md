# Repository Scan Report: db-chat-nl

**Scan Date**: 2026-01-26  
**Project ID**: db-chat-nl  
**Repository Path**: /c/work/db-chat-nl-master

## 1. Repository Identity

**Name**: ITFC Analysis (db-chat-nl)  
**Description**: Natural language interface for querying Ipswich Town fan databases using Claude AI  
**Git Remote**: No git remote found (local repository)  
**Production URL**: https://www.itfcanalysis.com  
**License**: MIT

## 2. High-Level Directory Tree

```
db-chat-nl-master/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── api/         # REST API routes
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic (13 services)
│   │   └── main.py      # FastAPI app entry
│   ├── scripts/         # Database scripts
│   ├── static/          # Built frontend files
│   ├── tests/           # Pytest tests
│   └── requirements.txt
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components (11)
│   │   ├── hooks/       # React hooks (4)
│   │   ├── services/    # API client
│   │   └── types/
│   └── package.json
├── ARCHITECTURE.md
├── README.md
├── build.sh
└── docker-compose.yml
```

## 3. Detected Technologies

### Frontend
- React 18.2.0, TypeScript 5.2.2, Vite 5.0.8
- Chart.js 4.5.1, react-chartjs-2
- react-markdown 9.0.1

### Backend
- FastAPI >= 0.109.0, Python 3.11, Uvicorn
- psycopg2-binary, python-tds, duckdb
- PyJWT 2.8.0, bcrypt 4.1.0
- anthropic >= 0.40.0 (Claude Opus 4)

### Databases
- Azure SQL Server (IpswichTown_cdm)
- AWS RDS PostgreSQL (app data)
- DuckDB (local/dev)

### DevOps
- Docker, Heroku (Standard-2X)
- pytest >= 7.4.0

## 4. How to Run Locally

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up --build
```

## 5. Key Modules

### Backend Services
- database_azure.py: Azure SQL Server
- database_pg.py: PostgreSQL
- auth.py: JWT + bcrypt
- llm.py: Claude AI integration
- chat.py: SSE streaming
- learning_store.py: Query learning

### Frontend Components
- AuthPage.tsx: Login/register
- ChatContainer.tsx: Main chat UI
- DataViewer.tsx: Query results
- QueryChart.tsx: Visualizations

### API Routes
- /api/v1/auth: Authentication
- /api/v1/chat/stream: SSE chat
- /api/v1/conversations: History
- /api/v1/database/schema: Schema

## 6. Risks & Unknowns

### Required Environment Variables
**Critical**:
- ANTHROPIC_API_KEY
- AZURE_SQL_* credentials
- POSTGRES_* credentials
- JWT_SECRET

### External Dependencies
- Azure SQL Server (requires IP whitelist)
- AWS RDS PostgreSQL (manual schema setup)
- Anthropic Claude API
- QuotaGuard Static (production)

### Security Concerns
1. JWT_SECRET must be secure
2. IP whitelisting required
3. .env.example outdated

### Testing Gaps
- No frontend tests
- No integration tests
- No load testing

### Documentation Gaps
- No API docs (Swagger)
- No schema diagram
- No monitoring docs

## Summary

**Type**: Full-stack AI database query interface  
**Stack**: React + FastAPI + Azure SQL + RDS + Claude  
**Status**: Production (https://www.itfcanalysis.com)  
**Strengths**: Clean architecture, learning system, streaming  
**Risks**: Missing env docs, no migrations, external deps
