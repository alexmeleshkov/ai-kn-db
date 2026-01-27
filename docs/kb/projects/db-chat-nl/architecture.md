# Architecture: ITFC Analysis

## System Architecture

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

## Technology Stack

### Frontend
- **Framework**: React 18.2.0
- **Language**: TypeScript 5.2.2
- **Build**: Vite 5.0.8
- **Visualization**: Chart.js 4.5.1, react-chartjs-2
- **Markdown**: react-markdown 9.0.1

**Sources**: frontend/package.json:L820-L827, frontend/tsconfig.json:L996-L1007

### Backend
- **Framework**: FastAPI >= 0.109.0
- **Runtime**: Python 3.11, Uvicorn (ASGI)
- **AI**: Anthropic Claude Opus 4 with Extended Thinking
- **Auth**: JWT (PyJWT 2.8.0) + bcrypt 4.1.0
- **Database Drivers**: psycopg2-binary, python-tds, duckdb

**Sources**: backend/app/main.py:L603-L640, README.md:L349-L360

### Databases
- **Primary Data**: Azure SQL Server (IpswichTown_cdm) - 13 tables, 11M+ rows
- **App Data**: AWS RDS PostgreSQL - users, conversations, messages, learned queries
- **Dev/Testing**: DuckDB for local development

**Sources**: ARCHITECTURE.md:L182-L203, README.md:L472-L492

### Infrastructure
- **Hosting**: Heroku Standard-2X dyno
- **Proxy**: QuotaGuard Static (SOCKS5) for Azure SQL access
- **Domain**: GoDaddy DNS to itfcanalysis.com
- **Containers**: Docker + docker-compose for local dev

**Sources**: README.md:L357-L359, ARCHITECTURE.md:L310-L326, docker-compose.yml:L772-L805

## Key Design Patterns

### 1. Database Adapter Pattern
Abstract base class `database_base.py` with concrete implementations:
- `database_azure.py` - Azure SQL Server (python-tds)
- `database_pg.py` - PostgreSQL (psycopg2)

### 2. AI Tool Use Pattern
Claude AI uses structured tools:
- `execute_sql` - Runs generated SQL queries
- `ask_clarification` - Requests user input when ambiguous

### 3. SSE Streaming Pattern
Server-Sent Events for real-time chat responses with heartbeat to prevent Heroku timeout (55s limit)

### 4. Learning System Pattern
Universal learning system stores successful SQL queries keyed by:
- Database type
- User question
- Generated SQL
- Success/failure status

### 5. JWT Authentication Pattern
Self-hosted auth replacing Supabase:
- bcrypt password hashing (12 rounds)
- JWT tokens (HS256, 7-day expiration)
- Stored in localStorage

## Data Flow

### Chat Query Flow
1. User submits natural language question
2. Frontend establishes SSE connection to `/api/v1/chat/stream`
3. Backend loads database schema from cache/Azure SQL
4. Backend retrieves learned queries for similar questions
5. Backend constructs prompt with:
   - Database schema
   - Few-shot examples (Ipswich-specific)
   - Learned queries
   - User question
6. Claude generates SQL using tool use
7. Backend validates and executes SQL
8. Results streamed back to frontend via SSE
9. Frontend renders table + optional chart
10. Successful query saved to learning system

### Authentication Flow
1. User submits email/password
2. Backend validates against `app_users` table (RDS)
3. Password verified with bcrypt
4. JWT token generated with 7-day expiration
5. Token stored in localStorage
6. Token sent in Authorization header for subsequent requests

## Security

- Read-only SQL queries (SELECT only)
- Query validation before execution
- Row limits (max 1000)
- IP whitelisting for Azure SQL
- JWT token validation on protected routes
- CORS configured for production domain
- bcrypt password hashing (12 rounds)

## Performance

| Operation | Time |
|-----------|------|
| Schema loading | ~100-200ms |
| Simple query (COUNT) | ~100-300ms |
| Complex query (JOIN) | ~500-2000ms |
| Extended thinking | ~3-5s |
| Total response | ~5-10s |

**Sources**: README.md:L388-L396

## Scalability Considerations

- Schema caching reduces database calls
- Connection pooling for PostgreSQL
- Learned queries improve accuracy (reduce retries)
- SSE streaming improves perceived performance
- Heroku horizontal scaling possible

## Migration History

1. **Jan 2026**: DuckDB + S3 → Azure SQL Server (performance)
2. **Jan 2026**: Supabase Auth → Self-hosted JWT + RDS (cost/control)
