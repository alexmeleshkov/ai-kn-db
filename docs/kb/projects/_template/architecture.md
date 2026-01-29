# Architecture

> **Purpose**: Document the WHY behind architectural choices and system design.
> This file informs structural decisions during generation.

## Architecture Pattern

**Pattern**: [Your Architecture Pattern - e.g., Layered Monolith, Microservices, Event-Driven, Hexagonal, MVC, Clean Architecture]

**Rationale**:
- [Why this pattern was chosen - e.g., simplicity, scalability, team expertise]
- [How it supports the business requirements]
- [Future considerations - e.g., migration paths, evolution strategy]

**Trade-offs**:
- ✅ **Advantages**: [List specific benefits for this project]
- ⚠️ **Disadvantages**: [List known limitations accepted]

**Alternative considered**: [Other pattern evaluated]
- **Rejected because**: [Specific reasons for not choosing alternative]

---

## System Components

### High-Level Architecture Diagram

```
[Draw ASCII diagram showing your system components]

Example formats:
- Web app: Client ◄─► Frontend ◄─► Backend ◄─► Database
- API: Client ◄─► API Gateway ◄─► Services ◄─► Data Store
- CLI: User ◄─► CLI ◄─► Core Logic ◄─► File System
- Microservices: Client ◄─► Gateway ◄─► [Service A, Service B, Service C] ◄─► [DB, Queue, Cache]
```

---

### [Component 1 Name - e.g., Frontend/API Layer/CLI Interface]

**Responsibility**: [What this component does - be specific]

**Key Subsystems**:
- **[Subsystem 1]**: [Purpose and approach]
- **[Subsystem 2]**: [Purpose and approach]
- **[Subsystem 3]**: [Purpose and approach]

**Technologies**: [List actual technologies used]

**Why this approach**: [Rationale for design choices - reference tech.md for details]

---

### [Component 2 Name - e.g., Backend/Core Logic/Service Layer]

**Responsibility**: [What this component does]

**Key Layers** (if layered):
1. **[Layer 1]** (`path/to/layer`): [Responsibility]
2. **[Layer 2]** (`path/to/layer`): [Responsibility]
3. **[Layer 3]** (`path/to/layer`): [Responsibility]

**Why this structure**:
- [Reason 1 - e.g., separation of concerns]
- [Reason 2 - e.g., testability]
- [Reason 3 - e.g., reusability]

---

### [Component 3 Name - e.g., Database/Data Store/State Management]

**Responsibility**: [What this component does]

**Design Approach**: [e.g., Relational/NoSQL/Document/Key-Value/In-Memory/File-based]

**Key Entities** (if applicable):
- **[Entity 1]**: [Purpose and key fields]
- **[Entity 2]**: [Purpose and key fields]
- **[Entity 3]**: [Purpose and key fields]

**Technology**: [Actual database/store technology used]

**Migration Strategy**: [How schema changes are managed - if applicable]

---

### [External Dependencies Section - Optional]

#### [External Service/API 1]
**Purpose**: Natural language to SQL generation
**Integration**: `services/llm.py` using official `anthropic` SDK
**Failure handling**: Graceful error messages, no fallback in MVP

#### Database Connection (Azure SQL / PostgreSQL)
**Purpose**: Execute generated SQL queries
**Integration**: `services/database.py` using appropriate driver
**Failure handling**: Connection pooling, timeout handling, retry logic

---

## Communication Patterns

### [Component A] ↔ [Component B]

**Protocol**: [Communication protocol - e.g., HTTP/HTTPS, gRPC, WebSocket, Message Queue, IPC]

**Patterns**:
1. **[Pattern 1]**: [Description]
   - [Key characteristic or example]
2. **[Pattern 2]**: [Description]
   - [Key characteristic or example]
3. **[Pattern 3]**: [Description - e.g., Authentication approach]
   - [Implementation detail]

**Why [this approach] instead of [alternative]**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

---

### [Component C] ↔ [Component D]

**Protocol**: [Communication protocol]

**Patterns**:
- [Pattern 1 - e.g., Connection pooling, retry logic]
- [Pattern 2 - e.g., Query optimization, caching]
- [Pattern 3 - e.g., Transaction handling]
- [Pattern 4 - e.g., Error handling strategy]

---

## Data Architecture

