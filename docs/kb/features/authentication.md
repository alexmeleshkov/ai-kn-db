# Authentication

**Category**: Security / User Management
**Related Projects**: [[db-chat-nl-master]]

---

## Overview

User authentication and session management enabling secure user registration, login, and authorization. Supports stateless and stateful authentication patterns with role-based access control.

**Core Capabilities**:
- User registration and login
- Password security (hashing, salting, validation)
- Session/token management
- Role-based access control (RBAC)
- Protected endpoint authorization
- Logout and session invalidation

---

## Key Concepts

**Authentication**: Verifying user identity (who are you?)
**Authorization**: Verifying permissions (what can you do?)
**Session Management**: Tracking authenticated users across requests
**Password Security**: Hashing, salting, validation rules
**Token-based Auth**: Stateless authentication using signed tokens
**Role-based Access**: Different permissions for user roles (admin, user, etc.)

---

## Common Patterns

### 1. Registration Flow
1. User submits email + password
2. Validate email format and password strength
3. Check if user already exists
4. Hash password with salt
5. Store user in database
6. Generate session/token
7. Return user data + session/token

### 2. Login Flow
1. User submits email + password
2. Find user by email
3. Verify password against stored hash
4. Generate session/token
5. Return user data + session/token

### 3. Authorization Flow
1. Extract session/token from request (header, cookie)
2. Validate session/token (signature, expiration)
3. Extract user identity and roles
4. Check permissions for requested resource
5. Allow/deny access

### 4. Logout Flow
- **Stateful**: Invalidate session in database/cache
- **Stateless**: Client discards token (optional: token blacklist)

---

## Implementation Variants

### Stateless (Token-based)
**Technologies**: [[jwt]], [[oauth2]], [[api-keys]]
- Tokens contain user data (signed, cannot be forged)
- No server-side session storage
- Scalable (no shared session state)
- Logout requires client to discard token (or token blacklist)

### Stateful (Session-based)
**Technologies**: [[session-cookies]], [[redis-sessions]], [[postgresql-sessions]]
- Server stores session data
- Client gets session ID (in cookie)
- Easy to revoke sessions
- Requires shared session store for scaling

---

## Security Considerations

**Password Security**:
- Hash passwords with strong algorithm ([[bcrypt]], [[argon2]], [[scrypt]])
- Use salt per password (prevents rainbow table attacks)
- Enforce minimum password length (8+ characters)
- Never store plain text passwords
- Never log or return passwords in responses

**Token/Session Security**:
- Use HTTPS in production (prevents token interception)
- Set appropriate token expiration (balance UX vs security)
- Validate token signature on every request
- Use secure random secret keys
- Store secrets in environment variables

**API Security**:
- Return generic error messages (prevent email enumeration)
- Use constant-time password comparison (prevent timing attacks)
- Rate limit authentication endpoints (prevent brute force)
- Implement account lockout after failed attempts
- Validate input (SQL injection, XSS prevention)

**Authorization**:
- Verify permissions on every protected endpoint
- Use role/permission checks (not just "is authenticated")
- Implement least privilege principle
- Audit sensitive operations

---

## Frontend Integration

**Login UI**:
- Email and password input fields
- Email validation (format)
- Password visibility toggle
- Loading state during submission
- Clear error messages
- Redirect on success

**Token/Session Storage**:
- localStorage (accessible to JavaScript)
- sessionStorage (cleared on tab close)
- httpOnly cookies (not accessible to JavaScript - more secure)

**Protected API Calls**:
- Include token in Authorization header or cookie
- Handle 401 responses (redirect to login)
- Handle 403 responses (insufficient permissions)
- Auto-refresh tokens before expiration

---

## Related Technologies

**Token Generation**: [[jwt]], [[oauth2]], [[paseto]]
**Password Hashing**: [[bcrypt]], [[argon2]], [[scrypt]]
**Session Storage**: [[redis]], [[postgresql]], [[memcached]]
**Frontend**: [[react-hooks]], [[vue-composables]], [[angular-services]]
**Backend**: [[fastapi]], [[express]], [[django]], [[spring-boot]]

---

## Usage Examples

### Registration API
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}

Response (200):
{
  "user": {
    "id": "1",
    "email": "user@example.com",
    "role": "user"
  },
  "token": "..."
}
```

### Login API
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}

Response (200):
{
  "user": {
    "id": "1",
    "email": "user@example.com",
    "role": "user"
  },
  "token": "..."
}
```

### Protected Endpoint
```
GET /auth/me
Authorization: Bearer <token>

Response (200):
{
  "id": "1",
  "email": "user@example.com",
  "role": "user"
}
```

---

## Decision Factors

**Choose Token-based (Stateless) when**:
- Building microservices or distributed systems
- Need horizontal scaling without shared state
- API-first architecture
- Mobile apps or SPAs
- Cross-domain authentication (CORS)

**Choose Session-based (Stateful) when**:
- Traditional web applications
- Need instant session revocation
- Simpler security model
- Smaller scale (single server or load balancer with sticky sessions)

---

## Testing Patterns

**Unit Tests**:
- Test password hashing and verification
- Test token generation and validation
- Test token expiration
- Test duplicate email registration
- Test wrong password handling

**Integration Tests**:
- Test full registration → login flow
- Test protected endpoint access
- Test token refresh flow
- Test logout and session invalidation

**Security Tests**:
- Test brute force protection
- Test SQL injection prevention
- Test timing attack resistance
- Test password strength enforcement
