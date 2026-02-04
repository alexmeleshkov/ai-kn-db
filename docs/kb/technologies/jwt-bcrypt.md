# JWT + bcrypt

**Technology**: PyJWT + bcrypt
**Category**: Authentication Library

---

## Overview

JWT token generation/verification with bcrypt password hashing for stateless authentication.

---

## Usage Files

- `backend/app/services/auth.py`
- `backend/app/api/auth_routes.py`

---

## Complete Usage Patterns

### Password Hashing (auth.py)

**Pattern**:
```python
import bcrypt
import jwt

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)
```

**All Behaviors**:
- Auto-generated salt with bcrypt.gensalt()
- Timing attack protection with checkpw
- UTF-8 encoding for string/bytes conversion

### JWT Token Creation (auth.py)

**Pattern**:
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str, email: str, is_admin: bool = False) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

**All Behaviors**:
- 7-day token expiration
- HS256 algorithm
- Automatic expiration checking
- Payload includes user_id, email, is_admin

---

## Configuration

```python
SECRET_KEY = "your-secret-key"  # From environment
TOKEN_EXPIRY_DAYS = 7
ALGORITHM = "HS256"
```
