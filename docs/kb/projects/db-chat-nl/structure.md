# Project Structure

## Directory Tree

```
db-chat-nl/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application entry
│   │   ├── api/                       # API routes
│   │   │   ├── routes.py              # Chat and database endpoints
│   │   │   ├── auth_routes.py         # JWT authentication
│   │   │   ├── conversation_routes.py # Chat history
│   │   │   └── admin_routes.py        # Admin panel
│   │   ├── core/                      # Config and logging
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── services/                  # Business logic
│   │   │   ├── llm.py                 # Claude API integration
│   │   │   ├── chat.py                # Chat orchestration
│   │   │   ├── auth.py                # JWT authentication
│   │   │   ├── database_azure.py      # Azure SQL service
│   │   │   ├── database_pg.py         # PostgreSQL service
│   │   │   ├── app_data.py            # RDS app data service
│   │   │   ├── learning_store.py      # Query learning
│   │   │   └── ipswich_examples.py    # Few-shot examples
│   │   ├── schemas/                   # Pydantic models
│   │   │   └── chat.py
│   │   └── models/                    # Database models
│   │       └── database.py
│   ├── static/                        # Built frontend
│   ├── requirements.txt
│   └── Procfile                       # Heroku deployment
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Root component
│   │   ├── components/
│   │   │   ├── AuthPage.tsx           # Login/register
│   │   │   ├── ChatContainer.tsx      # Main chat UI
│   │   │   ├── ChatMessage.tsx        # Message display
│   │   │   ├── ChatInput.tsx          # Input box
│   │   │   ├── DataViewer.tsx         # Query results table
│   │   │   ├── QueryChart.tsx         # Chart.js wrapper
│   │   │   ├── SidebarTabs.tsx        # History + Schema tabs
│   │   │   ├── DatabaseInfo.tsx       # Schema viewer
│   │   │   └── AdminConversationViewer.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.tsx            # Auth context
│   │   │   ├── useChat.ts             # Chat with streaming
│   │   │   └── useQueryHistory.ts     # History management
│   │   ├── services/
│   │   │   └── api.ts                 # API client
│   │   ├── types/
│   │   │   └── chat.ts                # TypeScript types
│   │   └── styles/
│   │       └── index.css              # Global styles
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── build.sh                           # Build frontend -> backend
└── README.md
```

## Directory Descriptions

### backend/app
**Purpose**: FastAPI application with layered architecture

**Key subdirectories**:
- `api/`: HTTP endpoints (routes)
- `services/`: Business logic (LLM, database, auth)
- `core/`: Configuration and logging
- `schemas/`: Pydantic models for validation
- `models/`: Database models

**Entry point**: main.py (creates FastAPI app)

### frontend/src
**Purpose**: React application with TypeScript

**Key subdirectories**:
- `components/`: UI components (functional with hooks)
- `hooks/`: Custom React hooks (useAuth, useChat)
- `services/`: API client (fetch wrapper)
- `types/`: TypeScript type definitions
- `styles/`: CSS with custom properties

**Entry point**: main.tsx (renders App.tsx)

## File Naming Conventions

**Backend**:
- Services: snake_case.py (llm.py, auth.py)
- Routes: snake_case_routes.py
- Tests: test_*.py

**Frontend**:
- Components: PascalCase.tsx (ChatContainer.tsx)
- Hooks: camelCase.ts (useAuth.tsx)
- Types: camelCase.ts (chat.ts)

## Module Organization Strategy

**Backend**: By layer (API -> Services -> Data)
**Frontend**: By feature (components grouped by domain)

## Capability Mapping

| Capability | Backend Files | Frontend Files |
|------------|--------------|----------------|
| Authentication | auth.py, auth_routes.py | useAuth.tsx, AuthPage.tsx |
| Chat | chat.py, routes.py | useChat.ts, ChatContainer.tsx |
| Visualizations | N/A | QueryChart.tsx, DataViewer.tsx |
| History | app_data.py, conversation_routes.py | useQueryHistory.ts, SidebarTabs.tsx |
| Schema Viewer | database_azure.py | DatabaseInfo.tsx |
