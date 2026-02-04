# FastAPI

**Technology**: FastAPI 0.104+
**Category**: Framework

---

## Overview

Modern Python web framework for building APIs with automatic OpenAPI documentation, type validation via Pydantic, and dependency injection.

**Key characteristics**:
- ASGI framework (async support)
- Automatic OpenAPI/Swagger documentation
- Pydantic integration for request/response validation
- Dependency injection system
- Built-in support for SSE (Server-Sent Events)

---

## Usage Files

- `backend/app/api/auth_routes.py`
- `backend/app/api/admin_routes.py`
- `backend/app/api/conversation_routes.py`
- `backend/app/api/routes.py`
- `backend/app/schemas/chat.py`

---

## Complete Usage Patterns

### 1. Router Pattern (auth_routes.py, admin_routes.py, conversation_routes.py)

**Purpose**: Organizing endpoints into logical groups using APIRouter

**Pattern**:
```python
from fastapi import APIRouter, Depends, HTTPException, Header

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register(email: EmailStr, password: str):
    # Implementation
    pass

@router.post("/login")
async def login(email: EmailStr, password: str):
    # Implementation
    pass

# Register router in main app
app.include_router(router)
```

**All Behaviors**:
- Prefix groups related endpoints ("/auth", "/admin", "/conversations")
- Tags for OpenAPI documentation grouping
- Automatic OpenAPI schema generation
- Router inclusion in main app via include_router()

---

### 2. Dependency Injection (all route files)

**Purpose**: Injecting services and authentication into route handlers

**Pattern**:
```python
from fastapi import Depends

# Dependency function
async def require_auth(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    # Verify token and return user
    return user

# Route with dependency
@router.get("/me")
async def get_current_user(current_user: dict = Depends(require_auth)):
    return current_user
```

**All Behaviors**:
- Dependencies declared with Depends()
- Automatic parameter injection
- Dependency results passed as parameters
- Multiple dependencies can be chained
- Dependencies can raise exceptions to short-circuit

---

### 3. Pydantic Validation (schemas/chat.py)

**Purpose**: Request/response validation using Pydantic models

**Pattern**:
```python
from pydantic import BaseModel, EmailStr

class ChatRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return ChatResponse(message="...", conversation_id="...")
```

**All Behaviors**:
- Automatic request body validation
- Type coercion and validation errors
- response_model ensures response schema
- EmailStr validation for emails
- Optional fields with defaults

---

### 4. SSE Streaming (routes.py)

**Purpose**: Server-Sent Events for real-time streaming

**Pattern**:
```python
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(request: ChatRequest):
    async def event_generator():
        for event in chat_service.stream_chat(...):
            yield event
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**All Behaviors**:
- StreamingResponse for SSE
- media_type="text/event-stream" required
- Generator function for event streaming
- Connection kept alive until generator completes
- Client receives events in real-time

---

### 5. Error Handling

**Pattern**:
```python
from fastapi import HTTPException

@router.get("/resource/{id}")
async def get_resource(id: str):
    resource = find_resource(id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
```

**All Behaviors**:
- HTTPException for error responses
- status_code and detail parameters
- Automatic JSON error response
- Exception propagation to FastAPI error handler

---

## Common Patterns

**Pattern 1: JWT Authentication Middleware**
- Usage: Protect routes with require_auth dependency
- Example files: auth_routes.py, admin_routes.py, conversation_routes.py

**Pattern 2: Router Organization**
- Usage: Group related endpoints with APIRouter
- Example files: All route files use routers with prefixes

**Pattern 3: Pydantic Schema Validation**
- Usage: Validate request/response bodies
- Example files: chat.py defines all Pydantic models

---

## Best Practices

From observed usage in the codebase:
- Use routers with prefixes for logical grouping
- Declare dependencies for auth, services, database connections
- Use Pydantic models for all request/response validation
- Raise HTTPException for error responses (not return)
- Use async def for route handlers (ASGI support)
- Document routes with docstrings (appears in OpenAPI)

---

## Used By Features

- **[JWT Authentication](../features/jwt-authentication.md)** - Auth routes
- **[Conversation CRUD](../features/conversation-crud.md)** - Conversation routes
- **[Natural Language SQL](../features/natural-language-sql.md)** - Chat endpoint
- **[Data Streaming](../features/data-streaming.md)** - SSE streaming
- **[Admin Panel](../features/admin-panel.md)** - Admin routes
- **[Schema Introspection](../features/schema-introspection.md)** - Schema endpoint

---

## Used In Projects

- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Main API framework

---

## Configuration

```python
# main.py example
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DB Chat API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(conversation_routes.router)
app.include_router(routes.router)
```
