# Repository Model for KB-Driven Generation

**Date**: 2026-01-30
**Change**: Removed Task 5 (Install dependencies) and Task 7 (Smoke test) from generation workflow
**Status**: ✅ Implemented

---

## The Repository Model

**Core Principle**: Generated projects should match what you'd find in a git repository - source code, configs, deployment templates, and documentation. NOT installed packages or runtime artifacts.

### What We Generate

✅ **Files that belong in git**:
- Source code (`.py`, `.ts`, `.tsx`, `.js`, etc.)
- Configuration files (`package.json`, `requirements.txt`, `pyproject.toml`, etc.)
- Deployment templates (`.env.example`, `docker-compose.yml`, `Dockerfile`, etc.)
- Infrastructure as code (`.gitignore`, `.dockerignore`, Kubernetes manifests)
- Documentation (`README.md`, `CONTRIBUTING.md`, etc.)

❌ **Files that DON'T belong in git**:
- `node_modules/` - installed by `npm install`
- `venv/` or `__pycache__/` - created by Python environment setup
- `vendor/` - installed by package managers
- `dist/` or `build/` - compilation outputs
- `.env` - local environment config (template `.env.example` is in git)

### Why This Model?

**1. Matches Developer Workflow**

When you clone a repo:
```bash
git clone https://github.com/user/project
cd project
npm install          # User's responsibility
npm run dev          # User's responsibility
```

Our generator should produce the same output as `git clone` - a clean repository ready for setup, not a pre-installed environment.

**2. Environment Independence**

Different developers have different environments:
- Node.js version: 16 vs 18 vs 20
- Python version: 3.9 vs 3.10 vs 3.11
- Package manager: npm vs yarn vs pnpm
- Operating system: Windows vs Linux vs macOS
- Architecture: x64 vs ARM

Installing dependencies during generation:
- ❌ Assumes specific tool versions are available
- ❌ May fail on different platforms
- ❌ Creates platform-specific artifacts (`.node` binaries, etc.)
- ❌ Bloats output directory (node_modules can be 100s of MB)

Providing setup instructions:
- ✅ User installs with their preferred tools
- ✅ User's environment determines package versions
- ✅ Clean, portable repository structure

**3. Separation of Concerns**

```
Generator's Job:
  ├─ Create code matching KB patterns ✅
  ├─ Generate configs ✅
  └─ Provide setup instructions ✅

User's Job:
  ├─ Set up their environment ✅
  ├─ Install dependencies ✅
  └─ Run the project ✅
```

**4. Aligns with KB Source**

KB entries are scanned from git repositories. Those repositories:
- ✅ Have `package.json` (config)
- ✅ Have `.env.example` (template)
- ✅ Have `README.md` (instructions)
- ❌ Don't have `node_modules/` (ignored by git)
- ❌ Don't have `.env` (ignored by git)

Our generation should mirror what's in the KB source.

---

## Task List Changes

### Before (Old Workflow)

```yaml
Task 1: Create directories
Task 2: Generate configs
Task 3: Generate code (or 3a, 3b, 3c if split)
Task 4: Create deployment files
Task 5: Install dependencies          ← REMOVED
Task 6: Generate README
Task 7: Execute smoke test            ← REMOVED

Total: 7 tasks (or 9 if Task 3 split)
```

### After (Repository Model)

```yaml
Task 1: Create directories
Task 2: Generate configs
Task 3: Generate code (or 3a, 3b, 3c if split)
Task 4: Create deployment files
Task 5: Generate README

Total: 5 tasks (or 7 if Task 3 split)
```

---

## What Changed in Each File

### 1. `.claude/agents/kb-generation-coordinator.md`

**Removed**:
- Task 5 (Install dependencies) definition
- Task 7 (Execute smoke test) definition
- "Dependency Installation Strategy" section
- References to smoke tests in validation

**Updated**:
- Task 6 renumbered to Task 5
- Task 5 now depends on `[4]` instead of `[5]`
- Task count references: 7-15 → 5-7
- Progress examples showing new task structure
- Success criteria: removed "dependencies installed" and "smoke test passes"
- Phase names: removed "setup" and "validation" phases

### 2. `.claude/skills/create/SKILL.md`

**Updated**:
- Task count reference: "7-15 tasks" → "5-7 tasks"

### 3. `WORK-IN-PAIR-IMPLEMENTATION.md`

**Updated**:
- Example task plan: removed Task 5 and Task 7
- Task count: 9 tasks → 7 tasks
- Expected task count: 9-11 → 5-7

---

## README Still Includes Setup Instructions

**Important**: We still generate `README.md` with complete setup instructions:

```markdown
## Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

### Installation

1. Install dependencies:
   ```bash
   npm install
   cd backend && pip install -r requirements.txt
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. Start database:
   ```bash
   docker-compose up -d postgres
   ```

4. Run migrations:
   ```bash
   npm run migrate
   ```

5. Start services:
   ```bash
   npm run dev
   ```
