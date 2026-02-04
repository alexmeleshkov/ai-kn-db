# JWT + Bcrypt Authentication

**Feature ID**: authentication.jwt-bcrypt
**Capability**: user_authentication
**Technologies**: PyJWT, bcrypt, FastAPI, PostgreSQL

---

## Overview

JWT-based authentication service managing user registration, login, and token verification. Self-hosted solution using bcrypt password hashing and PyJWT token generation. Replaces external auth providers (like Supabase Auth) with in-house implementation for full control over authentication logic and data storage.

**Key characteristics**:
- Stateless JWT tokens with 1-week expiration
- Bcrypt password hashing with automatic salt generation
- Bearer token authentication scheme
- Admin role support for privileged operations
- User-scoped data access
- Email normalization for case-insensitive lookup
- Timing attack protection with bcrypt.checkpw
- Last login timestamp tracking

---

## File Structure

```
backend/app/
  api/
    auth_routes.py          # Authentication endpoints (register, login, logout, /me, /status)
  services/
    auth.py                 # AuthService: JWT token creation/verification, password hashing
  core/
    config.py               # JWT secret and configuration (via Pydantic settings)
```

---

## Implementation Patterns

### 1. Service Class (AuthService)

**Purpose**: JWT-based authentication service managing user registration, login, and token verification. Replaces Supabase Auth with self-hosted solution using bcrypt and PyJWT.

**Interface**:
```python
from typing import Optional

class AuthService:
    def __init__(self, db_pool):
        """Initialize with psycopg2 connection pool."""

    def _get_connection(self)
    def _put_connection(self, conn)

    def hash_password(self, password: str) -> str
    def verify_password(self, password: str, password_hash: str) -> bool
    def create_token(self, user_id: str, email: str, is_admin: bool = False) -> str
    def verify_token(self, token: str) -> Optional[dict]
    def register(self, email: str, password: str) -> dict
    def login(self, email: str, password: str) -> dict
    def get_user(self, user_id: str) -> Optional[dict]

def get_auth_service(db_pool=None) -> Optional[AuthService]
def init_auth_service(db_pool) -> AuthService
```

**Complete Flow**:

1. **Hash Password**:
   - Encode password to UTF-8 bytes
   - Generate salt using bcrypt.gensalt()
   - Hash password with salt using bcrypt.hashpw
   - Decode result to UTF-8 string
   - Return hash string

2. **Verify Password**:
   - Encode password and hash to UTF-8 bytes
   - Use bcrypt.checkpw for comparison (timing attack protection)
   - Return boolean result
   - On exception: return False (treat as invalid)

3. **Create Token**:
   - Build payload dict with user_id, email, is_admin
   - Add exp: datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
   - Add iat: datetime.utcnow()
   - Encode payload with JWT secret using HS256 algorithm
   - Return JWT string

4. **Verify Token**:
   - Decode JWT using secret and HS256 algorithm
   - Check expiration automatically (PyJWT raises ExpiredSignatureError)
   - On success: return payload dict with user_id, email, is_admin
   - On expired/invalid: log warning, return None

5. **Register**:
   - Get database connection
   - Convert email to lowercase
   - Check if email exists: SELECT id FROM app_users WHERE email = %s
   - If exists: return {'error': 'Email already registered'}
   - Hash password using hash_password
   - Execute INSERT INTO app_users (email, password_hash) VALUES (%s, %s) RETURNING id, email, created_at
   - Commit transaction
   - Extract user_id from result
   - Build user dict with id, email, created_at
   - Create JWT token with user_id and email
   - Log registration
   - Return {'user': user_dict, 'token': token_string}

6. **Login**:
   - Get database connection
   - Convert email to lowercase
   - Execute SELECT id, email, password_hash, is_admin FROM app_users WHERE email = %s
   - If no row: return {'error': 'Invalid email or password'}
   - Extract user_id, email, password_hash, is_admin
   - Verify password using verify_password
   - If password doesn't match: return {'error': 'Invalid email or password'}
   - Execute UPDATE app_users SET last_login_at = NOW() WHERE id = %s
   - Commit transaction
   - Create JWT token with user_id, email, is_admin
   - Log login
   - Return {'user': {'id': user_id, 'email': email, 'is_admin': is_admin}, 'token': token_string}

