# Python + FastAPI - Service Layer Pattern

**Language**: Python
**Technology**: FastAPI
**Feature/Pattern**: Service layer with abstract base classes and dependency injection
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
pip install fastapi
```

**Required Knowledge**:
- Object-oriented programming (inheritance, abstract classes)
- FastAPI dependency injection
- Design patterns (Factory, Strategy)
- Type hints and protocols

---

## Overview

This snippet demonstrates the Service Layer pattern in FastAPI applications. The service layer separates business logic from HTTP route handlers, making code more testable, reusable, and maintainable. It uses abstract base classes to define contracts and dependency injection to provide implementations.

Key features:
- Abstract base classes for service contracts
- Multiple concrete implementations (PostgreSQL, DuckDB, Azure SQL)
- Factory pattern for service creation
- FastAPI dependency injection integration
- Clean separation of concerns (routes → services → data access)

---

## Implementation

### Basic Usage

#### Simple Service Class

```python
from fastapi import FastAPI, Depends

class UserService:
    """Service for user-related operations."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id: str) -> dict:
        """Get user by ID."""
        # Business logic here
        cur = self.db.cursor()
        cur.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()

        if row:
            return {"id": row[0], "email": row[1]}
        return None

    def create_user(self, email: str, password_hash: str) -> dict:
        """Create new user."""
        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
            (email, password_hash)
        )
        user_id = cur.fetchone()[0]
        self.db.commit()
        cur.close()

        return {"id": user_id, "email": email}


# Dependency to get service
def get_user_service() -> UserService:
    """Dependency injection for UserService."""
    db_conn = get_database_connection()  # Your DB connection logic
    return UserService(db_conn)


# Use in route
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    """Get user endpoint."""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Advanced Usage

#### Abstract Base Class for Multiple Implementations

```python
from abc import ABC, abstractmethod
from typing import Optional

class BaseDatabaseService(ABC):
    """
    Abstract base class for database services.
    All database implementations must inherit from this class.
    """

    @abstractmethod
    def test_connection(self) -> bool:
        """Test database connectivity."""
        pass

    @abstractmethod
    def get_schema(self, refresh: bool = False):
        """Retrieve database schema information."""
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> dict:
        """Execute a SQL query and return results."""
        pass

    @abstractmethod
    def get_loaded_tables(self) -> list[dict]:
        """Get list of all tables."""
        pass

    @property
    @abstractmethod
    def db_type(self) -> str:
        """Return database type identifier."""
        pass


# Concrete implementation 1: PostgreSQL
class PostgresDatabaseService(BaseDatabaseService):
    """PostgreSQL database service implementation."""

    def __init__(self):
        self._connection = self._create_connection()
        self._schema_cache = None

    def test_connection(self) -> bool:
        try:
            cur = self._connection.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return True
        except Exception:
            return False

    def get_schema(self, refresh: bool = False):
        if refresh or not self._schema_cache:
            self._schema_cache = self._introspect_schema()
        return self._schema_cache

    def execute_query(self, sql: str) -> dict:
        cur = self._connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        return {"rows": rows, "columns": columns}

    def get_loaded_tables(self) -> list[dict]:
        cur = self._connection.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [{"name": row[0]} for row in cur.fetchall()]
        cur.close()
        return tables

    @property
    def db_type(self) -> str:
        return "postgres"

    def _create_connection(self):
        import psycopg2
        return psycopg2.connect(
            host="localhost",
            database="myapp",
            user="postgres",
            password="password"
        )

    def _introspect_schema(self):
        # Schema introspection logic
        pass


# Concrete implementation 2: DuckDB
class DuckDBDatabaseService(BaseDatabaseService):
    """DuckDB database service implementation."""

    def __init__(self):
        import duckdb
        self._connection = duckdb.connect(":memory:")
        self._schema_cache = None

    def test_connection(self) -> bool:
        try:
            self._connection.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_schema(self, refresh: bool = False):
        if refresh or not self._schema_cache:
            self._schema_cache = self._introspect_schema()
        return self._schema_cache

    def execute_query(self, sql: str) -> dict:
        result = self._connection.execute(sql).fetchall()
        columns = [desc[0] for desc in self._connection.description]
        return {"rows": result, "columns": columns}

    def get_loaded_tables(self) -> list[dict]:
        result = self._connection.execute("SHOW TABLES").fetchall()
        return [{"name": row[0]} for row in result]

    @property
    def db_type(self) -> str:
        return "duckdb"

    def _introspect_schema(self):
        # Schema introspection logic
        pass
```

**Key Points**:
- ABC (Abstract Base Class) enforces contract across implementations
- `@abstractmethod` ensures subclasses implement required methods
- Each implementation handles database-specific details
- Common interface allows swapping implementations easily

---

## Complete Example

### Full Service Layer with Factory Pattern

```python
"""
Service layer pattern with factory and dependency injection.
"""

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException


# ========== Abstract Base Class ==========

class BaseDatabaseService(ABC):
    """Abstract base class for database services."""

    @abstractmethod
    def test_connection(self) -> bool:
        """Test database connectivity."""
        pass

    @abstractmethod
    def get_schema(self, refresh: bool = False):
        """Retrieve database schema."""
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> dict:
        """Execute SQL query."""
        pass

    @abstractmethod
    def get_loaded_tables(self) -> list[dict]:
        """Get list of tables."""
        pass

    @property
    @abstractmethod
    def db_type(self) -> str:
        """Database type identifier."""
        pass

    def validate_query(self, sql: str) -> tuple[bool, Optional[str]]:
        """
        Validate SQL query for safety.
        Returns (is_valid, error_message).
        """
        sql_upper = sql.strip().upper()

        # Allow SELECT or WITH (CTE) queries
        if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
            return False, "Only SELECT queries are allowed."

        # Check for dangerous keywords
        dangerous_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE",
            "ALTER", "CREATE", "EXEC", "EXECUTE"
        ]

        for keyword in dangerous_keywords:
            if f" {keyword} " in f" {sql_upper} ":
                return False, f"Query contains forbidden keyword: {keyword}"

        return True, None


# ========== Concrete Implementations ==========

class PostgresDatabaseService(BaseDatabaseService):
    """PostgreSQL implementation."""

    def __init__(self, connection):
        self._conn = connection
        self._schema_cache = None

    def test_connection(self) -> bool:
        try:
            cur = self._conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return True
        except Exception:
            return False

    def get_schema(self, refresh: bool = False):
        if refresh or not self._schema_cache:
            # Introspect schema from PostgreSQL
            self._schema_cache = self._build_schema()
        return self._schema_cache

    def execute_query(self, sql: str) -> dict:
        is_valid, error = self.validate_query(sql)
        if not is_valid:
            return {"error": error}

        try:
            cur = self._conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
            cur.close()
            return {"rows": rows, "columns": columns, "row_count": len(rows)}
        except Exception as e:
            return {"error": str(e)}

    def get_loaded_tables(self) -> list[dict]:
        cur = self._conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [{"name": row[0], "type": "table"} for row in cur.fetchall()]
        cur.close()
        return tables

    @property
    def db_type(self) -> str:
        return "postgres"

    def _build_schema(self):
        # Build schema representation
        from database_models import DatabaseSchema
        return DatabaseSchema(database_name="postgres", tables=[])


class DuckDBDatabaseService(BaseDatabaseService):
    """DuckDB implementation."""

    def __init__(self):
        import duckdb
        self._conn = duckdb.connect(":memory:")
        self._schema_cache = None

    def test_connection(self) -> bool:
        try:
            self._conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_schema(self, refresh: bool = False):
        if refresh or not self._schema_cache:
            self._schema_cache = self._build_schema()
        return self._schema_cache

    def execute_query(self, sql: str) -> dict:
        is_valid, error = self.validate_query(sql)
        if not is_valid:
            return {"error": error}

        try:
            result = self._conn.execute(sql)
            rows = result.fetchall()
            columns = [desc[0] for desc in result.description] if result.description else []
            return {"rows": rows, "columns": columns, "row_count": len(rows)}
        except Exception as e:
            return {"error": str(e)}

    def get_loaded_tables(self) -> list[dict]:
        result = self._conn.execute("SHOW TABLES").fetchall()
        return [{"name": row[0], "type": "table"} for row in result]

    @property
    def db_type(self) -> str:
        return "duckdb"

    def _build_schema(self):
        from database_models import DatabaseSchema
        return DatabaseSchema(database_name="duckdb", tables=[])


# ========== Factory Pattern ==========

class DatabaseServiceFactory:
    """Factory for creating database service instances."""

    @staticmethod
    def create(db_mode: str, **kwargs) -> BaseDatabaseService:
        """
        Create database service based on mode.

        Args:
            db_mode: "postgres", "duckdb", or "azure"
            **kwargs: Additional arguments for service initialization

        Returns:
            Concrete database service instance
        """
        if db_mode == "postgres":
            connection = kwargs.get("connection")
            if not connection:
                raise ValueError("PostgreSQL requires connection parameter")
            return PostgresDatabaseService(connection)

        elif db_mode == "duckdb":
            return DuckDBDatabaseService()

        elif db_mode == "azure":
            from database_azure import AzureSQLDatabaseService
            return AzureSQLDatabaseService()

        else:
            raise ValueError(f"Unknown database mode: {db_mode}")


# ========== FastAPI Integration ==========

# Global service instance
_db_service: Optional[BaseDatabaseService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize services at startup."""
    global _db_service

    # Initialize database service based on configuration
    db_mode = "duckdb"  # or get from environment

    print(f"Initializing database service (mode: {db_mode})...")
    _db_service = DatabaseServiceFactory.create(db_mode)

    if _db_service.test_connection():
        print("Database connection successful")
    else:
        print("Database connection failed")

    yield

    # Cleanup
    print("Shutting down services...")


