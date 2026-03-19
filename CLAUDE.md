# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI knowledge database stored in a **FalkorDB graph database**, accessed via the `kb-graph` MCP server. The KB contains projects, features, technologies, languages, snippets, people, and business goals organized as a property graph.

## Knowledge Graph Structure

```
Project HAS Feature, Technology, Language, Snippet, Detail
Feature USES Technology
Technology HAS Snippet
Language HAS Snippet
Person KNOWS Technology, Language
Detail ABOUT Technology, Feature
BusinessGoal HAS Project
```

**Entity Types** (8): Project, Feature, Technology, Language, Snippet, Detail, Person, BusinessGoal

**Details**: Detail nodes store project-specific implementation information. When an entity (Technology/Feature) is used differently across projects, Details split generic knowledge (in the entity node) from project-specific usage patterns (in Detail nodes). Query `Detail -[:ABOUT]-> Technology` to get project-specific implementation details.

## Using the Knowledge Base

Use `/ask` to query the KB via the **user-guide agent**:

```
/ask What technology should I use for authentication?
/ask Show me projects using PostgreSQL and FastAPI
/ask How does SSE streaming work?
/ask Who knows Python?
```

The user-guide agent queries FalkorDB directly using Cypher and returns structured answers with code examples.

## Agents

- `.claude/agents/user-guide.md` - KB navigator, answers questions about projects, features, and technologies via the kb-graph MCP server

## Language Rule

All documentation and code comments must be written in English.
