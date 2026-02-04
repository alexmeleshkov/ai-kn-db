# [Feature Name]

**Feature ID**: [category].[variant]
**Capability**: [capability_name_from_meta_yaml]
**Technologies**: [tech1], [tech2], [tech3]

---

## Overview

[Brief description of what this feature does and its key characteristics]

**Key characteristics**:
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]
- [Add more as needed]

---

## File Structure

```
[Show the file structure for this feature]
backend/app/
  api/
    [routes_file].py          # [Brief description]
  services/
    [service_file].py         # [Brief description]
  models/
    [model_file].py           # [Brief description]
```

---

## Implementation Patterns

### 1. [Component Name] ([filename])

**Purpose**: [What this component does]

**Interface**:
```python
# OR ```typescript for frontend
[Show the complete interface - classes, functions, types]
```

**Complete Flow**:

1. **[Operation Name]**:
   - [Step-by-step flow with exact logic]
   - [Include all conditionals, loops, error paths]
   - [Show data transformations]
   - [Reference line numbers if from scan]

2. **[Next Operation]**:
   - [Detailed steps]

**All Behaviors**:
- [List ALL behaviors this component exhibits]
- [Include edge cases]
- [Document default values]
- [State management patterns]
- [Caching/optimization behaviors]

**Dependencies** (with WHY):
- [package_name] - [why it's used, what problem it solves]
- [another_package] - [specific reason for inclusion]

**Error Handling**:
- [Error type]: [How it's handled, what's returned]
- [Exception]: [Recovery strategy]
- [Edge case]: [Behavior]

**Integration Points**:
- Calls [other_module].[method] → [what it returns]
- Called by [component] via [mechanism]
- Returns [data structure] for [consumer]

**Edge Cases**:
- [Scenario]: [Behavior]
- [Unusual input]: [How it's handled]

**Module Exports**:
```python
# [filename] exports:
[class/function]    # [Description]
[helper_function]   # [Description]
```

**Initialization Patterns**:
```python
[Show any initialization code, singleton patterns, factory functions]
```

**Constants and Configuration**:
```python
[Show all constants, defaults, config values used]
```

---

### 2. [Next Component]

[Repeat the same structure for each major component in the feature]

---

## Dependencies

**Backend Python packages** (if applicable):
- `[package]` - [Description and version]

**Frontend NPM packages** (if applicable):
- `[package]` - [Description and version]

**Configuration (environment variables)**:
- `[VAR_NAME]` - [Description and example]

**System requirements**:
- [Requirement] - [Why it's needed]

---

## Integration Points

### How Other Modules Use This Feature

**[Consumer Module Name]** ([filename]):
```python
[Show exact usage example from codebase]
```

[List all known consumers and their usage patterns]

---

## Usage Examples

### 1. [Use Case Name]

**Request**:
```http
[Show exact HTTP request or code invocation]
```

**Response** ([status code]):
```json
[Show exact response format]
```

**Error** ([error status]):
```json
[Show error response format]
```

### 2. [Next Use Case]

[Repeat for common scenarios]

### 3. Using in Code

**[Operation Name]**:
```python
[Show code example with all necessary imports and context]
```

---

## Security Considerations

### [Security Aspect 1]
- [Security measure]
- [Protection mechanism]
- [Best practice]

### [Security Aspect 2]
- [Details]

---

## Testing Patterns

### Unit Tests

**Test [scenario]**:
```python
[Show test example with setup, execution, assertions]
```

### Integration Tests

**Test [flow]**:
```python
[Show integration test example]
```

---

## Line Count Verification

**Source lines extracted**:
- [source_file] lines [start]-[end] ([component]): [N] lines
- [another_file] lines [start]-[end] ([component]): [N] lines

**Total source lines**: [N] lines

**Output document lines**: ~[N] lines (including examples, usage, testing)

**Information completeness**: [X]% - [Describe what was captured and any additions made]

---

## TEMPLATE USAGE INSTRUCTIONS

### Extraction Process

1. **Identify Source Material**:
   - Find relevant sections in `docs/kb/projects/[project-id]/modules.md`
   - Note line ranges for line count verification
   - Check architecture.md, tech.md for additional context

2. **Complete the 19-Point Pattern Extraction**:
   - Purpose statement
   - Complete interface definition
   - Complete flow (all operations step-by-step)
   - All behaviors (including defaults, caching, state)
   - Dependencies with WHY explanations
   - Error handling for all paths
   - Integration points (who calls, who's called)
   - Edge cases
   - Module exports
   - Initialization patterns
   - Constants and configuration
   - Security considerations
   - Testing patterns
   - Usage examples (code + HTTP)
   - Documentation quality check
   - Line count verification
   - Source citations
   - Completeness assessment
   - Related patterns cross-reference

3. **File Naming Convention**:
   - Use descriptive names: `[feature-category]/[implementation-variant].md`
   - Example: `authentication/jwt-bcrypt.md`
   - Example: `nl-to-sql/claude-tool-use.md`
   - Example: `data-streaming/sse-fastapi.md`

4. **Quality Gates**:
   - All code examples must be runnable (no placeholders)
   - All interfaces must be complete
   - All flows must include error paths
   - All dependencies must explain WHY
   - Line counts must match source material

5. **Feature ID Format**:
   - Format: `[category].[variant]`
   - Example: `authentication.jwt-bcrypt`
   - Example: `nl-to-sql.claude-tool-use`
   - Must be globally unique across all features

### When to Split Features

Split into multiple files when:
- Multiple independent implementations exist (e.g., different auth providers)
- Different technology stacks (e.g., REST vs GraphQL)
- Distinct architectural patterns (e.g., synchronous vs streaming)

Keep as single file when:
- Components are tightly coupled
- All code serves single capability
- Splitting would create excessive duplication
