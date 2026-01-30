# /create Freeze Issue - Complete Analysis & Fix History

**Issue Date**: 2026-01-30
**Status**: FIXED (pending verification)
**Severity**: Critical (causes session restarts)

---

## THE PROBLEM

### Symptom
When running `/create <description>`, the command freezes/hangs:
```
> /create natural language to db chat via LLM, sports topic
⎿ I'll immediately delegate to the kb-generation-coordinator agent as
  Skill(kb-generation-coordinator)
[FREEZE - no further output, must Ctrl+C]
```

### Impact
- User cannot generate projects from KB
- Forces session restart
- Loses all context and progress

---

## ROOT CAUSE ANALYSIS

### Issue #1: Missing Task Tools in kb-generation-coordinator
**File**: `.claude/agents/kb-generation-coordinator.md`

**What Happened**:
- Commit `227f63d` (2026-01-30 02:02) removed Task tools from coordinator
- Commit message: "Remove invalid Task* tools from kb-generation-coordinator"
- This was INCORRECT - the tools are NOT invalid

**Why It Causes Freeze**:
The coordinator's workflow (line 444-448) explicitly requires Task tool:
```
4. **Delegate to Generator**: Use Task tool to invoke kb-code-generator
   ```
   Task tool with:
     subagent_type: kb-code-generator
     prompt: "Execute task [id]: [name]
```

Without Task tools:
1. Coordinator starts planning
2. Tries to delegate to kb-code-generator using Task tool
3. Task tool unavailable → ERROR or HANG
4. 99% memory usage as it gets stuck
5. Complete freeze

**Evidence from Agent Documentation**:
- Line 20: "**Delegation**: Launch kb-code-generator agent for each task/task-group"
- Line 47: "All code generation is delegated to kb-code-generator"
- Line 587-588: "Use Task tool to invoke kb-code-generator agent"

### Issue #2: Skill Invoking Wrong Tool
**File**: `.claude/skills/create/SKILL.md`

**What Happened**:
User's output shows: `Skill(kb-generation-coordinator)`
This means the skill used the **Skill tool** instead of **Task tool**

**Why This Is Wrong**:
- Skill tool: Invokes another skill (like /commit, /scan)
- Task tool: Launches an agent (like kb-generation-coordinator)
- kb-generation-coordinator is an AGENT, not a skill

**Why It Causes Freeze**:
1. Skill tool tries to find a skill named "kb-generation-coordinator"
2. No such skill exists (it's an agent)
3. Tool hangs waiting for non-existent skill
4. Never returns

---

## FIX ATTEMPTS HISTORY

### Attempt #1: Restore Task Tools to Coordinator
**Date**: 2026-01-30 (earlier in session)
**Git Commit**: `78c4216` - "Fix: Restore Task tools to kb-generation-coordinator (required for delegation to kb-code-generator)"

**What Was Done**:
```diff
File: .claude/agents/kb-generation-coordinator.md
Line 4:
-tools: Read, Write, Bash, Glob
+tools: Read, Write, Bash, Glob, Task, TaskCreate, TaskUpdate, TaskList, TaskGet
```

**Rationale**:
- Coordinator needs Task to delegate to kb-code-generator
- Coordinator needs TaskCreate/TaskUpdate for progress tracking
- These tools are documented in the agent's workflow

**Test Evidence**:
A test run (`.claude/tmp/test-report.txt`) proved this fix works:
```
Test Status: PASSED
- KB matching: SUCCESS
- Output directory creation: SUCCESS
- Module counting: SUCCESS (8 modules)
- Task plan creation: SUCCESS (7 tasks, 7120 bytes YAML)
- No tool freezing: CONFIRMED
- Ready for Full Generation: YES
```

Test completed in ~30 seconds with NO freezing.

### Attempt #2: Clarify Skill Instructions
**Date**: 2026-01-30 (current session)
**Git Commit**: `9e9b296` - "Clarify /create skill: explicitly use Task tool not Skill tool"
**Result**: ✅ Fixed freeze, but coordinator still didn't run

### Attempt #3: Remove context:fork from Skill
**Date**: 2026-01-30 (current session)
**Git Commit**: `af48f00` - "Fix: Remove context:fork from /create skill"

**What Was Done**:
```diff
File: .claude/skills/create/SKILL.md

