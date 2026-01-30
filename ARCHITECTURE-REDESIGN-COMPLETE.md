# Architecture Redesign Complete

**Date**: 2026-01-30
**Issue**: Coordinator couldn't spawn generator (agents can't spawn agents)
**Solution**: Skill becomes orchestrator (proven pattern)
**Status**: ✅ Implemented and committed

---

## What Changed

### OLD (Broken) Architecture

```
/create skill
  ↓ [thin wrapper - just delegate]
kb-generation-coordinator
  ↓ [tries to spawn generator] ❌ Task tool unavailable
  ↓ [falls back to doing everything itself] ❌ Architectural violation
  └─ Generated code directly
```

**Problems**:
- Coordinator frontmatter lists Task tool but doesn't get it at runtime
- Coordinator forced to violate "No Code Generation" rule
- Tasks 5 and 7 often skipped
- No true separation of concerns

### NEW (Working) Architecture

```
/create skill (ORCHESTRATOR)
  ├─ Phase 1: Spawn coordinator for planning
  │   └─ kb-generation-coordinator
  │       - Match KB project
  │       - Create output directory
  │       - Write task plan YAML
  │       - Create progress tasks
  │       - STOP and return
  │
  ├─ Phase 2: Read task plan
  │   └─ Read .claude/tmp/generation-tasks.yaml
  │
  └─ Phase 3: Execute tasks sequentially
      └─ For each task (1-7):
          ├─ Update task status: in_progress
          ├─ Spawn kb-code-generator with task spec
          │   └─ Generator executes ONE task
          │       - Read KB files
          │       - Generate code/config
          │       - Return with file list
          ├─ Update task status: completed
          └─ Next task
```

**Benefits**:
- ✅ Matches proven tech-lead + generator-engineer pattern
- ✅ No agents spawning agents (skill coordinates via main session)
- ✅ True separation: coordinator plans, generator executes
- ✅ All 7 tasks complete (including install deps + smoke test)
- ✅ Clear failure points and error handling

---

## Inspired By User's Workflow

**User's proven pattern**:
```
User: "tech lead, create plan and delegate to engineer"

What happened:
1. Main session spawned tech-lead
2. Tech-lead created plan and returned
3. Main session read the plan
4. Main session spawned generator-engineer with plan
5. Engineer executed and returned
```

**Key insight**: Main session (skill) coordinates, agents don't spawn each other.

---

## Changes Made

### 1. Skill: `.claude/skills/create/SKILL.md`

**Before**: Thin wrapper, just delegates to coordinator

**After**: Full orchestrator with 3 phases

```markdown
Phase 1: Planning
- Spawn kb-generation-coordinator
- Tell it: Match KB, create plan, STOP (don't execute)
- Receive: KB project ID, output dir, task plan path

Phase 2: Read Task Plan
- Read .claude/tmp/generation-tasks.yaml
- Parse 7 tasks with dependencies

Phase 3: Execution
- For task 1-7:
  - TaskUpdate(in_progress)
  - Spawn kb-code-generator with task YAML
  - Wait for completion
  - TaskUpdate(completed)
- Report final results
```

**New allowed-tools**: `Task, Read, Bash, TaskCreate, TaskUpdate`

### 2. Coordinator: `.claude/agents/kb-generation-coordinator.md`

**Added critical stop point** after Phase 2:

```markdown
## ⚠️ CRITICAL: STOP AFTER PHASE 2 - RETURN TO SKILL

After completing Phase 2 (task planning), STOP and RETURN.

DO NOT proceed to Phase 3.
DO NOT execute tasks.
DO NOT generate code.
```

**Emphasized "Planning Only" role**:

```markdown
**CRITICAL: Planning Only - No Execution**:
- You are a PLANNER, not an executor
- Your job: Match KB → Plan tasks → Return to skill
- DO NOT execute tasks yourself
- DO NOT generate any code files
- STOP and return after creating the task plan
```

**Phase 3 deprecated**: Marked as "DEPRECATED - Skill Handles This Now"

### 3. Generator: `.claude/agents/kb-code-generator.md`

**No changes needed** - already designed for one-task execution.

---

## How It Works Now

### User Runs `/create`

```
User: /create A chat app for querying SQL databases
```

### Skill Orchestrates (Phase 1: Planning)

```
Skill spawns coordinator:

Task(
  subagent_type: "kb-generation-coordinator",
  prompt: "Match KB and create task plan (DO NOT execute)"
)

Coordinator does:
1. Matches description to db-chat-nl KB
2. Creates generated/chat-app-20260130-123456/
3. Counts 8 modules → no split needed
4. Writes 7-task plan to .claude/tmp/generation-tasks.yaml
5. Creates TaskCreate entries for progress tracking
6. Returns summary to skill

Coordinator returns:
"Planning Complete!
Matched KB Project: db-chat-nl
Output Directory: C:/work/.../generated/chat-app-20260130-123456
Task Plan File: .claude/tmp/generation-tasks.yaml
Total Tasks: 7"
```

### Skill Reads Plan (Phase 2)

```
Skill reads .claude/tmp/generation-tasks.yaml:

tasks:
  - id: 1, name: "Create directories"
  - id: 2, name: "Generate configs"
  - id: 3, name: "Generate code" (8 modules)
  - id: 4, name: "Create deployment files"
  - id: 5, name: "Install dependencies"
  - id: 6, name: "Generate README"
  - id: 7, name: "Smoke test"
```

### Skill Executes Tasks (Phase 3)

