# Architecture

Minimal architecture for testing authentication feature.

## Layers

**API Layer**:
- auth_routes.py (from authentication feature)

**Service Layer**:
- auth.py (from authentication feature)

**Data Layer**:
- PostgreSQL users table (from authentication feature)

**Configuration**:
- config.py with JWT settings (from authentication feature)
