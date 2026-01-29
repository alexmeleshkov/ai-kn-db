# Deployment & Operations

> **Purpose**: Document exact commands to build, run, test, and deploy.
> This enables README generation and smoke test implementation.

## Prerequisites

### System Requirements
- **Operating System**: [requirements]
- **Memory**: [requirement]
- **Disk Space**: [requirement]

### Required Software
- **[Tool]** - [version requirement]
- **[Tool]** - [version requirement]
- **[Tool]** - [version requirement]

### Required Credentials
- **[Service]** - [what's needed and where to get it]
- **[Service]** - [what's needed and where to get it]

---

## Local Development Setup

### 1. Clone & Navigate
```bash
[commands]
```

### 2. Backend Setup
```bash
[commands to install backend dependencies]
```

### 3. Frontend Setup
```bash
[commands to install frontend dependencies]
```

### 4. Database Setup
```bash
[commands to set up database]
```

### 5. Environment Configuration

> **IMPORTANT FOR KB ENTRY CREATORS**: Document ALL environment variables used in the project.
> - Extract from `.env.example`, `.env.template`, or code that reads `process.env` / `os.getenv` / `ENV`
> - Include example values for non-secrets (use placeholders for secrets)
> - Mark required vs optional
> - Explain where to obtain API keys/credentials

Create `.env` file in project root with required variables:

```bash
cp .env.example .env
# Edit .env with your actual values
```

**Environment Variables**:

| Variable | Required | Default | Description | Where to Get |
|----------|----------|---------|-------------|--------------|
| `[VAR_NAME]` | ✅ Yes | - | [Purpose and usage] | [Source: e.g., "OpenAI Dashboard"] |
| `[VAR_NAME]` | ⚠️ Optional | `[default]` | [Purpose] | - |
| `[VAR_NAME]` | ✅ Yes | - | [Purpose] | [Source] |

**Example `.env` file**:
```bash
# === API Keys & Secrets ===
[VAR_NAME]=[example_value_or_your-key-here]
[VAR_NAME]=[example_value]

# === Database Configuration ===
[DB_VAR]=[example_value]
[DB_VAR]=[example_value]

# === Application Settings ===
[APP_VAR]=[example_value]
[APP_VAR]=[example_value]

# === Optional Features ===
[OPTIONAL_VAR]=[example_value]
```

**Security Notes**:
- Never commit `.env` to version control
- `.env` is in `.gitignore`
- Use `.env.example` as template (with no real secrets)
- Rotate keys regularly for production

---

## Running the Application

### Development Mode

**Option 1: Run services separately**
```bash
# Terminal 1: Backend
[backend run command]

# Terminal 2: Frontend
[frontend run command]
```

**Option 2: Docker Compose**
```bash
[docker-compose command]
```

**Access**: [URLs for frontend and backend]

---

### Production Mode

```bash
[production build and run commands]
```

---

## Building

### Frontend Build
```bash
[build commands]
```

**Output**: [build artifacts location]

### Backend Build
```bash
[build commands if applicable]
```

---

## Testing

### Smoke Test
**Purpose**: Verify project builds and runs

```bash
[smoke test command]
```

**Expected output**:
```
[what success looks like]
```

### Unit Tests
```bash
# Backend
[backend test command]

# Frontend
[frontend test command]
```

### Integration Tests
```bash
[integration test commands if applicable]
```

---

## Database Management

### Migrations

**Create migration**:
```bash
[migration creation command]
```

**Apply migrations**:
```bash
[migration apply command]
```

**Rollback**:
```bash
[rollback command]
```

### Seeding Data
```bash
[seed command if applicable]
```

---

## Deployment

### [Platform 1]
```bash
[deployment commands for this platform]
```

### [Platform 2]
```bash
[deployment commands for this platform]
```

---

## Monitoring & Maintenance

### Health Checks
```bash
[health check command]
```

**Expected response**: [expected output]

### Logs
```bash
[log viewing commands]
```

---

## Troubleshooting

### Issue: [Common Problem 1]
```bash
[diagnosis command]
[fix command]
```

### Issue: [Common Problem 2]
```bash
[diagnosis command]
[fix command]
```

---

## Cleanup

```bash
[cleanup commands to stop services and remove artifacts]
```

---
