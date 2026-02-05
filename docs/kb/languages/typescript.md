# TypeScript

**Category**: Programming Language
**Website**: https://www.typescriptlang.org/
**Documentation**: https://www.typescriptlang.org/docs/

---

## Overview

TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. It adds optional static typing, interfaces, classes, and modern ECMAScript features to JavaScript.

---

## Key Features

**Static Typing**: Catch errors at compile time, not runtime
**Type Inference**: Automatic type detection
**Interfaces**: Define object shapes and contracts
**Generics**: Reusable, type-safe components
**Enums**: Named constants
**Modern JavaScript**: ES6+ features compiled to ES5

---

## Common Use Cases

- **Large Applications**: Type safety for maintainability
- **APIs**: Type-safe request/response models
- **React Apps**: Props and state typing
- **Node.js**: Backend with type safety
- **Libraries**: Publish with type definitions

---

## Prerequisites

**Installation**:
```bash
npm install -g typescript

# Or per-project
npm install --save-dev typescript
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

---

## Basic Types

```typescript
// Primitives
let name: string = "Alice";
let age: number = 30;
let active: boolean = true;

// Arrays
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b"];

// Objects
let user: { name: string; age: number } = {
  name: "Bob",
  age: 25
};

// Functions
function greet(name: string): string {
  return `Hello, ${name}`;
}

// Union types
let id: string | number = "123";

// Literal types
let status: "active" | "inactive" = "active";
```

---

## Interfaces

```typescript
interface User {
  id: string;
  email: string;
  age?: number;  // Optional
  readonly createdAt: Date;  // Read-only
}

function createUser(data: User): User {
  return { ...data, createdAt: new Date() };
}

// Extending interfaces
interface Admin extends User {
  permissions: string[];
}
```

---

## Type Aliases

```typescript
type ID = string | number;

type ApiResponse<T> = {
  data: T;
  error: string | null;
  loading: boolean;
};

type User = {
  id: ID;
  name: string;
};

const response: ApiResponse<User> = {
  data: { id: 1, name: "Alice" },
  error: null,
  loading: false
};
```

---

## Generics

```typescript
function identity<T>(value: T): T {
  return value;
}

interface Box<T> {
  value: T;
}

const stringBox: Box<string> = { value: "hello" };
const numberBox: Box<number> = { value: 42 };

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

---

## React with TypeScript

```typescript
import React, { useState } from 'react';

interface Props {
  name: string;
  age?: number;
  onUpdate: (name: string) => void;
}

const UserCard: React.FC<Props> = ({ name, age, onUpdate }) => {
  const [editing, setEditing] = useState(false);

  return (
    <div>
      <h2>{name}</h2>
      {age && <p>Age: {age}</p>}
      <button onClick={() => onUpdate(name)}>Update</button>
    </div>
  );
};
```

---

## Utility Types

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude specific properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record - map keys to type
type UserMap = Record<string, User>;
```

---

## Best Practices

**DO**:
- Enable strict mode in tsconfig.json
- Use interfaces for object shapes
- Prefer type inference over explicit types
- Use generics for reusable code
- Define types for API responses
- Use const assertions for literal types

**DON'T**:
- Don't use `any` (use `unknown` instead)
- Don't ignore TypeScript errors
- Don't over-complicate types
- Don't use type assertions unnecessarily
- Don't skip type checking with `//@ts-ignore`

---

## Type Guards

```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function processValue(value: string | number) {
  if (isString(value)) {
    console.log(value.toUpperCase());
  } else {
    console.log(value.toFixed(2));
  }
}
```

---

## Common Patterns

### Discriminated Unions
```typescript
type Success = { status: 'success'; data: any };
type Error = { status: 'error'; message: string };
type Loading = { status: 'loading' };

type ApiState = Success | Error | Loading;

function handleState(state: ApiState) {
  switch (state.status) {
    case 'success':
      return state.data;
    case 'error':
      return state.message;
    case 'loading':
      return 'Loading...';
  }
}
```

---

## Alternatives

**Flow**: Facebook's type checker (less popular)
**JSDoc**: Type annotations in comments (no compilation)
**ReScript**: Different syntax, stronger types
**Plain JavaScript**: No types (faster to write, harder to maintain)

**Why TypeScript**:
- Industry standard
- Excellent tooling and IDE support
- Catches bugs at compile time
- Self-documenting code
- Great for large teams

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[real-time-chat]], [[data-visualization]]
**Technologies often used with**: [[react-hooks]], [[fastapi]]