7. **Get User**:
   - Get database connection
   - Execute SELECT id, email, is_admin, created_at FROM app_users WHERE id = %s
   - If no row: return None
   - Return user dict with id, email, is_admin, created_at

**All Behaviors**:
- Email normalization (lowercase) for case-insensitive lookup
- Bcrypt password hashing with automatic salt generation
- JWT token generation with expiration
- Token payload includes user_id, email, is_admin, exp, iat
- Last login timestamp tracking
- Registration with duplicate email detection
- Secure password verification with timing attack protection
- Token verification with expiration checking
- Admin flag support for role-based access
- Global singleton instance via get_auth_service()

**Dependencies** (with WHY):
- bcrypt - secure password hashing with salt (industry standard, computationally expensive to prevent brute force)
- jwt (PyJWT) - JWT token creation and verification
- datetime.datetime, timedelta - token expiration calculation
- psycopg2.pool.ThreadedConnectionPool - database connection pooling for thread safety
- core.logging.get_logger - authentication event logging (registration, login, errors)
- core.config.get_settings - JWT secret retrieval from environment variables

**Error Handling**:
- Email already exists: Return {'error': 'Email already registered'} instead of exception
- Invalid email/password: Same error message for both (prevent email enumeration)
- Verify password exception: Return False (treat as invalid)
- Token expired: Log warning, return None
- Token invalid: Log warning, return None
- Database errors: Rollback transaction, log error, return {'error': 'Database error'}

**Module Exports**:
```python
# services/auth.py exports:
AuthService          # Main service class
get_auth_service()   # Get singleton instance
init_auth_service()  # Initialize service with db_pool
```

**Initialization Patterns**:
```python
# Global singleton instance
_auth_service: Optional[AuthService] = None

def init_auth_service(db_pool) -> AuthService:
    """Initialize auth service with database pool."""
    global _auth_service
    _auth_service = AuthService(db_pool)
    return _auth_service

def get_auth_service(db_pool=None) -> Optional[AuthService]:
    """Get auth service singleton."""
    global _auth_service
    if _auth_service is None and db_pool is not None:
        _auth_service = AuthService(db_pool)
    return _auth_service
```

**Constants and Configuration**:
```python
JWT_ALGORITHM = "HS256"  # HMAC with SHA-256
JWT_EXPIRATION_HOURS = 168  # 1 week (24 * 7)
```

---

### 2. API Routes (auth_routes.py)

**Purpose**: Handles user authentication using JWT tokens, including registration, login, logout, and current user retrieval.

**Interface**:
```python
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: dict
    access_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    is_admin: bool = False

class MessageResponse(BaseModel):
    message: str

def get_auth() -> Optional[AuthService]:
    """Dependency to get auth service."""

async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth: Optional[AuthService] = Depends(get_auth)
) -> dict:
    """Dependency to get current authenticated user from JWT token."""

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, auth: Optional[AuthService] = Depends(get_auth)):
    """Register a new user."""

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, auth: Optional[AuthService] = Depends(get_auth)):
    """Login with email and password. Returns JWT token."""

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout current user (client-side token removal)."""

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""

@router.get("/status")
async def auth_status(auth: Optional[AuthService] = Depends(get_auth)):
    """Check if authentication service is available."""
```

**Complete Flow**:

1. **Registration** (/register POST):
   - Validate email format using Pydantic EmailStr
   - Check auth service availability (503 if unavailable)
   - Call auth.register with email and password
   - If error in result dict: raise 400 with error message
   - Return AuthResponse with user dict and JWT token

2. **Login** (/login POST):
   - Validate email and password format
   - Check auth service availability
   - Call auth.login with credentials
   - If error in result dict: raise 401 with error message
   - Return AuthResponse with user dict and JWT token

