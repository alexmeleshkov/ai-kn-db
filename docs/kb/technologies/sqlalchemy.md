# SQLAlchemy

**Category**: ORM (Object-Relational Mapper)
**Website**: https://www.sqlalchemy.org/
**Documentation**: https://docs.sqlalchemy.org/

---

## Overview

SQLAlchemy is a Python SQL toolkit and Object-Relational Mapper that provides a full suite of enterprise-level persistence patterns. It offers both high-level ORM and low-level SQL expression language.

---

## Key Features

**Declarative ORM**: Map Python classes to database tables
**Query API**: Pythonic query building with type safety
**Relationships**: Foreign keys, one-to-many, many-to-many
**Database Agnostic**: Works with PostgreSQL, MySQL, SQLite, Oracle, etc.
**Connection Pooling**: Built-in connection management
**Migrations**: Integration with Alembic for schema changes

---

## Common Use Cases

- **Web Applications**: User, post, comment models
- **API Backends**: Database-backed REST/GraphQL APIs
- **Data Analysis**: Structured data storage and retrieval
- **Admin Panels**: CRUD operations on database entities
- **E-commerce**: Products, orders, customers

---

## Prerequisites

**Installation**:
```bash
pip install sqlalchemy

# With async support
pip install sqlalchemy[asyncio]

# PostgreSQL driver
pip install psycopg2-binary

# MySQL driver
pip install pymysql
```

---

## Basic Usage

### Define Models
```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))

    # One-to-many relationship
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Many-to-one relationship
    author = relationship('User', back_populates='posts')
```

### Create Tables
```python
engine = create_engine('postgresql://user:pass@localhost/mydb')
Base.metadata.create_all(engine)
```

### CRUD Operations
```python
Session = sessionmaker(bind=engine)
session = Session()

# Create
new_user = User(email='alice@example.com', name='Alice')
session.add(new_user)
session.commit()

# Read
user = session.query(User).filter_by(email='alice@example.com').first()

# Update
user.name = 'Alice Smith'
session.commit()

# Delete
session.delete(user)
session.commit()
```

---

## Common Patterns

### Querying
```python
# Filter
users = session.query(User).filter(User.name.like('%Alice%')).all()

# Order by
users = session.query(User).order_by(User.name.asc()).all()

# Limit
users = session.query(User).limit(10).all()

# Join
posts = session.query(Post).join(User).filter(User.name == 'Alice').all()

# Count
count = session.query(User).count()
```

### Relationships
```python
# One-to-many
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')

# Access relationship
user = session.query(User).first()
for post in user.posts:
    print(post.title)
```

### Many-to-Many
```python
from sqlalchemy import Table

# Association table
user_groups = Table('user_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    groups = relationship('Group', secondary=user_groups, back_populates='users')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=user_groups, back_populates='groups')
```

---

## Best Practices

**DO**:
- Use sessions properly (context managers)
- Close sessions after use
- Use connection pooling
- Define indexes on foreign keys
- Use relationship for joins (not manual joins)
- Batch inserts for performance

**DON'T**:
- Don't keep sessions open too long
- Don't use global session
- Don't forget to commit changes
- Don't use raw SQL strings (SQL injection risk)
- Don't load all data at once (use pagination)

---

## Session Management

### Context Manager
```python
from contextlib import contextmanager

@contextmanager
def get_db():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with get_db() as db:
    user = db.query(User).first()
```

### FastAPI Integration
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

---

## Migrations with Alembic

**Install**:
```bash
pip install alembic
alembic init alembic
```

**Create Migration**:
```bash
alembic revision --autogenerate -m "Add users table"
```

**Apply Migration**:
```bash
alembic upgrade head
```

---

## Performance

### Lazy vs Eager Loading
```python
# Lazy loading (default) - N+1 queries problem
users = session.query(User).all()
for user in users:
    print(user.posts)  # Separate query per user

# Eager loading - single query
from sqlalchemy.orm import joinedload

users = session.query(User).options(joinedload(User.posts)).all()
```

### Bulk Insert
```python
# Faster than add() in loop
session.bulk_insert_mappings(User, [
    {'email': 'user1@example.com'},
    {'email': 'user2@example.com'},
])
session.commit()
```

---

## Async SQLAlchemy (2.0+)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine('postgresql+asyncpg://user:pass@localhost/mydb')
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

---

## Alternatives

**Django ORM**: Tightly coupled to Django (but simpler for Django projects)
**Peewee**: Lighter weight (but less feature-rich)
**Tortoise ORM**: Async-first (but smaller ecosystem)
**Raw SQL**: Maximum control (but more boilerplate, SQL injection risk)

**Why SQLAlchemy**:
- Industry standard in Python
- Database-agnostic
- Powerful query API
- Excellent documentation
- Active development

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[authentication]], [[conversation-crud]]
**Technologies often used with**: [[postgresql]], [[fastapi]], [[alembic]]
