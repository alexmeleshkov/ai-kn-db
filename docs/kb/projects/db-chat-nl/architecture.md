# Architecture

## Folder structure (overview)

```
db-chat-nl-master/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/               # REST API route handlers
│   │   │   ├── auth_routes.py        # Login, register, token validation
│   │   │   ├── chat_routes.py        # SSE streaming chat endpoint
│   │   │   ├── conversation_routes.py # Conversation history CRUD
│   │   │   └── database_routes.py    # Schema introspection
│   │   ├── core/              # Core configuration and setup
│   │   │   ├── config.py             # Environment variable management
│   │   │   └── dependencies.py       # FastAPI dependency injection
│   │   ├── models/            # SQLAlchemy database models
│   │   │   ├── user.py               # User authentication model
│   │   │   └── conversation.py       # Conversation history model
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   │   ├── auth.py               # Auth DTOs
│   │   │   ├── chat.py               # Chat message schemas
│   │   │   └── conversation.py       # Conversation DTOs
│   │   ├── services/          # Business logic (13 services)
│   │   │   ├── auth.py               # JWT + bcrypt authentication
│   │   │   ├── database_azure.py     # Azure SQL Server connector
│   │   │   ├── database_pg.py        # PostgreSQL connector
│   │   │   ├── database_duckdb.py    # DuckDB local dev connector
│   │   │   ├── llm.py                # Claude AI integration
│   │   │   ├── chat.py               # SSE chat orchestration
│   │   │   ├── learning_store.py     # Query pattern storage
│   │   │   ├── query_intelligence.py # SQL validation & analysis
│   │   │   ├── ipswich_examples.py   # Domain-specific examples
│   │   │   └── conversation_service.py # History management
│   │   └── main.py            # FastAPI app entry, CORS, route registration
│   ├── scripts/               # Database maintenance scripts
│   │   └── init_pg_schema.sql       # PostgreSQL schema setup
│   ├── static/                # Built frontend files (production)
│   ├── tests/                 # Pytest unit tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container definition
│   └── .env.example          # Environment variables template
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── components/        # React components (11 components)
│   │   │   ├── AuthPage.tsx          # Login/register UI
│   │   │   ├── ChatContainer.tsx     # Main chat interface
│   │   │   ├── ChatMessage.tsx       # Individual message rendering
│   │   │   ├── DataViewer.tsx        # Query result tables
│   │   │   ├── QueryChart.tsx        # Chart.js visualizations
│   │   │   ├── SidebarTabs.tsx       # Navigation & history
│   │   │   └── [5 more components]
│   │   ├── hooks/             # Custom React hooks (4 hooks)
│   │   │   ├── useAuth.tsx           # Authentication state
│   │   │   ├── useChat.tsx           # SSE streaming connection
│   │   │   ├── useConversations.tsx  # History management
│   │   │   └── useDatabase.tsx       # Schema fetching
│   │   ├── services/          # API client layer
│   │   │   └── api.ts                # Axios-based HTTP client
│   │   ├── types/             # TypeScript type definitions
│   │   │   └── index.ts              # Shared interfaces
│   │   ├── styles/            # CSS styling
│   │   │   └── index.css             # Ipswich Town brand colors
│   │   ├── App.tsx            # Root component with routing
│   │   └── main.tsx           # React entry point
│   ├── public/                # Static assets
│   ├── index.html             # HTML entry point
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── vite.config.ts         # Vite build configuration
│   └── Dockerfile             # Frontend container definition
├── docker-compose.yml         # Multi-container orchestration
├── build.sh                   # Production build script
├── ARCHITECTURE.md            # Original architecture documentation
└── README.md                  # Project documentation
```

## Key decisions

### Decision: Multi-database adapter pattern
- **Rationale**: Support multiple data sources (Azure SQL for fan data, PostgreSQL for app data, DuckDB for local dev) with a unified query interface. Each database requires different drivers and connection strategies.
- **Trade-offs**: 
  - Increased complexity in managing three database connections
  - Performance overhead from database-specific query translation
  - Benefits: Development flexibility (DuckDB), production scalability (cloud databases), clean separation of concerns

### Decision: Server-Sent Events (SSE) for streaming
- **Rationale**: Claude AI generates SQL queries and explanations token-by-token. SSE provides unidirectional streaming from server to client, perfect for AI response streaming without WebSocket overhead.
- **Trade-offs**:
  - SSE is unidirectional (server → client only), requiring separate REST endpoints for user input
  - Limited browser support compared to WebSockets (though widely supported in modern browsers)
  - Benefits: Simpler than WebSockets, automatic reconnection, native browser EventSource API, HTTP/2 multiplexing

### Decision: Learning store for query improvement
- **Rationale**: Track successful natural language → SQL translations to improve future query generation. Store query patterns, execution results, and user feedback.
- **Trade-offs**:
  - Additional PostgreSQL storage overhead
  - Privacy considerations (storing user queries)
  - Benefits: Continuously improving accuracy, faster query generation for common patterns, reduced API costs

### Decision: Embedded domain knowledge (ipswich_examples.py)
- **Rationale**: Provide Claude with Ipswich Town-specific terminology, common queries, and database schema context to improve SQL generation accuracy.
- **Trade-offs**:
  - Manual maintenance of example library
  - Examples can become outdated as schema changes
  - Benefits: Higher accuracy for domain-specific queries, better understanding of fan data semantics, reduced ambiguity

### Decision: JWT token-based authentication
- **Rationale**: Stateless authentication suitable for API-first architecture. Tokens can be validated without database lookups, enabling horizontal scaling.
- **Trade-offs**:
  - Cannot invalidate tokens before expiration (no server-side session revocation)
  - Token size larger than session IDs
  - Benefits: Stateless, scalable, standard approach for API authentication

### Decision: Static IP proxy (QuotaGuard) for production
- **Rationale**: Azure SQL Server requires IP whitelisting. Heroku dynos have dynamic IPs, so a static IP proxy is needed for production database access.
- **Trade-offs**:
  - Additional cost (~$79/month for QuotaGuard Static)
  - Added latency for database connections
  - Single point of failure
  - Benefits: Meets Azure SQL security requirements, stable production connectivity

### Decision: Frontend builds served by FastAPI
- **Rationale**: Single deployment artifact. Vite builds frontend into `backend/static/`, and FastAPI serves both API and static files.
- **Trade-offs**:
  - Backend deployment size includes frontend assets
  - Cannot deploy frontend independently to CDN
  - Benefits: Simplified deployment, single Heroku dyno, no CORS complexity, reduced infrastructure costs

### Decision: Claude Opus 4 for SQL generation
- **Rationale**: Most capable model for complex reasoning tasks like SQL generation from natural language. Better accuracy than Sonnet for multi-table joins and aggregations.
- **Trade-offs**:
  - Higher API costs compared to Sonnet ($15/MTok input vs $3/MTok)
  - Slower response times (though mitigated by streaming)
  - Benefits: Superior SQL accuracy, better handling of ambiguous queries, improved schema understanding