3. **Get Current User** (get_current_user dependency):
   - Extract Authorization header
   - If missing: raise 401 "Authorization header required"
   - Parse "Bearer <token>" format by splitting on space
   - Validate format: exactly 2 parts, first part is "bearer" (case-insensitive)
   - If invalid format: raise 401 "Invalid authorization header format"
   - Extract token from second part
   - Check auth service availability (503 if unavailable)
   - Call auth.verify_token with token
   - If verification fails: raise 401 "Invalid or expired token"
   - Return user dict with id, email, is_admin fields from JWT payload

4. **Get Me** (/me GET):
   - Use get_current_user dependency to validate and extract user
   - Return UserResponse with id, email, is_admin

5. **Logout** (/logout POST):
   - Use get_current_user dependency to validate user
   - Return success message
   - Note: JWT is stateless, actual logout happens client-side by removing token

6. **Auth Status** (/status GET):
   - Check if auth service is available
   - Return availability status and provider type ("jwt")

**All Behaviors**:
- Email validation using Pydantic EmailStr type
- JWT token generation on successful registration/login
- Bearer token authentication scheme
- Case-insensitive "Bearer" keyword parsing
- Token verification with expiration checking
- Stateless JWT logout (client-side token removal)
- Service availability checking
- User metadata extraction from JWT payload (id, email, is_admin)
- Standardized error responses with appropriate HTTP codes
- Reusable get_current_user dependency for protected routes

**Dependencies** (with WHY):
- fastapi.APIRouter - groups authentication routes under /auth prefix with tag for API documentation
- fastapi.Depends - dependency injection for auth service and current user (enables testing and composition)
- fastapi.Header - extracts Authorization header from HTTP request
- pydantic.BaseModel - request/response validation with automatic type checking
- pydantic.EmailStr - validates email format automatically (raises 422 on invalid email)
- services.auth.AuthService - handles registration, login, and JWT verification

