# Auth Pilot Test Project

Minimal test project to validate feature-based generation with authentication only.

## Purpose

Test that the new feature-based KB structure can generate working code from a single feature (authentication/jwt-bcrypt).

## Features

- JWT + bcrypt authentication (from features/)
- No custom code

## Expected Output

Should generate:
- backend/app/api/auth_routes.py
- backend/app/services/auth.py
- backend/app/core/config.py
- backend/app/models/database.py (user model)
- backend/app/main.py (minimal entry point)
- backend/requirements.txt
