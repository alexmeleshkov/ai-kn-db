# SQLAlchemy

**Technology**: SQLAlchemy 2.0+
**Category**: ORM

---

## Overview

Python ORM for database modeling with declarative base, relationships, and automatic schema generation.

---

## Usage Files

- `backend/app/models/database.py`

---

## Complete Usage Patterns

### Model Definition (database.py)

**Pattern**:
```python
from sqlalchemy import Column, String, DateTime, UUID, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship, declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
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
- Declarative base pattern
- UUID primary keys
- Foreign keys with CASCADE delete
- Relationships for ORM queries
- Automatic timestamps
- Cascade delete (deleting user deletes conversations)

---

## Configuration

```python
# Database URL
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Create engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)
```