# Dependency injection
def get_db_service() -> BaseDatabaseService:
    """Get database service instance."""
    if _db_service is None:
        raise RuntimeError("Database service not initialized")
    return _db_service


# Create app
app = FastAPI(lifespan=lifespan)


# ========== Routes Using Service Layer ==========

@app.get("/database/schema")
async def get_schema(
    refresh: bool = False,
    db_service: BaseDatabaseService = Depends(get_db_service)
):
    """Get database schema."""
    schema = db_service.get_schema(refresh=refresh)
    return {
        "database_name": schema.database_name,
        "table_count": len(schema.tables)
    }


@app.post("/database/query")
async def execute_query(
    sql: str,
    db_service: BaseDatabaseService = Depends(get_db_service)
):
    """Execute SQL query."""
    result = db_service.execute_query(sql)

    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        "columns": result["columns"],
        "row_count": result["row_count"],
        "rows": result["rows"][:100]  # Limit to 100 rows
    }


@app.get("/database/tables")
async def get_tables(
    db_service: BaseDatabaseService = Depends(get_db_service)
):
    """Get list of tables."""
    tables = db_service.get_loaded_tables()
    return {"tables": tables}


@app.get("/database/info")
async def get_database_info(
    db_service: BaseDatabaseService = Depends(get_db_service)
):
    """Get database information."""
    return {
        "type": db_service.db_type,
        "connected": db_service.test_connection(),
        "table_count": len(db_service.get_loaded_tables())
    }
