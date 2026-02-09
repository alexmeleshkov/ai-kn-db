---
name: create
description: Generate a new project using the KB-driven project generator. Provide a description of the project you want to create.
argument-hint: "<project description>"
allowed-tools: Task, Read, Bash, TaskCreate, TaskUpdate
---

You are the `/create` skill orchestrator. You coordinate between gen-coordinator (planning), specialized code generators (gen-backend, gen-frontend), and gen-validator to generate a complete project.

## Input

- $ARGUMENTS: The project description provided by the user

## Workflow

### Phase 1: Planning (Spawn Coordinator)

**Step 1**: Spawn gen-coordinator for planning:

```
Task(
  subagent_type: "gen-coordinator",
  description: "Match KB and create task plan",
  prompt: "Match the best KB project for this description and create a task plan (DO NOT execute tasks):

User description: $ARGUMENTS

Your job:
1. Match KB project using token-based matching
2. Create output directory: generated/<slug>-<timestamp>/
3. Count modules and determine task split strategy
4. Write task plan to .claude/tmp/generation-tasks.yaml
5. Create progress tasks using TaskCreate
6. STOP - Return to skill (do NOT execute tasks, do NOT generate code)

Return the following:
- Matched KB project ID
- Output directory path
- Task plan file path (.claude/tmp/generation-tasks.yaml)
- Total number of tasks to execute"
)
```

**Step 2**: Read the task plan file returned by coordinator:
```
Read .claude/tmp/generation-tasks.yaml
```

### Phase 2: Execution (Specialized Generators + Validator Working in Pair)

For each task in the task plan (typically 5-7 tasks depending on Task 3 splitting):

**Step 3**: Update task status to in_progress:
```
TaskUpdate(taskId: N, status: "in_progress")
```

**Step 4**: Spawn appropriate code generator based on task phase:

**For backend code tasks** (phase: "code", backend files):
```
Task(
  subagent_type: "gen-backend",
  description: "Execute task N: <task name>",
  prompt: "Execute this task from the generation plan:

TASK SPECIFICATION:
[Copy full task YAML from plan]

KB PROJECT PATH:
[KB base path from coordinator]

WORKING DIRECTORY:
[Output directory from coordinator]

Instructions:
1. Read tech.md to understand backend stack (Python/FastAPI, Node/Express, Go/Gin, etc.)
2. Read modules.md for complete specifications (interfaces, flows, behaviors)
3. Generate all backend files specified in task outputs
4. Follow KB patterns exactly (1:1 fidelity)
5. Apply framework conventions (FastAPI, Express, Django, etc.)
6. Write files to WORKING_DIRECTORY
7. Report completion with list of files created"
)
```

**For frontend code tasks** (phase: "code", frontend files):
```
Task(
  subagent_type: "gen-frontend",
  description: "Execute task N: <task name>",
  prompt: "Execute this task from the generation plan:

TASK SPECIFICATION:
[Copy full task YAML from plan]

KB PROJECT PATH:
[KB base path from coordinator]

WORKING DIRECTORY:
[Output directory from coordinator]

Instructions:
1. Read tech.md to understand frontend stack (React, Vue, Angular, Svelte, etc.)
2. Read modules.md and uiDescription.md for component specifications
3. Generate all frontend files specified in task outputs
4. Follow KB patterns exactly (1:1 fidelity)
5. Apply framework conventions (React hooks, Vue composables, etc.)
6. Write files to WORKING_DIRECTORY
7. Report completion with list of files created"
)
```

**For structure/config/deployment/documentation tasks**:
```
Task(
  subagent_type: "gen-backend",
  description: "Execute task N: <task name>",
  prompt: "Execute this task from the generation plan:

TASK SPECIFICATION:
[Copy full task YAML from plan]

KB PROJECT PATH:
[KB base path from coordinator]

WORKING DIRECTORY:
[Output directory from coordinator]

Instructions:
1. Read relevant KB files (tech.md, deployment.md, meta.yaml)
2. Generate files as specified (directories, configs, docker files, README)
3. Follow KB specifications exactly
4. Write files to WORKING_DIRECTORY
5. Report completion with list of files created"
)
```

**Step 5**: After generator completes, spawn gen-validator to validate:

```
Task(
  subagent_type: "gen-validator",
  description: "Validate task N output",
  prompt: "Validate that task N was completed correctly:

TASK SPECIFICATION:
[Copy full task YAML from plan]

GENERATED FILES:
[List of files generator reported creating]

KB PROJECT PATH:
[KB base path from coordinator]

WORKING DIRECTORY:
[Output directory from coordinator]

Validation steps:
1. FILE EXISTENCE: Check all expected files exist
2. SYNTAX CHECK: Run language-specific syntax checkers (python -m py_compile, tsc --noEmit, etc.)
3. INTERFACE COMPLETENESS: Verify all methods from KB specs are implemented (use grep)
4. DEPENDENCIES: Check all imports present
5. ERROR HANDLING: Verify error handling patterns present
6. INTEGRATION POINTS: Check service connections
7. PATTERN COMPLIANCE: Verify framework conventions followed
8. PLACEHOLDER CHECK: Ensure no TODO/FIXME/NotImplementedError
9. FILE SIZE CHECK: Verify files aren't suspiciously small

Return detailed validation report with:
- VALIDATION REPORT: <Domain> <Task Name>
- Each check: ✅ PASS | ❌ FAIL | ⚠️ PARTIAL
- OVERALL: ✅ PASS | ❌ FAIL
- If FAIL: Specific issues with file:line references
- If FAIL: Recommended actions for fixing"
)
```

