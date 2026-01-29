---
name: scan
description: Scan a local directory and extract KB documentation
argument-hint: "<local_path> <project_id>"
allowed-tools: Task
context: fork
---

You are the `/scan` skill entry point. **IMMEDIATELY delegate to the kb-repo-scanner agent. Do NOT do any work yourself.**

## Input

- $ARGUMENTS: The local directory path and project ID (e.g., "/path/to/project project-id")

## Workflow

**IMMEDIATELY invoke the Task tool** - do not analyze, do not validate paths, do not read files:

```
Task(
  subagent_type: "kb-repo-scanner",
  description: "Scan repository and create KB entry",
  prompt: "Scan repository with these arguments: $ARGUMENTS"
)
```

That's it. The scanner agent handles everything else (parsing args, validation, extraction).

## Example

```
User: /scan /c/work/my-app my-app-kb
```

Your action:
```
Use Task tool with:
  subagent_type: kb-repo-scanner
  prompt: "Scan local directory at /c/work/my-app and create KB entry with project ID: my-app-kb"
```

## Notes

- This skill is a thin wrapper - all logic lives in the kb-repo-scanner agent
- Do NOT attempt to run the scanner script directly
- Do NOT ask clarification questions - the agent handles that
- Always delegate to the agent for consistency

Remember: Keep this skill minimal. The agent does the real work.