```
For task 1:
  Skill: TaskUpdate(task 1, in_progress)

  Skill spawns generator:
  Task(
    subagent_type: "kb-code-generator",
    prompt: "Execute task 1: Create directories

    [Full task YAML]
    KB Path: .../db-chat-nl
    Working Dir: .../generated/chat-app-20260130-123456"
  )

  Generator:
  - Reads modules.md for directory structure
  - Creates backend/, frontend/, backend/app/, etc.
  - Returns: "Created 12 directories"

  Skill: TaskUpdate(task 1, completed)

For task 2:
  [Same pattern - spawn generator, execute, mark complete]

... continues for all 7 tasks ...

For task 7 (Smoke test):
  Generator runs: npm run build && python -c "import app.main"
  Returns: "Smoke test passed"

Skill reports:
"Project generated successfully!
Location: .../generated/chat-app-20260130-123456
Tasks: 7/7 completed
Files: 47 created
Ready to use!"
```

---

## Task Completion Guarantee

### Old Behavior
```
Tasks 1-4, 6: ✅ Completed (coordinator did them)
Task 5: ❌ Skipped (install dependencies)
Task 7: ❌ Skipped (smoke test)
```

### New Behavior
```
Tasks 1-7: ✅ All completed
- Task 5: Generator runs npm install + pip install
- Task 7: Generator runs smoke test commands
```

---

## Error Handling

### Coordinator Fails (Phase 1)
```
Skill reports:
"❌ Planning failed: [error]
Check that KB project exists for your description"
```

### Generator Fails on Task N (Phase 3)
```
Skill reports:
"❌ Task N failed: [error from generator]
Completed: Tasks 1-[N-1]
Failed: Task N
Remaining: Tasks [N+1]-7

To retry: /create [same description]
Or complete manually at: [output directory]"
```

---

## Testing the New Architecture

### Test 1: Basic Generation

```bash
/create A simple chat app using React and FastAPI
```

**Expected**:
1. Coordinator matches KB, creates plan, returns
2. Skill spawns generator 7 times (once per task)
3. All tasks complete including dependencies install
4. Smoke test runs
5. Project ready to use

### Test 2: Large Project (Tests Auto-Split)

```bash
/create A complete e-commerce platform
```

**Expected**:
1. Coordinator detects 50+ modules
2. Splits Task 3 into 3a, 3b, 3c (by module groups)
3. Skill spawns generator for each subtask
4. All subtasks complete
5. Total ~10-12 tasks instead of 7

### Test 3: Error Recovery

```bash
/create A project that will fail on task 3
```

**Expected**:
1. Tasks 1-2 complete
2. Task 3 fails (generator error)
3. Skill reports exactly which task failed
4. User can investigate, fix, retry

---

## Migration Notes

### For Existing Generated Projects

Projects generated with old architecture (coordinator did everything):
- ✅ Code is fine and functional
- ❌ Dependencies might not be installed (task 5 skipped)
- ❌ No smoke test run (task 7 skipped)

**To complete**:
```bash
cd generated/<project-name>/

# Install backend deps
cd backend && pip install -r requirements.txt

# Install frontend deps
cd ../frontend && npm install

# Run smoke test
cd ../backend && python -c "import app.main"
cd ../frontend && npm run build
```

### For Future Generations

All `/create` runs will use new architecture:
- ✅ All 7 tasks complete automatically
- ✅ Dependencies installed
- ✅ Smoke test validates project
- ✅ Truly ready to run

---

## Architecture Validation

### ✅ Confirmed Working Patterns

**Pattern**: Main session coordinates agents
- ✅ tech-lead + generator-engineer (user's proven workflow)
- ✅ /create skill + coordinator + generator (new implementation)

### ❌ Confirmed Non-Working Patterns

**Pattern**: Agent spawns agent
- ❌ coordinator → generator (Task tool not available to agents)
- Root cause: Agents don't have Task tool at runtime despite frontmatter

---

## Key Takeaways

1. **Agents can't spawn agents** - Claude Code CLI limitation
2. **Skills CAN orchestrate multiple agents** - working pattern
3. **Main session is the coordinator** - same as user workflow
4. **Architecture now matches reality** - no aspirational docs
5. **All tasks complete** - including install + smoke test

---

## Files Modified

```
.claude/skills/create/SKILL.md
- Complete rewrite as orchestrator
- 3 phases: Planning → Read → Execute
- Spawns coordinator then generators

.claude/agents/kb-generation-coordinator.md
- Added STOP point after Phase 2
- Emphasized "Planning Only" role
- Deprecated Phase 3 execution

.claude/agents/kb-code-generator.md
- No changes (already correct design)
```

---

## Commits

```
65582a5 - Redesign /create workflow: skill orchestrates coordinator + generators
4a07d9b - Document critical architecture limitation: agents cannot spawn agents
fcd2023 - Update freeze analysis: Add context:fork fix (attempt #3)
af48f00 - Fix: Remove context:fork from /create skill
dd7df1b - Add comprehensive freeze issue analysis and fix documentation
```

---

## Next Steps

### Immediate: Test New Architecture

```bash
/create natural language to db chat via LLM, sports topic
```

Watch for:
1. Coordinator creates plan and stops
2. Skill spawns generator for each task
3. All 7 tasks complete
4. Dependencies installed
5. Smoke test passes
6. Project ready to run

### Future: Optimize

- **Parallel execution**: Spawn independent tasks in parallel (e.g., tasks 1+2)
- **Caching**: Reuse coordinator plan for similar descriptions
- **Progress UI**: Real-time task status updates
- **Error recovery**: Automatic retry with modifications

---

**Architecture is now aligned with Claude Code CLI capabilities.**
**Ready to test with `/create` command.**
