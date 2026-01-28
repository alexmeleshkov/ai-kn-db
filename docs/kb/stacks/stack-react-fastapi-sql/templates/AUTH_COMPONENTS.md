# Authentication Components

This document describes the authentication components added to the stack-react-fastapi-sql template.

## Overview

Authentication components have been added based on the db-chat-nl KB documentation. These components provide JWT-based authentication with login, registration, user profile, and protected routes.

## Backend Components Added

### 1. `backend/app/services/auth.py`

Authentication service with core functions:

- `hash_password(password)` - Hash password using bcrypt
- `verify_password(plain, hashed)` - Verify password against hash
- `create_access_token(user_id)` - Generate JWT token (24h expiration)
- `verify_token(token)` - Decode and validate JWT token

**Based on**: db-chat-nl modules.md:5-36

**Dependencies**: PyJWT, bcrypt

**Environment Variables Needed**:
- `JWT_SECRET` - Secret key for JWT signing (must be configured in production)
- `JWT_ALGORITHM` - Algorithm for JWT (default: HS256)

**TODOs**:
- Replace Settings stub with real config from `app.core.config`
- Implement database integration for user management
- Add functions: `create_user()`, `get_user_by_email()`, `authenticate_user()`

### 2. `backend/app/api/auth_routes.py`

API routes for authentication:

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Authenticate and get JWT token
- `POST /api/v1/auth/logout` - Logout (client-side token removal)
- `GET /api/v1/auth/me` - Get current user profile

**Based on**: db-chat-nl architecture.md:10, structure.md:26

**Features**:
- Pydantic schemas for request/response validation
- HTTPBearer security for token authentication
- `get_current_user()` dependency for protected routes

**TODOs**:
- Replace user stubs with real SQLAlchemy User model queries
- Add email uniqueness validation on registration
- Implement password strength validation

### 3. `backend/app/main.py` (updated)

Updated to include auth router:

```python
from .api import auth_routes
app.include_router(auth_routes.router)
```

## Frontend Components Added

### 1. `frontend/src/hooks/useAuth.tsx`

Authentication context and hook:

**Context State**:
- `currentUser` - User object or null
- `isAuthenticated` - Boolean authentication status
- `isLoading` - Loading state for async operations
- `error` - Error message string

**Functions**:
- `login(email, password)` - Authenticate user
- `register(username, email, password)` - Register new user
- `logout()` - Clear authentication state

**Based on**: db-chat-nl structure.md:19, architecture.md:54

**Storage**: JWT token stored in `localStorage` as `auth_token`

**Usage**:
```tsx
const { currentUser, isAuthenticated, login, logout } = useAuth();
```

### 2. `frontend/src/components/AuthPage.tsx`

Login and registration form component:

**Features**:
- Toggle between login/register modes
- Email and password validation
- Show/hide password toggle
- Error message display
- Responsive design with gradient background

**Based on**: db-chat-nl architecture.md:46, structure.md:27

**Styling**: Uses CSS variables from db-chat-nl styles.md (Ipswich Town brand colors)

### 3. `frontend/src/components/Sidebar.tsx`

Navigation sidebar with user profile:

**Features**:
- User avatar with initials
- Username and email display
- New chat button
- Logout button
- Conversation history section (stub)

**Based on**: db-chat-nl architecture.md:51, structure.md:49

**Styling**: Primary base color (#1a365d) from db-chat-nl

**TODOs**:
- Implement conversation history list
- Add conversation selection functionality
- Add mobile responsive menu toggle

### 4. `frontend/src/App.tsx` (updated)

Root component with authentication routing:

**Structure**:
```
App (AuthProvider wrapper)
  └── AppRouter (checks auth state)
      ├── AuthPage (if not authenticated)
      └── ChatInterface (if authenticated)
          ├── Sidebar
          └── Chat UI
```

**Based on**: db-chat-nl architecture.md:64

**Features**:
- AuthProvider wraps entire app
- Loading screen during auth check
- Protected chat interface
- CSS variables for consistent styling

## CSS Variables

The following CSS variables are defined for consistent styling:

```css
--primary-base: #1a365d    /* Sidebar, headings */
--primary-dark: #142850    /* Hover states */
--accent-base: #3182ce     /* Links, buttons */
--success: #38a169         /* Success messages */
--error: #e53e3e           /* Error messages */
```

**Based on**: db-chat-nl styles.md:11-19

## Integration Checklist

To fully integrate authentication in a generated project:

### Backend
- [ ] Install dependencies: `pip install pyjwt bcrypt python-multipart`
- [ ] Configure environment variables in `.env`:
  - `JWT_SECRET=your-secret-key-change-in-production`
  - `JWT_ALGORITHM=HS256`
- [ ] Create SQLAlchemy User model with fields:
  - `id`, `username`, `email`, `password_hash`, `created_at`
- [ ] Implement database user functions in `auth.py`
- [ ] Update auth routes to use real database queries
- [ ] Add Alembic migration for User table

### Frontend
- [ ] Ensure AuthProvider wraps App in `main.tsx`
- [ ] Test login/register flows
- [ ] Add password strength requirements
- [ ] Implement "Forgot Password" feature (optional)
- [ ] Add conversation history API integration
- [ ] Test protected route redirects

## Testing

### Backend Endpoints

Test with curl or Postman:

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Get current user
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Frontend Flow

1. Visit app without token → should show AuthPage
2. Register new user → should receive token and show chat
3. Refresh page → should stay logged in
4. Logout → should return to AuthPage
5. Login with existing credentials → should show chat

## Security Considerations

**Current State (Stub Implementation)**:
- Authentication accepts any credentials (demo mode)
- No database persistence
- JWT secret is hardcoded

**Production Requirements**:
- Strong JWT secret (32+ random characters)
- Database-backed user storage with SQLAlchemy
- Password hashing with bcrypt (already implemented)
- HTTPS only for production
- Token expiration handling
- CORS configuration for specific origins
- Rate limiting on auth endpoints
- Password strength requirements

## File Locations

### Backend
- `templates/backend/app/services/auth.py` (new)
- `templates/backend/app/api/auth_routes.py` (new)
- `templates/backend/app/main.py` (updated)

### Frontend
- `templates/frontend/src/hooks/useAuth.tsx` (new)
- `templates/frontend/src/components/AuthPage.tsx` (new)
- `templates/frontend/src/components/Sidebar.tsx` (new)
- `templates/frontend/src/App.tsx` (updated)

## References

All components are based on the db-chat-nl project KB documentation:

- `docs/kb/projects/db-chat-nl/architecture.md`
- `docs/kb/projects/db-chat-nl/modules.md`
- `docs/kb/projects/db-chat-nl/structure.md`
- `docs/kb/projects/db-chat-nl/styles.md`
- `docs/kb/projects/db-chat-nl/features.md`

## Next Steps

1. **Database Setup**: Create User model and migrations
2. **Environment Config**: Set up `.env` with JWT secret
3. **Conversation History**: Implement full conversation CRUD
4. **Token Refresh**: Add refresh token mechanism for security
5. **Email Verification**: Add email verification flow (optional)
6. **Password Reset**: Implement password reset flow (optional)
