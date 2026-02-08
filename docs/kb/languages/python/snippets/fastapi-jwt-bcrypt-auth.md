# Python + FastAPI - JWT Authentication with bcrypt

**Language**: Python
**Technology**: FastAPI
**Feature/Pattern**: JWT Authentication with bcrypt password hashing
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
pip install fastapi pydantic pydantic[email] bcrypt pyjwt psycopg2-binary
```

**Required Knowledge**:
- FastAPI dependency injection system
- HTTP Bearer token authentication
- JWT token structure and validation
- Password hashing with bcrypt
- PostgreSQL database operations

---

## Overview

This snippet demonstrates a complete JWT-based authentication system using FastAPI with bcrypt password hashing. It includes user registration, login, token creation/verification, and a dependency injection pattern for protecting routes. The implementation uses PostgreSQL for user storage and includes proper error handling and security practices.

Key features:
- Bcrypt password hashing (salt generation + secure hashing)
- JWT token creation with expiration
- FastAPI dependency injection for authentication
- Bearer token validation from headers
- Connection pool management
- Proper error responses

---

## Implementation

### Basic Usage

#### Password Hashing with bcrypt

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False
```

**Explanation**:
- Line 5: `bcrypt.gensalt()` generates a unique salt for each password
- Line 5: `hashpw()` combines password with salt and creates hash
- Line 10: `checkpw()` verifies password against stored hash (salt embedded in hash)

#### JWT Token Creation

```python
import jwt
from datetime import datetime, timedelta

JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24 * 7  # 1 week

def create_token(user_id: str, email: str, is_admin: bool = False, secret: str = "your-secret-key") -> str:
    """Create JWT token for user."""
    payload = {
        'user_id': user_id,
        'email': email,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)

def verify_token(token: str, secret: str = "your-secret-key") -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return {
            'user_id': payload['user_id'],
            'email': payload['email'],
            'is_admin': payload.get('is_admin', False)
        }
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

**Key Points**:
- `exp`: Expiration timestamp (automatically checked by PyJWT)
- `iat`: Issued at timestamp (for audit trail)
- Token is stateless (no server-side session storage needed)

### Advanced Usage

#### FastAPI Dependency for Authentication

```python
from fastapi import Depends, HTTPException, Header
from typing import Optional

async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth: Optional[AuthService] = Depends(get_auth)
) -> dict:
    """
    Dependency to get current authenticated user from JWT token.
    Extract and verify Bearer token from Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]

    # Verify token
    if not auth:
        raise HTTPException(status_code=503, detail="Authentication service unavailable")

    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        'id': payload['user_id'],
        'email': payload['email'],
        'is_admin': payload.get('is_admin', False)
    }
```

**Usage in Routes**:
```python
@router.get("/protected-resource")
async def protected_route(
    current_user: dict = Depends(get_current_user)
):
    """This route requires authentication."""
    return {"message": f"Hello {current_user['email']}"}
```

---

## Complete Example

### Full Authentication Service

```python
"""
JWT Authentication Service with bcrypt password hashing.
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional

JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24 * 7  # 1 week

class AuthService:
    """
    JWT-based authentication service.
    Uses bcrypt for password hashing and PyJWT for tokens.
    """

    def __init__(self, db_pool, jwt_secret: str):
        """Initialize with database connection pool and JWT secret."""
        self._db = db_pool
        self._jwt_secret = jwt_secret

    def _get_connection(self):
        """Get database connection from pool."""
        if hasattr(self._db, 'getconn'):
            return self._db.getconn()
        return self._db

    def _put_connection(self, conn):
        """Return connection to pool."""
        if hasattr(self._db, 'putconn'):
            self._db.putconn(conn)

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False

    def create_token(self, user_id: str, email: str, is_admin: bool = False) -> str:
        """Create JWT token for user."""
        payload = {
            'user_id': user_id,
            'email': email,
            'is_admin': is_admin,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self._jwt_secret, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=[JWT_ALGORITHM])
            return {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'is_admin': payload.get('is_admin', False)
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def register(self, email: str, password: str) -> dict:
        """Register a new user."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()

            # Check if email already exists
            cur.execute("SELECT id FROM app_users WHERE email = %s", (email.lower(),))
            if cur.fetchone():
                return {'error': 'Email already registered'}

            # Create user with hashed password
            password_hash = self.hash_password(password)
            cur.execute(
                """
                INSERT INTO app_users (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email, created_at
                """,
                (email.lower(), password_hash)
            )
            row = cur.fetchone()
            conn.commit()

            user_id = str(row[0])
            user = {
                'id': user_id,
                'email': row[1],
                'created_at': row[2].isoformat()
            }

            token = self.create_token(user_id, email)

            return {'user': user, 'token': token}

        except Exception as e:
            conn.rollback()
            return {'error': str(e)}
        finally:
            cur.close()
            self._put_connection(conn)

    def login(self, email: str, password: str) -> dict:
        """Login user with email and password."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()

            # Find user
            cur.execute(
                "SELECT id, email, password_hash, is_admin FROM app_users WHERE email = %s",
                (email.lower(),)
            )
            row = cur.fetchone()

            if not row:
                return {'error': 'Invalid email or password'}

            user_id, user_email, password_hash, is_admin = str(row[0]), row[1], row[2], row[3]

            # Verify password
            if not self.verify_password(password, password_hash):
                return {'error': 'Invalid email or password'}

            # Update last login timestamp
            cur.execute(
                "UPDATE app_users SET last_login_at = NOW() WHERE id = %s",
                (user_id,)
            )
            conn.commit()

            token = self.create_token(user_id, user_email, is_admin)

            return {
                'user': {
                    'id': user_id,
                    'email': user_email,
                    'is_admin': is_admin
                },
                'token': token
            }

        except Exception as e:
            return {'error': str(e)}
        finally:
            cur.close()
            self._put_connection(conn)
```

### FastAPI Routes

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

# Dependency to get current user (see "Advanced Usage" section above)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth: AuthService = Depends(get_auth_service)
) -> dict:
    """Get current authenticated user from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    token = parts[1]
    payload = auth.verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {
        'id': payload['user_id'],
        'email': payload['email'],
        'is_admin': payload.get('is_admin', False)
    }

@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    auth: AuthService = Depends(get_auth_service)
):
    """Register a new user."""
    result = auth.register(request.email, request.password)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return AuthResponse(
        user=result['user'],
        access_token=result['token']
    )

@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    auth: AuthService = Depends(get_auth_service)
):
    """Login with email and password. Returns JWT token."""
    result = auth.login(request.email, request.password)

    if 'error' in result:
        raise HTTPException(status_code=401, detail=result['error'])

    return AuthResponse(
        user=result['user'],
        access_token=result['token']
    )

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info."""
    return current_user
```

---

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_expiration_hours: int = 168  # 1 week

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_database: str = "myapp"

    class Config:
        env_file = ".env"
```

**Environment Variables** (.env):
```
JWT_SECRET=your-super-secret-key-minimum-32-characters
JWT_EXPIRATION_HOURS=168
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=myapp
```

**Database Schema**:
```sql
CREATE TABLE app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON app_users(email);
```

---

## Error Handling

```python
from fastapi import HTTPException, status

# Common error responses
def raise_unauthorized(message: str = "Invalid credentials"):
    """Raise 401 Unauthorized error."""
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"}
    )

def raise_forbidden(message: str = "Insufficient permissions"):
    """Raise 403 Forbidden error."""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )

