# /scan Skill

Scan an existing repository and create a KB entry using the universal scanning system.

## Usage

```bash
/scan <repo-path> [project-id]
```

## Arguments

- `repo-path` (required): Absolute path to the repository to scan
- `project-id` (optional): ID for the KB entry (defaults to repo folder name)

## Examples

```bash
# Scan db-chat-nl reference project
/scan /c/work/db-chat-nl-master db-chat-nl

# Scan a project with auto-generated ID
/scan /path/to/my-project

# Scan and create KB entry
/scan C:\projects\awesome-app awesome-app
```

## What it does

1. Runs the universal scanner with 8 specialized extractors
2. Generates 8 YAML files with structured data
3. Creates markdown documentation (business.md, architecture.md)
4. Validates the KB entry for completeness
5. Outputs results to `docs/kb/projects/<project-id>/`

## Output

The scan creates a complete KB entry with 11 files:
- `meta.yaml` - Project metadata
- `business.md` - Business context
- `architecture.md` - Architecture decisions
- `capability_mapping.yaml` - File-to-feature mapping
- `data_models.yaml` - Entities and schemas
- `dependencies.yaml` - Full dependency catalog
- `external_interfaces.yaml` - HTTP/WebSocket contracts
- `internal_boundaries.yaml` - Subsystem communication
- `runtime_config.yaml` - Environment variables
- `runtime_lifecycle.yaml` - Build/run commands
- `ui_structure.yaml` - Screens and navigation

## Implementation

This skill delegates to the `kb-repo-scanner` agent, which:
- Orchestrates the universal scanning pipeline
- Runs all 8 extractors
- Validates outputs
- Creates human-readable documentation
- Reports any gaps or unknowns
