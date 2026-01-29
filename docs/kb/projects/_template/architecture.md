# Architecture

> **Purpose**: Document WHY behind architectural choices and system design.
> Focus on decisions that inform structural patterns during generation.

## Architecture Pattern

**Pattern**: [pattern name]

**Why chosen**:
- [reason 1]
- [reason 2]
- [reason 3]

**Trade-offs**:
- ✅ [advantage 1]
- ✅ [advantage 2]
- ⚠️ [limitation 1]
- ⚠️ [limitation 2]

---

## System Components

### High-Level Diagram

```
[ASCII diagram showing component relationships]
```

---

### [Component 1 Name]

**Responsibility**: [what this component does]

**Key subsystems**:
- [subsystem 1]: [purpose]
- [subsystem 2]: [purpose]
- [subsystem 3]: [purpose]

**Technologies**: [list]

---

### [Component 2 Name]

**Responsibility**: [what this component does]

**Key layers**:
1. [layer 1] (`path`): [responsibility]
2. [layer 2] (`path`): [responsibility]
3. [layer 3] (`path`): [responsibility]

---

### [Component 3 Name]

**Responsibility**: [what this component does]

**Design approach**: [approach description]

**Key entities**:
- [entity 1]: [purpose and key fields]
- [entity 2]: [purpose and key fields]
- [entity 3]: [purpose and key fields]

---

## Communication Patterns

### [Component A] ↔ [Component B]

**Protocol**: [protocol]

**Patterns**:
1. [pattern 1]: [description]
2. [pattern 2]: [description]
3. [pattern 3]: [description]

**Why this approach**:
- [reason 1]
- [reason 2]

---

### [Component C] ↔ [Component D]

**Protocol**: [protocol]

**Patterns**:
- [pattern 1]
- [pattern 2]
- [pattern 3]

---

## Data Architecture

### [Entity/Table 1]

```
[schema definition in appropriate format]
```

### [Entity/Table 2]

```
[schema definition]
```

**Indexes**:
- [index 1]: [purpose]
- [index 2]: [purpose]

---

### Data Flow: [Key Operation]

1. [step 1]: [what happens]
2. [step 2]: [what happens]
3. [step 3]: [what happens]
4. [step 4]: [what happens]
5. [step 5]: [what happens]

---

## API Design

### [API Convention]

**Endpoint structure**: [pattern]

**Response format**:
```
[example response structure]
```

**Error format**:
```
[example error structure]
```

---

### [Key Flow Name]

1. [step 1]: [endpoint/method]
   - Input: [structure]
   - Output: [structure]
2. [step 2]: [endpoint/method]
   - Input: [structure]
   - Output: [structure]

---

## Design Decisions

### Decision 1: [Name]

**Context**: [problem that needed solving]

**Options considered**:
1. [option 1]
2. [option 2]
3. [option 3]

**Choice**: [chosen option]

**Rationale**:
- [reason 1]
- [reason 2]
- [reason 3]

**Implications**:
- ✅ [advantage]
- ⚠️ [limitation]

---

### Decision 2: [Name]

**Context**: [problem]

**Options considered**:
1. [option 1]
2. [option 2]

**Choice**: [chosen option]

**Rationale**:
- [reason 1]
- [reason 2]

**Implications**:
- ✅ [advantage]
- ⚠️ [limitation]

---

## Quality Attributes

### Modularity
**Rating**: [low / medium / high]
**Evidence**: [specific evidence]

### Testability
**Rating**: [low / medium / high]
**Evidence**: [how testing is enabled]

### Performance
**Rating**: [low / medium / high]
**Expected**: [performance characteristics]

### Security
**Rating**: [low / medium / high]
**Measures**: [security approaches]

### Scalability
**Rating**: [low / medium / high]
**Current capacity**: [description]
**Bottleneck**: [known limitation]

---
