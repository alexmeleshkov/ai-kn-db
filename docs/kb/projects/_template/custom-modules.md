# Custom Modules

> **NEW FILE**: Project-specific code patterns that don't belong in reusable features

## Purpose

This file contains implementation patterns for code that is unique to this project and cannot be generalized into reusable features.

**What goes here**:
- Project-specific business logic
- Custom glue code connecting features
- Unique data models specific to this domain
- Project-specific utilities

**What does NOT go here**:
- Reusable authentication patterns → features/authentication/
- Reusable database patterns → features/database/
- Framework-specific patterns → technologies/

---

## Custom Backend Modules

### [Module Name: backend/app/custom/filename.py]

**Purpose**: What this module does

**Interface**:
```python
[Class/function signatures]
```

**Complete Flow**:
1. [Step-by-step algorithm]

**All Behaviors**:
- [Complete list]

**Dependencies**:
- [With WHY]

**Integration Points**:
- [How it connects to features]

---

## Custom Frontend Modules

### [Module Name: frontend/src/custom/ComponentName.tsx]

**Purpose**: What this component does

**Interface**:
```typescript
[Props interface]
```

**Complete Flow**:
1. [Rendering logic]

**All Behaviors**:
- [Complete list]

---

## Custom Glue Code

Patterns for connecting features that are specific to this project.

### Example: Database + Auth Integration

**Purpose**: Custom middleware that validates JWT and injects database connection

[Implementation pattern]

---

## Notes

- Keep this file minimal - most code should use reusable features
- If a pattern appears useful for other projects, extract it to features/
- Update this file during scanning if new custom code is found
