---
name: scan
description: Scan a local directory and extract KB documentation using 3-phase workflow
argument-hint: "<local_path> <project_id>"
allowed-tools: Bash, Task, Read, Write
---

You are the `/scan` skill. Execute a **3-phase workflow** to scan repositories and generate KB entries.

## Input

- $ARGUMENTS: The local directory path and project ID (e.g., "/path/to/project project-id")

Parse $ARGUMENTS to extract:
- `repo_path`: First argument (local directory path)
- `project_id`: Second argument (KB entry identifier)

## 3-Phase Workflow

### Phase 1: File Discovery (Script)

Run the file discovery script to classify files:

```bash
python scripts/kb/file_discovery.py <repo_path> --output scratchpad/scan-<project_id>/file-tiers.json
```

This creates:
- `scratchpad/scan-<project_id>/file-tiers.json` with tier1/tier2/tier3 file classifications

Output message:
```
✅ Phase 1 complete: File discovery
📊 File tiers saved to scratchpad/scan-<project_id>/file-tiers.json
```

### Phase 2: Pattern Extraction (Agent)

Call the pattern-extractor agent:

```
Task(
  subagent_type: "pattern-extractor",
  description: "Extract code patterns",
  prompt: "Extract code patterns for project_id: <project_id>, scan_dir: scratchpad/scan-<project_id>"
)
```

This creates:
- `scratchpad/scan-<project_id>/patterns/batch-*.md` files with extracted patterns
- `scratchpad/scan-<project_id>/patterns/module-summary.md`

Output message:
```
✅ Phase 2 complete: Pattern extraction
📁 Patterns saved to scratchpad/scan-<project_id>/patterns/
```

### Phase 3: KB Documentation (Agent)

Call the kb-writer agent:

```
Task(
  subagent_type: "kb-writer",
  description: "Generate KB documentation",
  prompt: "Generate KB files for project_id: <project_id>, scan_dir: scratchpad/scan-<project_id>"
)
```

This creates:
- `docs/kb/projects/<project_id>/meta.yaml`
- `docs/kb/projects/<project_id>/README.md`
- `docs/kb/projects/<project_id>/modules.md`
- `docs/kb/projects/<project_id>/tech.md`
- `docs/kb/projects/<project_id>/architecture.md`
- `docs/kb/projects/<project_id>/deployment.md`
- `docs/kb/projects/<project_id>/uiDescription.md`

Output message:
```
✅ Phase 3 complete: KB documentation
📁 KB entry created at docs/kb/projects/<project_id>/
```

### Final Summary

After all phases complete, output:

```
✅ Scan complete!

📦 Repository: <repo_path>
🆔 Project ID: <project_id>
📁 KB Entry: docs/kb/projects/<project_id>/
📊 7 KB files generated

Next steps:
- Review the KB entry in docs/kb/projects/<project_id>/
- Use /create to generate a new project from this KB entry
```

## Error Handling

If Phase 1 fails:
- Check if repo_path exists
- Check if file_discovery.py script is available
- Report error and stop

If Phase 2 fails:
- Check if file-tiers.json exists
- Report error but continue to Phase 3 if possible

If Phase 3 fails:
- Check if pattern files exist
- Report error

## Example

```
User: /scan c/work/db-chat-nl-master db-chat-nl
```

Your actions:
1. Run file_discovery.py on c/work/db-chat-nl-master
2. Call pattern-extractor agent with project_id=db-chat-nl
3. Call kb-writer agent with project_id=db-chat-nl
4. Report completion

## Notes

- **Execute phases sequentially** - each phase depends on the previous one
- **Clear progress messages** - user should see what's happening
- **File-based handoffs** - phases communicate via files, not memory
- **No freezing** - small batches prevent context overflow
