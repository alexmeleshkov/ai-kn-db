# /create Skill

A simple skill to generate new projects using the KB-driven project generator.

## Usage

```
/create <project description>
```

## Examples

```
/create A chat app where users can query SQL databases in natural language
```

```
/create An inventory management system with React and FastAPI
```

```
/create A real-time dashboard for monitoring system metrics
```

## How It Works

1. The `/create` skill receives your project description
2. Delegates to the `project-creator` agent
3. The agent invokes `scripts/new-project` with your description
4. The generator:
   - Matches your description to the best KB project template
   - Resolves the technology stack
   - Scaffolds the project structure
   - Extracts and applies style preferences (colors, fonts)
   - Creates a runnable project in `generated/<slug>-<timestamp>/`

## Output

The generated project will be in:
```
generated/<slug>-<timestamp>/
```

The agent provides:
- Absolute path to the generated project
- Instructions on how to run it
- Next steps for development

## MVP Limitations

For the initial MVP:
- No clarification questions (generates directly from your description)
- Single KB reference project available (db-chat-nl)
- No automatic smoke tests

## Related Files

- Skill definition: `.claude/skills/create/SKILL.md`
- Project Creator Agent: `.claude/agents/project-creator.md`
- Generator script: `scripts/new-project`
- Core generator: `scripts/kb/generate_from_kb.py`
