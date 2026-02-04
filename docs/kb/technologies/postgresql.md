# PostgreSQL

**Technology**: PostgreSQL 13+
**Category**: Database

---

## Overview

Open-source relational database used for persistent storage of users, conversations, messages, and learned queries with connection pooling and UUID primary keys.

**Key characteristics**:
- ACID transactions
- UUID primary keys
- Foreign key constraints with cascade delete
- Connection pooling with psycopg2
- JSON column support
- Timestamp columns with automatic updates

---

## Usage Files

- `backend/app/models/database.py` (SQLAlchemy models)
- `backend/app/services/app_data.py` (CRUD operations)
- `backend/app/services/auth.py` (User authentication)
- `backend/app/services/database_pg.py` (Schema introspection)
- `backend/app/services/learning_store.py` (Learned queries)

---

## Complete Usage Patterns

### 1. Connection Pooling (app_data.py, auth.py)

**Purpose**: Manage database connections efficiently for concurrent requests

**Pattern**:
```python
from psycopg2.pool import SimpleConnectionPool

# Create pool at startup
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.postgres_host,
    port=settings.postgres_port,
    user=settings.postgres_user,
    password=settings.postgres_password,
    database=settings.postgres_database
)

# Use connection from pool
conn = pool.getconn()
try:
    cursor = conn.cursor()
    # Execute queries
    conn.commit()
finally:
    cursor.close()
    pool.putconn(conn)
```

**All Behaviors**:
- Pool created once at application startup
- getconn() retrieves connection from pool
- putconn() returns connection to pool
- Automatic connection reuse
- Min/max connection configuration
- Thread-safe for concurrent requests

---

### 2. SQLAlchemy Models (database.py)

**Purpose**: ORM models for users, conversations, and messages

**Pattern**:
```python
from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")
```

**All Behaviors**:
- UUID primary keys (uuid.uuid4())
- Foreign keys with CASCADE delete
- Automatic timestamps (created_at, updated_at)
- SQLAlchemy relationships for joins
- Cascade delete (deleting user deletes conversations and messages)

---

### 3. Raw SQL with psycopg2 (app_data.py)

**Purpose**: Direct SQL execution for CRUD operations

**Pattern**:
```python
def create_conversation(self, user_id: str, title: str) -> Optional[dict]:
    conn = self._get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING *",
            (user_id, title)
        )
        row = cursor.fetchone()
        conn.commit()
        if row:
            return {
                "id": str(row[0]),
                "user_id": str(row[1]),
                "title": row[2],
                "created_at": row[3].isoformat(),
                "updated_at": row[4].isoformat()
            }
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to create conversation: {e}")
        return None
    finally:
        cursor.close()
        self._put_connection(conn)
```

**All Behaviors**:
- Parameterized queries (%s placeholders)
- RETURNING clause to get inserted row
- Transaction management (commit/rollback)
- UUID to string conversion for JSON
- Datetime to ISO format conversion
- Connection cleanup in finally block

---

### 4. Schema Introspection (database_pg.py)

**Purpose**: Query database metadata for schema discovery

**Pattern**:
```python
# Get tables
cursor.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
""")
tables = cursor.fetchall()

# Get columns
cursor.execute("""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = %s AND table_schema = 'public'
    ORDER BY ordinal_position
""", (table_name,))
columns = cursor.fetchall()

# Get approximate row count (instant)
cursor.execute("SELECT reltuples::bigint FROM pg_class WHERE relname = %s", (table_name,))
row_count = cursor.fetchone()[0]
```

**All Behaviors**:
- information_schema for metadata
- pg_class.reltuples for row counts (instant, no full scan)
- Schema filtering (public schema only)
- Column metadata includes type, nullable, default

---

### 5. JSON Column Usage

**Pattern**:
```python
# Model definition
metadata = Column(JSON, nullable=True)

# Insert JSON
cursor.execute(
    "INSERT INTO conversation_messages (conversation_id, role, content, metadata) VALUES (%s, %s, %s, %s)",
    (conversation_id, role, content, json.dumps({"key": "value"}))
)

# Query JSON
cursor.execute("SELECT metadata FROM conversation_messages WHERE id = %s", (message_id,))
metadata = json.loads(cursor.fetchone()[0])
```

**All Behaviors**:
- JSON column type for flexible schema
- json.dumps() to serialize
- json.loads() to deserialize
- Nullable JSON columns

---

## Common Patterns

**Pattern 1: Connection Pool Management**
- Usage: All database services use connection pooling
- Example files: app_data.py, auth.py

**Pattern 2: UUID Primary Keys**
- Usage: All tables use UUID primary keys
- Example files: database.py models

**Pattern 3: CASCADE Delete**
- Usage: Foreign keys with CASCADE for automatic cleanup
- Example files: User → Conversations → Messages

---

## Best Practices

From observed usage:
- Use connection pooling (SimpleConnectionPool)
- UUID primary keys for distributed systems
- Parameterized queries (%s) to prevent SQL injection
- Transaction management (commit/rollback)
- Connection cleanup in finally blocks
- CASCADE delete for referential integrity
- Timestamp columns for created_at/updated_at

---

## Used By Features

- **[Conversation CRUD](../features/conversation-crud.md)** - Data storage
- **[JWT Authentication](../features/jwt-authentication.md)** - User storage
- **[Learning Store](../features/learning-store.md)** - Query patterns
- **[Schema Introspection](../features/schema-introspection.md)** - Metadata queries

---

## Used In Projects

- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Primary database

---

## Configuration

```python
# Database connection settings
postgres_host = "localhost"
postgres_port = 5432
postgres_user = "postgres"
postgres_password = "password"
postgres_database = "dbchat"

# Connection pool settings
pool = SimpleConnectionPool(
    minconn=1,    # Minimum connections
    maxconn=10,   # Maximum connections
    host=postgres_host,
    port=postgres_port,
    user=postgres_user,
    password=postgres_password,
    database=postgres_database,
    connect_timeout=30  # Connection timeout seconds
)
```
