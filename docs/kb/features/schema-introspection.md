# Schema Introspection

**Feature ID**: database.schema-introspection
**Capability**: schema-introspection
**Technologies**: postgresql, fastapi

---

## Overview

Multi-database schema discovery and introspection supporting PostgreSQL, DuckDB, and Azure SQL. Dynamically extracts table structures, column types, relationships, and sample data for AI context generation.

**Key characteristics**:
- Abstract base class pattern for database service implementations
- Schema caching with 5-minute TTL
- Approximate row counts (instant, no full table scan)
- Sample data extraction (top 5 rows per table)
- Dataclass representation for LLM context
- Support for multiple database dialects (PostgreSQL, T-SQL, DuckDB SQL)

---

## File Structure

```
backend/app/
  services/
    database_base.py       # Abstract schema introspection interface
    database_pg.py         # PostgreSQL implementation
    database_azure.py      # Azure SQL implementation
  api/
    routes.py              # Schema endpoint (GET /schema)
```

---

## Implementation Patterns

### 1. PostgreSQL Schema Introspection (database_pg.py)

**Purpose**: PostgreSQL-specific schema introspection using information_schema and pg_class

**Interface**:
```python
class PostgresDatabaseService(DatabaseService):
    def get_schema(self) -> DatabaseSchema
    def _get_approximate_row_count(self, table_name: str) -> int
```

**Complete Flow - get_schema()**:
1. Query information_schema.tables for all tables in 'public' schema
2. For each table:
   a. Query information_schema.columns for column metadata (name, type, nullable, default)
   b. Call _get_approximate_row_count(table_name) using pg_class.reltuples
   c. Get sample data: SELECT * FROM table LIMIT 5
   d. Build TableSchema object with columns and samples
3. Return DatabaseSchema with list of tables

**SQL Queries**:
```sql
-- Get tables
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'

-- Get columns
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = %s AND table_schema = 'public'
ORDER BY ordinal_position

-- Get approximate row count (instant, no full scan)
SELECT reltuples::bigint FROM pg_class WHERE relname = %s

-- Get sample data
SELECT * FROM {table_name} LIMIT 5
```

**All Behaviors**:
- Approximate row counts from pg_class.reltuples (instant, updated by ANALYZE)
- Sample data limited to 5 rows per table
- Column metadata includes: name, data_type, nullable, default value
- Schema filtered to 'public' schema only
- Returns dataclass objects for type safety

---

### 2. Azure SQL Schema Introspection (database_azure.py)

**Purpose**: Azure SQL-specific schema introspection using INFORMATION_SCHEMA

**Interface**:
```python
class AzureSQLDatabaseService(DatabaseService):
    def get_schema(self) -> DatabaseSchema
```

**SQL Queries**:
```sql
-- Get tables
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'

-- Get columns
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = @p1 AND TABLE_SCHEMA = 'dbo'
ORDER BY ORDINAL_POSITION

-- Get row count (exact, requires table scan)
SELECT COUNT(*) FROM {table_name}

-- Get sample data (T-SQL syntax)
SELECT TOP 5 * FROM {table_name}
```

**All Behaviors**:
- T-SQL syntax (TOP N instead of LIMIT)
- Exact row counts (COUNT(*) - slow for large tables)
- Schema filtered to 'dbo' schema
- Uses pyodbc parameter binding (@p1, @p2)

---

### 3. Abstract Base Class (database_base.py)

**Purpose**: Defines interface for all database service implementations

**Interface**:
```python
class DatabaseService(ABC):
    @abstractmethod
    def get_schema(self) -> DatabaseSchema

    @abstractmethod
    def execute_query(self, query: str) -> QueryResult

    @property
    @abstractmethod
    def db_type(self) -> str

    @property
    @abstractmethod
    def database_id(self) -> str
```

**Dataclass Definitions**:
```python
@dataclass
class ColumnSchema:
    name: str
    data_type: str
    nullable: bool
    default: Optional[str] = None

@dataclass
class TableSchema:
    name: str
    columns: list[ColumnSchema]
    row_count: int
    sample_data: Optional[list[dict]] = None

@dataclass
class DatabaseSchema:
    tables: list[TableSchema]
```

---

### 4. Schema API Endpoint (routes.py)

**Purpose**: FastAPI endpoint returning schema as JSON

**Interface**:
```python
@app.get("/schema")
async def get_schema(database: DatabaseService = Depends(get_database_service)) -> dict
```

**Complete Flow**:
1. Get database service from dependency injection
2. Call database.get_schema()
3. Convert DatabaseSchema to dict
4. Return as JSON

**All Behaviors**:
- Public endpoint (no authentication required)
- Returns full schema including sample data
- Used by frontend to display database structure
- Cached in memory (schema object cached for 5 minutes)

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Schema context for NL-to-SQL

---

## Related Technologies

- **[PostgreSQL](../technologies/postgresql.md)** - Database introspection
- **[FastAPI](../technologies/fastapi.md)** - Schema API endpoint

---

## Variants

### Variant 1: information_schema (Current)
- **When to use**: Standard SQL databases (PostgreSQL, MySQL, SQL Server)
- **Trade-offs**:
  - ✅ Pros: Standard SQL, portable, comprehensive metadata
  - ❌ Cons: Slower than system catalogs, limited to SQL databases

### Variant 2: Database-specific catalogs
- **When to use**: Performance-critical introspection, database-specific features
- **Trade-offs**:
  - ✅ Pros: Faster, more detailed metadata, database-optimized
  - ❌ Cons: Not portable, requires database-specific code
