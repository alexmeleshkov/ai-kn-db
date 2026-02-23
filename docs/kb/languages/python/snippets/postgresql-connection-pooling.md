# Python + psycopg2 - PostgreSQL Connection Pooling

**Language**: Python
**Technology**: postgresql
**Feature/Pattern**: Connection pooling with ThreadedConnectionPool
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
pip install psycopg2-binary
# Or for production:
pip install psycopg2
```

**Required Knowledge**:
- PostgreSQL connection strings
- Context managers (with statement)
- Thread safety in Python
- Connection lifecycle management

---

## Overview

This snippet demonstrates PostgreSQL connection pooling using psycopg2's ThreadedConnectionPool. Connection pooling reuses database connections instead of creating new ones for each request, significantly improving performance in multi-threaded applications like web servers.

Key features:
- Thread-safe connection pool (min/max connections)
- getconn/putconn pattern for acquiring and releasing connections
- Context manager for automatic connection cleanup
- Connection lifecycle management (startup/shutdown)
- Error handling and connection validation

---

## Implementation

### Basic Usage

#### Create Connection Pool

```python
from psycopg2 import pool

# Create thread-safe connection pool
app_db_pool = pool.ThreadedConnectionPool(
    minconn=1,          # Minimum idle connections in pool
    maxconn=5,          # Maximum connections allowed
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="myapp"
)

# Get connection from pool
conn = app_db_pool.getconn()

try:
    # Use connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM users LIMIT 10")
    rows = cur.fetchall()
    print(f"Found {len(rows)} users")
    cur.close()
finally:
    # IMPORTANT: Always return connection to pool
    app_db_pool.putconn(conn)

# Cleanup on shutdown
app_db_pool.closeall()
```

**Explanation**:
- Line 4-11: Initialize pool with connection parameters
- Line 14: Acquire connection from pool (blocks if pool is exhausted)
- Line 26: Release connection back to pool (don't close the connection!)
- Line 29: Close all connections in pool on application shutdown

### Advanced Usage

#### Context Manager for Automatic Cleanup

```python
from contextlib import contextmanager
from psycopg2 import pool
from typing import Generator

class DatabasePool:
    """Wrapper for psycopg2 connection pool with context manager."""

    def __init__(self, minconn: int = 1, maxconn: int = 10, **kwargs):
        """Initialize connection pool."""
        self._pool = pool.ThreadedConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            **kwargs
        )

    @contextmanager
    def get_connection(self) -> Generator:
        """
        Context manager for getting connection from pool.

        Usage:
            with db_pool.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT ...")
        """
        conn = self._pool.getconn()
        try:
            yield conn
        except Exception as e:
            # Rollback on error
            conn.rollback()
            raise
        finally:
            # Always return connection to pool
            self._pool.putconn(conn)

    def close(self):
        """Close all connections in pool."""
        self._pool.closeall()


# Usage
db_pool = DatabasePool(
    minconn=2,
    maxconn=10,
    host="localhost",
    port=5432,
    user="postgres",
    password="password",
    database="myapp"
)

# Automatically handles connection cleanup
with db_pool.get_connection() as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    print(f"Total users: {count}")
    cur.close()
    # Connection automatically returned to pool

# Shutdown
db_pool.close()
```

**Key Points**:
- Context manager ensures connection is returned even if exception occurs
- Automatic rollback on errors
- Cleaner code without try/finally blocks

---

## Complete Example

### FastAPI Application with Connection Pool

```python
"""
FastAPI application with PostgreSQL connection pooling.
Demonstrates proper lifecycle management in async web framework.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from psycopg2 import pool
import logging

logger = logging.getLogger(__name__)

# Global connection pool (initialized at startup)
_db_pool: pool.ThreadedConnectionPool | None = None


def get_db_pool() -> pool.ThreadedConnectionPool:
    """Get the global database pool."""
    if _db_pool is None:
        raise RuntimeError("Database pool not initialized")
    return _db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initialize connection pool at startup, close on shutdown.
    """
    global _db_pool

    logger.info("Initializing database connection pool...")

    try:
        _db_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=5,
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="myapp"
        )
        logger.info("Database connection pool initialized")

        # Test connection
        conn = _db_pool.getconn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            logger.info("Database connection test successful")
        finally:
            _db_pool.putconn(conn)

    except Exception as e:
        logger.error(f"Failed to initialize database pool: {e}")
        _db_pool = None

    yield

    # Shutdown - close all connections
    if _db_pool:
        logger.info("Closing database connection pool...")
        _db_pool.closeall()
        logger.info("Database connection pool closed")


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


