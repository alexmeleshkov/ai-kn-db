---
name: kb-repo-scanner
description: "[DEPRECATED] Use pattern-extractor + kb-writer instead"
tools: Read, Bash, Glob, Write, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
---

# ⚠️ DEPRECATED: KB Repository Scanner

**This agent is DEPRECATED. Use the new 3-phase workflow instead:**

1. **Phase 1**: Run `scripts/kb/file_discovery.py` script
2. **Phase 2**: Call `pattern-extractor` agent
3. **Phase 3**: Call `kb-writer` agent

See `.claude/skills/scan/SKILL.md` for the updated workflow.

**Why deprecated?**
- Single agent tried to do too much
- Context overflow on large repositories
- Frequent freezing during execution
- Poor separation of concerns

**New approach benefits:**
- Clear phase boundaries
- File-based handoffs (no context overflow)
- Each agent has single responsibility
- Better progress visibility
- More reliable execution

---

# Original Documentation (for reference only)

Generate complete Knowledge Base entry from repository using a **task-based workflow**.

## Input Parameters

```
repo_path: Path to repository to scan (e.g., "C:/work/db-chat-nl-master")
project_id: KB entry identifier (e.g., "db-chat-nl")
```

## Workflow Overview

This agent uses a structured task-based approach:
1. **Create tasks** for each step of the scan
2. **Work through tasks** one by one
3. **Mark complete** when done
4. **No open-ended exploration** - every action is tied to a task

## Phase 1: Initialize Task List

On first invocation, create the following tasks using TaskCreate:

### Task 1: Run file discovery
- **Subject**: "Run file discovery script"
- **Description**: Run `python scripts/kb/file_discovery.py <repo_path> --output .claude/tmp/kb-extraction/file_manifest.json` to classify files into tier1/tier2/tier3
- **ActiveForm**: "Running file discovery"
- **Done when**: file_manifest.json exists

### Task 2: Read manifest and plan modules.md
- **Subject**: "Analyze manifest and plan module extraction batches"
- **Description**: Read .claude/tmp/kb-extraction/file_manifest.json and determine how many batches needed for tier1+tier2 files (8 files per batch). Create sub-tasks for each batch.
- **ActiveForm**: "Analyzing manifest"
- **Done when**: Module extraction batch tasks created

### Task 3: Generate meta.yaml
- **Subject**: "Generate meta.yaml"
- **Description**: Read template from docs/kb/projects/_template/meta.yaml, read manifest + package files, write docs/kb/projects/<project-id>/meta.yaml
- **ActiveForm**: "Generating meta.yaml"
- **Done when**: meta.yaml file exists

### Task 4: Generate README.md
- **Subject**: "Generate README.md"
- **Description**: Read template from docs/kb/projects/_template/README.md, read repo README, write docs/kb/projects/<project-id>/README.md
- **ActiveForm**: "Generating README.md"
- **Done when**: README.md file exists

### Task 5: Generate tech.md
- **Subject**: "Generate tech.md"
- **Description**: Read template from docs/kb/projects/_template/tech.md, read package.json/requirements.txt/go.mod, write docs/kb/projects/<project-id>/tech.md
- **ActiveForm**: "Generating tech.md"
- **Done when**: tech.md file exists

### Task 6: Generate deployment.md
- **Subject**: "Generate deployment.md"
- **Description**: Read template from docs/kb/projects/_template/deployment.md, read docker-compose.yml/.env.example/Dockerfile, write docs/kb/projects/<project-id>/deployment.md
- **ActiveForm**: "Generating deployment.md"
- **Done when**: deployment.md file exists

### Task 7: Generate architecture.md
- **Subject**: "Generate architecture.md"
- **Description**: Read template from docs/kb/projects/_template/architecture.md, infer from code structure, write docs/kb/projects/<project-id>/architecture.md
- **ActiveForm**: "Generating architecture.md"
- **Done when**: architecture.md file exists

### Task 8: Generate uiDescription.md
- **Subject**: "Generate uiDescription.md"
- **Description**: Read template from docs/kb/projects/_template/uiDescription.md, analyze UI structure, write docs/kb/projects/<project-id>/uiDescription.md
- **ActiveForm**: "Generating uiDescription.md"
- **Done when**: uiDescription.md file exists

### Task 9: Verify completion
- **Subject**: "Verify all 7 KB files exist"
- **Description**: Run `ls docs/kb/projects/<project-id>/ | wc -l` and verify output is 7
- **ActiveForm**: "Verifying completion"
- **Done when**: 7 files confirmed

**After creating tasks, set up dependencies**:
- Task 2 blocked by Task 1 (need manifest first)
- Task 3-8 blocked by Task 2 (need manifest analysis)
- Module batch tasks (created in Task 2) blocked by Task 2
- Task 9 blocked by all file generation tasks

## Phase 2: Execute Tasks

Use TaskList to find next available task (status=pending, no blockedBy).

For each task:
1. **TaskUpdate** to mark as in_progress
2. **Execute** the task following its description
3. **TaskUpdate** to mark as completed
4. **TaskList** to find next task

### Important: Task 2 Special Handling

Task 2 creates dynamic sub-tasks for modules.md batches:

1. Read manifest to get tier1 + tier2 files
2. Group into batches of 8 files each
3. Create tasks like:
   - "Extract module patterns (batch 1/N)"
   - "Extract module patterns (batch 2/N)"
   - etc.
4. Create final task: "Assemble modules.md from all batches"
5. Set dependencies so batches run in order
6. Mark Task 2 as completed

### Module Batch Tasks

Each batch task:
- Reads 8 source files from its batch
- Extracts code patterns (full implementation for tier1, signatures for tier2)
- Writes patterns to temporary file `.claude/tmp/kb-extraction/modules_batch_<N>.md`
- Marks task as completed

Final assembly task:
- Reads all batch files
- Reads template from docs/kb/projects/_template/modules.md
- Combines: file tree + all batch patterns
- Writes docs/kb/projects/<project-id>/modules.md
- Marks task as completed

## Pattern Extraction Rules

**For tier1 files** (services, components, routes):
- Extract complete implementation with actual names
- Show full code structure (no line limits)
- No comments in code blocks
- Include imports, error handling, state management

**For tier2 files** (utils, helpers):
- Extract key functions with signatures
- Keep actual names and parameters
- Show usage patterns

**For tier3 files** (configs):
- Extract dependencies, versions, environment variables
- Note build/run commands

## Memory Management

- Read files in small batches (8 files max at a time)
- Write batch results to temp files immediately
- Don't try to hold all patterns in memory

## Done When

Task 9 (verification) completes successfully:
- ✅ All 7 KB files exist in `docs/kb/projects/<project-id>/`
- ✅ modules.md has patterns for ALL tier1 + tier2 files from manifest

Report completion:
```
✅ KB entry created: docs/kb/projects/<project-id>/
📊 7/7 files generated
📁 <N> module patterns extracted
```

## Key Principles

1. **Every action is part of a task** - No work outside the task system
2. **Small, focused tasks** - Each task does ONE thing
3. **Clear completion criteria** - Know when a task is done
4. **Sequential execution** - Work through tasks in order
5. **No looping** - If stuck, mark task as blocked and move on
