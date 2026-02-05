# bcrypt

**Category**: Security / Password Hashing
**Website**: https://en.wikipedia.org/wiki/Bcrypt
**Documentation**: https://github.com/pyca/bcrypt

---

## Overview

bcrypt is a password hashing function designed to be slow and computationally expensive, making brute-force attacks impractical. It automatically generates salts and includes a configurable work factor.

---

## Key Features

**Adaptive Hashing**: Adjustable work factor (cost parameter) increases computation time as hardware improves
**Automatic Salting**: Generates unique salt for each password (22-character random salt)
**Constant-Time Comparison**: checkpw() uses constant-time comparison to prevent timing attacks
**Slow by Design**: Intentionally slow hashing (tunable) to thwart brute-force attacks

---

## How It Works

1. **Generate Salt**: Random 22-character salt (128 bits)
2. **Hash Password**: bcrypt(password + salt, cost_factor)
3. **Store Hash**: Hash includes algorithm version, cost, salt, and hash (60 chars total)
4. **Verify**: Extract salt from stored hash, hash input password with same salt, compare

**Hash Format**: `$2b$12$salthere...hashhere...`
- `$2b$`: Algorithm version (2b = latest)
- `12`: Cost factor (2^12 iterations)
- Salt + hash embedded in single string

---

## Work Factor (Cost)

**Cost Parameter**: Number of hashing rounds = 2^cost
- Cost 10 = 1,024 rounds (~100ms)
- Cost 12 = 4,096 rounds (~300ms) - **recommended default**
- Cost 14 = 16,384 rounds (~1.2s)
- Cost 16 = 65,536 rounds (~5s)

**Recommendation**: Use 12-14 for web apps (balance security vs UX)

---

## Security Advantages

**Timing Attack Resistance**:
- checkpw() uses constant-time comparison
- Takes same time for valid/invalid passwords

**Rainbow Table Resistance**:
- Unique salt per password
- Cannot precompute hashes

**Brute Force Resistance**:
- Slow hashing (tunable)
- Cost factor increases over time

**Salt Security**:
- Salt stored with hash (no separate storage needed)
- Salt is not secret (just needs to be unique)

---

## Implementation (Python)

**Installation**:
```bash
pip install bcrypt
```

**Hash Password**:
```python
import bcrypt

def hash_password(password: str) -> str:
    # Generate salt (auto-generated)
    salt = bcrypt.gensalt(rounds=12)  # Cost factor 12

    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return as string (includes salt + hash)
    return hashed.decode('utf-8')
```

**Verify Password**:
```python
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

**Complete Auth Service Example**:
```python
class AuthService:
    def register(self, email: str, password: str) -> dict:
        # Check if user exists
        if self._get_user_by_email(email):
            return {"error": "User already exists"}

        # Hash password
        hashed_password = hash_password(password)

        # Create user
        user = self._create_user(email, hashed_password)

        # Generate JWT
        token = create_access_token(user.id, user.email)

        return {"user": user.to_dict(), "access_token": token}

    def login(self, email: str, password: str) -> dict:
        # Get user
        user = self._get_user_by_email(email)
        if not user:
            return {"error": "Invalid credentials"}

        # Verify password
        if not verify_password(password, user.hashed_password):
            return {"error": "Invalid credentials"}

        # Generate JWT
        token = create_access_token(user.id, user.email)

        return {"user": user.to_dict(), "access_token": token}
```

---

## Best Practices

**DO**:
- Use cost factor 12-14 for web applications
- Always use encode('utf-8') when passing strings to bcrypt
- Store entire hash string (includes algorithm, cost, salt, hash)
- Use constant-time comparison (checkpw handles this)
- Return generic error messages (don't reveal if email exists)

**DON'T**:
- Don't use cost < 10 (too fast, insecure)
- Don't use cost > 16 for web apps (UX suffers)
- Don't store salt separately (it's embedded in hash)
- Don't hash passwords client-side (server should hash)
- Don't log or return passwords/hashes in responses

---

## Password Policy

**Minimum Requirements**:
- Length: 8+ characters (12+ recommended)
- Complexity: Optional (bcrypt makes brute force hard anyway)
- No maximum length (but bcrypt has 72-byte limit)

**Validation Example**:
```python
from pydantic import BaseModel, validator

class RegisterRequest(BaseModel):
    email: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        # Optional: Check complexity
        return v
```

---

## Migration from Existing Hashes

**Scenario**: Migrating from MD5/SHA1 to bcrypt

**Approach 1**: Force password reset
- Safest but impacts UX

**Approach 2**: Gradual migration
```python
def login(email: str, password: str):
    user = get_user(email)

    if user.hash_type == "md5":
        # Verify old hash
        if hashlib.md5(password.encode()).hexdigest() != user.password:
            return {"error": "Invalid credentials"}

        # Rehash with bcrypt
        new_hash = hash_password(password)
        update_user(user.id, hash=new_hash, hash_type="bcrypt")

    elif user.hash_type == "bcrypt":
        # Normal bcrypt verification
        if not verify_password(password, user.password):
            return {"error": "Invalid credentials"}

    return {"token": create_token(user)}
```

---

## Performance Considerations

**Benchmarks** (cost factor 12):
- Hashing: ~300ms per password
- Verification: ~300ms per password

**For high-traffic APIs**:
- Consider async hashing (don't block event loop)
- Use work queues for registration
- Cache login results briefly (with caution)

**FastAPI Async Example**:
```python
import asyncio

async def hash_password_async(password: str) -> str:
    # Run bcrypt in thread pool (it's CPU-bound)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        hash_password,
        password
    )
```

---

## Alternatives

**Argon2**: Winner of Password Hashing Competition (PHC)
- More memory-hard than bcrypt
- Resistant to GPU/ASIC attacks
- Recommended for new projects

**scrypt**: Memory-hard like Argon2
- Good for cryptocurrency applications

**PBKDF2**: Standardized (NIST)
- Less resistant to GPU attacks than bcrypt

**Why bcrypt is still good**:
- Battle-tested (20+ years)
- Wide library support
- Simple API
- Good enough for most web apps

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[authentication]], [[password-security]]
**Often used with**: [[jwt]], [[postgresql]], [[fastapi]]
**Alternatives**: [[argon2]], [[scrypt]], [[pbkdf2]]