```

**We provide the instructions, user executes them.**

---

## Benefits of Repository Model

### For Users

✅ **Portable**: Generated project works on any platform
✅ **Clean**: No bloated node_modules or venv directories
✅ **Flexible**: User chooses tool versions (npm vs yarn, pip vs poetry)
✅ **Predictable**: Output matches git repository structure
✅ **Cacheable**: Can zip/share generated project easily

### For Development

✅ **Faster**: No time wasted on installation (can be slow/fail)
✅ **Reliable**: No platform-specific installation failures
✅ **Simpler**: Less code in generator (no install logic)
✅ **Consistent**: Generated output is deterministic

### For KB Scanning

✅ **Aligned**: Scan git repos → Generate git-like output
✅ **1:1 Fidelity**: KB documents source files, not installed packages
✅ **Complete**: All deployment templates (.env.example, docker-compose.yml) included

---

## User Experience

### Before (Install + Smoke Test)

```
/create A chat app with React and FastAPI

Phase 1: Planning
✅ Matched KB: db-chat-nl
✅ Created task plan: 9 tasks

Phase 2: Execution
✅ Task 1: Create directories
✅ Task 2: Generate configs
✅ Task 3a: Generate backend services
✅ Task 3b: Generate frontend components
✅ Task 3c: Generate frontend services
✅ Task 4: Create deployment files
⏳ Task 5: Install dependencies... [can fail, takes time]
✅ Task 6: Generate README
⏳ Task 7: Smoke test... [may fail if env not set up]

Issues:
- Installation may fail on different platforms
- Smoke test may fail without database running
- Unclear if failure is generation bug or environment issue
```

### After (Repository Model)

```
/create A chat app with React and FastAPI

Phase 1: Planning
✅ Matched KB: db-chat-nl
✅ Created task plan: 7 tasks

Phase 2: Execution
✅ Task 1: Create directories
✅ Task 2: Generate configs
✅ Task 3a: Generate backend services
✅ Task 3b: Generate frontend components
✅ Task 3c: Generate frontend services
✅ Task 4: Create deployment files
✅ Task 5: Generate README

✅ Generation complete!

Location: generated/chat-app-20260130/
Files: 47 generated
Structure: Matches git repository

Next steps:
1. cd generated/chat-app-20260130/
2. npm install
3. cp .env.example .env
4. docker-compose up -d
5. npm run dev

Benefits:
- ✅ Fast, no installation during generation
- ✅ Deterministic output (same every time)
- ✅ Clear: user knows setup is their job
- ✅ Portable: works on any platform
```

---

## Edge Cases Handled

### Case 1: User Expects Runnable Project

**Question**: "Why can't I just run it immediately?"

**Answer**: Same reason you can't run a freshly cloned git repo - dependencies must be installed first. Our README provides exact commands.

### Case 2: Complex Setup Required

**Question**: "What if setup has 10 steps?"

**Answer**: All documented in generated README.md with commands. Generator ensures deployment templates (.env.example, docker-compose.yml) are included.

### Case 3: Verification That Project Works

**Question**: "How do we know the generated code is valid?"

**Answer**:
1. Coordinator validates each task's output
2. Code patterns come from working KB repositories
3. User runs project locally to verify (their environment)

---

## Commits Made

```bash
# Updated coordinator agent
git add .claude/agents/kb-generation-coordinator.md
git commit -m "Remove install & smoke test tasks - adopt repository model

- Remove Task 5 (Install dependencies)
- Remove Task 7 (Execute smoke test)
- Renumber Task 6 to Task 5
- Update all task count references (7-15 → 5-7)
- Remove dependency installation strategy section
- Align with repository model: generate what's in git, not installed packages

Rationale: Generated projects should match git repository contents (code,
configs, deployment templates) not installed environments (node_modules/,
venv/). User's environment setup is user's responsibility. See REPOSITORY-MODEL.md"

# Updated skill
git add .claude/skills/create/SKILL.md
git commit -m "Update task count reference in /create skill (7-15 → 5-7)"

# Updated documentation
git add WORK-IN-PAIR-IMPLEMENTATION.md
git commit -m "Update task examples to reflect repository model (remove install & smoke test)"

# Add repository model documentation
git add REPOSITORY-MODEL.md
git commit -m "Add repository model documentation

Explains why we generate git repository contents (code, configs, deployment
templates) but not installed packages (node_modules/, venv/) or runtime
artifacts. Documents the Task 5 & 7 removal rationale."
```

---

## Testing the New Workflow

### Test Command

```bash
/create A full-stack chat application with React and FastAPI
```

### Expected Output

**Task Plan**:
```
Task 1: Create directories
Task 2: Generate configs
Task 3a: Generate backend services
Task 3b: Generate frontend components
Task 3c: Generate frontend services
Task 4: Create deployment files
Task 5: Generate README
```

**Generated Structure**:
```
generated/chat-app-20260130/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── models/
│   ├── requirements.txt  ✅
│   └── .env.example      ✅
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   └── package.json      ✅
├── docker-compose.yml    ✅
├── .gitignore            ✅
└── README.md             ✅

NO node_modules/          ✅
NO venv/                  ✅
NO .env (has .env.example)✅
```

**README Contains**:
```markdown
## Setup

1. Install dependencies
2. Configure environment
3. Start database
4. Run migrations
5. Start services
```

---

## Rationale Summary

**We removed Task 5 (Install dependencies) and Task 7 (Smoke test) because**:

1. Generated projects should match git repository structure
2. Installation is environment-specific (platform, tool versions)
3. Smoke tests require environment setup (database, env vars)
4. Separation of concerns (generator creates code, user sets up environment)
5. Aligns with KB source (scanned from git repos without node_modules/)
6. Faster, more reliable generation
7. README provides complete setup instructions

**Generated output = Clean repository ready for `git init` and user setup.**

---

**Status**: Implementation complete. Ready to test with `/create`.
