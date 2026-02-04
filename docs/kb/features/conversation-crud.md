# Conversation CRUD

**Feature ID**: conversation.crud
**Capability**: conversation-crud
**Technologies**: postgresql, fastapi, react-hooks

---

## Overview

Full CRUD operations for conversation management with user-scoped access control, PostgreSQL persistence, and React state management. Enables users to create, retrieve, update, and delete conversations with message history.

**Key characteristics**:
- User-scoped access (users can only access their own conversations)
- PostgreSQL storage with cascade delete (deleting conversation removes all messages)
- Connection pooling with psycopg2.pool.SimpleConnectionPool
- RESTful API with FastAPI
- Optimistic UI updates in React
- Conversation listing with pagination
- Message threading within conversations

---

## File Structure

```
backend/app/
  api/
    conversation_routes.py  # REST API endpoints
  services/
    app_data.py            # Conversation CRUD implementation
    conversations.py       # Conversation service wrapper
  models/
    database.py            # Conversation and ConversationMessage models

frontend/src/
  components/
    SidebarTabs.tsx        # Conversation list UI
  hooks/
    useChat.ts             # Conversation state management
```

---

## Implementation Patterns

### 1. Conversation Routes (conversation_routes.py)

**Purpose**: FastAPI REST API for conversation CRUD with JWT authentication

**Interface**:
```python
@router.get("/conversations")
async def get_user_conversations(current_user: dict = Depends(require_auth)) -> dict

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, current_user: dict = Depends(require_auth)) -> dict

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user: dict = Depends(require_auth)) -> dict
```

**All Behaviors**:
- GET /conversations: Returns user's conversations ordered by updated_at DESC
- GET /conversations/{id}: Returns single conversation with all messages
- DELETE /conversations/{id}: Cascade deletes conversation and messages
- User-scoped access (filtered by user_id from JWT)
- 404 Not Found if conversation doesn't exist or doesn't belong to user
- Returns conversation objects with id, title, created_at, updated_at, messages

---

### 2. App Data Service (app_data.py)

**Purpose**: PostgreSQL-backed CRUD service for conversations and messages

**Interface**:
```python
class AppDataService:
    def create_conversation(user_id: str, title: str = "New Chat") -> Optional[dict]
    def get_conversations(user_id: str, limit: int = 50) -> list[dict]
    def get_conversation(conversation_id: str, user_id: str) -> Optional[dict]
    def update_conversation_title(conversation_id: str, user_id: str, title: str) -> bool
    def delete_conversation(conversation_id: str, user_id: str) -> bool

    def add_message(conversation_id: str, role: str, content: str, metadata: dict = None) -> Optional[dict]
    def get_messages(conversation_id: str, limit: int = 100) -> list[dict]
```

**Complete Flow - Create Conversation**:
1. Get connection from pool
2. Execute: INSERT INTO conversations (user_id, title) VALUES (%s, %s) RETURNING *
3. Fetch result row
4. Commit transaction
5. Return dict with id (cast to str), user_id, title, created_at.isoformat(), updated_at.isoformat()
6. On exception: rollback, log error, return None
7. Finally: close cursor, return connection to pool

**Complete Flow - Get Conversations**:
1. Get connection from pool
2. Execute: SELECT * FROM conversations WHERE user_id = %s ORDER BY updated_at DESC LIMIT %s
3. Fetch all rows
4. For each row: convert to dict with UUIDs cast to str, dates to isoformat()
5. Return list of conversation dicts
6. Finally: close cursor, return connection

**Complete Flow - Delete Conversation**:
1. Get connection from pool
2. Execute: DELETE FROM conversations WHERE id = %s AND user_id = %s
3. Check cursor.rowcount > 0 (row was deleted)
4. Commit transaction
5. Return True if deleted, False otherwise
6. On exception: rollback, log error, return False
7. Finally: close cursor, return connection

