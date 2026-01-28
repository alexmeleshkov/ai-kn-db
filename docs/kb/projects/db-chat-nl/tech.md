# Tech stack

## Frontend

### Core Framework
- React 18.2.0 - Component-based UI library
- TypeScript 5.2.2 - Type-safe JavaScript
- Vite 5.0.8 - Fast build tool with HMR

### Visualization
- Chart.js 4.5.1 - Canvas-based charting
- react-chartjs-2 5.3.1 - React wrapper for Chart.js
- react-markdown 9.0.1 - Markdown rendering

### Frontend Dependency Catalog

| Package | Version | Category | Purpose |
|---------|---------|----------|---------|
| react | 18.2.0 | Core | UI framework |
| react-dom | 18.2.0 | Core | React renderer |
| typescript | 5.2.2 | Dev | Type safety |
| vite | 5.0.8 | Dev | Build tool |
| chart.js | 4.5.1 | Visualization | Charts |
| react-chartjs-2 | 5.3.1 | Visualization | Chart wrapper |
| react-markdown | 9.0.1 | Content | Markdown |
| remark-gfm | 4.0.0 | Content | GFM support |

## Backend

### Core Framework
- FastAPI >= 0.109.0 - Modern async web framework
- Uvicorn >= 0.27.0 - ASGI server
- Pydantic >= 2.5.0 - Data validation

### Database Drivers
- python-tds >= 1.15.0 - Azure SQL Server
- psycopg2-binary >= 2.9.0 - PostgreSQL
- duckdb >= 1.0.0 - Local development

### AI Integration
- anthropic >= 0.40.0 - Claude API client

### Authentication
- PyJWT >= 2.8.0 - JWT encoding/decoding
- bcrypt >= 4.1.0 - Password hashing

### Backend Dependency Catalog

| Package | Version | Category | Purpose |
|---------|---------|----------|---------|
| fastapi | >=0.109.0 | Core | Web framework |
| uvicorn | >=0.27.0 | Core | ASGI server |
| python-tds | >=1.15.0 | Database | Azure SQL |
| psycopg2-binary | >=2.9.0 | Database | PostgreSQL |
| duckdb | >=1.0.0 | Database | Local dev |
| anthropic | >=0.40.0 | AI/ML | Claude API |
| PyJWT | >=2.8.0 | Auth | JWT tokens |
| bcrypt | >=4.1.0 | Auth | Passwords |
| pysocks | >=1.7.0 | Cloud | SOCKS proxy |
| pytest | >=7.4.0 | Testing | Test framework |

## Database / Storage

### Azure SQL Server
- Primary data source for Ipswich Town fan analytics
- Access via python-tds with SOCKS proxy
- IP whitelisting, TLS encryption, read-only access

### AWS RDS PostgreSQL
- Application data: users, conversations, learned queries
- JSONB for flexible conversation storage
- SSL required

### DuckDB
- Local development database
- Zero-configuration embedded database

## Tooling

### Build Tools
- Vite 5.0.8 - Frontend bundling
- build.sh - Production build script

### Testing
- pytest - Python test framework
- No frontend tests configured

### Infrastructure
- Heroku Standard-2X dyno
- QuotaGuard Static for Azure SQL whitelist
- Cost: ~$129/month