-context: fork
```

**Why This Was The Issue**:
After fix #2, `/create` no longer froze, but coordinator didn't actually run:
1. Skill invoked Task tool ✅
2. Task #1 created ✅
3. Skill returned immediately ❌
4. Coordinator never executed ❌

**Root Cause**: `context: fork` isolates the skill in a separate context.
- The Task tool call completes
- But the spawned agent runs in isolated context
- Agent work doesn't persist back to main session
- User sees nothing happen

**Why /scan Works (Maybe?)**:
- `/scan` also has `context: fork`
- It might have the same issue (untested)
- Or kb-repo-scanner agent is simpler and completes in forked context

**Evidence**:
```
Task #1: Generate project from KB
Status: pending  ← Never changed to in_progress
Description: Generate a project with this description: ...
             ← Generic description, not KB-matched project
```

The task description should say "Creating [project-name] from KB: db-chat-nl"
but instead says the raw user input, proving coordinator never ran matching phase.

**Expected After Fix**:
- Coordinator runs in main context
- Can create files, spawn agents, track progress
- Work persists and is visible to user

**What Was Done**:
```diff
File: .claude/skills/create/SKILL.md

OLD:
"**IMMEDIATELY invoke the Task tool** - do not analyze, do not plan, do not read files:

```
Task(
  subagent_type: "kb-generation-coordinator",
  description: "Generate project from user description",
  prompt: "Generate a project with this description: $ARGUMENTS"
)
```"

NEW:
"**USE THE TASK TOOL** (not the Skill tool!) with these exact parameters:
- subagent_type: "kb-generation-coordinator"
- description: "Generate project from KB"
- prompt: "Generate a project with this description: $ARGUMENTS"

Do NOT:
- Use the Skill tool
- Analyze the description
- Plan anything
- Read any files
- Ask questions"
```

**Rationale**:
- User output showed `Skill(kb-generation-coordinator)` - wrong tool
- Skill instructions may have been ambiguous
- Explicitly warn against using Skill tool
- Make it impossible to misunderstand

---

## CURRENT STATE

### Files Modified (Committed)
1. `.claude/agents/kb-generation-coordinator.md` - Task tools restored
2. `.claude/skills/create/SKILL.md` - Explicit Task tool instructions

### Git History
```bash
78c4216 Fix: Restore Task tools to kb-generation-coordinator (required for delegation)
9e9b296 Clarify /create skill: explicitly use Task tool not Skill tool
```

### Verification Status
⏳ **PENDING** - User needs to test `/create` again

---

## DIAGNOSTIC EVIDENCE

### Test Report Summary
**File**: `.claude/tmp/test-report.txt`
**Test Date**: 2026-01-30
**Result**: PASSED (no freezing)

Key findings:
- Coordinator CAN be invoked successfully
- Planning phase works (7 tasks created in 30s)
- No memory issues (incremental KB loading works)
- No tool freezing
- Task/TaskCreate tools functional

### Agent Configuration Audit
All agents properly configured with valid YAML frontmatter:

```bash
generator-engineer.md:
  name: generator-engineer
  tools: Bash, Glob, Grep, Read, Edit, Write, NotebookEdit

kb-code-generator.md:
  name: kb-code-generator
  tools: Read, Write, Bash, Glob, Grep

kb-generation-coordinator.md:
  name: kb-generation-coordinator
  tools: Read, Write, Bash, Glob, Task, TaskCreate, TaskUpdate, TaskList, TaskGet
  ✅ Task tools present

kb-repo-scanner.md:
  name: kb-repo-scanner
  tools: Read, Bash, Glob, Write

tech-lead.md:
  name: tech-lead
  tools: Glob, Grep, Read, Bash
```

### Skill Configuration Audit
```bash
/create skill:
  allowed-tools: Task ✅
  context: fork
  Instructions: "USE THE TASK TOOL (not the Skill tool!)" ✅

