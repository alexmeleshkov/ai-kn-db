# TypeScript - Type-Safe API Service with Generic Fetch Wrapper

**Language**: TypeScript
**Technology**: Fetch API
**Feature/Pattern**: Generic Type-Safe API Calls, Error Handling, Token Management
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
# No external packages required - uses native Fetch API
npm install typescript
```

**Required Knowledge**:
- TypeScript generics
- Fetch API
- Async/await
- Custom error classes
- HTTP status codes
- LocalStorage API

---

## Overview

This snippet demonstrates a production-ready type-safe API service layer using TypeScript generics and the Fetch API. It provides a centralized wrapper for API calls with automatic error handling, authentication token injection, and type-safe request/response handling.

Key features:
- Generic fetchApi wrapper with type inference
- Custom ApiError class with status codes
- Automatic JSON parsing and error handling
- Authentication token management (localStorage)
- Type-safe request bodies and responses
- Reusable across all API endpoints

---

## Implementation

### Basic Usage

```typescript
import { fetchApi, ApiError } from './api';

interface User {
  id: string;
  email: string;
  name: string;
}

// Type-safe GET request
async function getUser(id: string): Promise<User> {
  return fetchApi<User>(`/users/${id}`);
}

// Type-safe POST request
async function createUser(data: { email: string; name: string }): Promise<User> {
  return fetchApi<User>('/users', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// Usage
try {
  const user = await getUser('123');
  console.log(user.email); // Type-safe access
} catch (err) {
  if (err instanceof ApiError) {
    console.error(`API error ${err.status}: ${err.message}`);
  }
}
```

**Explanation**:
- Generic type parameter `<User>` ensures return type
- fetchApi automatically handles JSON parsing
- ApiError provides status code for error handling

### Advanced Usage with Auth and Error Handling

```typescript
// Authenticated request
async function getCurrentUser(): Promise<User> {
  return fetchApi<User>('/auth/me', {
    headers: getAuthHeaders(),
  });
}

// Request with custom headers
async function uploadFile(file: File): Promise<UploadResult> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData, // Don't set Content-Type for FormData
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new ApiError(response.status, error.detail || 'Upload failed');
  }

  return response.json();
}

// Error handling with status codes
async function loginWithErrorHandling(email: string, password: string) {
  try {
    const response = await fetchApi<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    setAuthToken(response.access_token);
    return response.user;
  } catch (err) {
    if (err instanceof ApiError) {
      switch (err.status) {
        case 401:
          throw new Error('Invalid email or password');
        case 429:
          throw new Error('Too many login attempts. Try again later.');
        case 500:
          throw new Error('Server error. Please try again.');
        default:
          throw new Error('Login failed');
      }
    }
    throw new Error('Network error');
  }
}
```

**Key Points**:
- `getAuthHeaders()` injects Bearer token automatically
- FormData uploads don't use fetchApi (no Content-Type header)
- Status-specific error messages for better UX
- ApiError allows granular error handling

---

## Complete Example

```typescript
/**
 * API service for communicating with the backend.
 */

const API_BASE = '/api/v1';

// Custom error class with status code
class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Generic fetch wrapper with type safety
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(response.status, error.detail || 'Request failed');
  }

  return response.json();
}

// ============ Auth Token Management ============

export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token');
}

export function setAuthToken(token: string): void {
  localStorage.setItem('auth_token', token);
}

export function removeAuthToken(): void {
  localStorage.removeItem('auth_token');
}

export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// ============ Type-Safe API Functions ============

export interface AuthUser {
  id: string;
  email: string;
  is_admin?: boolean;
}

export interface AuthResponse {
  user: AuthUser;
  access_token: string;
}

// Register new user
export async function register(email: string, password: string): Promise<AuthResponse> {
  return fetchApi<AuthResponse>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

// Login user
export async function login(email: string, password: string): Promise<AuthResponse> {
  return fetchApi<AuthResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

// Get current user (authenticated)
export async function getCurrentUser(): Promise<AuthUser> {
  return fetchApi<AuthUser>('/auth/me', {
    headers: getAuthHeaders(),
  });
}

// Logout user (authenticated)
export async function logout(): Promise<void> {
  try {
    await fetchApi('/auth/logout', {
      method: 'POST',
      headers: getAuthHeaders(),
    });
  } finally {
    removeAuthToken();
  }
}

// ============ Conversation API ============

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationWithMessages extends Conversation {
  messages: ConversationMessage[];
}

export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  metadata?: Record<string, unknown>;
}

// Get all conversations (authenticated)
export async function getConversations(): Promise<{ conversations: Conversation[] }> {
  return fetchApi<{ conversations: Conversation[] }>('/conversations', {
    headers: getAuthHeaders(),
  });
}

// Create conversation (authenticated)
export async function createConversation(title?: string): Promise<Conversation> {
  return fetchApi<Conversation>('/conversations', {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ title: title || 'New Chat' }),
  });
}

// Get conversation with messages (authenticated)
export async function getConversation(id: string): Promise<ConversationWithMessages> {
  return fetchApi<ConversationWithMessages>(`/conversations/${id}`, {
    headers: getAuthHeaders(),
  });
}

