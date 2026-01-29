# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI knowledge database repository with a KB-driven project generator. The system stores project templates, patterns, and best practices, then generates new projects based on user descriptions.

## Development Commands

### Generate a New Project

Use the `/create` skill to generate a new project from the knowledge base:

```
/create <project description>
```

Example:
```
/create A chat app where users can query SQL databases in natural language
```

This command:
1. Matches your description to the best KB project template
2. Scaffolds the project using the appropriate technology stack
3. Creates a runnable project in `generated/<slug>-<timestamp>/`

### Scan an Existing Project

Use the `/scan` skill to scan a repository and create a KB entry:

```
/scan <repo-path> [project-id]
```

Example:
```
/scan /c/work/db-chat-nl-master db-chat-nl
```

This command:
1. Runs universal scanner with 8 specialized extractors
2. Generates structured YAML documentation
3. Creates markdown files (business.md, architecture.md)
4. Validates KB entry completeness
5. Outputs to `docs/kb/projects/<project-id>/`

### Direct Script Usage

You can also call the generator script directly:

```bash
./scripts/new-project "Your project description"
```

Or with environment variable:
```bash
PROJECT_PROMPT="Your project description" ./scripts/new-project
```

## Architecture

### KB-Driven Generator Pipeline

The project uses a multi-phase generation approach:

1. **KB (Knowledge Base)**: Stores project templates in `docs/kb/projects/`
2. **Match**: Token-based matching selects the best KB entry for user requirements
3. **Scaffold**: Technology stacks (`docs/kb/stacks/`) define CLI commands and templates
4. **Output**: Generated project ready to run

**Note**: The current generator (v1) uses generic scaffolding. Phase 2 will implement 1:1 generation from detailed KB documentation (architecture.md, modules.md, etc.).

### Key Components

- `scripts/kb/generate_from_kb.py` - Core generator (matching, scaffolding) [v1 - will be rewritten]
- `scripts/kb/scan_repo_universal.py` - Universal KB scanner with 8 specialized extractors
- `scripts/kb/extract_*.py` - 8 specialized extractors for KB documentation
- `scripts/kb/validate_kb.py` - KB validation script
- `scripts/new-project` - Bash wrapper for the generator
- `docs/kb/projects/*/meta.yaml` - KB project metadata
- `docs/kb/stacks/*/stack.yaml` - Stack definitions with scaffold steps

### Agents & Skills

- `.claude/agents/project-creator.md` - Orchestrates project generation workflow
- `.claude/skills/create/SKILL.md` - Entry point for `/create` command
- `.claude/skills/scan/SKILL.md` - Entry point for `/scan` command
- `.claude/agents/kb-repo-scanner.md` - Scans repositories and creates KB entries
- `.claude/agents/kb-project-writer.md` - Writes KB documentation
- `.claude/agents/generator-engineer.md` - Implements generator pipeline features
- `.claude/agents/tech-lead.md` - Coordinates architecture and planning

## Key Conventions

### Repository Structure

```
docs/kb/
├── projects/           # Reference projects with rich documentation
│   ├── _template/      # Template for new KB entries
│   └── <project-id>/   # Individual projects
│       ├── meta.yaml   # Project metadata, capabilities, stack reference
│       ├── business.md # Business context and requirements
│       ├── architecture.md
│       ├── modules.md
│       ├── tech.md
│       ├── features.md
│       └── styles.md
│       ├── capability_mapping.yaml
│       ├── data_models.yaml
│       ├── dependencies.yaml
│       ├── external_interfaces.yaml
│       ├── internal_boundaries.yaml
│       ├── runtime_config.yaml
│       ├── runtime_lifecycle.yaml
│       └── ui_structure.yaml
└── stacks/            # Technology stack definitions
    └── <stack-id>/
        ├── stack.yaml  # Scaffold steps, smoke tests
        └── templates/  # Template files to copy
```

### Generated Projects

Generated projects are created in `generated/<slug>-<timestamp>/` with:
- Full scaffolded application structure
- README with run instructions
- Docker Compose setup (for applicable stacks)

### Evidence-Driven Development

When documenting or analyzing reference repositories:
- Every non-trivial claim must cite: `filename:lineStart-lineEnd`
- If evidence cannot be found, mark it under "Unknowns"
- Never make assumptions about implementation details

## Language rule

All documentation in `docs/`, all generated code, and all code comments must be written in English.
