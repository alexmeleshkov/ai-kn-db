# Deployment

Minimal deployment for auth testing.

## Environment Variables

```.env
DATABASE_URL=postgresql://user:pass@localhost:5432/testdb
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168
```

## Run Locally

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run server
python backend/app/main.py
```

Server runs on http://localhost:8000