**Step 6**: Based on validation result, update task status:
```
If validator returns "OVERALL: ✅ PASS":
  TaskUpdate(taskId: N, status: "completed")
Else if validator returns "OVERALL: ❌ FAIL":
  TaskUpdate(taskId: N, status: "failed")
  Report validation failures to user
  Option 1: Stop and let user decide
  Option 2: Retry task with fixes (if issues are clear)
```

**Step 7**: Repeat steps 3-6 for all tasks in dependency order

### Phase 3: Completion

**Step 7**: Report final results to user:
```
Project generated successfully!

Location: [output directory]
KB Project: [matched project ID]
Tasks Completed: [N/N]
Files Generated: [count from generators]

Quick Start:
[Copy from generated README.md]
```

## Important Notes

**Coordinator's Role**:
- Match KB project ✅
- Create task plan ✅
- Create output directory ✅
- DO NOT execute tasks ❌
- DO NOT generate code ❌

**Backend-Code-Generator's Role**:
- Generate backend code (Python, Node, Go, Rust, Java, C#, Ruby, PHP) ✅
- Adapt to framework (FastAPI, Express, Django, Gin, etc.) ✅
- Follow KB patterns exactly (1:1 fidelity) ✅
- Execute structure/config/deployment tasks ✅

**Frontend-Code-Generator's Role**:
- Generate frontend code (React, Vue, Angular, Svelte, Solid, etc.) ✅
- Adapt to framework conventions (hooks, composables, etc.) ✅
- Follow KB UI specifications ✅

**Code-Validator's Role**:
- Validate all generated files ✅
- Run syntax checks (compile checks) ✅
- Verify interface completeness ✅
- Check dependencies, error handling, patterns ✅
- Report PASS/FAIL with specific issues ✅

**Your Role (Skill)**:
- Spawn coordinator for planning
- Read task plan
- Spawn appropriate generator for each task based on task type
- Spawn validator after each generation
- Update task status based on validation
- Report final results

## Error Handling

If coordinator fails:
- Report matching error to user
- Suggest checking KB project exists

If generator fails on a task:
- Mark task as failed
- Report which task failed and why
- Suggest manual completion or retry

If validator fails on a task:
- Report specific validation failures (file missing, syntax errors, etc.)
- Option 1: Stop and show user the issues
- Option 2: Create fix task for generator to address issues
- Option 3: Ask user if they want to continue despite failures

## Example Flow

```
User: /create A chat app for querying SQL databases

Skill:
  1. Spawns coordinator
     → Coordinator matches db-chat-nl KB
     → Coordinator creates generated/chat-app-20260130/
     → Coordinator writes 7-task plan to .claude/tmp/generation-tasks.yaml
     → Coordinator returns

  2. Skill reads task plan

  3. For task 1 (Create directories):
     → Skill spawns gen-backend with task 1 spec
     → Generator creates directory structure
     → Skill spawns gen-validator
     → Validator checks directories exist
     → Validator returns PASS
     → Skill marks task 1 completed

  4. For task 2 (Generate configs):
     → Skill spawns gen-backend with task 2 spec
     → Generator creates requirements.txt, package.json, etc.
     → Skill spawns gen-validator
     → Validator checks files exist, syntax valid
     → Validator returns PASS
     → Skill marks task 2 completed

  5. For task 3 (Generate backend code):
     → Skill spawns gen-backend with task 3 spec
     → Generator creates 8 Python files with FastAPI patterns
     → Skill spawns gen-validator
     → Validator runs py_compile, checks interfaces, checks imports
     → Validator returns PASS
     → Skill marks task 3 completed

  6. For task 4 (Generate frontend code):
     → Skill spawns gen-frontend with task 4 spec
     → Generator creates React 18 + TypeScript components
     → Skill spawns gen-validator
     → Validator runs tsc --noEmit, checks hooks, checks types
     → Validator returns PASS
     → Skill marks task 4 completed

  7. ... continues for remaining tasks

  6. Skill reports success with project location
```

## Architecture

```
User → /create skill (YOU - the orchestrator)
         │
         ├─→ Phase 1: Planning
         │   └─→ gen-coordinator
         │       └─→ Returns: task plan, output directory, matched KB
         │
         └─→ Phase 2: Execution (for each task)
             │
             ├─→ Step A: Generate Code
             │   ├─→ gen-backend (for backend tasks)
             │   │   └─→ Returns: files created (Python/FastAPI, Node/Express, etc.)
             │   │
             │   ├─→ gen-frontend (for frontend tasks)
             │   │   └─→ Returns: files created (React, Vue, Angular, etc.)
             │   │
             │   └─→ gen-backend (for config/deployment/docs tasks)
             │       └─→ Returns: files created
             │
             └─→ Step B: Validate Code
                 └─→ gen-validator
                     └─→ Returns: PASS/FAIL with validation report
```

**Workflow Summary**:
1. Coordinator plans (matches KB, creates tasks)
2. For each task:
   - Specialized generator creates files
   - Validator checks completeness and correctness
   - Task marked completed or failed
3. Final report to user

This matches how dev-architect and specialized engineers work together - the main session coordinates between domain experts.
