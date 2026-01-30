# Coordinator Architecture Violation Report

**Date**: 2026-01-30
**Issue**: kb-generation-coordinator doing code generation instead of delegating
**Severity**: Critical - Breaks separation of concerns

---

## The Architecture Design

### Intended Two-Agent Workflow

```
/create skill
  ↓ [Task tool]
kb-generation-coordinator (ORCHESTRATOR)
  ↓ [Task tool - for EACH task]
kb-code-generator (EXECUTOR)
  ↓
Generated code
```

### Coordinator's Explicit Instructions

**File**: `.claude/agents/kb-generation-coordinator.md:45-48`

```
**No Code Generation**:
- You coordinate but DO NOT write code yourself
- All code generation is delegated to kb-code-generator
- You review and validate, not implement
```

**File**: `.claude/agents/kb-generation-coordinator.md:444-448`

```
4. **Delegate to Generator**: Use Task tool to invoke kb-code-generator
   ```
   Task tool with:
     subagent_type: kb-code-generator
     prompt: "Execute task [id]: [name]
```

---

## What Actually Happened

### Test Run: `/create natural language to db chat via LLM, sports topic`

**Tasks Created**:
1. Task 1: Create project directory structure
2. Task 2: Generate configuration files
3. Task 3: Generate all code files (8 modules)
4. Task 4: Create deployment files
5. Task 5: Install dependencies
6. Task 6: Generate project documentation
7. Task 7: Execute smoke test

**Tasks Executed by Coordinator Itself**:
- ✅ Task 1: Created directories
- ✅ Task 2: Generated requirements.txt, package.json, docker-compose.yml
- ✅ Task 3: **Generated all 8 code modules** ❌ VIOLATION
- ✅ Task 4: Generated .env.example, .gitignore
- ✅ Task 6: Generated README.md

**Tasks Skipped**:
- ❌ Task 5: Install dependencies (status: pending)
- ❌ Task 7: Execute smoke test (status: pending)

**Delegations to kb-code-generator**: **ZERO**

---

## Evidence

### Task List After Generation

```
#2. [completed] Generate project: natural language to db chat via LLM, sports topic
#3. [completed] Task 1: Create project directory structure
#4. [completed] Task 2: Generate configuration files
#5. [completed] Task 3: Generate all code files
#6. [completed] Task 4: Create deployment files
#7. [pending] Task 5: Install dependencies
#8. [completed] Task 6: Generate project documentation
#9. [pending] Task 7: Execute smoke test
```

### Files Created

```
generated/natural-language-to-db-chat-20260130-023931/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── auth_routes.py
│   │   │   └── conversation_routes.py
│   │   ├── services/
│   │   │   ├── llm.py
│   │   │   ├── auth.py
│   │   │   └── app_data.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatContainer.tsx
│   │   └── hooks/
│   │       └── useChat.ts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

All files created by coordinator, none by kb-code-generator.

---

## Impact

### Immediate Problems

1. **Incomplete Project**: Dependencies not installed, can't run immediately
2. **No Validation**: Smoke test not executed, unknown if project works
3. **Architecture Broken**: Two-agent design violated

### Long-Term Problems

1. **Scalability**: Coordinator will fail on large projects (memory issues)
2. **Maintainability**: Single agent doing everything is harder to debug
3. **Specialization Lost**: Generator's specific code-gen optimizations unused
4. **Context Overflow**: Large projects will exceed coordinator's context window

### Why Delegation Matters

**Coordinator (Orchestrator)**:
- Light context: Only KB metadata, task plans
- Fast: Makes decisions, tracks progress
- Resilient: Can retry failed tasks

**Generator (Executor)**:
- Heavy context: Full KB files, code patterns
- Focused: One task at a time
- Replaceable: If fails, coordinator can retry with new instance

---

## Root Cause Analysis

### Why Did Coordinator Do Code Generation?

**Hypothesis #1: Instructions Not Strong Enough**
- Coordinator has "No Code Generation" section
- But maybe not enforced strongly enough
- Agent may interpret "create files from KB" as allowed

**Hypothesis #2: No Validation Preventing It**
- Coordinator has Write tool
- Nothing technically prevents it from writing code
- Should Write tool be removed from coordinator?

**Hypothesis #3: Delegation Complexity**
- Using Task tool to spawn kb-code-generator is complex
- Coordinator may take easier path of doing work directly
- Need stricter workflow enforcement