@app.get("/users")
async def get_users(db_pool: pool.ThreadedConnectionPool = Depends(get_db_pool)):
    """Get all users from database."""
    conn = db_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, email FROM users")
        rows = cur.fetchall()
        cur.close()

        users = [{"id": row[0], "email": row[1]} for row in rows]
        return {"users": users}

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        # Always return connection to pool
        db_pool.putconn(conn)


@app.post("/users")
async def create_user(
    email: str,
    password_hash: str,
    db_pool: pool.ThreadedConnectionPool = Depends(get_db_pool)
):
    """Create a new user."""
    conn = db_pool.getconn()
    try:
        cur = conn.cursor()

        # Insert user
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            (email, password_hash)
        )
        user_id = cur.fetchone()[0]

        # Commit transaction
        conn.commit()
        cur.close()

        return {"id": user_id, "email": email}

    except Exception as e:
        # Rollback on error
        conn.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user")
    finally:
        db_pool.putconn(conn)


@app.get("/health")
async def health_check(db_pool: pool.ThreadedConnectionPool = Depends(get_db_pool)):
    """Health check endpoint - test database connection."""
    conn = db_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
    finally:
        db_pool.putconn(conn)
```

### Service Class with Connection Pool

```python
"""
Service class pattern for database operations.
Encapsulates connection pool usage.
"""

from psycopg2 import pool
from typing import Optional

class UserService:
    """User service with connection pooling."""

    def __init__(self, db_pool: pool.ThreadedConnectionPool):
        """Initialize service with database pool."""
        self._db_pool = db_pool

    def _get_connection(self):
        """Get connection from pool."""
        return self._db_pool.getconn()

    def _put_connection(self, conn):
        """Return connection to pool."""
        self._db_pool.putconn(conn)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email address."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, email, created_at FROM users WHERE email = %s",
                (email,)
            )
            row = cur.fetchone()
            cur.close()

            if row:
                return {
                    "id": str(row[0]),
                    "email": row[1],
                    "created_at": row[2].isoformat()
                }
            return None

        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            self._put_connection(conn)

    def create_user(self, email: str, password_hash: str) -> Optional[dict]:
        """Create a new user."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()

            # Check if email exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return None  # Email already exists

            # Insert user
            cur.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email, created_at
                """,
                (email, password_hash)
            )
            row = cur.fetchone()
            conn.commit()
            cur.close()

            return {
                "id": str(row[0]),
                "email": row[1],
                "created_at": row[2].isoformat()
            }

        except Exception as e:
            conn.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            self._put_connection(conn)

    def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE users SET last_login_at = NOW() WHERE id = %s",
                (user_id,)
            )
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating last login: {e}")
            return False
        finally:
            self._put_connection(conn)


# Usage
db_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    host="localhost",
    database="myapp"
)

user_service = UserService(db_pool)

# Get user
user = user_service.get_user_by_email("test@example.com")
if user:
    print(f"Found user: {user['id']}")

# Create user
new_user = user_service.create_user("new@example.com", "hashed_password")
if new_user:
    print(f"Created user: {new_user['id']}")
```

---

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL connection
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_database: str = "myapp"

    # Connection pool settings
    db_pool_min: int = 1
    db_pool_max: int = 10

    # Connection timeout
    db_connect_timeout: int = 10  # seconds

    # SSL mode
    postgres_sslmode: str = "prefer"  # disable, allow, prefer, require

    class Config:
        env_file = ".env"


# Initialize pool from settings
settings = Settings()

db_pool = pool.ThreadedConnectionPool(
    minconn=settings.db_pool_min,
    maxconn=settings.db_pool_max,
    host=settings.postgres_host,
    port=settings.postgres_port,
    user=settings.postgres_user,
    password=settings.postgres_password,
    database=settings.postgres_database,
    sslmode=settings.postgres_sslmode,
    connect_timeout=settings.db_connect_timeout
)
```

**Environment Variables** (.env):
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=myapp
DB_POOL_MIN=1
DB_POOL_MAX=10
DB_CONNECT_TIMEOUT=10
POSTGRES_SSLMODE=prefer
```

---

## Error Handling

```python
from psycopg2 import pool, OperationalError, DatabaseError
import logging
import time

logger = logging.getLogger(__name__)

def create_pool_with_retry(max_retries: int = 3, **kwargs) -> pool.ThreadedConnectionPool:
    """Create connection pool with retry logic."""
    for attempt in range(max_retries):
        try:
            db_pool = pool.ThreadedConnectionPool(**kwargs)
            logger.info("Database pool created successfully")
            return db_pool
        except OperationalError as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

