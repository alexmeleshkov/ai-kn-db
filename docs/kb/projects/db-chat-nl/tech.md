# Technology Stack

## Backend Technologies
- **FastAPI** (>=0.109.0): Async framework for SSE streaming
- **Python** 3.11: Modern Python with type hints
- **PostgreSQL**: AWS RDS for app data (auth, conversations)
- **Azure SQL Server**: Live production data queries
- **PyJWT + bcrypt**: Self-hosted JWT authentication
- **Anthropic Claude API**: Claude Opus 4 with extended thinking

## Frontend Technologies  
- **React** 18: Hooks and Context API
- **TypeScript** 5.2: Type safety
- **Vite** 5: Fast build tool
- **Chart.js**: Data visualization
- **Vanilla CSS**: Custom properties for theming

## Why These Technologies

**FastAPI**: Chosen for async support (SSE streaming), automatic API docs, Python ecosystem.
**Claude Opus 4**: Superior SQL generation, extended thinking, agentic tool use.
**Self-hosted JWT**: Cost savings vs Supabase, full control, no vendor lock-in.
**PostgreSQL**: Reliable, ACID-compliant, free tier availability.
**React**: Mature ecosystem, TypeScript support, easy SSE integration.
**Vite**: 10x faster than Webpack, better DX.

## Security
- bcrypt password hashing (12 rounds)
- JWT tokens (HS256, 7-day expiration)
- Parameterized queries (SQL injection prevention)
- CORS whitelist
- Read-only database permissions

## Performance
- Async I/O throughout backend
- Connection pooling (5 connections)
- SSE heartbeat (15s) for Heroku timeout
- Code splitting and lazy loading
