# Core Modules

> **CRITICAL**: This file must include IMPLEMENTATION PATTERNS with code snippets.
> These patterns enable 1:1 project generation without guessing.
>
> **This is a TEMPLATE showing structure** - the scanner will fill with actual code.

## [Section Name - e.g., Backend Services / Frontend Components / Core Logic]

### 1. [filename].[ext] - [Module Purpose in 5-10 words]

**Responsibilities**:
- [Specific responsibility 1 - be concrete, not generic]
- [Specific responsibility 2]
- [Specific responsibility 3]

**Key Functions/Methods**:
- `[function_name]([param1]: [type], [param2]: [type]) -> [return_type]` - [What it does]
- `[another_function]([params]) -> [return]` - [Purpose and behavior]
- `[third_function]([params])` - [Side effects if any]

**Code Pattern**:
```[language]
[Show 15-30 lines of ACTUAL implementation from the reference repo]
[Include: imports/requires, function signatures, key logic, error handling]
[Show real patterns: async/await, error handling, data transformation]
[NOT pseudocode - real code that compiles/runs]

[Example structure - DO NOT use this exact code:]
import [necessary_libraries]

[type_definitions_or_interfaces]

function [core_function]([params_with_types]): [return_type] {
  [validation_or_setup]

  [main_logic_with_error_handling]

  return [result]
}

[Show 1-2 more key functions if critical to understanding]
```

**Dependencies**: [package-name]>=[version], [another-package]
**Environment Variables**: [VAR_NAME], [ANOTHER_VAR]
**Configuration**: [Config file path or special settings if needed]

**Integration Points**:
- Calls: [module_name], [another_module], [external_api]
- Called by: [consuming_module], [route_handler]
- External services: [database_name], [api_name], [queue_name]

---

### 2. [another_filename].[ext] - [Another Purpose]

**Responsibilities**:
- [Responsibility 1]
- [Responsibility 2]

**Key Functions/Methods**:
- `[function_signature]` - [Behavior]

**Code Pattern**:
```[language]
[Show actual implementation - class-based example structure]

class [ClassName] {
  [Show constructor/initialization]
  constructor([dependencies]) {
    [dependency_injection_or_setup]
  }

  [Show 1-2 key methods with full implementation]
  async [method_name]([params]): [return_type] {
    [validation]
    [core_logic]
    [error_handling]
    return [result]
  }
}

[Export or usage pattern]
```

**Dependencies**: [list]
**Environment Variables**: [list]
**Error Handling**: [Approach - e.g., try/catch with custom errors, Result<T,E>, panic]

---

## [Another Section - e.g., Frontend Components / API Handlers / CLI Commands]

### 3. [ComponentOrModuleName].[ext] - [Purpose]

**Component Contract** (if applicable):
```[language]
[Show interface/props/public API]

interface [Name] {
  [field]: [type];
  [optional_field]?: [type];
  [callback]?: ([param]: [type]) => [return];
}
```

**Code Pattern**:
```[language]
[Show complete implementation - component example structure]

[imports]

export [const|function|class] [Name] = ([params]) => {
  [Show state management - hooks, signals, observables, etc.]

  [Show event handlers or methods]

  [Show render/return logic or main execution]

  return [result_structure]
}

[OR for class-based]
export class [Name] {
  [properties]

  [methods_with_full_implementation]
}
```

**Dependencies**: [framework], [libraries]
**State Management**: [Approach used - Context, Redux, Signals, etc.]
**Styling Approach**: [CSS modules, Tailwind, styled-components, etc.]

---

## [Section for Utilities/Helpers/Shared Code]

### 4. [utils_or_helper_file].[ext] - [Utility Purpose]

**Exported Functions**:
- `[function_name]([params])` - [What it does]
- `[another_function]([params])` - [Purpose]

**Code Pattern**:
```[language]
[Show utility functions with full implementation]

export function [utility_name]([param]: [type]): [return_type] {
  [full_implementation]
  return [result]
}

export const [constants_or_config] = {
  [KEY]: [value],
  [ANOTHER_KEY]: [value]
}

[Show 2-3 actual utility functions from reference]
```

**Usage Example**:
```[language]
[Show how other modules import and use this]
import { [function], [constant] } from '[path]'

const [result] = [function]([args])
```

---

## [Section for Data Layer - if applicable]

### 5. [database_or_storage_file].[ext] - [Data Access Purpose]

**Responsibilities**:
- [Database connection management / File I/O / API client]
- [Query execution / Data persistence]
- [Schema validation / Data transformation]

**Code Pattern**:
```[language]
[Show connection/initialization pattern]

export function [create_connection_or_client](): [Type] {
  return new [Client]({
    [configuration_from_env_vars]
  })
}

[Show query/access patterns]
export async function [query_or_operation]<T>([params]): Promise<T> {
  const [connection] = await [get_connection]()
  try {
    [execute_operation]
    return [result]
  } catch ([error]) {
    [error_handling]
  } finally {
    [cleanup]
  }
}

[Show 1-2 more critical data operations]
```

**Dependencies**: [database_driver], [ORM], [connection_pool_library]
**Environment Variables**: [DB_HOST], [DB_PORT], [DB_NAME], [DB_USER], [DB_PASSWORD]
**Migration Strategy**: [How schema changes are managed - Alembic, Flyway, migrations folder]

---
