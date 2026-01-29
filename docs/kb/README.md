# Knowledge Base (KB)

This repository is a knowledge base of **reference projects** used to generate new runnable projects through pure 1:1 generation from KB documentation.

## Folder layout

- `docs/kb/projects/` — reference projects with complete documentation (end-to-end implementations)

## How a reference project is documented

Each project lives in its own folder:
`docs/kb/projects/<project-id>/`

**7 Core KB files** (used for 1:1 generation):
- `meta.yaml` — project metadata, technologies, capabilities (used for matching)
- `modules.md` — **MOST IMPORTANT** — complete module structure with code patterns
- `architecture.md` — architecture patterns, layers, boundaries
- `tech.md` — technology stack, versions, dependencies
- `deployment.md` — deployment configuration (Docker, K8s, etc.)
- `uiDescription.md` — UI structure and component descriptions
- `README.md` — project overview and setup instructions

**Additional documentation**:
- `business.md` — user-facing goal and scenarios
- `features.md` — user-visible features

## Language requirement

All KB documentation, generated code, and code comments must be written in **English**.
