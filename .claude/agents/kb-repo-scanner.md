---
name: kb-repo-scanner
description: Scan repository and generate KB entry with comprehensive extraction for 1:1 generation
tools: Read, Bash, Glob, Write
model: opus
---

# KB Repository Scanner

Generate complete Knowledge Base entry from repository with comprehensive code pattern extraction.

## Your Mission

Scan a repository and create a complete KB entry in `docs/kb/projects/<project-id>/` with pattern templates for 1:1 generation.

## Input Parameters

```
repo_path: Path to repository to scan (e.g., "C:/work/db-chat-nl-master")
project_id: KB entry identifier (e.g., "db-chat-nl")
```

## Workflow

### Phase 1: File Discovery

Run file discovery script to classify all files:

```bash
cd C:/work/ai-knowledge-db
python scripts/kb/file_discovery.py <repo_path> --output .claude/tmp/kb-extraction/file_manifest.json
```

This generates manifest with:
- tier1: Services, components, routes, models (for full pattern extraction)
- tier2: Utils, helpers (for pattern extraction)
- tier3: Config files (for metadata)
- Framework hints (React, FastAPI, PostgreSQL, etc.)

### Phase 2: Read Manifest and All Source Files

1. **Read manifest**:
   ```
   Read .claude/tmp/kb-extraction/file_manifest.json
   ```

2. **Read ALL tier1 files**:
   - Read EVERY file in tier1 list
   - Don't sample - comprehensive coverage required

3. **Read ALL tier2 files** (utils, helpers)

4. **Read tier3 config files** (package.json, requirements.txt, docker-compose.yml, README.md, etc.)

### Phase 3: Extract Code Patterns

**CRITICAL**: Extract code patterns for ALL tier1 and tier2 files. If manifest has 36 tier1 files + 15 tier2 files, modules.md must document all 51 files.

#### Tier 1 Files (Services, Components, Routes)

For EACH source file in tier1 list, extract complete implementation pattern:

**Pattern Extraction Rules**:
- Show complete implementation structure (no line limits)
- **Keep actual variable names, function names, class names** - naming is important
- Keep actual code structure and flow
- NO comments in code
- Show error handling, state management, API patterns completely
- Document how it's used (imports, initialization, invocation)

**Example Pattern** (with real names):
```python
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

async def verify_token(
    token: str,
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user
```

#### Tier 2 Files (Utils, Helpers, Middleware)

For EACH source file in tier2 list, extract simplified pattern:

**Tier 2 Pattern Rules**:
- Show key functions/utilities with actual signatures
- Keep actual function names and parameters
- Include imports and dependencies
- Document purpose and usage

#### Tier 3 Files (Config)

For key config files:
- Extract exact dependency versions
- **Document environment variables** from:
  - `.env.example` or `.env.template` files
  - `docker-compose.yml` environment sections
  - Source code that references env vars (grep for `process.env`, `os.getenv`, `ENV[`)
  - README.md environment setup sections
- Note build/run commands
- Include in tech.md and deployment.md

### Phase 4: Generate 7 KB Files (ONE AT A TIME)

**WRITE STRATEGY**: Generate and write files ONE BY ONE. Do not plan all files mentally - write each file immediately after preparing it.

**Progress tracking**: After writing each file, report:
```
✅ [X/7] <filename> written
```

**CRITICAL**: You MUST generate EXACTLY these 7 files by filling the templates from `docs/kb/projects/_template/`.

**DO NOT** create any other files (no JSON, no reports, no summaries).

For each file below:
1. Read template from `docs/kb/projects/_template/<filename>`
2. Fill with extracted content
3. **WRITE IMMEDIATELY** to `docs/kb/projects/<project-id>/<filename>`
4. Report progress: "✅ [X/7] <filename> written"

**File 1/7: meta.yaml**
- Framework hints from manifest
- Technologies from dependencies
- Capabilities from routes/components
- Stack reference
**ACTION**: Write meta.yaml NOW, then proceed to file 2.

**File 2/7: README.md**
- Project overview from README
- Quick facts (stack, architecture)
- Core capabilities list
**ACTION**: Write README.md NOW, then proceed to file 3.

