# Technology Stack

## Backend

**Language**: Python 3.11+

**Framework**: FastAPI 0.100+
- Async/await support
- Dependency injection
- Pydantic validation

**Database**: PostgreSQL 14+
- psycopg2 connection pooling

**Authentication**:
- PyJWT 2.8+ for token generation/verification
- bcrypt 4.0+ for password hashing

## Dependencies

```
# backend/requirements.txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
psycopg2-binary>=2.9.0
PyJWT>=2.8.0
bcrypt>=4.0.0
python-dotenv>=1.0.0
```