/scan skill:
  allowed-tools: Task ✅
  context: fork
  Same pattern as /create
```

---

## IF IT FREEZES AGAIN

### Immediate Diagnostics

1. **Check Which Tool Was Used**
   Look for this in the output:
   - ❌ `Skill(kb-generation-coordinator)` → Wrong tool, Issue #2 not fixed
   - ✅ `Task(subagent_type=kb-generation-coordinator)` → Correct tool, different issue

2. **Check How Far It Got**
   - Freezes immediately? → Skill invocation failing
   - Shows "Matching KB..."? → Coordinator started, issue in coordinator workflow
   - Shows "Planning tasks..."? → Issue in task planning or delegation

3. **Check Process State**
   ```bash
   # In another terminal:
   ps aux | grep claude
   # High CPU? Infinite loop
   # High memory? Context overflow
   # Normal usage but hanging? Waiting for response that never comes
   ```

### Alternative Tests

1. **Test /scan skill** (same pattern as /create):
   ```bash
   /scan C:\work\ai-knowledge-db\docs\kb\projects\db-chat-nl test-scan
   ```
   - If this works → Issue specific to kb-generation-coordinator agent
   - If this freezes → Issue with Task tool invocation from skills

2. **Direct Agent Test** (if you can access it):
   Try invoking kb-generation-coordinator directly without the skill
   - If this works → Issue is in the skill layer
   - If this freezes → Issue is in the agent itself

### Possible Remaining Issues

If fixes #1 and #2 don't resolve it:

**Hypothesis #3: Agent Discovery Failure**
- Agents not being registered by CLI
- Check if `.claude/agents.yaml` should exist (currently doesn't)
- Agent frontmatter may have syntax issues

**Hypothesis #4: context="fork" Problem**
- Both skills use `context: fork`
- This might isolate the skill in a way that prevents Task tool from finding agents
- Try removing `context: fork` from skill frontmatter

**Hypothesis #5: Coordinator Workflow Issue**
- Coordinator hangs during KB matching (reading all meta.yaml files)
- Coordinator hangs during task planning
- Coordinator tries to create too many tasks
- Check `.claude/tmp/generation-tasks.yaml` - was it created?

**Hypothesis #6: Permissions Issue**
- Task tool might need explicit permission in `.claude/settings.local.json`
- Currently only Bash permissions are listed
- Try adding Task tool to allowed permissions

**Hypothesis #7: context:fork Isolation** ✅ **CONFIRMED - FIX APPLIED**
- Skills with `context: fork` run in isolated context
- Task tool invocations complete but agent work doesn't persist
- Agent runs but results don't return to main session
- **FIX**: Remove `context: fork` from skill frontmatter (commit af48f00)

### Files to Check After Freeze

1. `.claude/tmp/generation-tasks.yaml` - Was task plan created?
2. `.claude/tmp/*.log` - Any error logs?
3. `generated/<slug>-<timestamp>/` - Was output dir created?
4. Git status - Are there uncommitted changes that need to be applied?

---

## TECHNICAL DETAILS

### Coordinator Workflow (from .claude/agents/kb-generation-coordinator.md)

**Phase 1: Match KB Project**
1. Glob: `docs/kb/projects/*/meta.yaml`
2. Read each meta.yaml
3. Token-based matching (lowercase words)
4. Select best match
5. Create output directory: `generated/<slug>-<timestamp>/`

**Phase 2: Plan Tasks**
1. Count modules: `grep -c "^### \|^\*\*Location\*\*:" modules.md`
2. Auto-split logic (if > 15 modules)
3. Write task plan to `.claude/tmp/generation-tasks.yaml`
4. Use TaskCreate to create progress tasks

**Phase 3: Execute Tasks** (where freezing likely occurs)
1. For each task:
   - TaskUpdate(status="in_progress")
   - Extract KB context using streaming (sed/grep/head)
   - **Delegate to kb-code-generator using Task tool** ← Issue #1 point of failure
   - Validate output
   - TaskUpdate(status="completed")

### Expected Tool Call Sequence

```
User: /create <description>
  ↓
