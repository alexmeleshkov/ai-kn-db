# PostgreSQL

**Category**: Relational Database
**Website**: https://www.postgresql.org/
**Documentation**: https://www.postgresql.org/docs/

---

## Overview

PostgreSQL is an advanced open-source relational database management system (RDBMS) known for its reliability, feature robustness, and SQL compliance. It supports both SQL (relational) and JSON (non-relational) querying.

---

## Key Features

**ACID Compliance**: Full transaction support with atomicity, consistency, isolation, and durability
**Advanced Data Types**: JSON, JSONB, Arrays, HStore, UUID, Geometric types, Full-text search
**Extensibility**: Custom functions, data types, operators, and extensions (PostGIS, pg_trgm, etc.)
**Concurrency**: MVCC (Multi-Version Concurrency Control) for high-performance concurrent access
**Replication**: Streaming replication, logical replication, and hot standby support
**Performance**: Query planner, indexes (B-tree, Hash, GiST, GIN, BRIN), partitioning

---

## Common Use Cases

- **Web Applications**: User data, sessions, transactional data
- **Analytics**: Complex queries, aggregations, window functions
- **GIS Applications**: PostGIS extension for geographic data
- **Time-Series Data**: With TimescaleDB extension
- **Full-Text Search**: Built-in text search capabilities
- **Document Storage**: JSONB for semi-structured data

---

## Prerequisites

**System Requirements**:
- Linux, macOS, Windows, or Docker
- Minimum 1GB RAM (4GB+ recommended for production)
- Disk space for data and indexes

**Installation**:

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS (Homebrew)**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Docker**:
```bash
docker run --name postgres -e POSTGRES_PASSWORD=mysecret -d -p 5432:5432 postgres:15
```

---

## Basic Operations

### Connection
```python
# Python (psycopg2)
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="postgres",
    password="password"
)

# Python (SQLAlchemy)
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost:5432/mydb')
```

```javascript
// Node.js (pg)
const { Client } = require('pg')

const client = new Client({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'postgres',
  password: 'password'
})

await client.connect()
```

### CRUD Operations
```sql
-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert
INSERT INTO users (email) VALUES ('user@example.com') RETURNING *;

-- Query
SELECT * FROM users WHERE email = 'user@example.com';

-- Update
UPDATE users SET email = 'new@example.com' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;
```

---

## Common Patterns

### 1. Connection Pooling
```python
# psycopg2 pool
from psycopg2.pool import SimpleConnectionPool

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host='localhost',
    database='mydb',
    user='postgres',
    password='password'
)

# Get connection from pool
conn = pool.getconn()
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
finally:
    pool.putconn(conn)
```

### 2. Transactions
```python
conn = psycopg2.connect(...)
try:
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    conn.commit()
except Exception as e:
    conn.rollback()
    raise e
finally:
    conn.close()
```

### 3. JSON/JSONB Queries
```sql
-- Store JSON data
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO events (data) VALUES ('{"user": "alice", "action": "login"}');

-- Query JSON fields
SELECT * FROM events WHERE data->>'user' = 'alice';
SELECT * FROM events WHERE data @> '{"action": "login"}';

-- Index JSON field
CREATE INDEX idx_events_user ON events ((data->>'user'));
```

### 4. Full-Text Search
```sql
-- Add tsvector column
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Update search vector
UPDATE articles SET search_vector =
    to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''));

-- Create index
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Search
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql & performance');
```

### 5. UUID Primary Keys
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Use UUID as primary key
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL
);
```

---

## Performance Optimization

### Indexes
```sql
-- B-tree index (default, good for equality and range queries)
CREATE INDEX idx_users_email ON users(email);

-- Partial index (index only specific rows)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Multi-column index
CREATE INDEX idx_users_name ON users(first_name, last_name);

-- GIN index (for JSONB, arrays, full-text search)
CREATE INDEX idx_data_gin ON events USING GIN(data);
```

### EXPLAIN ANALYZE
```sql
-- See query execution plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';
```

### Vacuum and Analyze
```sql
-- Reclaim space and update statistics
VACUUM ANALYZE users;

-- Auto-vacuum (enabled by default)
-- Runs automatically when needed
```

---

## Security

### User Management
```sql
-- Create user
CREATE USER myuser WITH PASSWORD 'securepassword';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
GRANT SELECT, INSERT, UPDATE ON users TO myuser;

-- Revoke privileges
REVOKE DELETE ON users FROM myuser;
```

### SSL Connections
```python
conn = psycopg2.connect(
    host='localhost',
    database='mydb',
    user='postgres',
    password='password',
    sslmode='require'  # require, verify-ca, verify-full
)
```

### Row-Level Security (RLS)
```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY user_isolation ON users
    USING (user_id = current_user_id());
```

---

## Best Practices

**DO**:
- Use connection pooling (don't create new connections per request)
- Use parameterized queries (prevent SQL injection)
- Create indexes on frequently queried columns
- Use EXPLAIN ANALYZE to understand query performance
- Enable auto-vacuum (default in modern PostgreSQL)
- Use JSONB instead of JSON for better performance
- Use transactions for multi-step operations

**DON'T**:
- Don't use string concatenation for SQL (SQL injection risk)
- Don't create too many indexes (slows down writes)
- Don't use SELECT * in production (specify columns)
- Don't forget to close connections
- Don't use SERIAL for distributed systems (use UUID instead)

---

## Backup and Restore

### pg_dump
```bash
# Backup database
pg_dump mydb > backup.sql

# Backup with compression
pg_dump mydb | gzip > backup.sql.gz

# Backup specific table
pg_dump mydb --table=users > users_backup.sql
```

### pg_restore
```bash
# Restore database
psql mydb < backup.sql

# Restore from compressed backup
gunzip -c backup.sql.gz | psql mydb
```

---

## Common Issues

**Connection Refused**:
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Check pg_hba.conf for connection permissions
- Check listen_addresses in postgresql.conf

**Too Many Connections**:
- Increase max_connections in postgresql.conf
- Use connection pooling (PgBouncer, application-level pooling)

**Slow Queries**:
- Run EXPLAIN ANALYZE to see execution plan
- Add indexes on WHERE/JOIN columns
- Consider partitioning for large tables

---

## Alternatives

**MySQL**: Simpler, faster for reads (but less feature-rich)
**SQLite**: Embedded, serverless (but single-writer, no network access)
**Oracle**: Enterprise features (but expensive, proprietary)
**SQL Server**: Windows integration (but Windows-centric, licensing costs)

**Why PostgreSQL**:
- Open-source and free
- Feature-rich (JSON, full-text search, GIS, etc.)
- Strong data integrity (ACID, constraints, foreign keys)
- Excellent performance for complex queries
- Active community and ecosystem

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Code snippets**: See `languages/python/snippets/`, `languages/typescript/snippets/`
**Features**: [[authentication]], [[conversation-crud]], [[schema-introspection]], [[learning-store]]
**Technologies often used with**: [[fastapi]], [[sqlalchemy]], [[docker]]