**Hypothesis #4: Missing Delegation Examples**
- Coordinator docs describe delegation abstractly
- May need concrete, mandatory examples
- "MUST use this exact pattern" instead of "should delegate"

---

## Proposed Fixes

### Fix #1: Remove Write Tool from Coordinator (Breaking Change)

```diff
File: .claude/agents/kb-generation-coordinator.md

-tools: Read, Write, Bash, Glob, Task, TaskCreate, TaskUpdate, TaskList, TaskGet
+tools: Read, Bash, Glob, Task, TaskCreate, TaskUpdate, TaskList, TaskGet
```

**Rationale**: If coordinator can't write files, it MUST delegate
**Risk**: Coordinator needs Write for task plan YAML - must handle this

### Fix #2: Stricter Delegation Enforcement

Add to coordinator instructions:

```markdown
## CRITICAL WORKFLOW RULE

For EVERY task in the task plan:

1. TaskUpdate(taskId: N, status: "in_progress")
2. **MANDATORY**: Use Task tool to invoke kb-code-generator:
   ```
   Task(
     subagent_type: "kb-code-generator",
     description: "Execute task [id]",
     prompt: "[full task details from plan]"
   )
   ```
3. Wait for generator to complete
4. Validate generator output
5. TaskUpdate(taskId: N, status: "completed")

**ABSOLUTELY FORBIDDEN**:
- Using Write tool to create code files
- Using Write tool to create config files
- Doing ANY file generation yourself
- Skipping delegation to generator

**ONLY ALLOWED Write Usage**:
- Creating task plan YAML in .claude/tmp/
- Creating validation reports

If you find yourself writing code or config files, STOP and delegate instead.
```

### Fix #3: Complete Unfinished Tasks

Run tasks 5 and 7 manually:

```bash
# Task 5: Install dependencies
cd generated/natural-language-to-db-chat-20260130-023931/backend
pip install -r requirements.txt

cd ../frontend
npm install

# Task 7: Smoke test
cd ../backend
python -m pytest tests/ || echo "No tests found"

cd ../frontend
npm run type-check || npm run build
```

### Fix #4: Add Validation Step

After coordinator completes, check:
- Did coordinator use Task tool to spawn kb-code-generator? (count invocations)
- Are all tasks marked completed?
- Does generated project pass smoke test?

---

## Testing Plan

### Test Case 1: Verify Delegation Happens

1. Apply Fix #2 (stricter instructions)
2. Run `/create` command
3. Monitor for Task tool invocations
4. **Expected**: 7 Task tool calls to kb-code-generator (one per task)
5. **Expected**: All tasks completed (including 5 and 7)
6. **Expected**: Coordinator only writes task plan YAML, nothing else

### Test Case 2: Verify Generator Does Work

1. Check kb-code-generator agent receives task specifications
2. Verify generator reads KB files
3. Verify generator creates code files
4. Verify generator returns to coordinator with status

### Test Case 3: Large Project Scalability

1. Create KB project with 50+ modules
2. Coordinator should auto-split Task 3 into multiple subtasks
3. Each subtask delegated to separate kb-code-generator instance
4. Coordinator should never load all 50 modules into context

---

## Acceptance Criteria

The architecture is fixed when:

1. ✅ Coordinator creates task plan only
2. ✅ Coordinator delegates ALL tasks to kb-code-generator
3. ✅ Generator creates all files (coordinator creates none)
4. ✅ All 7 tasks complete (no pending tasks)
5. ✅ Dependencies installed automatically
6. ✅ Smoke test executes automatically
7. ✅ Generated project runs without manual intervention

---

## Current Status

- **Issue Identified**: ✅ Documented
- **Root Cause**: ⏳ Under investigation (hypotheses 1-4)
- **Fix Applied**: ❌ Not yet
- **Testing**: ❌ Not yet
- **Project Usable**: ⚠️ Yes, but manual setup required (install deps)

---

## Related Documents

- `FREEZE-ISSUE-ANALYSIS.md` - Original freeze issue investigation
- `.claude/agents/kb-generation-coordinator.md` - Coordinator design
- `.claude/agents/kb-code-generator.md` - Generator design
- `.claude/skills/create/SKILL.md` - Entry point

---

**Next Steps**:
1. Apply Fix #2 (stricter delegation enforcement)
2. Test with new `/create` run
3. Verify kb-code-generator is invoked for each task
4. Complete tasks 5 and 7 for current generated project
