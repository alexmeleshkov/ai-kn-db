# Code Modules & Implementation Patterns

> **CRITICAL**: This file must contain ACTUAL CODE PATTERNS from the reference project.
> Include real implementation with proper imports, types, and error handling.
> NO pseudocode - show real, working code that enables 1:1 project generation.

## File Structure Overview

```
[Show actual project directory tree with file paths]
```

**Organization Strategy**: [describe approach - by feature / by layer / hybrid]

**Import Patterns**:
- [describe import style used]
- [path aliases if any]

---

## Backend Modules

### [Module 1: filename.ext]

**Purpose**: [what this module does]

**Responsibilities**:
- [responsibility 1]
- [responsibility 2]
- [responsibility 3]

**Key Functions/Methods**:
- `[function_signature]` - [description]
- `[function_signature]` - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL CODE - 20-60 lines showing real implementation]
```

**Dependencies**: [list packages]
**Environment Variables**: [list vars if any]
**Integration**: [what this calls / what calls this]

---

### [Module 2: filename.ext]

**Purpose**: [what this module does]

**Responsibilities**:
- [responsibility 1]
- [responsibility 2]

**Key Functions/Methods**:
- `[function_signature]` - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL CODE]
```

**Dependencies**: [list packages]
**Environment Variables**: [list vars if any]

---

### [Module 3: filename.ext]

**Purpose**: [what this module does]

**Endpoints** (if API routes):
- `[METHOD] [/path]` - [description]
- `[METHOD] [/path]` - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL CODE]
```

**Dependencies**: [list packages]
**Integration**: [calls which services]

---

## Frontend Modules

### [Module 4: ComponentName.ext]

**Purpose**: [what this component does]

**Props/Interface**:
```[language]
[PASTE ACTUAL INTERFACE/PROPS TYPE]
```

**Code Pattern**:
```[language]
[PASTE ACTUAL COMPONENT CODE - 30-60 lines]
```

**Dependencies**: [list packages]
**State Management**: [approach used]
**Styling**: [approach used]

---

### [Module 5: filename.ext]

**Purpose**: [what this module does]

**Exported Functions**:
- `[function_signature]` - [description]
- `[function_signature]` - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL CODE]
```

**Dependencies**: [list packages]
**Environment Variables**: [list vars if any]

---

## Database/Data Layer

### [Module 6: filename.ext]

**Purpose**: [what this module does]

**Schema/Fields**:
- [field]: [type] - [description]
- [field]: [type] - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL CODE showing model/schema definition]
```

**Database**: [database type and ORM]
**Migrations**: [migration tool and location]

---

## Utility Modules

### [Module 7: filename.ext]

**Purpose**: [what this module provides]

**Exported Functions**:
- `[function_signature]` - [description]
- `[function_signature]` - [description]

**Code Pattern**:
```[language]
[PASTE ACTUAL UTILITY FUNCTIONS]
```

---

## Capability Implementation Mapping

[Map each capability from meta.yaml to specific files/functions]

| Capability | Backend Implementation | Frontend Implementation |
|------------|----------------------|------------------------|
| [capability_1] | [file:function] | [file:component] |
| [capability_2] | [file:function] | [file:component] |
| [capability_3] | [file:function] | [file:component] |

---

## Integration Points

**Backend → Database**:
- Connection: [approach]
- ORM: [tool]
- Migrations: [tool and location]

**Frontend → Backend**:
- Protocol: [protocol]
- Auth: [auth approach]
- Real-time: [approach if any]

**Backend → External Services**:
- [Service]: [integration details]
- [Service]: [integration details]

---

## Error Handling Patterns

**Backend**:
```[language]
[PASTE ACTUAL ERROR HANDLING CODE]
```

**Frontend**:
```[language]
[PASTE ACTUAL ERROR HANDLING CODE]
```

---

## Testing Patterns (if applicable)

**Backend Tests** (location):
```[language]
[PASTE TEST EXAMPLE if critical]
```

**Frontend Tests** (location):
```[language]
[PASTE TEST EXAMPLE if critical]
```

---
