# Technology Stack

> **Purpose**: Document WHAT technologies and WHY they were chosen.
> This file informs package.json/requirements.txt generation and technology decisions.

## Technology Overview

**Architecture**: [Pattern name - e.g., Layered Monolith, Microservices, SPA + API]
**Deployment Model**: [e.g., Containerized, Serverless, Traditional VM]

---

## Backend Technologies

### Core Framework
**[Framework Name]** - [Version requirement if critical]

**Key features used**:
- [Feature 1]
- [Feature 2]
- [Feature 3]
- [Feature 4]

---

### Database & ORM
**[Database Type and Name]** - [Version]

**ORM/Query Builder**: [Name and version if used]
- [Key feature 1]
- [Key feature 2]
- [Key feature 3]

---

### Authentication & Security
**[Library/Approach]** - [Version]

**Purpose**: [Authentication method - e.g., session-based, token-based, OAuth]

**Security approach**:
- [Security measure 1]
- [Security measure 2]
- [Security measure 3]
- [Security measure 4]

---

### External Service Integration
**[Service/API Name]**

**Library**: [Client library name and version]
**[Model/Version used]**: [If applicable]
**Fallback strategy**: [How failures are handled]

---

### Other Backend Dependencies

**[Library Name]** - [Purpose and rationale]

**[Library Name]** - [Purpose and rationale]

**[Library Name]** - [Purpose and rationale]

---

## Frontend Technologies

### Core Framework
**[Framework Name]** - [Version]

**Key features used**:
- [Feature 1]
- [Feature 2]
- [Feature 3]
- [Feature 4]

---

### Language & Type System
**[Language]** - [Version]

**[Config file - e.g., tsconfig] settings**:
- [Setting 1]
- [Setting 2]
- [Setting 3]

---

### Build Tool
**[Tool]** - [Version]

**Key features**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

### UI Component Library
**[Library name or "Custom components"]**

**CSS approach**: [CSS Modules, Tailwind, styled-components, etc.]

---

### State Management
**[Approach]**

**Implementation**:
- [Detail 1]
- [Detail 2]
- [Detail 3]

---

### Data Fetching
**[Approach]**

**Implementation**:
- [Detail 1]
- [Detail 2]
- [Detail 3]

---

### Data Visualization
**[Library]**

**Chart types supported**:
- [Chart type 1]
- [Chart type 2]
- [Chart type 3]

---

### Other Frontend Dependencies

**[Library]** - Purpose
- Example: `date-fns` - Date formatting and manipulation

**[Library]** - Purpose
- Example: `react-router-dom` - Client-side routing

**[Library]** - Purpose
- Example: `axios` - HTTP client with interceptors (if not using fetch)

---

## Infrastructure & DevOps

### Containerization
**[Tool - e.g., Docker]**

**Dockerfile approach**:
- Multi-stage builds for frontend
- Python slim base image for backend
- Layer caching optimization

**Docker Compose** for local development:
- Frontend container
- Backend container
- Database container
- Volumes for persistence

---

### Deployment Platform
**[Platform]**

**Infrastructure as Code**: [Tool or approach]

---

### Environment Management
**Approach**: Environment variables via .env files

**Required variables**:
- `DATABASE_URL`
- `JWT_SECRET`
- `ANTHROPIC_API_KEY`
- `CORS_ORIGINS`

**Config library**: [e.g., python-dotenv, dotenv-webpack]

---

### Monitoring & Logging
**Logging**: [e.g., Python logging module, Winston]

**Approach**:
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error tracking: [Tool name or none]

---

### Testing

**Backend Testing**:
- Framework: [e.g., pytest]
- Coverage tool: [e.g., pytest-cov]
- Test types: Unit, integration

**Frontend Testing**:
- Framework: [e.g., Vitest, Jest]
- Component testing: [e.g., React Testing Library]
- E2E: [e.g., Playwright, Cypress, none]

**CI/CD**: [e.g., GitHub Actions, GitLab CI, none]

---

## Development Tools

### Package Management
**Backend**: [e.g., pip + requirements.txt, Poetry, pipenv]
**Frontend**: [e.g., npm, yarn, pnpm]

### Code Quality
**Linting**:
- Backend: [e.g., pylint, flake8, ruff]
- Frontend: [e.g., ESLint with typescript-eslint]

**Formatting**:
- Backend: [e.g., Black, autopep8]
- Frontend: [e.g., Prettier]

**Type Checking**:
- Backend: [e.g., mypy for type hints]
- Frontend: [e.g., TypeScript compiler]

---

## Security Considerations

**Authentication**: JWT tokens with HTTP-only cookies (or Bearer tokens)
**Password Storage**: bcrypt hashing with salt
**SQL Injection Prevention**: Parameterized queries via ORM
**XSS Prevention**: React escapes by default, sanitize user HTML if rendering
**CORS**: Whitelist specific origins
**Rate Limiting**: [Tool/approach or none]
**Secrets Management**: Environment variables, never committed to repo

---

## Performance Considerations

**Backend**:
- Async I/O for database and API calls
- Connection pooling for database
- Caching strategy: [Approach or none]

**Frontend**:
- Code splitting by route
- Lazy loading for heavy components
- Image optimization
- Bundle size target: [e.g., < 500KB gzipped]

**Database**:
- Indexes on frequently queried columns
- Query optimization for N+1 problems
- Pagination for large result sets

---

## Technology Constraints & Trade-offs

**Known limitations**:
- [Limitation - e.g., SSE not supported in HTTP/1.0]
- [Limitation - e.g., SQLite not suitable for production]

**Scalability bottlenecks**:
- [Bottleneck - e.g., Stateful SSE connections limit horizontal scaling]
- [Mitigation - e.g., Use Redis for session storage if scaling needed]

**Browser compatibility**:
- Target: Modern browsers (Chrome, Firefox, Safari, Edge)
- IE11: Not supported
- Critical APIs: EventSource, fetch, ES6+

---

## Migration & Upgrade Paths

**Database migrations**: [Tool - e.g., Alembic, Flyway, none]
**Frontend versioning**: [Approach - e.g., Semver in package.json]
**API versioning**: [Approach - e.g., /api/v1/ prefix]

**Planned upgrades**:
- [Future change - e.g., React 18 → 19 when stable]
- [Future change - e.g., Consider switching to WebSockets for bidirectional chat]

---

## Dependency Version Strategy

**Backend**:
- Pin major versions, allow minor/patch updates
- Example: `anthropic>=0.40.0,<1.0.0`

**Frontend**:
- Use caret ranges for stability
- Example: `"react": "^18.2.0"`

**Security updates**: Monitor Dependabot/Snyk for vulnerabilities

---
