# Admin Panel

**Feature ID**: admin.panel
**Capability**: admin-panel
**Technologies**: fastapi, react-hooks, postgresql

---

## Overview

Admin-only panel for viewing all user conversations with role-based access control, read-only conversation viewer, and user management capabilities.

**Key characteristics**:
- Role-based access control (admin flag in JWT)
- View all conversations across all users
- Read-only conversation viewer with message history
- User listing and statistics
- Admin middleware for endpoint protection

---

## File Structure

```
backend/app/
  api/
    admin_routes.py        # Admin-only API endpoints

frontend/src/
  components/
    SidebarTabs.tsx        # Admin tab in sidebar
    AdminConversationViewer.tsx  # Read-only conversation display
```

---

## Implementation Patterns

### 1. Admin Routes (admin_routes.py)

**Purpose**: FastAPI router with admin-only endpoints protected by require_admin middleware

**Interface**:
```python
async def require_admin(authorization: str = Header(None)) -> dict

@router.get("/admin/conversations")
async def get_all_conversations(limit: int = 200, admin_user: dict = Depends(require_admin)) -> dict

@router.get("/admin/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, admin_user: dict = Depends(require_admin)) -> dict

@router.get("/admin/users")
async def get_all_users(admin_user: dict = Depends(require_admin)) -> dict
```

**Complete Flow - require_admin()**:
1. Extract Authorization header
2. Check header starts with "Bearer "
3. Extract token: token = authorization.replace("Bearer ", "")
4. Verify token with auth.verify_token(token)
5. Check payload has is_admin = True
6. If any check fails: raise HTTPException 401 or 403
7. Return user dict if admin

**All Behaviors**:
- Admin authentication required for all routes
- 401 Unauthorized if token missing or invalid
- 403 Forbidden if user exists but is not admin
- 503 Service Unavailable if auth service unavailable
- Returns paginated conversation list (default limit 200)
- Returns user list with email and admin status

---

### 2. Admin Sidebar Tab (SidebarTabs.tsx)

**Purpose**: React component with admin tab visible only to admin users

**Interface**:
```typescript
function AdminPanel({ onViewConversation }: { onViewConversation?: (id: string) => void }): JSX.Element
```

**Complete Flow**:
1. Check if user is admin via useAuth().isAdmin
2. If admin, show Admin tab button in sidebar
3. On Admin tab click: fetch all conversations via getAdminConversations(200)
4. Display conversations with user email badge, title, and date
5. On conversation click: call onViewConversation(id)

**All Behaviors**:
- Admin tab only visible if isAdmin = true
- Fetches all conversations across all users
- Shows user email badge for each conversation
- Read-only view (no delete button)
- Loading state with spinner
- Error state with retry button
- Relative date formatting

---

### 3. Admin Conversation Viewer (AdminConversationViewer.tsx)

**Purpose**: Read-only view of conversation details and message history

**Interface**:
```typescript
interface AdminConversationViewerProps {
  conversationId: string;
}

export function AdminConversationViewer({ conversationId }: AdminConversationViewerProps): JSX.Element
```

**Complete Flow**:
1. On mount: fetch conversation details via getAdminConversation(conversationId)
2. Display conversation metadata (title, user email, created date)
3. Render all messages in chronological order
4. Show message role (user/assistant), content, timestamp
5. No edit or delete capabilities (read-only)

**All Behaviors**:
- Read-only display (no interaction)
- Shows full message history
- Message rendering with markdown support
- Loading state while fetching
- Error state if conversation not found

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Admin conversation monitoring

---

## Related Technologies

- **[FastAPI](../technologies/fastapi.md)** - Admin API endpoints
- **[React Hooks](../technologies/react-hooks.md)** - Admin UI components
- **[PostgreSQL](../technologies/postgresql.md)** - Data storage

---

## Variants

### Variant 1: JWT Admin Flag (Current)
- **When to use**: Simple role-based access with JWT
- **Trade-offs**:
  - ✅ Pros: Stateless, easy to implement, works with existing auth
  - ❌ Cons: Role changes require new token, limited granularity

### Variant 2: Role-Based Access Control (RBAC)
- **When to use**: Complex permission systems, multiple roles
- **Trade-offs**:
  - ✅ Pros: Fine-grained permissions, dynamic role assignment
  - ❌ Cons: More complex, requires permission database
