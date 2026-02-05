# React Hooks

**Category**: Frontend Library / Pattern
**Website**: https://react.dev/
**Documentation**: https://react.dev/reference/react

---

## Overview

React Hooks are functions that let you use state and other React features in functional components. Introduced in React 16.8, they enable state management, side effects, and custom logic reuse without class components.

---

## Key Hooks

**useState**: State management in functional components
**useEffect**: Side effects (data fetching, subscriptions, DOM updates)
**useContext**: Access React context without nesting
**useRef**: Mutable values and DOM references
**useMemo**: Memoized computations for performance
**useCallback**: Memoized callbacks to prevent re-renders
**useReducer**: Complex state logic (like Redux)

---

## Common Use Cases

- **State Management**: Local component state
- **API Calls**: Fetch data on component mount
- **Event Listeners**: Subscribe/unsubscribe to events
- **Form Handling**: Input state and validation
- **WebSockets/SSE**: Real-time data streaming
- **Local Storage**: Persist state across sessions

---

## Basic Examples

### useState
```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

### useEffect
```typescript
import { useEffect, useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser);

    return () => {
      // Cleanup (cancel requests, unsubscribe)
    };
  }, [userId]);

  return <div>{user?.name}</div>;
}
```

---

## Custom Hooks

Custom hooks encapsulate reusable logic:

### useLocalStorage
```typescript
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### useAsync (Data Fetching)
```typescript
function useAsync<T>(fn: () => Promise<T>, deps: any[]) {
  const [state, setState] = useState({
    loading: true,
    data: null as T | null,
    error: null as Error | null
  });

  useEffect(() => {
    let cancelled = false;

    fn()
      .then(data => !cancelled && setState({ loading: false, data, error: null }))
      .catch(error => !cancelled && setState({ loading: false, data: null, error }));

    return () => { cancelled = true; };
  }, deps);

  return state;
}
```

### useDebounce
```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
```

---

## Best Practices

**DO**:
- Name custom hooks with "use" prefix
- Include all dependencies in useEffect arrays
- Use functional updates for derived state
- Extract reusable logic into custom hooks
- Clean up in useEffect return functions

**DON'T**:
- Don't call hooks conditionally
- Don't call hooks in loops
- Don't call hooks in regular functions
- Don't forget cleanup (memory leaks)
- Don't use empty deps when you need dependencies

---

## Performance

### useMemo
```typescript
const sorted = useMemo(() => {
  return [...items].sort((a, b) => a - b);
}, [items]);
```

### useCallback
```typescript
const handleClick = useCallback(() => {
  console.log('Clicked');
}, []);
```

---

## Common Pitfalls

**Stale Closures**:
```typescript
// ❌ Bad
const [count, setCount] = useState(0);
useEffect(() => {
  setInterval(() => setCount(count + 1), 1000); // Stale
}, []);

// ✅ Good
useEffect(() => {
  setInterval(() => setCount(c => c + 1), 1000);
}, []);
```

---

## Alternatives

**Redux**: Global state management
**MobX**: Reactive state management
**Zustand**: Minimal state library
**Jotai**: Atomic state management

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[real-time-chat]], [[data-visualization]]
**Technologies often used with**: [[typescript]], [[sse]]