def raise_service_unavailable(message: str = "Service temporarily unavailable"):
    """Raise 503 Service Unavailable error."""
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=message
    )

# Example usage in dependency
async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth: Optional[AuthService] = Depends(get_auth)
) -> dict:
    if not authorization:
        raise_unauthorized("Authorization header required")

    if not auth:
        raise_service_unavailable("Authentication service unavailable")

    # ... rest of implementation
```

**Common Errors**:
1. **ExpiredSignatureError**: JWT token has expired - user needs to login again
2. **InvalidTokenError**: Malformed or tampered token - reject request
3. **Missing Authorization Header**: Client didn't send token - return 401
4. **Invalid Bearer Format**: Header doesn't match "Bearer <token>" - return 401
5. **Database Connection Error**: Connection pool exhausted - return 503

---

## Testing

```python
import pytest
from fastapi.testclient import TestClient

def test_register_success(client: TestClient):
    """Test successful user registration."""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_register_duplicate_email(client: TestClient):
    """Test registration with existing email."""
    # Register first user
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    # Try to register with same email
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "differentpassword"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_login_success(client: TestClient):
    """Test successful login."""
    # Register user
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    # Login
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client: TestClient):
    """Test login with wrong password."""
    # Register user
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "correctpassword"
    })

    # Try login with wrong password
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_protected_route_with_valid_token(client: TestClient):
    """Test accessing protected route with valid token."""
    # Register and get token
    register_response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = register_response.json()["access_token"]

    # Access protected route
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_protected_route_without_token(client: TestClient):
    """Test accessing protected route without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401
```

---

## Performance Considerations

- **bcrypt rounds**: Default (12) provides good security/performance balance
- **Connection pooling**: Use ThreadedConnectionPool for psycopg2 (min 1, max 5-20 depending on load)
- **Token expiration**: Balance security (shorter) vs UX (longer) - 1 week is typical
- **Password validation**: Implement minimum length/complexity on client and server
- **Rate limiting**: Add rate limiting to login/register endpoints to prevent brute force attacks
- **Token refresh**: Consider implementing refresh tokens for better UX (auto-renewal without re-login)

---

## Security Considerations

- **JWT Secret**: Use strong, random secret (minimum 32 characters). Store in environment variables, never in code
- **HTTPS Only**: Always use HTTPS in production to prevent token interception
- **Password Requirements**: Enforce minimum password strength (length, complexity)
- **Email Normalization**: Always lowercase emails before storage to prevent duplicate accounts
- **SQL Injection**: Use parameterized queries (psycopg2 `%s` placeholders) - never string concatenation
- **Token Storage**: Client should store token in httpOnly cookie (if same-origin) or secure localStorage
- **CORS**: Configure CORS properly to prevent unauthorized domains from accessing your API
- **Bcrypt Work Factor**: Default salt rounds (12) is good for 2024. Increase over time as hardware improves
- **Token Revocation**: Consider maintaining a blacklist for revoked tokens if needed (adds state)

---

## Related

**Feature**: [[authentication]]
**Technology**: [[fastapi]], [[postgresql]], [[jwt]], [[bcrypt]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[typescript-jwt-auth.md]], [[nodejs-passport-jwt.md]]
