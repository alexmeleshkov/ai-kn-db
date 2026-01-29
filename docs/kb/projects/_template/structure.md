# Project Structure

> **Purpose**: Document the directory layout and file organization.
> This file informs project scaffolding and file placement during generation.
>
> **This is a TEMPLATE showing structure** - the scanner will fill with actual paths.

## Directory Tree

```
[project-root]/
├── [backend-dir]/                    # Backend/server code (or main application for CLI/monorepo)
│   ├── [source-dir]/                 # Main source code directory
│   │   ├── [entry-file].[ext]       # Application entry point
│   │   ├── [config-file].[ext]      # Configuration and settings
│   │   ├── [models-dir]/             # Data models / Domain entities
│   │   │   ├── [model1].[ext]
│   │   │   └── [model2].[ext]
│   │   ├── [routes-or-handlers-dir]/ # API endpoints / Request handlers
│   │   │   ├── [route1].[ext]
│   │   │   ├── [route2].[ext]
│   │   │   └── [route3].[ext]
│   │   ├── [services-or-logic-dir]/  # Business logic / Core services
│   │   │   ├── [service1].[ext]
│   │   │   ├── [service2].[ext]
│   │   │   └── [service3].[ext]
│   │   ├── [schemas-or-types-dir]/   # Type definitions / Validation schemas
│   │   │   ├── [schema1].[ext]
│   │   │   └── [schema2].[ext]
│   │   └── [utils-dir]/              # Utility functions / Helpers
│   │       ├── [util1].[ext]
│   │       └── [util2].[ext]
│   ├── [tests-dir]/                  # Test suite
│   │   ├── [test-file1].[ext]
│   │   ├── [test-file2].[ext]
│   │   └── [test-config].[ext]       # Test fixtures/config
│   ├── [migrations-dir]/             # Database migrations (if applicable)
│   │   └── [migration-files]
│   ├── [dependencies-file]           # Dependency manifest (requirements.txt, package.json, Cargo.toml, go.mod)
│   ├── [env-example]                 # Environment variable template
│   ├── [dockerfile]                  # Container definition (if using Docker)
│   └── [readme]                      # Backend-specific documentation
│
├── [frontend-dir]/                   # Frontend application (if web app with separate frontend)
│   ├── [public-or-static-dir]/       # Static assets
│   │   ├── [asset1]
│   │   └── [asset2]
│   ├── [source-dir]/                 # Source code
│   │   ├── [entry-file].[ext]       # Entry point (main.tsx, index.js, App.vue)
│   │   ├── [root-component].[ext]   # Root component
│   │   ├── [components-dir]/        # UI components
│   │   │   ├── [category1]/         # Grouped by feature/domain
│   │   │   │   ├── [Component1].[ext]
│   │   │   │   └── [Component2].[ext]
│   │   │   ├── [category2]/
│   │   │   │   ├── [Component3].[ext]
│   │   │   │   └── [Component4].[ext]
│   │   │   └── [shared-or-common]/  # Reusable components
│   │   │       ├── [SharedComp1].[ext]
│   │   │       └── [SharedComp2].[ext]
│   │   ├── [pages-or-views-dir]/    # Page-level components (if using router)
│   │   │   ├── [Page1].[ext]
│   │   │   ├── [Page2].[ext]
│   │   │   └── [Page3].[ext]
│   │   ├── [hooks-or-composables]/  # Custom hooks/composables/stores
│   │   │   ├── [hook1].[ext]
│   │   │   ├── [hook2].[ext]
│   │   │   └── [hook3].[ext]
│   │   ├── [contexts-or-stores]/    # State management
│   │   │   ├── [context1].[ext]
│   │   │   └── [store1].[ext]
│   │   ├── [services-or-api-dir]/   # API client / Service layer
│   │   │   ├── [api-client].[ext]
│   │   │   └── [api-endpoints].[ext]
│   │   ├── [utils-dir]/             # Utility functions
│   │   │   ├── [util1].[ext]
│   │   │   └── [util2].[ext]
│   │   ├── [types-or-interfaces]/   # Type definitions
│   │   │   ├── [types1].[ext]
│   │   │   └── [types2].[ext]
│   │   └── [styles-dir]/            # Styling (if not component-colocated)
│   │       ├── [global].[ext]
│   │       └── [theme].[ext]
│   ├── [tests-dir]/                 # Frontend tests
│   │   ├── [test1].[ext]
│   │   └── [test2].[ext]
│   ├── [dependencies-file]          # package.json, etc.
│   ├── [build-config]               # vite.config, webpack.config, etc.
│   ├── [env-example]
│   └── [readme]
│
├── [shared-or-common-dir]/          # Shared code (if monorepo)
│   ├── [types-dir]/                 # Shared types/interfaces
│   ├── [utils-dir]/                 # Shared utilities
│   └── [constants-dir]/             # Shared constants
│
├── [config-dir]/                    # Configuration files (optional)
│   ├── [deployment-configs]
│   └── [environment-configs]
│
├── [docs-dir]/                      # Documentation (optional)
│   ├── [api-docs]
│   └── [architecture-diagrams]
│
├── [scripts-dir]/                   # Build/deployment scripts (optional)
│   ├── [build-script]
│   ├── [deploy-script]
│   └── [migration-script]
│
├── [docker-compose-file]            # Docker Compose (if using)
├── [ci-cd-config]                   # .github/workflows, .gitlab-ci.yml, etc.
├── [gitignore]
├── [readme]                         # Main project README
└── [license]
```