```

---

## Configuration

```python
from pydantic_settings import BaseSettings
from enum import Enum

class DatabaseMode(str, Enum):
    """Supported database modes."""
    POSTGRES = "postgres"
    DUCKDB = "duckdb"
    AZURE = "azure"

class Settings(BaseSettings):
    # Database configuration
    db_mode: DatabaseMode = DatabaseMode.DUCKDB

    # PostgreSQL settings (if db_mode=postgres)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_database: str = "myapp"

    class Config:
        env_file = ".env"


# Initialize with configuration
settings = Settings()

if settings.db_mode == DatabaseMode.POSTGRES:
    import psycopg2
    conn = psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_database
    )
    db_service = DatabaseServiceFactory.create("postgres", connection=conn)
else:
    db_service = DatabaseServiceFactory.create(settings.db_mode.value)
```

---

## Error Handling

```python
class ServiceError(Exception):
    """Base exception for service layer errors."""
    pass

class ConnectionError(ServiceError):
    """Database connection error."""
    pass

class QueryError(ServiceError):
    """Query execution error."""
    pass

class ValidationError(ServiceError):
    """Query validation error."""
    pass


# Enhanced base class with error handling
class BaseDatabaseService(ABC):

    def safe_execute_query(self, sql: str) -> dict:
        """Execute query with comprehensive error handling."""
        try:
            # Validate query
            is_valid, error = self.validate_query(sql)
            if not is_valid:
                raise ValidationError(error)

            # Test connection
            if not self.test_connection():
                raise ConnectionError("Database connection lost")

            # Execute query
            result = self.execute_query(sql)

            if result.get("error"):
                raise QueryError(result["error"])

            return result

        except ValidationError as e:
            return {"error": f"Validation error: {str(e)}", "type": "validation"}
        except ConnectionError as e:
            return {"error": f"Connection error: {str(e)}", "type": "connection"}
        except QueryError as e:
            return {"error": f"Query error: {str(e)}", "type": "query"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "type": "unknown"}
