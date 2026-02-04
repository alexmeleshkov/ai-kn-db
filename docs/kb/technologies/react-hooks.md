# React Hooks

**Technology**: React 18+ Hooks API
**Category**: Library / Pattern

---

## Overview

React custom hooks for state management, side effects, and component logic reuse.

---

## Usage Files

- `frontend/src/hooks/useChat.ts`
- `frontend/src/hooks/useQueryHistory.ts`
- `frontend/src/hooks/useSuggestions.ts`
- `frontend/src/components/SidebarTabs.tsx`

---

## Complete Usage Patterns

### Custom Hook Pattern (useChat.ts)

**Pattern**:
```typescript
import { useState, useCallback, useRef, useEffect } from 'react';

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendUserMessage = useCallback(async (content: string) => {
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    // ... implementation
  }, []);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    messages,
    isLoading,
    sendUserMessage,
  };
}
```

**All Behaviors**:
- useState for state management
- useCallback for memoized functions
- useRef for mutable values (no re-render)
- useEffect for side effects and cleanup
- Custom hook returns object with state and functions

---

## Common Patterns

**Pattern 1: State Management**
- Usage: useState for component state
- Example: messages, isLoading, error states

**Pattern 2: Memoization**
- Usage: useCallback to prevent function recreation
- Example: sendUserMessage, cancelStream

**Pattern 3: Refs for Mutable Values**
- Usage: useRef for values that don't trigger re-render
- Example: AbortController, timers

**Pattern 4: Side Effects**
- Usage: useEffect for subscriptions, timers, cleanup
- Example: Elapsed time timer, stream cleanup

---

## Best Practices

- Use useCallback for functions passed as props
- Use useRef for mutable values (timers, abort controllers)
- Clean up side effects in useEffect return function
- Memoize expensive computations with useMemo
- Extract reusable logic into custom hooks
