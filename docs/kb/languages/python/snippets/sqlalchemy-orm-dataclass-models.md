# Python + SQLAlchemy - ORM Dataclass Models

**Language**: Python
**Technology**: SQLAlchemy
**Feature/Pattern**: Dataclass-based ORM models for database schema representation
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
pip install sqlalchemy
```

**Required Knowledge**:
- Python dataclasses
- Database schema concepts (tables, columns, keys, relationships)
- Type hints
- Object-oriented programming

---

## Overview

This snippet demonstrates using Python dataclasses to represent database schema metadata for LLM context. Unlike traditional SQLAlchemy ORM models (which map to actual database tables), these lightweight dataclass models represent schema information extracted from databases for documentation or AI prompt context.

Key features:
- Dataclass-based models with type hints
- Hierarchical structure (Database → Table → Column)
- Schema string generation for LLM prompts
- Foreign key and constraint representation
- Compact and verbose string formats

---

## Implementation

### Basic Usage

#### Column Information Model

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ColumnInfo:
    """Represents a database column."""

    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key_reference: Optional[str] = None
    description: Optional[str] = None

    def to_schema_string(self) -> str:
        """Convert to schema representation string."""
        parts = [f"{self.name} {self.data_type}"]

        if self.is_primary_key:
            parts.append("PRIMARY KEY")
        if not self.is_nullable:
            parts.append("NOT NULL")
        if self.is_foreign_key and self.foreign_key_reference:
            parts.append(f"REFERENCES {self.foreign_key_reference}")

        return " ".join(parts)


# Usage
column = ColumnInfo(
    name="user_id",
    data_type="UUID",
    is_nullable=False,
    is_foreign_key=True,
    foreign_key_reference="users(id)"
)

print(column.to_schema_string())
# Output: "user_id UUID NOT NULL REFERENCES users(id)"
```

**Explanation**:
- Line 6-13: Dataclass fields with type hints and defaults
- Line 15-26: Generate SQL-like schema string for documentation
- Lines 18-25: Build string with constraints (PRIMARY KEY, NOT NULL, REFERENCES)

### Advanced Usage

#### Table Information Model

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TableInfo:
    """Represents a database table with its columns."""

    name: str
    schema_name: str = "main"
    columns: list[ColumnInfo] = field(default_factory=list)
    description: Optional[str] = None
    row_count: Optional[int] = None

    @property
    def full_name(self) -> str:
        """Get table name (without schema prefix for DuckDB)."""
        return self.name

    def to_schema_string(self) -> str:
        """Convert to CREATE TABLE-like schema string."""
        columns_str = ",\n    ".join(col.to_schema_string() for col in self.columns)
        return f"CREATE TABLE {self.name} (\n    {columns_str}\n)"

    def to_compact_string(self) -> str:
        """Convert to compact schema representation."""
        columns = ", ".join(f"{c.name} ({c.data_type})" for c in self.columns)
        return f"{self.name}: {columns}"


# Usage
table = TableInfo(
    name="users",
    columns=[
        ColumnInfo(name="id", data_type="UUID", is_nullable=False, is_primary_key=True),
        ColumnInfo(name="email", data_type="VARCHAR(255)", is_nullable=False),
        ColumnInfo(name="created_at", data_type="TIMESTAMP", is_nullable=False)
    ],
    row_count=1250
)

print(table.to_schema_string())
# Output:
# CREATE TABLE users (
#     id UUID NOT NULL PRIMARY KEY,
#     email VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP NOT NULL
# )