```

---

## Testing

```python
import pytest
from unittest.mock import Mock, MagicMock

# Test with mock service
class MockDatabaseService(BaseDatabaseService):
    """Mock database service for testing."""

    def __init__(self):
        self._connected = True
        self._tables = [{"name": "users"}, {"name": "posts"}]

    def test_connection(self) -> bool:
        return self._connected

    def get_schema(self, refresh: bool = False):
        return Mock(tables=[], database_name="mock")

    def execute_query(self, sql: str) -> dict:
        return {
            "rows": [[1, "test@example.com"]],
            "columns": ["id", "email"],
            "row_count": 1
        }

    def get_loaded_tables(self) -> list[dict]:
        return self._tables

    @property
    def db_type(self) -> str:
        return "mock"


def test_service_abstraction():
    """Test service implements interface."""
    service = MockDatabaseService()

    assert service.test_connection() == True
    assert service.db_type == "mock"
    assert len(service.get_loaded_tables()) == 2

def test_query_execution():
    """Test query execution."""
    service = MockDatabaseService()
    result = service.execute_query("SELECT * FROM users")

    assert result["row_count"] == 1
    assert "email" in result["columns"]

def test_dependency_injection(test_client):
    """Test FastAPI dependency injection."""
    # Override dependency with mock
    def override_get_db_service():
        return MockDatabaseService()

    app.dependency_overrides[get_db_service] = override_get_db_service

    response = test_client.get("/database/tables")
    assert response.status_code == 200
    assert len(response.json()["tables"]) == 2

def test_factory_pattern():
    """Test factory creates correct service."""
    service = DatabaseServiceFactory.create("duckdb")
    assert isinstance(service, DuckDBDatabaseService)
    assert service.db_type == "duckdb"
```

---

## Performance Considerations

- **Lazy Initialization**: Don't introspect schema until first use
- **Caching**: Cache schema and expensive operations (TTL: 5-15 minutes)
- **Connection Pooling**: Use connection pools for database services (not shown in example)
- **Service Reuse**: Create service once at startup, reuse across requests
- **Async Support**: Consider async implementations for I/O-bound operations
- **Resource Cleanup**: Properly close connections in service destructors

---

## Security Considerations

- **Input Validation**: Validate all inputs at service layer, not just routes
- **SQL Injection**: Use parameterized queries in service implementations
- **Error Messages**: Don't expose internal details in error messages
- **Access Control**: Implement permission checks in service layer
- **Audit Logging**: Log all service operations with user context
- **Rate Limiting**: Apply rate limits at service layer for expensive operations

---

## Related

**Feature**: [[architecture-patterns]], [[dependency-injection]]
**Technology**: [[fastapi]], [[design-patterns]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[django-service-layer.md]], [[flask-blueprints.md]]