### [Data Schema/Structure]

**[Entity/Table 1]**:
```
[Show actual schema definition in appropriate format]

Examples:
- SQL: CREATE TABLE ...
- NoSQL: Document structure { }
- GraphQL: type definition
- File format: JSON/YAML structure
```

**[Entity/Table 2]**:
```
[Schema definition]
```

**[Entity/Table 3]**:
```
[Schema definition]
```

**Indexes/Optimization**:
- [Index 1 - purpose]
- [Index 2 - purpose]
- [Index 3 - purpose]

---

### Data Flow: [Key Operation Name]

[Describe the step-by-step flow of data through the system for a critical operation]

1. **[Step 1]**: [What happens]
2. **[Step 2]**: [What happens - reference specific component]
3. **[Step 3]**: [What happens - reference specific module]
4. **[Step 4]**: [What happens - data transformation]
5. **[Step 5]**: [What happens - response/result]

---

## API Design (If Applicable)

### [API Convention - e.g., REST, GraphQL, RPC]

**Endpoint structure**: [Pattern - e.g., /api/v1/resource/action or verb-based]

**[Protocol] specifics**:
- [Convention 1]
- [Convention 2]
- [Convention 3]

**Response format**: [Format description]
```
[Show actual response format example]
```

**Error format**:
```
[Show actual error format example]
```

---

### [Key Flow Name - e.g., Authentication, Data Processing]

[Describe the flow with actual endpoint/method names]

1. **[Step 1]**: [Endpoint/method]
   - Input: [Structure]
   - Output: [Structure]
2. **[Step 2]**: [Endpoint/method]
   - Input: [Structure]
   - Output: [Structure]
3. **Protected routes**: Include `Authorization: Bearer <token>` header
4. **Token validation**: Middleware checks JWT signature and expiry

---

## Design Decisions

### Decision 1: [Decision Name]

**Context**: [What problem needed solving]

**Options considered**:
1. [Option 1] - [Brief description]
2. [Option 2] - [Brief description]
3. [Option 3] - [Brief description]

**Choice**: [Chosen option]

**Rationale**:
- [Reason 1 - technical]
- [Reason 2 - business/practical]
- [Reason 3 - team/organizational]
- [Reason 4 - future considerations]

**Implications**:
- ✅ [Advantage 1]
- ✅ [Advantage 2]
- ⚠️ [Limitation 1 and mitigation if any]
- ⚠️ [Limitation 2 and mitigation if any]

---

### Decision 2: [Decision Name]

**Context**: [What problem needed solving]

**Options considered**:
1. [Option 1]
2. [Option 2]
3. [Option 3]

**Choice**: [Chosen option]

**Rationale**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Implications**:
- ✅ [Advantages]
- ⚠️ [Limitations]

---

### Decision 3: [Decision Name]

**Context**: [What problem needed solving]

**Options considered**:
1. [Option 1]
2. [Option 2]
3. [Option 3]

**Choice**: [Chosen option]

**Rationale**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Implications**:
- ✅ [Advantages]
- ⚠️ [Limitations]

---

## Quality Attributes

### Modularity
**Rating**: [Low/Medium/High]
**Evidence**: [Specific evidence from codebase - reference modules.md]

### Testability
**Rating**: [Low/Medium/High]
**Evidence**: [How testing is enabled - e.g., dependency injection, mocking support]

### Performance
**Rating**: [Low/Medium/High]
**Expected**: [Specific performance characteristics - e.g., response times, throughput]

### Security
**Rating**: [Low/Medium/High]
**Measures**: [Security approaches implemented]

### Scalability
**Rating**: [Low/Medium/High]
**Current**: [Current capacity]
**Bottleneck**: [Known scaling limitations]

---

## Future Architecture Evolution

### Phase 1 (Current): [Current State]
- [Characteristic 1]
- [Characteristic 2]

### Phase 2: [Next Evolution]
- [Change 1]
- [Change 2]
- [Change 3]

### Phase 3: [Future State - if applicable]
- [Change 1]
- [Change 2]
- [Change 3]

---

## Unknowns

- [ ] **[Unknown 1]**: [Question or area needing research]
- [ ] **[Unknown 2]**: [Question or area needing validation]
- [ ] **[Unknown 3]**: [Question or area needing decision]

---