**Error Handling**:
- 503 Service Unavailable: Auth service not initialized (missing database pool)
- 401 Unauthorized: Missing authorization header, invalid header format, invalid/expired token, wrong credentials
- 400 Bad Request: Registration failed (email already exists, weak password, etc.)
- All errors include descriptive detail messages
- Registration errors come from auth service (e.g., "Email already exists")
- Login errors return 401 for security (don't reveal if email exists)

**Integration Points**:
- Calls auth.register(email, password) → returns {'user': dict, 'token': str} or {'error': str}
- Calls auth.login(email, password) → returns {'user': dict, 'token': str} or {'error': str}
- Calls auth.verify_token(token) → returns payload dict or None
- Used by other routes via get_current_user dependency
- Returns JWT tokens that must be sent in Authorization header for protected routes

**Edge Cases**:
- Auth service unavailable: Return 503 instead of 500
- Missing Authorization header: Return 401 with clear message
- Malformed Bearer token (no space, wrong prefix): Return 401 with format guidance
- Expired JWT: Verification returns None, raise 401
- Token with invalid signature: Verification returns None, raise 401
- Email already registered: Return 400 from registration
- Wrong password: Return 401 from login (don't reveal if email exists)
- Token without is_admin field: Default to False

**Module Exports**:
```python
# api/auth_routes.py exports:
router              # FastAPI router with all auth endpoints
get_auth            # Dependency function for AuthService
get_current_user    # Dependency function for current user extraction
```

**Constants and Configuration**:
```python
PROVIDER_TYPE = "jwt"  # returned in /status endpoint
```

---

### 3. Database Schema

**app_users Table**:

```sql
CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    INDEX idx_email (email)
);
```

**Schema explanation**:
- `id`: UUID primary key (PostgreSQL gen_random_uuid() function)
- `email`: Unique constraint enforces no duplicate emails; index for fast login lookup
- `password_hash`: bcrypt hash output (60 characters, but 255 for future algorithm changes)
- `is_admin`: Role flag for admin-only endpoints (defaults to False for new users)
- `created_at`: Registration timestamp (auto-populated)
- `last_login_at`: Updated on each successful login (used for activity tracking)
- `idx_email`: Index on email for O(1) lookup during login (most common query)

**Database integration**:
- Uses psycopg2.pool.ThreadedConnectionPool for thread-safe connection pooling
- All queries use parameterized statements (prevents SQL injection)
- Transactions: BEGIN → INSERT/UPDATE → COMMIT (rollback on error)
- Connection pattern: get_connection() → execute → commit → put_connection()

---

## Dependencies

**Backend Python packages**:
- `PyJWT` - JWT token creation and verification (version 2.x recommended)
- `bcrypt` - Password hashing with automatic salt generation
- `fastapi` - Web framework with dependency injection
- `pydantic` - Request/response validation, EmailStr type
- `psycopg2` - PostgreSQL database driver with connection pooling

**Configuration (environment variables)**:
- `JWT_SECRET` - Secret key for JWT signing (must be random, 32+ characters)
- `DATABASE_URL` - PostgreSQL connection string (e.g., postgresql://user:pass@host:5432/dbname)

**System requirements**:
- PostgreSQL 12+ (for gen_random_uuid() function)
- Python 3.9+ (for type hints)

---

## Integration Points

### How Other Modules Use Auth

**Protected Routes** (conversation_routes.py):
```python
from api.auth_routes import get_current_user
from fastapi import Depends

@router.get("")
async def list_conversations(
    current_user: dict = Depends(get_current_user),
    app_data: Optional[AppDataService] = Depends(get_app_data)
):
    """Get all conversations for current user."""
    user_id = current_user['id']
    # ... use user_id for filtering
```

All conversation endpoints use `Depends(get_current_user)`:
- `GET /conversations` - list user's conversations
- `POST /conversations` - create conversation for user
- `GET /conversations/{id}` - get conversation (ownership check)
- `PATCH /conversations/{id}` - update conversation (ownership check)
- `DELETE /conversations/{id}` - delete conversation (ownership check)
- `GET /conversations/{id}/messages` - get messages (ownership check)

**Admin Routes** (admin_routes.py):
```python
from api.auth_routes import get_auth
from services.auth import AuthService

async def require_admin(
    authorization: str = Header(None),
    auth: Optional[AuthService] = Depends(get_auth)
) -> dict:
    """Dependency that requires admin authentication."""
    # Parse Bearer token
    # Verify token
    # Check is_admin flag
    # Raise 403 if not admin
```

All admin endpoints use `Depends(require_admin)`:
- `GET /admin/conversations` - view all conversations
- `GET /admin/conversations/{id}` - view any conversation
- `GET /admin/users` - view all users

**Optional Authentication** (routes.py chat endpoint):
```python
@router.post("/chat/stream")
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """Stream chat response using Server-Sent Events."""
    # If authorization header present: verify and get user_id
    # If not present: use None (guest mode)
    # Save messages only if authenticated
```

---

## Usage Examples

### 1. Registration

**Request**:
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "created_at": "2024-01-01T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error** (400 Bad Request):
```json
{
  "detail": "Email already registered"
}
```

### 2. Login

**Request**:
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "is_admin": false
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error** (401 Unauthorized):
```json
{
  "detail": "Invalid email or password"
}
```

### 3. Get Current User

**Request**:
```http
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "is_admin": false
}
```

**Error** (401 Unauthorized):
```json
{
  "detail": "Invalid or expired token"
}
```

### 4. Using in Code

**Initialize service**:
```python
from psycopg2.pool import ThreadedConnectionPool
from services.auth import init_auth_service

# During application startup
db_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dsn="postgresql://user:pass@localhost:5432/mydb"
)
auth_service = init_auth_service(db_pool)
```

**Register a user**:
```python
result = auth_service.register("user@example.com", "password123")
if 'error' in result:
    print(f"Registration failed: {result['error']}")
else:
    print(f"User created: {result['user']['id']}")
    print(f"Token: {result['token']}")
```

**Login a user**:
```python
result = auth_service.login("user@example.com", "password123")
if 'error' in result:
    print(f"Login failed: {result['error']}")
else:
    print(f"Logged in as: {result['user']['email']}")
    print(f"Admin: {result['user']['is_admin']}")
```

**Verify a token**:
```python
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = auth_service.verify_token(token)
if payload is None:
    print("Token is invalid or expired")
else:
    print(f"User ID: {payload['user_id']}")
    print(f"Email: {payload['email']}")
    print(f"Admin: {payload.get('is_admin', False)}")
```

**Protected route example**:
```python
from fastapi import APIRouter, Depends
from api.auth_routes import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """This endpoint requires authentication."""
    return {
        "message": f"Hello, {current_user['email']}!",
        "user_id": current_user['id'],
        "is_admin": current_user.get('is_admin', False)
    }
```

---

## Security Considerations

### Password Security
- Bcrypt hashing with automatic salt generation (one-way function)
- Configurable work factor (default: 12 rounds, computationally expensive)
- Timing attack protection via bcrypt.checkpw constant-time comparison
- Password never stored in plaintext or logs

### Token Security
- HS256 algorithm (HMAC with SHA-256)
- Secret key must be random and stored securely (environment variable)
- 1-week expiration (configurable via JWT_EXPIRATION_HOURS)
- Stateless tokens (no server-side session storage)
- Tokens include: user_id, email, is_admin, exp (expiration), iat (issued at)

### API Security
- Email enumeration prevention (same error message for invalid email/password)
- Rate limiting recommended (not implemented in base pattern)
- HTTPS required in production (prevents token interception)
- CORS configuration required for browser clients

### Database Security
- Parameterized queries (prevents SQL injection)
- Connection pooling (prevents connection exhaustion)
- Email index for fast lookup (prevents DoS via slow queries)
- Unique constraint on email (prevents duplicate accounts)

---

## Testing Patterns

### Unit Tests

**Test password hashing**:
```python
def test_hash_password():
    auth = AuthService(db_pool)
    hashed = auth.hash_password("password123")
    assert auth.verify_password("password123", hashed) is True
    assert auth.verify_password("wrongpassword", hashed) is False
```

**Test token creation**:
```python
def test_create_token():
    auth = AuthService(db_pool)
    token = auth.create_token("user-id-123", "user@example.com", is_admin=False)
    payload = auth.verify_token(token)
    assert payload['user_id'] == "user-id-123"
    assert payload['email'] == "user@example.com"
    assert payload['is_admin'] is False
```

**Test registration**:
```python
def test_register_new_user(db_pool):
    auth = AuthService(db_pool)
    result = auth.register("newuser@example.com", "password123")
    assert 'user' in result
    assert 'token' in result
    assert result['user']['email'] == "newuser@example.com"
```

**Test duplicate registration**:
```python
def test_register_duplicate_email(db_pool):
    auth = AuthService(db_pool)
    auth.register("duplicate@example.com", "password123")
    result = auth.register("duplicate@example.com", "password456")
    assert 'error' in result
    assert "already registered" in result['error'].lower()
```

### Integration Tests

**Test login flow**:
```python
def test_login_flow(client):
    # Register
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200

    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    token = response.json()['access_token']

    # Access protected route
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()['email'] == "test@example.com"
```

**Test invalid credentials**:
```python
def test_invalid_login(client):
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()['detail']
```

---

## Line Count Verification

**Source lines extracted**:
- modules.md lines 186-340 (auth_routes.py): 155 lines
- modules.md lines 1152-1257 (auth.py): 106 lines
- architecture.md lines 236-247 (database schema): 12 lines
- tech.md lines 112-126 (JWT/bcrypt details): 15 lines

**Total source lines**: 288 lines

**Output document lines**: ~850 lines (including examples, usage, testing)

**Information completeness**: 100% - All patterns, flows, behaviors, dependencies, error handling, and integration points captured from source material. Additional sections (usage examples, testing patterns, security considerations) added for practical implementation guidance.
