# TypeScript + React - Authentication Context with useAuth Hook

**Language**: TypeScript
**Technology**: React
**Feature/Pattern**: React Context API, Authentication State Management
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
npm install react typescript
npm install --save-dev @types/react
```

**Required Knowledge**:
- React Context API (createContext, useContext)
- React hooks (useState, useEffect, useCallback)
- TypeScript interfaces
- JWT token management
- LocalStorage API

---

## Overview

This snippet demonstrates a production-ready authentication context using React Context API. It provides centralized authentication state management with token persistence, automatic session restoration, and a custom hook for consuming auth state throughout the application.

Key features:
- React Context for global auth state
- Automatic token restoration on mount
- Token persistence in localStorage
- Type-safe auth context
- Custom useAuth hook for easy consumption
- Login, register, and logout flows
- Admin role detection

---

## Implementation

### Basic Usage

```typescript
import { AuthProvider, useAuth } from './hooks/useAuth';

// Wrap your app with AuthProvider
function App() {
  return (
    <AuthProvider>
      <YourApp />
    </AuthProvider>
  );
}

// Use auth in any component
function ProfileComponent() {
  const { user, isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  return (
    <div>
      <p>Welcome, {user?.email}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

**Explanation**:
- AuthProvider wraps the app to provide auth context
- useAuth hook accesses auth state from any component
- Context automatically manages loading and session restoration

### Advanced Usage with Protected Routes

```typescript
import { useAuth } from './hooks/useAuth';
import { Navigate } from 'react-router-dom';

// Protected route component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
}

// Admin-only route
function AdminRoute({ children }: { children: React.ReactNode }) {
  const { isAdmin, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAdmin) {
    return <Navigate to="/" />;
  }

  return <>{children}</>;
}

// Login component
function LoginForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      // Redirect handled by router
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}
```

**Key Points**:
- `isLoading` prevents flash of wrong content during session check
- `isAdmin` provides role-based access control
- Protected routes automatically redirect unauthenticated users
- Error handling in login/register forms

---

## Complete Example

```typescript
/**
 * Auth context and hook for managing authentication state.
 */

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import {
  AuthUser,
  login as apiLogin,
  register as apiRegister,
  logout as apiLogout,
  getCurrentUser,
  setAuthToken,
  getAuthToken,
  removeAuthToken,
} from '../services/api';

interface AuthContextType {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    const token = getAuthToken();
    if (token) {
      getCurrentUser()
        .then(setUser)
        .catch(() => {
          removeAuthToken();
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await apiLogin(email, password);
    setAuthToken(response.access_token);
    setUser(response.user);
  }, []);

  const register = useCallback(async (email: string, password: string) => {
    const response = await apiRegister(email, password);
    setAuthToken(response.access_token);
    setUser(response.user);
  }, []);

  const logout = useCallback(async () => {
    await apiLogout();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        isAdmin: !!user?.is_admin,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

---

## Configuration

```typescript
// API service configuration (api.ts)
export interface AuthUser {
  id: string;
  email: string;
  is_admin?: boolean;
}

export interface AuthResponse {
  user: AuthUser;
  access_token: string;
}

// Token storage functions
export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token');
}

export function setAuthToken(token: string): void {
  localStorage.setItem('auth_token', token);
}

export function removeAuthToken(): void {
  localStorage.removeItem('auth_token');
}

// Auth headers for API requests
export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
```

---

## Error Handling

```typescript
// Error handling in login/register
function LoginForm() {
  const { login } = useAuth();
  const [error, setError] = useState('');

  const handleLogin = async (email: string, password: string) => {
    try {
      setError('');
      await login(email, password);
      // Success - router will redirect
    } catch (err) {
      if (err instanceof ApiError) {
        switch (err.status) {
          case 401:
            setError('Invalid email or password');
            break;
          case 429:
            setError('Too many attempts. Please try again later.');
            break;
          default:
            setError('Login failed. Please try again.');
        }
      } else {
        setError('Network error. Please check your connection.');
      }
    }
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      handleLogin(email, password);
    }}>
      {/* form fields */}
      {error && <div className="error">{error}</div>}
    </form>
  );
}

// Session restoration error handling
useEffect(() => {
  const token = getAuthToken();
  if (token) {
    getCurrentUser()
      .then(setUser)
      .catch((err) => {
        // Token expired or invalid
        console.error('Session restoration failed:', err);
        removeAuthToken();
        setUser(null);
      })
      .finally(() => setIsLoading(false));
  } else {
    setIsLoading(false);
  }
}, []);
```

**Common Errors**:
1. **401 Unauthorized**: Invalid credentials - show user-friendly message
2. **Token Expired**: Caught in session restoration - silently remove token and redirect to login
3. **Network Error**: API unreachable - show connectivity message
4. **useAuth outside Provider**: Throws error with clear message about AuthProvider requirement

---

## Testing

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from './useAuth';

// Mock API functions
jest.mock('../services/api', () => ({
  login: jest.fn(),
  getCurrentUser: jest.fn(),
  getAuthToken: jest.fn(),
  setAuthToken: jest.fn(),
  removeAuthToken: jest.fn(),
}));

describe('useAuth', () => {
  it('provides authentication state', () => {
    function TestComponent() {
      const { isAuthenticated } = useAuth();
      return <div>{isAuthenticated ? 'Logged in' : 'Logged out'}</div>;
    }

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByText('Logged out')).toBeInTheDocument();
  });

  it('restores session on mount', async () => {
    const mockUser = { id: '1', email: 'test@example.com' };
    (getAuthToken as jest.Mock).mockReturnValue('token123');
    (getCurrentUser as jest.Mock).mockResolvedValue(mockUser);

    function TestComponent() {
      const { user, isLoading } = useAuth();
      if (isLoading) return <div>Loading...</div>;
      return <div>{user?.email}</div>;
    }

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('test@example.com')).toBeInTheDocument();
    });
  });

  it('throws error when used outside provider', () => {
    function TestComponent() {
      useAuth(); // Should throw
      return null;
    }

    expect(() => render(<TestComponent />)).toThrow(
      'useAuth must be used within an AuthProvider'
    );
  });
});
```

---

## Performance Considerations

- **Memoized Callbacks**: login, register, logout wrapped in useCallback to prevent re-renders
- **Single Session Check**: Session restoration runs once on mount, not on every render
- **Lazy Loading**: isLoading prevents unnecessary component renders during session check
- **Local State**: User state stored locally, not fetched on every auth check
- **Token Caching**: Token stored in localStorage, survives page refreshes

---

## Security Considerations

- **Token Storage**: Tokens stored in localStorage (consider httpOnly cookies for XSS protection)
- **Token Cleanup**: Tokens removed on logout and session restoration failure
- **Error Sanitization**: Sensitive error details not exposed to users
- **HTTPS Only**: Tokens should only be transmitted over HTTPS
- **Token Expiration**: Backend should implement token expiration and refresh
- **No Password Storage**: Passwords never stored, only passed to API

---

## Related

**Feature**: [[authentication/jwt-bcrypt]]
**Technology**: [[react]], [[typescript]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[python-jwt-auth.md]], [[python-bcrypt-password-hashing.md]]
