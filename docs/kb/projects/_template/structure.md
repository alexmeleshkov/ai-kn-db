# Project Structure: [Project Name]

## Directory Tree

```
project-root/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py              # Main API routes
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py              # Configuration management
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── [service_files]        # Business logic services
│   │   └── main.py                    # Application entry point
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Backend container definition
│   └── .env.example                   # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── [components]           # React components
│   │   ├── hooks/
│   │   │   └── [hooks]                # Custom React hooks
│   │   ├── services/
│   │   │   └── api.ts                 # API client
│   │   ├── types/
│   │   │   └── [types]                # TypeScript type definitions
│   │   ├── styles/
│   │   │   └── index.css              # Global styles
│   │   ├── App.tsx                    # Root component
│   │   └── main.tsx                   # React entry point
│   ├── public/
│   │   └── [assets]                   # Static assets
│   ├── index.html                     # HTML entry point
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── vite.config.ts                 # Build tool configuration
│   └── Dockerfile                     # Frontend container definition
├── docker-compose.yml                 # Multi-container orchestration
└── README.md                          # Project documentation
```

## File Categorization

### Core Files (Always Present)

| File | Purpose | Modifiable |
|------|---------|------------|
| `backend/app/main.py` | FastAPI application entry, CORS, route registration | Yes - add route imports |
| `backend/app/core/config.py` | Environment variable configuration | Yes - add new settings |
| `frontend/src/App.tsx` | React root component, routing setup | Yes - add routes |
| `frontend/src/main.tsx` | React application entry point | Rarely |
| `frontend/src/styles/index.css` | Global styles and CSS variables | Yes - extend variables |

### Capability-Specific Files

Document files that belong to specific capabilities:

| Capability | Files | Must Coexist |
|------------|-------|--------------|
| `[capability_name]` | `backend/app/api/[routes].py`, `backend/app/services/[service].py`, `frontend/src/components/[Component].tsx`, `frontend/src/hooks/[useHook].tsx` | Yes/No - explain dependencies |

### Configuration Files (Generator Must Modify)

| File | When to Modify |
|------|----------------|
| `backend/requirements.txt` | Add Python dependencies for enabled capabilities |
| `frontend/package.json` | Add Node dependencies for enabled capabilities |
| `backend/.env.example` | Add environment variables for enabled capabilities |
| `docker-compose.yml` | Add service definitions if needed |

## Integration Points

### Adding New Capabilities

Document how to integrate new features into the existing structure:

1. **Backend Integration**:
   - Add route file to `backend/app/api/`
   - Add service file to `backend/app/services/`
   - Import router in `backend/app/main.py`:
     ```python
     from app.api.[feature]_routes import router as [feature]_router
     app.include_router([feature]_router, prefix="/api/v1/[feature]", tags=["[feature]"])
     ```
   - Add dependencies to `requirements.txt`
   - Add environment variables to `.env.example`

2. **Frontend Integration**:
   - Add component files to `frontend/src/components/`
   - Add hook files to `frontend/src/hooks/`
   - Update `App.tsx` routing or context providers
   - Add dependencies to `package.json`

### File Dependencies Graph

```
[Document major file relationships]
Example:
main.py
  ├─> routes.py ────> service.py
  └─> config.py

App.tsx
  ├─> Component.tsx ─> useHook.ts ─> api.ts
  └─> OtherComponent.tsx
```

## Naming Conventions

**Backend**:
- Route files: `[feature]_routes.py`
- Service files: `[feature].py`
- API prefix: `/api/v1/[feature]/`
- Python modules: snake_case

**Frontend**:
- Components: PascalCase (e.g., `ComponentName.tsx`)
- Hooks: camelCase with "use" prefix (e.g., `useFeatureName.tsx`)
- Types: PascalCase interfaces (e.g., `TypeName`)
- Utilities: camelCase (e.g., `utilityFunction.ts`)

## Build and Deployment

### Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up --build
```

### Production
[Document production build and deployment steps if applicable]

## Evidence

[Reference source files or documentation used to create this structure map]
