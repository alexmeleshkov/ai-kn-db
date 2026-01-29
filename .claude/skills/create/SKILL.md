---
name: create
description: Generate a new project using the KB-driven project generator. Provide a description of the project you want to create.
argument-hint: "<project description>"
allowed-tools: Task
context: fork
---

You are the `/create` skill entry point. **IMMEDIATELY delegate to the kb-generation-coordinator agent. Do NOT do any work yourself.**

## Input

- $ARGUMENTS: The project description provided by the user

## Workflow

**IMMEDIATELY invoke the Task tool** - do not analyze, do not plan, do not read files:

```
Task(
  subagent_type: "kb-generation-coordinator",
  description: "Generate project from user description",
  prompt: "Generate a project with this description: $ARGUMENTS"
)
```

That's it. The coordinator handles everything else.

## Example

```
User: /create A chat app for querying SQL databases in natural language
```

Your action:
```
Use Task tool with:
  subagent_type: kb-generation-coordinator
  prompt: "Generate a project with this description: A chat app for querying SQL databases in natural language"
```

## Architecture

The new two-agent workflow:
- **kb-generation-coordinator**: Reads KB, plans tasks, delegates to generator, validates outputs
- **kb-code-generator**: Executes individual tasks, generates code following KB patterns

This skill delegates to the coordinator, which orchestrates the entire process.

## Notes

- This skill is a thin wrapper - all logic lives in the coordinator agent
- Do NOT attempt to run the generator script directly
- Do NOT ask clarification questions - the coordinator handles that
- Always delegate to the coordinator for consistency

Remember: Keep this skill minimal. The coordinator orchestrates, the generator executes.
