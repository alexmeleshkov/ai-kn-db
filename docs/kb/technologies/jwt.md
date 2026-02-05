# JWT (JSON Web Tokens)

**Category**: Authentication / Security
**Website**: https://jwt.io/
**Documentation**: https://datatracker.ietf.org/doc/html/rfc7519

---

## Overview

JSON Web Tokens (JWT) is a compact, URL-safe token format for securely transmitting information between parties. JWTs are stateless and self-contained, carrying user identity and claims in a signed payload.

---

## Key Concepts

**Structure**: `header.payload.signature`
- **Header**: Algorithm and token type (e.g., {"alg": "HS256", "typ": "JWT"})
- **Payload**: Claims (user data, expiration, issuer, etc.)
- **Signature**: HMAC or RSA signature preventing tampering

**Claims**:
- `sub` (subject): User identifier
- `exp` (expiration): Unix timestamp when token expires
- `iat` (issued at): When token was created
- `iss` (issuer): Who created the token
- Custom claims: email, role, permissions, etc.

**Stateless**: Server doesn't store tokens - validation uses signature only

---

## Common Use Cases

- **API Authentication**: REST APIs, microservices
- **Single Sign-On (SSO)**: Share authentication across domains
- **Mobile Apps**: Token storage in secure storage
- **Serverless**: No session state required

---

## Algorithms

**Symmetric (HMAC)**:
- `HS256` (HMAC-SHA256): Shared secret key
- Fast, simple, but secret must be shared between services

**Asymmetric (RSA/ECDSA)**:
- `RS256` (RSA-SHA256): Public/private key pair
- `ES256` (ECDSA-SHA256): Elliptic curve (smaller keys)
- Private key signs, public key verifies
- Good for distributed systems (public key can be shared)

---

## Security Considerations

**Token Expiration**:
- Short-lived access tokens (15 min - 24 hours)
- Long-lived refresh tokens (days to weeks)
- Balance security vs UX

**Secret Key Security**:
- Store in environment variables (never in code)
- Use strong random secrets (256+ bits)
- Rotate keys periodically

**Token Storage**:
- **localStorage**: Accessible to JavaScript (XSS risk)
- **sessionStorage**: Cleared on tab close
- **httpOnly cookie**: Not accessible to JavaScript (more secure)

**Validation**:
- Always verify signature
- Check expiration (exp claim)
- Validate issuer if multi-tenant
- Reject tokens with "none" algorithm

**Logout**:
- Client discards token
- Optional: Server-side token blacklist (adds state)
- Short expiration reduces risk

---

## Implementation (Python)

**Installation**:
```bash
pip install pyjwt
```

**Create Token**:
```python
import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: str, email: str, is_admin: bool, secret: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, secret, algorithm="HS256")
```

**Verify Token**:
```python
def verify_token(token: str, secret: str) -> dict | None:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.DecodeError:
        return None  # Invalid token
```

**Bearer Token in FastAPI**:
```python
from fastapi import Header, HTTPException

def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(401, "Authorization header required")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(401, "Invalid authorization header format")

    token = parts[1]
    payload = verify_token(token, JWT_SECRET)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    return payload
```

---

## Implementation (TypeScript)

**Installation**:
```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken
```

**Frontend Usage** (no verification, just storage):
```typescript
// Store token
localStorage.setItem('jwt_token', token)

// Send with request
const response = await fetch('/api/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})

// Handle 401
if (response.status === 401) {
  localStorage.removeItem('jwt_token')
  navigate('/login')
}
```

---

## Best Practices

**DO**:
- Use HTTPS in production
- Set short expiration times
- Store secrets securely
- Validate on every request
- Use refresh tokens for long sessions

**DON'T**:
- Store sensitive data in payload (it's not encrypted, just signed)
- Use "none" algorithm
- Store tokens in URLs or query parameters
- Share secret keys publicly
- Skip signature verification

---

## Common Patterns

### Access Token + Refresh Token
1. Login returns short-lived access token (15 min) + long-lived refresh token (7 days)
2. Frontend uses access token for API calls
3. When access token expires, use refresh token to get new access token
4. Refresh tokens stored securely (httpOnly cookie or secure storage)
5. If refresh token expired, user must login again

### Token Refresh Endpoint
```python
@app.post("/auth/refresh")
async def refresh(refresh_token: str) -> dict:
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    new_access_token = create_access_token(
        payload["user_id"],
        payload["email"],
        payload["is_admin"]
    )
    return {"access_token": new_access_token}
```

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[authentication]], [[authorization]]
**Alternatives**: [[oauth2]], [[session-cookies]], [[paseto]]
**Often used with**: [[bcrypt]], [[fastapi]], [[react-hooks]]
