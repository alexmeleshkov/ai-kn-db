# [Technology Name] - Implementation Patterns

**Technology**: [Full technology name with version]
**Category**: [Framework / Library / Database / Service]
**Language**: [Primary programming language]

---

## Overview

**What it is**: [Brief description of the technology]

**Why we use it**:
- [Key reason 1]
- [Key reason 2]
- [Key reason 3]

**Common use cases**:
- [Use case 1]
- [Use case 2]
- [Use case 3]

---

## Installation & Setup

### Package Installation

**Backend (if applicable)**:
```bash
pip install [package-name]==[version]
```

**Frontend (if applicable)**:
```bash
npm install [package-name]@[version]
```

### Configuration

**Environment Variables**:
```bash
[VAR_NAME]=[description]
[ANOTHER_VAR]=[description]
```

**Configuration File** ([filename]):
```[language]
[Show configuration structure with comments]
```

### Initialization

**Application Setup**:
```[language]
[Show initialization code with all necessary imports and setup]
```

---

## Common Patterns

### Pattern 1: [Pattern Name]

**Purpose**: [What this pattern achieves]

**When to use**: [Scenarios where this pattern is appropriate]

**Implementation**:
```[language]
[Complete code example showing the pattern]
```

**Key points**:
- [Important aspect 1]
- [Important aspect 2]
- [Gotcha or consideration]

**Example usage**:
```[language]
[Show how to use this pattern in practice]
```

---

### Pattern 2: [Next Pattern]

[Repeat structure for each common pattern]

---

## Integration with Other Technologies

### With [Technology A]

**Integration point**: [How they connect]

**Pattern**:
```[language]
[Show integration code]
```

**Configuration**:
```
[Any special configuration needed]
```

---

### With [Technology B]

[Repeat for other common integrations]

---

## Best Practices

### 1. [Best Practice Category]

**Do**:
- [Recommended approach]
- [Another recommendation]

**Don't**:
- [Anti-pattern to avoid]
- [Common mistake]

**Example**:
```[language]
[Show the right way to do it]
```

---

### 2. [Next Category]

[Repeat for other categories]

---

## Error Handling

### Common Errors

**Error: [Error type or message]**
- **Cause**: [Why this happens]
- **Solution**: [How to fix]
- **Prevention**: [How to avoid]

**Example**:
```[language]
[Show error handling code]
```

---

### Debugging Tips

1. [Tip 1]
2. [Tip 2]
3. [Tip 3]

---

## Performance Optimization

### Optimization 1: [Technique]

**Problem**: [What performance issue this addresses]

**Solution**:
```[language]
[Show optimized code]
```

**Impact**: [Expected improvement]

---

### Optimization 2: [Next Technique]

[Repeat for other optimizations]

---

## Security Considerations

### 1. [Security Concern]

**Risk**: [What the security issue is]

**Mitigation**:
```[language]
[Show secure implementation]
```

**Why this matters**: [Impact of not following this]

---

### 2. [Next Concern]

[Repeat for other security topics]

---

## Testing Patterns

### Unit Testing

**Testing approach**: [How to test components using this technology]

**Example**:
```[language]
[Show test example]
```

**Key considerations**:
- [Testing consideration 1]
- [Testing consideration 2]

---

### Integration Testing

**Testing approach**: [How to test integration points]

**Example**:
```[language]
[Show integration test]
```

---

## Version-Specific Notes

### Version [X.Y]

**Breaking changes**:
- [Change 1]
- [Change 2]

**New features**:
- [Feature 1]
- [Feature 2]

**Migration guide**:
```[language]
[Show before/after code for migration]
```

---

### Version [X.Z]

[Repeat for other significant versions]

---

## Common Pitfalls

### Pitfall 1: [Description]

**Problem**: [What goes wrong]

**Why it happens**: [Root cause]

**Solution**: [How to fix or avoid]

**Example**:
```[language]
// Bad
[Show problematic code]

// Good
[Show correct code]
```

---

### Pitfall 2: [Next Pitfall]

[Repeat for other common pitfalls]

---

## Resources

**Official Documentation**: [URL]

**Useful Guides**:
- [Guide 1] - [URL]
- [Guide 2] - [URL]

**Community Resources**:
- [Resource 1] - [URL]
- [Resource 2] - [URL]

**Related Technologies**:
- [Tech 1] - [How it relates]
- [Tech 2] - [How it relates]

---

## Framework-Specific Conventions

### File Organization

```
[Show typical file structure for projects using this technology]
```

### Naming Conventions

- **[Component Type]**: [Naming pattern]
- **[Another Type]**: [Naming pattern]

### Code Style

```[language]
[Show idiomatic code style for this technology]
```

---

## Real-World Usage Examples

### Example 1: [Scenario]

**Context**: [What this example demonstrates]

**Code**:
```[language]
[Complete working example]
```

**Explanation**:
- [Key point 1]
- [Key point 2]

---

### Example 2: [Next Scenario]

[Repeat for other examples]

---

## Source Attribution

**Extracted from**:
- Project: [project-id]
- Files: [list of source files]
- Patterns observed: [number] instances

**Completeness**: [Description of what patterns were captured]

---

## TEMPLATE USAGE INSTRUCTIONS

### Extraction Process

1. **Identify Technology Usage**:
   - Find all references in `docs/kb/projects/[project-id]/tech.md`
   - Scan modules.md for actual usage patterns
   - Check architecture.md for architectural decisions

2. **Document Patterns**:
   - Extract real code examples from modules.md
   - Show complete setup and initialization
   - Include error handling and edge cases
   - Document integration patterns with other techs

3. **Quality Standards**:
   - All code examples must be complete and runnable
   - Include version numbers where applicable
   - Explain WHY, not just WHAT
   - Show both correct and incorrect usage
   - Include real-world context

4. **File Naming Convention**:
   - Use lowercase with hyphens: `[tech-name]/patterns.md`
   - Example: `react-18/patterns.md`
   - Example: `fastapi/patterns.md`
   - Example: `postgresql/patterns.md`

5. **Cross-References**:
   - Link to related features that use this technology
   - Reference other technologies commonly used together
   - Point to official documentation
