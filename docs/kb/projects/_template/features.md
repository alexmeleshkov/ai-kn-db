# Project Features

> **NEW FILE**: This file links to reusable features from `docs/kb/features/`

## Feature List

List all features used by this project with links to their documentation.

**Format**:
```markdown
### [Feature Name](../../features/<feature-name>/<variant>.md)

**Capability**: capability_name
**Usage**: Brief description of how this project uses this feature
**Customizations**: Any project-specific modifications
```

## Example

### [JWT + Bcrypt Authentication](../../features/authentication/jwt-bcrypt.md)

**Capability**: user_authentication
**Usage**: Stateless JWT authentication with bcrypt password hashing for user login/register
**Customizations**:
- 1-week token expiration (default: 1 day)
- Admin role support enabled

### [SSE Streaming Chat](../../features/chat/sse-streaming.md)

**Capability**: real_time_data_streaming
**Usage**: Server-Sent Events for streaming LLM responses to frontend
**Customizations**: None

---

## Integration Notes

Describe how features interact with each other in this project:

- Authentication provides user context to Chat service
- Chat service uses Database service for schema introspection
- etc.