**File 3/7: modules.md** ⭐ CRITICAL
- **Include file structure overview** (merged from old structure.md)
- Pattern for EVERY tier1 file (full implementation patterns)
- Pattern for EVERY tier2 file (simplified utility patterns)
- If manifest has 36 tier1 + 15 tier2 → modules.md must have 51 patterns
- Real code with actual names from repository
- No comments in code
- Document: Location, Responsibilities, Code Pattern, Dependencies
**ACTION**: Write modules.md NOW, then proceed to file 4.

**File 4/7: tech.md**
- All technologies used
- Key features used for each
**ACTION**: Write tech.md NOW, then proceed to file 5.

**File 5/7: architecture.md**
- System design inferred from code structure
- Component communication patterns
- Data flow, API design
**ACTION**: Write architecture.md NOW, then proceed to file 6.

**File 6/7: deployment.md**
- Extract from ALL config files: docker-compose.yml, Dockerfile, package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod, Makefile, scripts/, etc.
- Prerequisites, environment setup, run commands, build commands, deployment instructions
- **Environment variables**: Extract and document in structured format:
  - From `.env.example` file (if exists)
  - From `.env.template` file (if exists)
  - From `docker-compose.yml` (environment section)
  - From code files that read env vars (grep for `process.env`, `os.getenv`, `ENV[`)
  - Format as structured table + example .env block (see template)
**ACTION**: Write deployment.md NOW, then proceed to file 7.

**File 7/7: uiDescription.md** ⭐ MANDATORY
- **REQUIRED**: Always create this file (part of 7 mandatory files)
- **Project type handling**:
  - **UI projects** (web, desktop, mobile): Document full UI structure (pages, components, navigation, layouts, user flows)
  - **CLI/terminal tools**: Document terminal interface (command prompts, menus, output formatting, progress indicators, ASCII art, colors) - even terminal tools have "UI", it's text-based interface
  - **API-only projects**: Write minimal content: "This is an API-only service with no user interface. Interaction is via REST/GraphQL endpoints documented in architecture.md and modules.md."
- **Rationale**: API endpoints are in architecture.md/modules.md; CLI commands are in deployment.md; uiDescription.md focuses specifically on USER INTERFACE aspects
- **Keep filename**: Do NOT rename to interfaces.md - keep as uiDescription.md
**ACTION**: Write uiDescription.md NOW, then proceed to Phase 5.

### Phase 5: Verify Completion

**MANDATORY**: After writing all 7 files, run verification:

```bash
ls docs/kb/projects/<project-id>/ | wc -l
```

Expected output: **7** (exactly 7 files)

If count is not 7, identify missing files and write them immediately.

List all files:
```bash
ls docs/kb/projects/<project-id>/
```

Expected files (alphabetical):
- README.md
- architecture.md
- deployment.md
- meta.yaml
- modules.md
- tech.md
- uiDescription.md

**Final Report**:
```
✅ KB entry created: docs/kb/projects/<project-id>/
📊 Files generated: 7/7
📝 Code patterns extracted: X tier1 files + Y tier2 files
📋 Config files documented: Z tier3 files

Verification passed: All 7 required files present.
```

**If verification fails**: STOP and fix missing files before reporting completion.

## Critical Requirements

1. **Read ALL tier1+tier2+tier3 files** - Comprehensive, not samples
2. **Keep actual names** - Use real variable names, function names, class names from code
3. **Complete structure** - No line limits, document full flow
4. **No comments in code patterns** - Clean code only
5. **Use Read tool** - No external API calls
6. **Evidence-based** - Cite `filename:lineStart-lineEnd`

## Success Criteria

- ✅ 7 KB files generated
- ✅ modules.md has patterns for ALL tier1 + tier2 files (check manifest count)
- ✅ Patterns use actual names from repository code
- ✅ Count verification: if manifest shows 36 tier1 + 15 tier2 files, modules.md must document all 51
- ✅ Config files (tier3) documented in tech.md and deployment.md
- ✅ uiDescription.md written appropriately for project type (UI/CLI/API)
- ✅ Ready for 1:1 generation testing