// Update conversation title (authenticated)
export async function updateConversationTitle(id: string, title: string): Promise<void> {
  await fetchApi(`/conversations/${id}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ title }),
  });
}

// Delete conversation (authenticated)
export async function deleteConversation(id: string): Promise<void> {
  await fetchApi(`/conversations/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
}
```

---

## Configuration

```typescript
// Environment-based API configuration
const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1';

// Request timeout wrapper
async function fetchWithTimeout<T>(
  endpoint: string,
  options: RequestInit = {},
  timeoutMs: number = 30000
): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetchApi<T>(endpoint, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } finally {
    clearTimeout(timeout);
  }
}
```

---

## Error Handling

```typescript
// Comprehensive error handling
async function handleApiRequest<T>(
  requestFn: () => Promise<T>
): Promise<T> {
  try {
    return await requestFn();
  } catch (err) {
    if (err instanceof ApiError) {
      // HTTP error with status code
      switch (err.status) {
        case 400:
          throw new Error('Invalid request. Please check your input.');
        case 401:
          // Token expired - redirect to login
          removeAuthToken();
          window.location.href = '/login';
          throw new Error('Please log in again.');
        case 403:
          throw new Error('You do not have permission to access this resource.');
        case 404:
          throw new Error('Resource not found.');
        case 429:
          throw new Error('Too many requests. Please try again later.');
        case 500:
        case 502:
        case 503:
          throw new Error('Server error. Please try again.');
        default:
          throw new Error(err.message || 'Request failed.');
      }
    } else if (err.name === 'AbortError') {
      throw new Error('Request timed out. Please try again.');
    } else {
      // Network error
      throw new Error('Network error. Please check your connection.');
    }
  }
}

// Usage
async function safeGetUser(id: string): Promise<User | null> {
  try {
    return await handleApiRequest(() => getUser(id));
  } catch (err) {
    console.error('Failed to load user:', err.message);
    return null;
  }
}

// Error parsing with fallback
if (!response.ok) {
  const error = await response.json().catch(() => ({
    detail: 'Unknown error'
  }));
  throw new ApiError(response.status, error.detail || 'Request failed');
}
```

**Common Errors**:
1. **401 Unauthorized**: Token expired or invalid - remove token and redirect to login
2. **404 Not Found**: Resource doesn't exist - show user-friendly message
3. **429 Too Many Requests**: Rate limited - show retry message with delay
4. **500 Server Error**: Backend issue - show generic error and suggest retry

---

## Testing

```typescript
import { fetchApi, ApiError } from './api';

// Mock fetch globally
global.fetch = jest.fn();

describe('fetchApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns typed response on success', async () => {
    const mockUser = { id: '1', email: 'test@example.com' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUser,
    });

    const result = await fetchApi<typeof mockUser>('/users/1');

    expect(result).toEqual(mockUser);
    expect(fetch).toHaveBeenCalledWith('/api/v1/users/1', {
      headers: { 'Content-Type': 'application/json' },
    });
  });

  it('throws ApiError on HTTP error', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'Not found' }),
    });

    await expect(fetchApi('/users/999')).rejects.toThrow(ApiError);
    await expect(fetchApi('/users/999')).rejects.toMatchObject({
      status: 404,
      message: 'Not found',
    });
  });

  it('handles malformed error responses', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => {
        throw new Error('Invalid JSON');
      },
    });

    await expect(fetchApi('/test')).rejects.toMatchObject({
      status: 500,
      message: 'Unknown error',
    });
  });

  it('includes auth headers when token exists', async () => {
    localStorage.setItem('auth_token', 'token123');

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    const headers = getAuthHeaders();
    await fetchApi('/auth/me', { headers });

    expect(fetch).toHaveBeenCalledWith(
      '/api/v1/auth/me',
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: 'Bearer token123',
        }),
      })
    );
  });
});
```

---

## Performance Considerations

- **Generic Type Inference**: TypeScript infers return types automatically, no runtime overhead
- **Single JSON Parse**: Response parsed once in fetchApi, not in each endpoint function
- **Token Caching**: Auth token cached in localStorage, not fetched repeatedly
- **Connection Reuse**: Native fetch reuses HTTP connections automatically
- **Error Handling**: Error responses parsed safely with fallback to prevent hanging

---

## Security Considerations

- **Token Storage**: Tokens in localStorage (consider httpOnly cookies for production)
- **HTTPS Only**: API calls should only use HTTPS in production
- **Token in Header**: Bearer token in Authorization header, never in URL
- **Token Cleanup**: Tokens removed on logout and auth errors
- **CORS**: Backend must set proper CORS headers
- **Error Messages**: Sanitized error messages don't expose sensitive details
- **Input Validation**: Always validate request bodies on backend

---

## Related

**Feature**: [[authentication/jwt-bcrypt]], [[conversation/postgresql-crud]]
**Technology**: [[typescript]], [[react]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[python-fastapi-endpoints.md]]
