# TypeScript

**Technology**: TypeScript 5+
**Category**: Language

---

## Overview

Typed superset of JavaScript providing static type checking and improved IDE support.

---

## Usage Files

All `.ts` and `.tsx` files in frontend:
- `frontend/src/hooks/*.ts`
- `frontend/src/components/*.tsx`
- `frontend/src/services/*.ts`

---

## Complete Usage Patterns

### Interface Definitions

**Pattern**:
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  executedQueries?: Array<{
    query: string;
    success: boolean;
    rows?: number;
  }>;
}

interface StreamingState {
  isStreaming: boolean;
  currentText: string;
  queryStatus: 'idle' | 'executing' | 'success' | 'error';
}
```

**All Behaviors**:
- Interface for object shapes
- Union types for constrained values
- Optional properties with ?
- Array types with Array<T> or T[]

### Function Typing

**Pattern**:
```typescript
function sendUserMessage(content: string): Promise<void> {
  // Implementation
}

const handleClick = useCallback((id: string) => {
  // Implementation
}, []);
```

**All Behaviors**:
- Parameter types
- Return type annotations
- Promise<T> for async functions
- void for no return value

---

## Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true
  }
}
```
