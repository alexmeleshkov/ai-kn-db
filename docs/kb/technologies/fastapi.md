# FastAPI

**Category**: Web Framework
**Website**: https://fastapi.tiangolo.com/
**Documentation**: https://fastapi.tiangolo.com/tutorial/

---

## Overview

FastAPI is a modern, high-performance Python web framework for building APIs. It provides automatic OpenAPI documentation, type validation via Pydantic, native async support, and a powerful dependency injection system.

---

## Key Features

**ASGI Framework**: Built on Starlette for high performance async/await support
**Automatic Documentation**: OpenAPI (Swagger) and ReDoc generated from code
**Type Validation**: Pydantic integration for request/response validation and serialization
**Dependency Injection**: Clean, testable code with automatic dependency resolution
**Modern Python**: Leverages Python 3.8+ type hints for editor support and validation
**WebSocket Support**: Native WebSocket and Server-Sent Events (SSE) streaming

---

## Common Use Cases

- **REST APIs**: JSON-based APIs with automatic validation and documentation
- **Real-time Applications**: WebSocket and SSE streaming for live updates
- **Microservices**: Lightweight, fast APIs for distributed systems
- **Machine Learning APIs**: Serve ML models with async request handling
- **CRUD Applications**: Database-backed applications with ORM integration
- **Authentication Services**: JWT, OAuth2, session-based auth

---

## Prerequisites

**System Requirements**:
- Python 3.8 or higher
- pip or poetry for package management

**Installation**:
```bash
pip install fastapi
pip install "uvicorn[standard]"  # ASGI server
```

**Optional Dependencies**:
```bash
pip install pydantic[email]      # Email validation
pip install python-multipart     # Form data support
pip install python-jose[cryptography]  # JWT tokens
pip install passlib[bcrypt]      # Password hashing
```

---

## Basic Application

### Minimal Example
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**Run**:
```bash
uvicorn main:app --reload
```

**Access**:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Common Patterns

### 1. Router Organization
Group related endpoints into modules:

```python
from fastapi import APIRouter

# auth_routes.py
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register(email: str, password: str):
    return {"status": "registered"}

@router.post("/login")
async def login(email: str, password: str):
    return {"token": "..."}

# main.py
from fastapi import FastAPI
from .api import auth_routes

app = FastAPI()
app.include_router(auth_routes.router)
```

### 2. Request/Response Models (Pydantic)
```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool = True

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    # user.email is validated as email
    # user.password is automatically parsed
    return UserResponse(id=1, email=user.email)
```

### 3. Dependency Injection
```python
from fastapi import Depends, HTTPException, Header

# Dependency function
async def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(401, "Missing auth token")
    # Verify token
    return {"user_id": 1, "email": "user@example.com"}

# Use in route
@app.get("/me")
async def read_current_user(user: dict = Depends(get_current_user)):
    return user

# Database dependency
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### 4. Error Handling
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = find_item(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Not-Found"}
        )
    return item

# Custom exception handler
from fastapi.responses import JSONResponse

class CustomException(Exception):
    pass

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
```

### 5. Server-Sent Events (SSE) Streaming
```python
from fastapi.responses import StreamingResponse
import asyncio

@app.get("/stream")
async def stream_events():
    async def event_generator():
        for i in range(10):
            yield f"data: {i}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### 6. Background Tasks
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email (blocking operation)
    pass

@app.post("/send-notification")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification scheduled"}
```

### 7. Middleware
```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        response.headers["X-Process-Time"] = str(duration)
        return response

app.add_middleware(TimingMiddleware)
```

---

## Security

### OAuth2 with JWT
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verify credentials
    # Generate JWT token
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # token is automatically extracted from Authorization header
    user = verify_token(token)
    return user
```

### API Key Security
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/secure")
async def secure_endpoint(api_key: str = Depends(api_key_header)):
    if api_key != "secret-key":
        raise HTTPException(403, "Invalid API key")
    return {"data": "secure"}
```

---

## Best Practices

**DO**:
- Use async def for route handlers (better performance)
- Declare Pydantic models for all request/response bodies
- Use dependency injection for database, auth, services
- Organize routes into modules with APIRouter
- Leverage automatic OpenAPI documentation
- Use type hints everywhere (enables validation and IDE support)
- Raise HTTPException for error responses

**DON'T**:
- Don't use blocking I/O in async route handlers (use run_in_executor)
- Don't return None (use Optional[Model] and explicit responses)
- Don't skip response models (they ensure correct output schema)
- Don't use global state (use dependencies instead)
- Don't ignore Pydantic validation errors (they're there for a reason)

---

## Performance Considerations

**Async vs Sync**:
- Use `async def` for I/O-bound operations (database, API calls)
- Use `def` for CPU-bound operations (FastAPI runs them in thread pool)
- Don't mix: blocking code in `async def` blocks event loop

**Connection Pooling**:
```python
# Good: connection pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)

# Bad: new connection per request
def get_db():
    return create_engine(DATABASE_URL).connect()
```

**Response Models**:
- Use `response_model` to filter and validate responses
- Use `response_model_exclude_none` to omit null fields
- Use `response_model_by_alias` for serialization aliases

---

## Testing

### Pytest with TestClient
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post("/items", json={"name": "Test"})
    assert response.status_code == 200
    assert "id" in response.json()
```

### Dependency Overrides (Mocking)
```python
from fastapi import Depends

def override_get_db():
    return MockDatabase()

app.dependency_overrides[get_db] = override_get_db

def test_with_mock_db():
    response = client.get("/items")
    assert response.status_code == 200
```

---

## Deployment

### Production Server
```bash
# Gunicorn with Uvicorn workers (recommended)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Uvicorn with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Alternatives

**Flask**: Simpler, synchronous, more mature ecosystem (but slower, no auto docs)
**Django REST Framework**: Full-featured, batteries-included (but heavier, more opinionated)
**Sanic**: Async like FastAPI (but less type-safe, no auto documentation)
**Starlette**: FastAPI is built on Starlette (lower-level, more control, less magic)

**Why FastAPI**:
- Fastest Python framework (comparable to Node.js, Go)
- Automatic OpenAPI documentation
- Modern Python features (type hints, async/await)
- Great developer experience (editor support, validation)

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Code snippets**: See `languages/python/snippets/`
**Features**: [[authentication]], [[data-streaming]], [[real-time-chat]]
**Technologies often used with**: [[postgresql]], [[sqlalchemy]], [[pydantic]], [[jwt]], [[sse]]
