# Project Structure: ITFC Analysis

## Directory Tree

Main directories:
- backend/ - FastAPI Python backend with 13 services
- frontend/ - React TypeScript frontend with 11 components
- docker-compose.yml - Multi-container setup

### Backend Structure
- app/api/ - REST API routes (auth, chat, conversation, database)
- app/core/ - Configuration and dependencies
- app/models/ - SQLAlchemy models (user, conversation)
- app/services/ - Business logic (auth, llm, database adapters, chat)
- app/main.py - FastAPI application entry point

### Frontend Structure
- src/components/ - React UI components
- src/hooks/ - Custom React hooks (useAuth, useChat, useConversations)
- src/services/ - API client layer
- src/styles/ - CSS with Ipswich Town brand colors

## Capability File Mapping

### authentication_jwt
Backend: app/services/auth.py, app/api/auth_routes.py, app/models/user.py
Frontend: components/AuthPage.tsx, hooks/useAuth.tsx
Dependencies: PyJWT, bcrypt

### natural_language_query
Backend: app/services/llm.py, app/services/ipswich_examples.py
Dependencies: anthropic

### streaming_chat
Backend: app/api/chat_routes.py, app/services/chat.py
Frontend: hooks/useChat.tsx, components/ChatContainer.tsx
Dependencies: FastAPI SSE support

### multi_database_query
Backend: app/services/database_azure.py, database_pg.py, database_duckdb.py
Dependencies: python-tds, psycopg2-binary, duckdb

### data_visualization
Frontend: components/QueryChart.tsx
Dependencies: chart.js, react-chartjs-2

### conversation_history
Backend: app/models/conversation.py, app/api/conversation_routes.py
Frontend: hooks/useConversations.tsx, components/SidebarTabs.tsx

## Build Process

Development:
- Backend: uvicorn app.main:app --reload
- Frontend: npm run dev

Production:
- build.sh compiles frontend into backend/static/
- Heroku deploys single backend container serving both API and static files

## Evidence
Structure based on scan of C:/work/db-chat-nl-master/
