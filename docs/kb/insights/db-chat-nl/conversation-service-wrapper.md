# Conversation Service Wrapper Pattern

**Project**: [[db-chat-nl-master]]
**Category**: architecture-decision
**Author**: [[dima-efremov]]
**Date**: 2024-11-15

---

## Context

The project needed a clean API for conversation CRUD operations while keeping database access logic centralized in AppDataService.

---

## Problem

- AppDataService handles multiple concerns (users, conversations, messages, learned queries)
- API routes would need to call multiple AppDataService methods
- Mixing conversation logic with other database operations reduces code clarity

---

## Solution

Created a thin ConversationService wrapper that:
- Accepts AppDataService as dependency (composition pattern)
- Provides conversation-focused API (create, get, delete)
- Delegates all database operations to AppDataService
- Enforces user-scoped access via user_id parameter

**Interface**:
```python
class ConversationService:
    def __init__(self, app_data_service: AppDataService)
    def create_conversation(self, user_id: str, title: str = "New Chat") -> Optional[dict]
    def get_user_conversations(self, user_id: str) -> list[dict]
    def get_conversation(self, conversation_id: str, user_id: str) -> Optional[dict]
    def delete_conversation(self, conversation_id: str, user_id: str) -> bool
```

**Benefits**:
- Single Responsibility: Each service has one focus
- Composition over inheritance
- Easy to mock for testing
- Clear separation of concerns

---

## Alternatives Considered

**Option A: Direct AppDataService calls from routes**
- Simpler (fewer classes)
- But: Routes would be tightly coupled to AppDataService implementation
- But: Harder to change database layer later

**Option B: Repository pattern with interfaces**
- More flexible (can swap implementations)
- But: Over-engineering for this project size
- But: Extra abstraction layers add complexity

---

## Lessons Learned

- Thin wrappers are okay when they provide clear domain-focused APIs
- Composition (dependency injection) makes testing easier
- Don't over-abstract - wrapper is fine for small projects
- User-scoped access should be enforced at service layer, not routes