print(table.to_compact_string())
# Output: "users: id (UUID), email (VARCHAR(255)), created_at (TIMESTAMP)"
```

**Key Points**:
- `field(default_factory=list)`: Safely initialize mutable default (list)
- Multiple string formats: verbose (CREATE TABLE) and compact (single line)
- Property decorator for computed attributes

---

## Complete Example

### Full Database Schema Model

```python
"""
Database metadata models.
Represents database schema structure for LLM context.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColumnInfo:
    """Represents a database column."""

    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key_reference: Optional[str] = None
    description: Optional[str] = None

    def to_schema_string(self) -> str:
        """Convert to schema representation string."""
        parts = [f"{self.name} {self.data_type}"]

        if self.is_primary_key:
            parts.append("PRIMARY KEY")
        if not self.is_nullable:
            parts.append("NOT NULL")
        if self.is_foreign_key and self.foreign_key_reference:
            parts.append(f"REFERENCES {self.foreign_key_reference}")

        return " ".join(parts)


@dataclass
class TableInfo:
    """Represents a database table with its columns."""

    name: str
    schema_name: str = "main"
    columns: list[ColumnInfo] = field(default_factory=list)
    description: Optional[str] = None
    row_count: Optional[int] = None

    @property
    def full_name(self) -> str:
        """Get table name (without schema prefix for DuckDB)."""
        return self.name

    def to_schema_string(self) -> str:
        """Convert to CREATE TABLE-like schema string."""
        columns_str = ",\n    ".join(col.to_schema_string() for col in self.columns)
        return f"CREATE TABLE {self.name} (\n    {columns_str}\n)"

    def to_compact_string(self) -> str:
        """Convert to compact schema representation."""
        columns = ", ".join(f"{c.name} ({c.data_type})" for c in self.columns)
        return f"{self.name}: {columns}"


@dataclass
class DatabaseSchema:
    """Represents the complete database schema."""

    tables: list[TableInfo] = field(default_factory=list)
    database_name: Optional[str] = None

    def to_schema_string(self) -> str:
        """Convert entire schema to string for LLM context."""
        parts = []

        if self.database_name:
            parts.append(f"-- Database: {self.database_name}")
            parts.append("")

        for table in self.tables:
            parts.append(table.to_schema_string())
            if table.description:
                parts.append(f"-- Description: {table.description}")
            if table.row_count is not None:
                parts.append(f"-- Approximate row count: {table.row_count}")
            parts.append("")

        return "\n".join(parts)

    def to_compact_string(self) -> str:
        """Convert to compact representation for shorter prompts."""
        return "\n".join(table.to_compact_string() for table in self.tables)

    def get_table(self, name: str) -> Optional[TableInfo]:
        """Get table by name."""
        for table in self.tables:
            if table.name.lower() == name.lower():
                return table
            if table.full_name.lower() == name.lower():
                return table
        return None


# Example: Build schema from database introspection
def extract_schema_from_postgres(conn) -> DatabaseSchema:
    """Extract schema information from PostgreSQL database."""
    schema = DatabaseSchema(database_name="myapp")

    # Get all tables
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    for (table_name,) in cur.fetchall():
        table = TableInfo(name=table_name)

        # Get columns for this table
        cur2 = conn.cursor()
        cur2.execute("""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = %s AND table_schema = 'public'
            ORDER BY ordinal_position
        """, (table_name,))

        for col_name, data_type, is_nullable, col_default in cur2.fetchall():
            column = ColumnInfo(
                name=col_name,
                data_type=data_type.upper(),
                is_nullable=(is_nullable == 'YES'),
                is_primary_key=('nextval' in str(col_default) if col_default else False)
            )
            table.columns.append(column)

        cur2.close()

        # Get row count (approximate)
        cur3 = conn.cursor()
        cur3.execute(f"SELECT COUNT(*) FROM {table_name}")
        table.row_count = cur3.fetchone()[0]
        cur3.close()

        schema.tables.append(table)

    cur.close()
    return schema


# Usage
if __name__ == "__main__":
    # Create schema manually
    schema = DatabaseSchema(database_name="blog")

    # Add users table
    users_table = TableInfo(
        name="users",
        description="User accounts",
        row_count=1250,
        columns=[
            ColumnInfo(
                name="id",
                data_type="UUID",
                is_nullable=False,
                is_primary_key=True
            ),
            ColumnInfo(
                name="email",
                data_type="VARCHAR(255)",
                is_nullable=False
            ),
            ColumnInfo(
                name="created_at",
                data_type="TIMESTAMP",
                is_nullable=False
            )
        ]
    )
    schema.tables.append(users_table)

    # Add posts table
    posts_table = TableInfo(
        name="posts",
        description="Blog posts",
        row_count=4320,
        columns=[
            ColumnInfo(
                name="id",
                data_type="UUID",
                is_nullable=False,
                is_primary_key=True
            ),
            ColumnInfo(
                name="user_id",
                data_type="UUID",
                is_nullable=False,
                is_foreign_key=True,
                foreign_key_reference="users(id)"
            ),
            ColumnInfo(
                name="title",
                data_type="VARCHAR(500)",
                is_nullable=False
            ),
            ColumnInfo(
                name="content",
                data_type="TEXT",
                is_nullable=True
            ),
            ColumnInfo(
                name="published_at",
                data_type="TIMESTAMP",
                is_nullable=True
            )
        ]
    )
    schema.tables.append(posts_table)

    # Generate schema string for LLM prompt
    print("=== Verbose Format ===")
    print(schema.to_schema_string())

    print("\n=== Compact Format ===")
    print(schema.to_compact_string())

    # Query specific table
    users = schema.get_table("users")
    if users:
        print(f"\n=== Users Table ===")
        print(f"Columns: {len(users.columns)}")
        print(f"Rows: {users.row_count}")
```

**Output**:
```
=== Verbose Format ===
-- Database: blog

CREATE TABLE users (
    id UUID NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
)
-- Description: User accounts
-- Approximate row count: 1250

CREATE TABLE posts (
    id UUID NOT NULL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    content TEXT,
    published_at TIMESTAMP
)
-- Description: Blog posts
-- Approximate row count: 4320

=== Compact Format ===
users: id (UUID), email (VARCHAR(255)), created_at (TIMESTAMP)
posts: id (UUID), user_id (UUID), title (VARCHAR(500)), content (TEXT), published_at (TIMESTAMP)
```

---

## Configuration

```python
# Schema extraction configuration
class SchemaConfig:
    """Configuration for schema extraction."""

    # Include/exclude patterns
    include_tables: list[str] = ["*"]  # Default: all tables
    exclude_tables: list[str] = ["migrations", "alembic_version"]

    # Include system information
    include_row_counts: bool = True
    include_descriptions: bool = True
    include_indexes: bool = False

    # String format preferences
    default_format: str = "verbose"  # "verbose" or "compact"
    max_tables_compact: int = 50  # Switch to compact if more tables


# Apply configuration
def extract_schema(conn, config: SchemaConfig) -> DatabaseSchema:
    """Extract schema with configuration."""
    schema = DatabaseSchema()

    # Apply include/exclude filters
    tables = get_all_tables(conn)
    filtered_tables = filter_tables(tables, config)

    for table_name in filtered_tables:
        table = extract_table_info(conn, table_name, config)
        schema.tables.append(table)

    return schema
```

---

## Error Handling

```python
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def safe_extract_schema(conn) -> Optional[DatabaseSchema]:
    """Extract schema with error handling."""
    try:
        schema = DatabaseSchema()

        # Get tables
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        cur.close()

        for (table_name,) in tables:
            try:
                table = extract_table_info(conn, table_name)
                schema.tables.append(table)
            except Exception as e:
                logger.warning(f"Failed to extract table {table_name}: {e}")
                # Continue with other tables
                continue

        if not schema.tables:
            logger.error("No tables extracted")
            return None

        return schema

    except Exception as e:
        logger.error(f"Schema extraction failed: {e}")
        return None

def validate_schema(schema: DatabaseSchema) -> tuple[bool, list[str]]:
    """Validate schema completeness."""
    errors = []

    if not schema.tables:
        errors.append("Schema has no tables")

    for table in schema.tables:
        if not table.columns:
            errors.append(f"Table {table.name} has no columns")

        # Check for primary key
        has_pk = any(col.is_primary_key for col in table.columns)
        if not has_pk:
            errors.append(f"Table {table.name} has no primary key")

    return (len(errors) == 0, errors)
```

**Common Errors**:
1. **Missing columns**: Table introspection failed - check permissions
2. **Type mismatch**: Data types not properly mapped - add type conversion
3. **Empty schema**: No tables found - verify database connection and permissions
4. **Circular references**: Foreign keys create loops - handle with topological sort
5. **Memory issues**: Too many tables/columns - use compact format or pagination

---

## Testing

```python
import pytest

def test_column_info_basic():
    """Test basic column creation."""
    col = ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True)
    assert col.name == "id"
    assert col.data_type == "INTEGER"
    assert col.is_primary_key == True

def test_column_to_schema_string():
    """Test column schema string generation."""
    col = ColumnInfo(
        name="user_id",
        data_type="UUID",
        is_nullable=False,
        is_foreign_key=True,
        foreign_key_reference="users(id)"
    )
    schema_str = col.to_schema_string()
    assert "user_id" in schema_str
    assert "UUID" in schema_str
    assert "NOT NULL" in schema_str
    assert "REFERENCES users(id)" in schema_str

def test_table_info_basic():
    """Test table creation with columns."""
    table = TableInfo(
        name="users",
        columns=[
            ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True),
            ColumnInfo(name="email", data_type="VARCHAR(255)")
        ]
    )
    assert table.name == "users"
    assert len(table.columns) == 2

def test_table_to_schema_string():
    """Test table schema string generation."""
    table = TableInfo(
        name="users",
        columns=[
            ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True)
        ]
    )
    schema_str = table.to_schema_string()
    assert "CREATE TABLE users" in schema_str
    assert "id INTEGER" in schema_str
    assert "PRIMARY KEY" in schema_str

def test_database_schema():
    """Test full database schema."""
    schema = DatabaseSchema(database_name="test_db")

    table1 = TableInfo(name="users", columns=[
        ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True)
    ])
    table2 = TableInfo(name="posts", columns=[
        ColumnInfo(name="id", data_type="INTEGER", is_primary_key=True)
    ])

    schema.tables.append(table1)
    schema.tables.append(table2)

    assert len(schema.tables) == 2
    assert schema.get_table("users") == table1
    assert schema.get_table("posts") == table2

def test_schema_to_string():
    """Test schema string generation."""
    schema = DatabaseSchema(database_name="test_db")
    table = TableInfo(name="users", columns=[
        ColumnInfo(name="id", data_type="INTEGER")
    ])
    schema.tables.append(table)

    schema_str = schema.to_schema_string()
    assert "-- Database: test_db" in schema_str
    assert "CREATE TABLE users" in schema_str

    compact_str = schema.to_compact_string()
    assert "users:" in compact_str
    assert "id (INTEGER)" in compact_str
```

---

## Performance Considerations

- **Lazy Loading**: Extract schema on-demand, not at startup
- **Caching**: Cache schema after first extraction (TTL: 5-15 minutes)
- **Compact Format**: Use compact format for prompts with many tables (>20)
- **Selective Extraction**: Only extract tables relevant to user query
- **Row Count Approximation**: Use statistics tables instead of COUNT(*) for large tables
- **Parallel Extraction**: Extract multiple tables in parallel for large databases

---

## Security Considerations

- **SQL Injection**: Use parameterized queries for table/column name lookups
- **Information Disclosure**: Don't expose internal tables (migrations, system tables)
- **Permission Checks**: Verify user has SELECT permission before adding table to schema
- **Sensitive Columns**: Optionally exclude sensitive columns (passwords, tokens) from schema
- **Schema Access Control**: Limit which users can view schema information

---

## Related

**Feature**: [[database-introspection]], [[schema-metadata]]
**Technology**: [[sqlalchemy]], [[dataclasses]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[pydantic-models.md]], [[sqlalchemy-core-reflection.md]]
