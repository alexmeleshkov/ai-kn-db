---
name: create
description: Generate a new project using the KB-driven project generator. Provide a description of the project you want to create.
argument-hint: "<project description>"
allowed-tools: Task
context: fork
---

You are the `/create` skill entry point. Your only job is to delegate to the project-creator agent.

## Input

- $ARGUMENTS: The project description provided by the user

## Workflow

1. Extract the project description from $ARGUMENTS
2. Use the Task tool to invoke the `project-creator` agent
3. Pass the project description to the agent
4. Let the agent handle the entire generation workflow

## Example

```
User: /create A chat app for querying SQL databases in natural language
```

Your action:
```
Use Task tool with:
  agent: project-creator
  message: "Generate a project with this description: A chat app for querying SQL databases in natural language"
```

## Notes

- This skill is a thin wrapper - all logic lives in the project-creator agent
- Do NOT attempt to run the generator script directly
- Do NOT ask clarification questions - the agent handles that
- Always delegate to the agent for consistency

Remember: Keep this skill minimal. The agent does the real work.
