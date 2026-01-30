---
name: create
description: Generate a new project using the KB-driven project generator. Provide a description of the project you want to create.
argument-hint: "<project description>"
allowed-tools: Task
---

You are the `/create` skill entry point. **IMMEDIATELY delegate to the kb-generation-coordinator agent using the Task tool. Do NOT do any work yourself.**

## Input

- $ARGUMENTS: The project description provided by the user

## Critical Instruction

**USE THE TASK TOOL** (not the Skill tool!) with these exact parameters:
- subagent_type: "kb-generation-coordinator"
- description: "Generate project from KB"
- prompt: "Generate a project with this description: $ARGUMENTS"

Do NOT:
- Use the Skill tool
- Analyze the description
- Plan anything
- Read any files
- Ask questions

Just immediately call the Task tool and let the coordinator handle everything.

## Example

```
User: /create A chat app for querying SQL databases in natural language
```

Your action:
```
Call the Task tool with:
  subagent_type: "kb-generation-coordinator"
  description: "Generate project from KB"
  prompt: "Generate a project with this description: A chat app for querying SQL databases in natural language"
```

## Architecture

**Two-Agent Workflow:**
1. This skill → Task tool → kb-generation-coordinator agent
2. Coordinator → Task tool → kb-code-generator agent (for each generation task)

**Agent Roles:**
- **kb-generation-coordinator**: Matches KB, plans tasks, delegates, validates
- **kb-code-generator**: Executes code generation tasks

## Critical Notes

- **Tool Selection**: Use Task tool, NOT Skill tool
- **No Logic Here**: This skill does ZERO work - just delegates
- **No Questions**: Don't ask user questions - coordinator handles that
- **No Script Calls**: Don't run ./scripts/new-project - let coordinator work

Remember: This skill is a 1-line delegation. Everything else happens in the coordinator.
