# Knowledge Base (KB)

This repository is a knowledge base of **reference projects**, **patterns**, and **stacks** used to generate new runnable projects "from scratch" while reusing proven architecture and decisions.

## Folder layout

- `docs/kb/projects/` — reference projects (end-to-end implementations)
- `docs/kb/patterns/` — reusable architectural/functional building blocks (auth, logging, i18n, etc.)
- `docs/kb/stacks/` — technology stacks (Next/React/Vite + backend + DB combinations)

## How a reference project is documented

Each project lives in its own folder:
`docs/kb/projects/<project-id>/`

Minimum required files:
- `meta.yaml` — structured metadata used for matching and composition
- `business.md` — user-facing goal and scenarios
- `architecture.md` — folder structure + key design decisions
- `modules.md` — core modules and responsibilities
- `tech.md` — technologies and why/how they are used
- `features.md` — user-visible features

## Language requirement

All KB documentation, generated code, and code comments must be written in **English**.
