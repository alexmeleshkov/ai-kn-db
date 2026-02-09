# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI knowledge database repository structured as a **knowledge graph**. The system stores project documentation, patterns, and best practices organized by relationships between features, technologies, languages, and projects.

**Current Focus**: Knowledge graph navigation and querying via the Explanator Agent.

**Future Goal**: KB-driven project generation (not currently implemented).

## Knowledge Graph Structure

```
Business Goal → Projects → Features + Technologies
                             ↓
                   Language × Technology = Code Snippets
```

**Entity Types**:
- **features/** - Abstract, code-agnostic capabilities (authentication, data-streaming)
  - **features/ui/** - Visual layouts and UI patterns (chat-interface, sidebar-navigation)
- **technologies/** - Specific implementations (jwt, fastapi, postgresql)
- **languages/** - Programming languages (python, typescript, css) with code snippets
- **projects/** - Reference implementations demonstrating features + technologies
- **business-goals/** - Business objectives and requirements
- **insights/** - Project-specific learnings and decisions
- **people/** - Team expertise profiles

## Using the Knowledge Base

### Query the KB

The **Explanator Agent** helps navigate the knowledge graph and answer questions:

**Examples**:
- "What technologies should I use for authentication?"
- "Show me a project using PostgreSQL and FastAPI"
- "How does data streaming work?"
- "What's the difference between JWT and session-based auth?"

Claude will automatically invoke the Explanator Agent when you ask questions about technologies, features, or projects.

### Generate a New Project (Future)

Use the `/create` skill to generate a new project from the knowledge base:

```
/create <project description>
```

**Note**: Code generation is not the current focus. The KB is optimized for navigation and understanding.

## Architecture

### Knowledge Graph Design

**Principles**:
1. **Features** describe WHAT (user capabilities) - code-agnostic
2. **Technologies** describe HOW (specific implementations)
3. **Languages** contain code snippets (Language × Technology)
4. **Projects** demonstrate features + technologies working together

**Example Flow**:
1. User asks: "How to implement authentication?"
2. Explanator reads `features/authentication.md` (abstract patterns)
3. Shows technology options: JWT (stateless) vs Session cookies (stateful)
4. Links to `technologies/jwt.md` and `technologies/bcrypt.md`
5. Shows reference project: `projects/db-chat-nl-master`
6. Points to code snippets: `languages/python/snippets/fastapi-jwt-auth.md`

### Key Components

**KB Documentation**:
- `docs/kb/` - Complete knowledge graph
- `docs/kb/README.md` - KB structure documentation
- `docs/kb/projects/*/meta.yaml` - Project metadata, technologies, capabilities
- `docs/kb/features/*.md` - Abstract feature documentation
- `docs/kb/technologies/*.md` - Technology-specific implementation guides
- `docs/kb/languages/*/snippets/*.md` - Code examples (Language × Technology)

### Agents

**Knowledge Navigation**:
- `.claude/agents/user-guide.md` - Navigates KB to answer questions about features, technologies, and projects

## Key Conventions

### Repository Structure

```
docs/kb/
├── projects/              # Reference projects
│   ├── _template/         # Template for new KB entries
│   └── <project-id>/      # Individual projects
│       ├── meta.yaml      # Metadata, capabilities, technologies
│       ├── architecture.md # Directory tree, architecture decisions, WHY
│       ├── features.md    # Links to backend feature documentation
│       ├── ui-features.md # Links to UI feature documentation
│       └── tech.md        # Links to technology documentation
├── features/              # Abstract, code-agnostic capabilities
│   ├── authentication.md  # Backend features (system capabilities)
│   ├── data-streaming.md
│   ├── ui/                # UI features (visual layouts)
│   │   ├── chat-interface.md
│   │   ├── sidebar-navigation.md
│   │   └── ...
│   └── ...
├── technologies/          # Specific implementations
│   ├── jwt.md
│   ├── fastapi.md
│   ├── postgresql.md
│   └── ...
├── languages/             # Programming languages with code snippets
│   ├── python/
│   │   ├── snippets/      # Python code examples (Language × Technology)
│   │   └── python.md
│   ├── typescript/
│   │   ├── snippets/      # TypeScript code examples
│   │   └── typescript.md
│   └── ...
├── business-goals/        # Business objectives and requirements
├── insights/              # Project-specific learnings
│   └── <project-id>/
│       └── *.md           # Architecture decisions, performance insights
└── people/                # Team expertise profiles
```

### KB Project Documentation

Each project in the KB contains:
- **meta.yaml** - Metadata, technologies used, capabilities implemented
- **architecture.md** - Directory tree, architecture decisions, WHY choices were made
- **features.md** - Links to abstract feature documentation
- **tech.md** - Links to technology-specific documentation

Code patterns are stored separately in:
- **languages/\*/snippets/** - Reusable code examples organized by Language × Technology

### Documentation Principles

When creating or updating KB documentation:
- **Features** are code-agnostic (describe WHAT, not HOW)
- **Technologies** are implementation-specific (describe HOW)
- **Code snippets** live in languages/, not in project or technology docs
- **Architecture** documents WHY decisions were made, not just what exists
- All documentation must be in English

## Language rule

All documentation in `docs/`, all generated code, and all code comments must be written in English.