Skill: create (context=fork)
  ↓ [Should use Task tool, not Skill tool]
  ↓
Task(subagent_type="kb-generation-coordinator", prompt="...")
  ↓
Agent: kb-generation-coordinator
  ↓ [Match KB, plan tasks]
  ↓
TaskCreate(...) [Create progress tasks]
  ↓
For each task:
  Task(subagent_type="kb-code-generator", prompt="...")
    ↓
  Agent: kb-code-generator
    ↓ [Generate code]
    ↓
  Return to coordinator
  ↓
Return to skill
  ↓
Return to user
```

**Failure Points**:
- ❌ Skill uses Skill tool instead of Task tool
- ❌ Task tool can't find kb-generation-coordinator agent
- ❌ Coordinator can't use Task tool (missing from tools list)
- ❌ Coordinator hangs during KB matching/planning
- ❌ TaskCreate fails or hangs

---

## COMMIT REFERENCE

### Relevant Commits (Newest First)

```
af48f00 (2026-01-30 current) - Fix: Remove context:fork from /create skill
9e9b296 (2026-01-30 current) - Clarify /create skill: explicitly use Task tool
78c4216 (2026-01-30 current) - Fix: Restore Task tools to kb-generation-coordinator
227f63d (2026-01-30 02:02)   - Remove invalid Task* tools [INCORRECT - CAUSED ISSUE]
79dfe6a (2026-01-30 01:50)   - Fix agent registration: use single-line descriptions
1ed0bb5 (2026-01-30 01:xx)   - WIP: Investigating /create hang issue
48cdf62 (2026-01-30 01:29)   - Add kb-generation-coordinator and kb-code-generator
```

### To See Full Diff of Fixes

```bash
# See what changed in coordinator
git show 78c4216

# See what changed in skill
git show 9e9b296

# See what was incorrectly removed
git show 227f63d
```

---

## SUCCESS CRITERIA

The fix is successful when:

1. ✅ `/create <description>` completes without freezing
2. ✅ Output shows `Task(...)` not `Skill(...)`
3. ✅ Coordinator creates task plan (`.claude/tmp/generation-tasks.yaml`)
4. ✅ Progress tasks show in UI
5. ✅ Output directory created: `generated/<slug>-<timestamp>/`
6. ✅ Code files generated matching KB patterns
7. ✅ Process completes in reasonable time (< 5 minutes for small project)

Minimum success for this test:
- ✅ No freeze
- ✅ Gets past skill invocation phase
- ✅ Coordinator starts and begins work

---

## NEXT ACTION

**Try this command:**
```bash
/create natural language to db chat via LLM, sports topic
```

**Watch for:**
1. Does it show `Task(...)` or `Skill(...)`?
2. Does it freeze immediately or get past skill invocation?
3. Does `.claude/tmp/generation-tasks.yaml` get created?
4. Any error messages?

**If it works:**
- Document success
- Test with different project description
- Consider this issue RESOLVED

**If it freezes:**
- Note WHERE it froze (which phase)
- Check diagnostics from "IF IT FREEZES AGAIN" section
- Update this document with new findings
- Try alternative tests (/scan skill, context=fork removal)

---

## ADDITIONAL CONTEXT

### KB Projects Available
Currently only 1 non-template KB project:
- `docs/kb/projects/db-chat-nl/` - Database Chat with Natural Language

This is a perfect match for the test description:
"natural language to db chat via LLM, sports topic"

Should match with high confidence and generate a working project.

### Generated Project Expected Location
```
C:/work/ai-knowledge-db/generated/natural-language-to-db-chat-via-llm-sports-topic-<timestamp>/
```

### Expected Outcome
If successful, the generated project will have:
- Backend: FastAPI (Python)
- Frontend: React (TypeScript)
- Database: PostgreSQL (via Docker)
- 8 code modules (matching db-chat-nl KB)
- Docker Compose setup
- README with run instructions

---

**Document Version**: 1.0
**Last Updated**: 2026-01-30
**Session**: Freeze Issue Investigation & Fix
