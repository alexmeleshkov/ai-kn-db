# React + FastAPI + SQL Chat Template

This template provides a minimal setup for a chat interface with AI-powered database queries, based on the db-chat-nl knowledge base.

## Features

- **Backend**: FastAPI with SSE streaming for real-time chat responses
- **Frontend**: React + TypeScript with Vite
- **Chat Interface**: Full-featured chat UI with message history
- **Database Integration**: Abstract database service (implement for your database)
- **LLM Integration**: Anthropic Claude API support (configurable)

## Architecture

Based on db-chat-nl documentation:
- SSE streaming pattern (architecture.md:76-77)
- Chat orchestration service (modules.md:100-108)
- Database adapter pattern (architecture.md:66-71)
- Heartbeat mechanism for timeout prevention (tech.md:63-64)

## Getting Started

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your configuration:
# ANTHROPIC_API_KEY=your-api-key
# DATABASE_URL=your-database-url
```

3. Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

### Docker Setup

```bash
docker-compose up
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # SSE streaming endpoints
│   │   ├── services/
│   │   │   ├── chat.py            # Chat orchestration
│   │   │   ├── database.py        # Database adapter
│   │   │   └── llm.py             # LLM integration
│   │   └── main.py                # FastAPI app
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatContainer.tsx  # Message list with auto-scroll
    │   │   └── ChatInput.tsx      # Input field with submit
    │   ├── hooks/
    │   │   └── useChat.ts         # SSE connection management
    │   ├── types/
    │   │   └── chat.ts            # TypeScript types
    │   └── App.tsx                # Main application
    └── package.json
```

## Implementation Notes

### Backend

The backend provides minimal stubs that need customization:

1. **Database Service** (`backend/app/services/database.py`):
   - Implement `DatabaseService` for your specific database
   - Replace `DatabaseServiceStub` with real implementation
   - Based on db-chat-nl database adapter pattern

2. **LLM Service** (`backend/app/services/llm.py`):
   - Add Anthropic API integration
   - Implement streaming response handling
   - Based on db-chat-nl llm.py (modules.md:90-98)

3. **Chat Service** (`backend/app/services/chat.py`):
   - Implement full streaming logic with heartbeat
   - Add schema loading and caching
   - Implement learned query system
   - Based on db-chat-nl chat orchestration (modules.md:100-108)

4. **Routes** (`backend/app/api/routes.py`):
   - Wire real service instances via dependency injection
   - Add authentication if needed
   - Based on db-chat-nl routes.py (modules.md:7-12)

### Frontend

The frontend provides a working chat interface with:

1. **ChatContainer**: Displays messages with auto-scroll
2. **ChatInput**: Textarea with Enter key handling
3. **useChat hook**: Manages SSE connections and message state
4. **Type definitions**: Full TypeScript support

#### Customization Points

- Add markdown rendering with `react-markdown` (modules.md:187-190)
- Add data visualization with Chart.js (modules.md:219-224)
- Add conversation history (modules.md:198-203)
- Add authentication (modules.md:164-169)

## KB Documentation References

All code includes citations to the source KB documentation:

- **architecture.md**: System architecture and data flow
- **modules.md**: Module structure and API endpoints
- **features.md**: Feature descriptions and capabilities
- **tech.md**: Technical decisions and solutions

## TODO: Required Customizations

### Backend
- [ ] Implement real database adapter for your database type
- [ ] Configure Anthropic API key in environment
- [ ] Implement full SSE streaming with heartbeat
- [ ] Add learned query system for improved accuracy
- [ ] Add authentication if needed
- [ ] Add conversation persistence

### Frontend
- [ ] Add markdown rendering (react-markdown)
- [ ] Add data table viewer component
- [ ] Add chart visualization (Chart.js)
- [ ] Add conversation history sidebar
- [ ] Add authentication UI if needed
- [ ] Improve error handling and retry logic

## Testing

### Backend
```bash
cd backend
# TODO: Add test command
# pytest
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

## Deployment

See docker-compose.yml for containerized deployment.

For production:
1. Build frontend: `cd frontend && npm run build`
2. Serve frontend static files from backend
3. Configure environment variables
4. Set up database connection
5. Deploy to your hosting platform

## License

This template is based on the db-chat-nl project architecture.