**Complete Flow - Add Message**:
1. Get connection from pool
2. Execute: INSERT INTO conversation_messages (conversation_id, role, content, metadata) VALUES (%s, %s, %s, %s) RETURNING *
3. Fetch result row
4. Update conversation updated_at: UPDATE conversations SET updated_at = NOW() WHERE id = %s
5. Commit transaction
6. Return message dict
7. On exception: rollback, log error, return None

**All Behaviors**:
- User-scoped access enforced by user_id in WHERE clauses
- Cascade delete via foreign key constraint (ON DELETE CASCADE)
- Automatic updated_at timestamp on message add
- Connection pooling for concurrent requests
- Transaction management (commit on success, rollback on error)
- UUID to string conversion for JSON serialization
- Datetime to ISO format conversion
- Default title "New Chat" for new conversations
- Limit parameter for pagination (default 50 conversations, 100 messages)

**Error Handling**:
- psycopg2 exceptions caught, logged, transaction rolled back
- Returns None or False on error (not raised to caller)
- Logs include conversation_id and user_id for debugging

---

### 3. Conversation Service (conversations.py)

**Purpose**: Wrapper service for conversation operations (delegates to AppDataService)

**Interface**:
```python
class ConversationService:
    def __init__(app_data_service: AppDataService)
    def create_conversation(user_id: str, title: str = "New Chat") -> Optional[dict]
    def get_user_conversations(user_id: str) -> list[dict]
    def get_conversation(conversation_id: str, user_id: str) -> Optional[dict]
    def delete_conversation(conversation_id: str, user_id: str) -> bool
```

**Purpose**: Provides conversation-focused API, delegates to AppDataService

---

### 4. Database Models (database.py)

**Purpose**: SQLAlchemy ORM models for conversations and messages

**Interface**:
```python
class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = 'conversation_messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
```

**All Behaviors**:
- UUID primary keys for conversations and messages
- Foreign key CASCADE delete (deleting conversation deletes messages)
- Automatic timestamps (created_at, updated_at)
- JSON metadata field for extensibility
- SQLAlchemy relationships for ORM queries

---

### 5. Frontend Sidebar (SidebarTabs.tsx)

**Purpose**: React component displaying user's conversation list with delete functionality

**Interface**:
```typescript
interface SidebarTabsProps {
  onSelectConversation?: (id: string) => void;
  refreshTrigger?: number;
}

export const SidebarTabs = memo(function SidebarTabs(props): JSX.Element)
```

**Complete Flow**:
1. On mount: fetch user's conversations via getConversations()
2. Display conversations ordered by updated_at (most recent first)
3. Show title, relative date (Today, Yesterday, N days ago)
4. User clicks conversation: call onSelectConversation(id)
5. User clicks delete button: show confirm dialog, call deleteConversation(id)
6. On delete success: remove from local state optimistically
7. RefreshTrigger prop change: re-fetch conversations

**All Behaviors**:
- Memoized component (prevents unnecessary re-renders)
- Optimistic UI update on delete
- Relative date formatting
- Loading state with spinner
- Empty state message
- Delete confirmation dialog
- stopPropagation on delete button (prevents conversation selection)

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Chat conversation management

---

## Related Technologies

- **[PostgreSQL](../technologies/postgresql.md)** - Database storage
- **[FastAPI](../technologies/fastapi.md)** - REST API framework
- **[React Hooks](../technologies/react-hooks.md)** - Frontend state management

---

## Variants

### Variant 1: PostgreSQL with SQLAlchemy (Current)
- **When to use**: Standard relational conversation storage
- **Trade-offs**:
  - ✅ Pros: ACID transactions, foreign key constraints, familiar SQL
  - ❌ Cons: Schema rigidity, scaling requires careful indexing

### Variant 2: NoSQL Document Store
- **When to use**: Highly nested conversation structures, flexible schema
- **Trade-offs**:
  - ✅ Pros: Flexible schema, easy nesting, horizontal scaling
  - ❌ Cons: No foreign key enforcement, eventual consistency