def safe_query_execution(db_pool: pool.ThreadedConnectionPool, query: str, params: tuple = ()):
    """Execute query with comprehensive error handling."""
    conn = None
    try:
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result

    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        if conn:
            conn.rollback()
        # Connection may be broken - don't return it to pool
        raise

    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if conn:
            try:
                db_pool.putconn(conn)
            except Exception as e:
                logger.error(f"Error returning connection to pool: {e}")

def test_connection(db_pool: pool.ThreadedConnectionPool) -> bool:
    """Test if database connection is working."""
    try:
        conn = db_pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        db_pool.putconn(conn)
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
```

**Common Errors**:
1. **PoolError**: Pool exhausted (all connections in use) - increase maxconn or reduce connection hold time
2. **OperationalError**: Connection failed - check host/port/credentials, network connectivity
3. **DatabaseError**: SQL error - validate query syntax and parameters
4. **AttributeError** ('NoneType' has no 'putconn'): Pool not initialized - ensure pool created before use
5. **Connection not returned**: Always use try/finally or context manager to return connections

---

## Testing

```python
import pytest
from psycopg2 import pool

@pytest.fixture
def db_pool():
    """Create test database pool."""
    test_pool = pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=5,
        host="localhost",
        database="test_db",
        user="test_user",
        password="test_pass"
    )
    yield test_pool
    test_pool.closeall()

def test_pool_basic_operations(db_pool):
    """Test basic pool operations."""
    # Get connection
    conn = db_pool.getconn()
    assert conn is not None

    # Use connection
    cur = conn.cursor()
    cur.execute("SELECT 1")
    result = cur.fetchone()
    assert result[0] == 1
    cur.close()

    # Return connection
    db_pool.putconn(conn)

def test_pool_multiple_connections(db_pool):
    """Test pool handles multiple connections."""
    connections = []

    # Acquire multiple connections
    for _ in range(3):
        conn = db_pool.getconn()
        connections.append(conn)

    # All should be different connections
    assert len(set(id(c) for c in connections)) == 3

    # Return all connections
    for conn in connections:
        db_pool.putconn(conn)

def test_pool_context_manager(db_pool):
    """Test pool with context manager."""
    class PoolWrapper:
        def __init__(self, pool):
            self._pool = pool

        @contextmanager
        def get_connection(self):
            conn = self._pool.getconn()
            try:
                yield conn
            finally:
                self._pool.putconn(conn)

    wrapper = PoolWrapper(db_pool)

    with wrapper.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        assert result[0] == 1
        cur.close()

def test_pool_error_handling(db_pool):
    """Test pool handles errors correctly."""
    conn = db_pool.getconn()

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM nonexistent_table")
    except Exception:
        conn.rollback()
    finally:
        db_pool.putconn(conn)

    # Pool should still work after error
    conn2 = db_pool.getconn()
    assert conn2 is not None
    db_pool.putconn(conn2)
```

---

## Performance Considerations

- **Pool Size**: Set minconn to expected concurrent connections, maxconn to peak load
- **Connection Reuse**: Reusing connections is 10-100x faster than creating new ones
- **Thread Safety**: ThreadedConnectionPool is thread-safe, SimpleConnectionPool is not
- **Hold Time**: Minimize time connections are held - acquire late, release early
- **Transaction Scope**: Keep transactions short to avoid blocking other requests
- **Prepared Statements**: Use parameterized queries (%s) - they're cached and faster

**Recommended Pool Sizes**:
- Web server (FastAPI/Flask): minconn=1-2, maxconn=10-20
- Background workers: minconn=1, maxconn=5
- High-traffic API: minconn=5, maxconn=50

---

## Security Considerations

- **Credentials**: Store database credentials in environment variables, never in code
- **SSL/TLS**: Use `sslmode='require'` for production to encrypt connections
- **Parameterized Queries**: Always use %s placeholders to prevent SQL injection
- **Least Privilege**: Use database user with minimal required permissions
- **Connection Timeout**: Set connect_timeout to prevent hanging on connection failures
- **Password Rotation**: Restart application after password changes to refresh pool
- **Connection Validation**: Periodically test connections to detect stale/broken connections

---

## Related

**Feature**: [[database]], [[connection-management]]
**Technology**: [[postgresql]], [[psycopg2]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[sqlalchemy-connection-pool.md]], [[asyncpg-pool.md]]
