---
name: scan
description: Scan a local directory and extract KB documentation
argument-hint: "<local_path> <project_id>"
allowed-tools: Task
context: fork
---

You are the `/scan` skill entry point. Your only job is to delegate to the kb-repo-scanner agent.

## Input

- $ARGUMENTS: The local directory path and project ID provided by the user (e.g., "/path/to/project project-id")

## Workflow

1. Parse $ARGUMENTS to extract local_path and project_id
2. Use the Task tool to invoke the `kb-repo-scanner` agent
3. Pass both the local path and project ID to the agent
4. Let the agent handle the entire scanning workflow

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
