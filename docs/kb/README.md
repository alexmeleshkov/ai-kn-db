# Knowledge Base (KB)

This is a knowledge graph of software development patterns, organized for the Explanator Agent to answer questions about technologies, features, and best practices.

## Structure

```
docs/kb/
├── projects/           # Reference projects with implementation examples
├── features/           # Abstract, code-agnostic capabilities
│   ├── *.md           # Backend/system features (authentication, data-streaming)
│   └── ui/            # UI layouts, visual components, user interfaces
├── technologies/       # Specific implementations (libraries, frameworks, platforms)
├── languages/          # Programming and styling languages
├── business-goals/     # Business objectives and requirements
├── insights/           # Project-specific learnings and decisions
└── people/             # Team expertise and profiles
```

---

## Entity Types

### Projects
**Location**: `projects/<project-id>/`

**Files**:
- `meta.yaml` - Project metadata, capabilities, technologies
- `features.md` - Links to feature documentation
- `tech.md` - Links to technology documentation
- `architecture.md` - Architectural patterns and decisions
- `modules.md` - Module structure (code-agnostic)

**Purpose**: Reference implementations demonstrating how features and technologies work together.

---

### Features
**Location**: `features/<feature-name>.md`

**Abstract, code-agnostic capabilities** for backend/system functionality (e.g., authentication, data-streaming, natural-language-sql).

**Key principle**: Features describe **WHAT** (user-facing capability), not **HOW** (implementation).

**Example**: `authentication.md` describes auth patterns generically, not JWT specifically.

**UI Features Subfolder**: `features/ui/<ui-feature-name>.md`
- Visual interface patterns and layouts (e.g., chat-interface, sidebar-navigation, admin-panel)
- Describe **WHAT USERS SEE** (layout, appearance, interaction), not code implementation
- Example: `chat-interface.md` describes chat layout, message display, input positioning

---

### Technologies
**Location**: `technologies/<technology-name>.md`

**Specific implementations** (e.g., jwt, bcrypt, postgresql, fastapi, docker).

**Key principle**: Technologies describe **HOW** to implement something.

**Example**: `jwt.md` describes JSON Web Tokens specifically, `bcrypt.md` describes password hashing.

---

### Languages
**Location**: `languages/<language-name>.md`

**Programming and styling languages** (e.g., python, typescript, css).

**Includes**: Conventions, style guides, common libraries.

**Code Snippets**: `languages/<language>/snippets/` - Language × Technology specific examples.

---

### Business Goals
**Location**: `business-goals/<goal-name>.md`

**Business objectives** with problem statements, success metrics, required features.

---

### Insights
**Location**: `insights/<project-id>/<insight-name>.md`

**Project-specific learnings**: Architecture decisions, performance optimizations, lessons learned.

**Metadata**: Author, date, category (architecture-decision, performance, security, etc.).

---

### People
**Location**: `people/<person-name>.yaml`

**Team expertise profiles**: Technologies, languages, project ownership, specializations.

---

## Knowledge Graph

```
Business Goal → Projects → Features + Technologies
                              ↓
                    Language × Technology = Code Snippets
```

**Relationships**:
- Business goals require features
- Projects implement features using technologies
- Technologies have code snippets in different languages
- People own projects and have expertise in technologies
- Insights document learnings from projects

---

## Templates

Each entity type has a `_template.md` or `_template.yaml` showing the expected structure.

---

## Language Requirement

All KB documentation must be written in **English**.

---

## Purpose

This KB enables the **Explanator Agent** to:
- Answer "What technology should I use for X?"
- Explain "How does feature X work?"
- Recommend "What's the best practice for Y?"
- Navigate relationships between business goals, features, and technologies
