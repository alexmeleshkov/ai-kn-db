---
name: create
description: Generate a new project using the KB-driven project generator. Provide a description of the project you want to create.
argument-hint: "<project description>"
allowed-tools: Task, Read, Bash, TaskCreate, TaskUpdate
---

You are the `/create` skill orchestrator. You coordinate between kb-generation-coordinator (planning) and kb-code-generator (execution) to generate a complete project.

## Input

- $ARGUMENTS: The project description provided by the user

## Workflow

### Phase 1: Planning (Spawn Coordinator)

**Step 1**: Spawn kb-generation-coordinator for planning:

```
Task(
  subagent_type: "kb-generation-coordinator",
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

### Phase 2: Execution (Generator + Validator Working in Pair)

For each task in the task plan (typically 5-7 tasks depending on Task 3 splitting):

**Step 3**: Update task status to in_progress:
```
TaskUpdate(taskId: N, status: "in_progress")
```

**Step 4**: Spawn kb-code-generator to execute the task:

```
Task(
  subagent_type: "kb-code-generator",
  description: "Execute task N: <task name>",
  prompt: "Execute this task from the generation plan:

TASK SPECIFICATION:
[Copy full task YAML from plan]

KB PROJECT PATH:
[KB base path from coordinator]

WORKING DIRECTORY:
[Output directory from coordinator]

Instructions:
1. Read full KB files as needed (paths provided in task)
2. Generate all files specified in task outputs
3. Follow KB patterns exactly (1:1 fidelity)
4. Write files to WORKING_DIRECTORY
5. Report completion with list of files created"
)
```

**Step 5**: After generator completes, spawn coordinator to validate:

```
Task(
  subagent_type: "kb-generation-coordinator",
  description: "Validate task N output",
  prompt: "Validate that task N was completed correctly:

TASK SPECIFICATION:
[Copy full task YAML from plan]

KB PROJECT PATH:
[KB base path]

OUTPUT DIRECTORY:
[Output directory]

GENERATOR REPORTED:
[What generator said it created]

Your validation job:
1. Check that ALL files in task outputs exist
2. Verify files are not empty
3. For code tasks: Check imports/syntax are reasonable
4. Compare against acceptance criteria
5. Report: PASS or FAIL with specific issues

Return one of:
- VALIDATION PASSED: All acceptance criteria met
- VALIDATION FAILED: [Specific issues found]"
)
```

**Step 6**: Based on validation result, update task status:
```
If validation says "PASSED":
  TaskUpdate(taskId: N, status: "completed")
Else:
  TaskUpdate(taskId: N, status: "failed")
  Report failure to user and stop (or retry if possible)
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

**Generator's Role**:
- Execute ONE task at a time ✅
- Generate code following KB patterns ✅
- Report completion ✅

**Your Role (Skill)**:
- Spawn coordinator for planning
- Read task plan
- Spawn generator for each task (sequential)
- Coordinate task status updates
- Report final results

## Error Handling

If coordinator fails:
- Report matching error to user
- Suggest checking KB project exists

If generator fails on a task:
- Mark task as failed
- Report which task failed and why
- Suggest manual completion or retry

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
     → Skill spawns generator with task 1 spec
     → Generator creates directory structure
     → Generator returns
     → Skill marks task 1 completed

  4. For task 2 (Generate configs):
     → Skill spawns generator with task 2 spec
     → Generator creates requirements.txt, package.json, etc.
     → Generator returns
     → Skill marks task 2 completed

  5. ... continues for all 7 tasks

  6. Skill reports success with project location
```

## Architecture

```
User → /create skill (YOU - the orchestrator)
         ├─→ kb-generation-coordinator (planning phase only)
         │   └─→ Returns task plan
         │
         └─→ For each task:
             └─→ kb-code-generator (execution)
                 └─→ Returns with files created
```

This matches how tech-lead and generator-engineer work together - the main session coordinates between specialized agents.
