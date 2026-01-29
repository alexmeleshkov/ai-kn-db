# Core Modules

> **CRITICAL**: This file includes IMPLEMENTATION PATTERNS with real code snippets

## Backend Services

### 1. llm.py - Claude AI Integration with Tool Use

**Location**: backend/app/services/llm.py

**Responsibilities**:
- Natural language to SQL via Claude Opus 4
- Agentic tool use (execute_sql, ask_clarification)
- Extended thinking (5000 tokens)
- SSE streaming with heartbeat

**Key Functions**:
- generate_sql_stream() - Streams SQL generation with tool use
- serialize_rows() - JSON-safe result serialization

**Code Pattern** (simplified):
```python
from anthropic import Anthropic

SQL_TOOLS = [{
    "name": "execute_sql",
    "description": "Execute SQL query (SELECT only)",
    "input_schema": {"type": "object", "properties": {"sql": {"type": "string"}}}
}]

def generate_sql_stream(question, schema, db_service):
    client = Anthropic(api_key=settings.api_key)
    
    with client.messages.stream(
        model="claude-opus-4",
        thinking={"type": "enabled", "budget_tokens": 5000},
        tools=SQL_TOOLS,
        messages=[{"role": "user", "content": question}]
    ) as stream:
        for event in stream:
            if event.type == "tool_use" and event.name == "execute_sql":
                sql = event.input["sql"]
                yield {"type": "sql", "content": sql}
                results = db_service.execute_query(sql)
                yield {"type": "results", "data": results}
```

**Dependencies**: anthropic>=0.40.0
**Environment**: ANTHROPIC_API_KEY

---

### 2. auth.py - JWT Authentication

**Location**: backend/app/services/auth.py

**Responsibilities**:
- User registration/login with bcrypt
- JWT token generation (HS256, 7-day expiration)
- Token validation

**Code Pattern**:
```python
import bcrypt
import jwt
from datetime import datetime, timedelta

class AuthService:
    def register(self, email, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # Insert user into app_users table
        token = self.create_token(user_id, email)
        return {"user": user, "token": token}
    
    def create_token(self, user_id, email):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
```

**Dependencies**: PyJWT>=2.8.0, bcrypt>=4.1.0
**Database**: app_users (id, email, password_hash)

---

### 3. routes.py - FastAPI SSE Streaming

**Location**: backend/app/api/routes.py

**Responsibilities**:
- HTTP endpoints (chat, health, schema)
- SSE streaming for real-time responses

**Code Pattern**:
```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def stream_chat(request, chat_request):
    async def event_generator():
        for event in chat_service.stream_response(chat_request.message):
            yield f"data: {json.dumps(event)}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

---

## Frontend Components

### 4. useAuth.tsx - Auth Context

**Location**: frontend/src/hooks/useAuth.tsx

**Responsibilities**:
- Global auth state (React Context)
- Login/logout functions
- Token storage (localStorage)

**Code Pattern**:
```typescript
const AuthContext = createContext<AuthContextType>(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = async (email, password) => {
    const response = await apiLogin(email, password);
    setAuthToken(response.token);
    setUser(response.user);
  };
  
  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
}
```

---

### 5. useChat.ts - SSE Streaming Hook

**Location**: frontend/src/hooks/useChat.ts

**Responsibilities**:
- Chat state management
- SSE connection for streaming
- Message sending/receiving

**Code Pattern**:
```typescript
export function useChat() {
  const [messages, setMessages] = useState([]);
  
  const sendMessage = (content) => {
    const eventSource = new EventSource("/api/v1/chat/stream");
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "sql") {
        setMessages(prev => [...prev, { sql: data.content }]);
      } else if (data.type === "results") {
        setMessages(prev => [...prev, { results: data.data }]);
      }
    };
  };
  
  return { messages, sendMessage };
}
```

---

### 6. QueryChart.tsx - Chart.js Visualization

**Location**: frontend/src/components/QueryChart.tsx

**Responsibilities**:
- Auto-generate charts from results
- Chart type detection (bar/line/pie)

**Code Pattern**:
```typescript
import { Bar, Line } from "react-chartjs-2";

export function QueryChart({ data }) {
  const chartData = {
    labels: data.map(row => row[0]),
    datasets: [{ data: data.map(row => row[1]) }]
  };
  
  return <Bar data={chartData} options={{ responsive: true }} />;
}
```

**Dependencies**: chart.js>=4.5.1, react-chartjs-2>=5.3.1

---

## Key Patterns Summary

1. **Agentic Tool Use**: Claude autonomously calls execute_sql and ask_clarification
2. **SSE Streaming**: Real-time server-to-client events
3. **JWT Auth**: Self-hosted with bcrypt + PyJWT
4. **React Context**: Global auth state
5. **Connection Pooling**: PostgreSQL ThreadedConnectionPool
6. **Extended Thinking**: 5000-token budget for complex queries

All patterns extracted from C:/work/db-chat-nl-master (production-tested).