## Directory Descriptions

### [backend-dir] / [main-application-dir]
**Purpose**: [Server-side logic / Core application / API implementation]

**Key subdirectories**:
- `[source-dir]/`: [Main application source code]
- `[routes-or-handlers-dir]/`: [HTTP endpoints / Request handlers / CLI commands]
- `[services-or-logic-dir]/`: [Business logic separated from routing]
- `[models-dir]/`: [Data models / Domain entities / Database schemas]
- `[tests-dir]/`: [Test files mirroring source structure]

**Entry point**: `[entry-file].[ext]` - [Starts the application / Defines main function]

**Configuration**: `[config-file].[ext]` - [Environment-based config / Settings management]

---

### [frontend-dir] (if applicable)
**Purpose**: [User interface / Client application]

**Key subdirectories**:
- `[components-dir]/`: [UI components organized by feature or type]
- `[pages-or-views-dir]/`: [Top-level page components]
- `[hooks-or-composables]/`: [Reusable logic hooks / Vue composables / Svelte stores]
- `[services-or-api-dir]/`: [API client / Backend communication layer]

**Entry point**: `[entry-file].[ext]` - [Application bootstrap / Root render]

**Routing**: [How navigation is handled - React Router, Vue Router, file-based routing]

---

### [shared-or-common-dir] (if monorepo)
**Purpose**: [Code shared between frontend and backend / Multiple services]

**Contents**:
- Type definitions used across boundaries
- Validation schemas
- Constants and enums
- Utility functions

---

## File Naming Conventions

**[Describe the naming patterns used]**

Examples:
- Component files: `[PascalCase].[ext]` or `[kebab-case].[ext]`
- Service files: `[camelCase].[ext]` or `[snake_case].[ext]`
- Test files: `[name].test.[ext]` or `[name].spec.[ext]` or `test_[name].[ext]`
- Type files: `[name].types.[ext]` or `[name].interface.[ext]`

---

## Module Organization Strategy

**[Describe how modules are organized]**

Options:
- **By feature**: Each feature has its own directory with routes, services, models
- **By layer**: All routes together, all services together, all models together
- **Hybrid**: Layer separation within feature directories

**This project uses**: [Chosen strategy with rationale]

---

## Import Path Patterns

**[Show how modules import each other]**

Examples:
- Relative imports: `import { [function] } from './[relative-path]'`
- Absolute imports: `import { [function] } from '@/[absolute-path]'`
- Package imports: `import { [function] } from '[package-name]'`

**Alias configuration**: [If using path aliases, describe them]
- `@/` → `[resolved-to-directory]`
- `~/` → `[resolved-to-directory]`

---

## Configuration Files

**[List and describe key configuration files]**

Examples:
- `[dependencies-file]`: [Package manifest - dependencies and scripts]
- `[build-config-file]`: [Build tool configuration]
- `[env-example]`: [Template for environment variables]
- `[docker-compose-file]`: [Multi-container orchestration]
- `[ci-cd-config]`: [Continuous integration/deployment]

---

## Capability Mapping

**[Map features to file locations - helps with targeted generation]**

| Capability | Backend Files | Frontend Files |
|------------|--------------|----------------|
| [Feature 1 - e.g., Authentication] | `[backend-paths]` | `[frontend-paths]` |
| [Feature 2 - e.g., Data Query] | `[backend-paths]` | `[frontend-paths]` |
| [Feature 3 - e.g., User Profile] | `[backend-paths]` | `[frontend-paths]` |

---

## Build Artifacts

**[Describe generated/compiled directories - should be in .gitignore]**

- `[build-output-dir]/` - [Compiled/bundled code]
- `[dist-dir]/` - [Distribution files]
- `[cache-dir]/` - [Build cache]
- `[coverage-dir]/` - [Test coverage reports]

---
