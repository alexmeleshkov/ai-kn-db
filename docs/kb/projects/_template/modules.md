# Code Modules & Implementation Patterns

> **APPROACH**: Interface-first with code examples for complex logic only.
> This file contains interfaces, behaviors, and patterns - NOT full code dumps.
> LLMs can generate standard patterns; we store only what's unique or complex.

## File Structure Overview

```
[Show actual project directory tree with file paths]
```

**Organization Strategy**: [describe approach - by feature / by layer / hybrid]

**Import Patterns**:
- [describe import style used]
- [path aliases if any]

---

## Backend Modules

### [Module 1: filename.ext]

**Purpose**: [1-2 sentence description of what this module does]

**Interface** (ALL methods, not just main ones):
```[language]
[Class definitions, function signatures, type definitions - include ALL methods]
class ServiceName:
    def __init__(self, param: Type):
        """Initialization logic"""

    def method_name(self, param: Type) -> ReturnType:
        """Method description"""

    def _private_method(self, param: Type):
        """Even private methods"""
```

**Complete Flow** (for complex modules):
1. Step 1: Detailed description
2. Step 2: Detailed description
3. For loops/branches:
   - Condition A: What happens
   - Condition B: What happens
4. Step 4: Continue until complete algorithm is described

**All Behaviors** (complete list, not just key ones):
- Behavior 1: Full description including edge cases
- Behavior 2: Full description including performance notes
- Behavior 3: etc.
- Edge case: How X is handled
- Edge case: How Y is handled
- Optimization: Why Z is done this way

**Dependencies** (with WHY):
- library1 - used for X functionality
- library2 - used for Y functionality

**Error Handling** (complete description):
- Error type 1: How it's caught and handled
- Error type 2: How it's caught and handled
- Logging: What gets logged where
- Recovery: How errors are recovered from

**Integration Points**:
- Calls: What services/modules this calls
- Called by: What calls this service
- Data flow: Input/output patterns

**State Management** (if stateful):
- State tracked: List what state is maintained
- Initialization: How state is set up
- Updates: How state changes
- Persistence: How state is stored (if applicable)

**Performance Considerations** (if applicable):
- Caching: What is cached and why
- Async: What runs asynchronously
- Pooling: Connection/thread pools used
- Timeouts: Timeout values and handling

**Constants and Configuration** (if any):
```
CONSTANT_NAME = value  # explanation with units/meaning
CONFIG_DEFAULT = value  # why this default
MAGIC_NUMBER = value  # what it represents
```

**Template Strings** (if any - INCLUDE FULL TEXT):
```
TEMPLATE_NAME = """
[Complete template text with {placeholders}]
"""
```

**Detailed Iteration Logic** (if applicable):
```
Loop/Recursion mechanism:
- Start condition: ...
- Loop while: ...
- Each iteration:
  1. ...
  2. ...
- State updates: ...
- Base case: ...
- Return: ...
```

**Advanced Error Patterns** (if applicable):
```
Error handling by type:
- "pattern" in error:
  → Detection: ...
  → Response: ...
  → Recovery: ...
```

**Algorithm Details** (if complex logic present):
```
Algorithm name:
1. Step with formula/logic
2. Step with conditions
3. etc.
```

**Module Exports and Public API** (CRITICAL - what other modules can import):
```
Exported Classes:
- ClassName: Description

Exported Functions:
- init_service(params) -> Service: Factory function, creates singleton instance
- get_service() -> Service: Getter function, retrieves initialized instance
- utility_function(params) -> Result: Helper function for X

Module-level Globals (if any):
- _service_instance: Optional[Service] = None  # Private singleton

Usage Pattern:
- At startup: service = init_service(config)
- In other modules: from .module import get_service
                    service = get_service()
```

**Initialization and Lifecycle Patterns** (CRITICAL - how to create instances correctly):
```
Constructor Signature:
- def __init__(self, required_param: Type, optional_param: Type = default)
- Requires: Exact parameters needed
- Does NOT accept: Common mistakes to avoid
- Gets settings from: Where configuration comes from

Factory Pattern (if applicable):
- init_service(params) function creates and stores singleton
- get_service() retrieves the singleton
- Lifecycle: When created (once at startup, per-request, cached)

Initialization Order:
1. Dependency X must be created first
2. Then create this service
3. Then services that depend on this

Correct Usage:
✅ service = init_service(required_param)
✅ service = get_service()

Incorrect Usage:
❌ service = Service()  # Missing required parameter
❌ service = Service(wrong_param=value)  # Wrong parameter name
```

**[Code Example]** (ONLY if complex/non-standard):
```[language]
[Full code for complex logic only - not standard CRUD]
```

---

### [Module 2: filename.ext]

**Purpose**: [what this module does]

**Interface** (ALL methods):
```[language]
[All signatures, interfaces, types - include private methods too]
```

**Complete Flow** (if complex) / **All Behaviors** (if simpler):
- [Complete description of algorithm OR full behavior list]

**Dependencies** (with WHY):
- [library] - [purpose]

**Error Handling** (complete):
- [Error types and handling]

**Integration Points**: [What it calls, what calls it]

**Constants and Configuration** (if any): [List with explanations]

**Template Strings** (if any): [Include full text]

**Iteration Logic** (if applicable): [Loop/recursion details]

**Advanced Error Patterns** (if applicable): [Error type mapping]

**Algorithm Details** (if complex): [Pseudocode for algorithms]

---

## Frontend Modules

### [Module 3: ComponentName.tsx]

**Purpose**: [what this component does]

**Interface**:
```typescript
interface ComponentProps {
  propName: Type;
  onEvent: (param: Type) => void;
}

export function ComponentName(props: ComponentProps): JSX.Element
```

**Complete Flow** (if complex rendering logic):
1. [Step-by-step description of component lifecycle]

**All Behaviors**:
- Behavior 1: [description]
- Behavior 2: [description]
- Keyboard shortcuts: [if applicable]
- Edge cases: [how handled]

**Dependencies** (with WHY): [list hooks, libraries with purpose]

**State Management**: [approach - useState, custom hook, context]

**Integration Points**: [What it calls, parent components, child components]

**Performance Considerations** (if applicable):
- Memoization: [what and why]
- Lazy loading: [if applicable]
- Debouncing: [if applicable]

**Constants** (if any): [Component-level constants]

**Template Strings** (if any): [UI text templates, format strings]

**[Code Example]** (ONLY if complex):
```typescript
[Complex logic only - e.g., keyboard navigation, SSE processing]
```

---

### [Module 4: CustomHook.ts]

**Purpose**: [what this hook provides]

**Interface**:
```typescript
function useCustomHook(param: Type): {
  state1: Type;
  state2: Type;
  method: () => void;
}
```

**Complete Flow**: [Hook lifecycle: initialization → updates → cleanup]

**All Behaviors**:
- [behavior 1]
- [behavior 2]
- [edge cases]

**Dependencies** (with WHY): [list with purpose]

**State Management**: [How state is tracked and updated]

**Performance Considerations** (if applicable):
- Dependency arrays: [optimization strategy]
- Cleanup: [cleanup logic]

**[Code Example]** (if non-standard pattern):
```typescript
[Complex hook logic if needed]
```

---

## CSS & Styling Patterns

> **NOTE**: This section describes the visual design system. Include for projects with frontend/UI.

**Styling Methodology**: [CSS Modules / Styled Components / Tailwind / vanilla CSS / mixed approach]

**Global Theme**:
- **Color Palette**:
  - Primary: [color name] (#hex) - [usage]
  - Secondary: [color name] (#hex) - [usage]
  - Background: [color] (#hex) - [main/alternate backgrounds]
  - Text: [color] (#hex) primary, [color] (#hex) secondary
  - Border: [color] (#hex)
  - Status colors: Success (#hex), Error (#hex), Warning (#hex)

- **Typography System**:
  - Font families: [primary font], [fallbacks]
  - Heading sizes: h1 (Xpx), h2 (Xpx), h3 (Xpx) with weights
  - Body text: Xpx, line-height X.X, weight XXX
  - Small text: Xpx for labels, Xpx for captions

- **Spacing Scale**: [base unit]px base → [derived values: 8px, 12px, 16px, 24px, etc.]

**Component Visual Patterns**:
- **[ComponentName]**: [Describe appearance]
  - Layout: [flexbox/grid structure, dimensions]
  - Colors: [background, text, borders]
  - Spacing: [padding, margins]
  - Visual effects: [shadows, borders, radius]

- **[ComponentName2]**: [Describe appearance]
  - [Structure and visual properties]

**Interactive States**:
- Hover: [what changes - colors, shadows, scale]
- Focus: [focus rings, outlines, highlights]
- Active: [pressed state appearance]
- Disabled: [opacity, cursor, color changes]

**Layout Patterns**:
- Container: [max-width, centering, padding]
- Grids: [column counts, gap sizes]
- Flexbox: [direction, alignment, common patterns]
- Positioning: [sticky headers, fixed elements]

**Responsive Behavior**:
- Mobile (<768px): [layout changes, stacking, font sizes]
- Tablet (768-1024px): [intermediate layout]
- Desktop (>1024px): [full layout with sidebars/columns]

**Animations & Transitions**:
- [Element type]: [animation description - fade in, slide, etc.]
- Timing: [duration values - 0.2s, 0.3s]
- Easing: [ease-in-out, ease-out, cubic-bezier values]

**Visual Hierarchy**:
- How importance is conveyed: [size, weight, color contrast, spacing]
- Focus patterns: [how user attention is directed]

---

## Application Structure & Entry Points

> **NOTE**: Critical infrastructure files that bootstrap the application.

### HTML Entry Point (index.html)

**Document Structure**:
- Doctype and HTML structure
- Meta tags: [charset, viewport, description]
- Title: [page title pattern]
- Root element: [div id and any data attributes]
- Script tag: [type, src path, defer/async]
- Stylesheets: [link tags if any]
- Other head elements: [favicons, manifest, etc.]

**Example Description**: "Standard HTML5 document with viewport meta tag for mobile, title 'Database Chat NL', root div with id='root', module script loading /src/main.tsx, no external stylesheets"

---

### Frontend Entry Point (main.tsx / index.tsx)

**Bootstrap Pattern**:
- React import style: [React, ReactDOM from libraries]
- Root element selection: [getElementById or querySelector]
- Render method: [createRoot, legacy render, hydrateRoot]
- Wrapper components: [StrictMode, any providers at entry level]
- Root component imported: [App, Main, Root, etc.]
- Global imports: [CSS, polyfills, initialization scripts]

**Example Description**: "Imports React 18's createRoot, selects #root element, renders App wrapped in StrictMode, imports ./index.css for global styles"

---

### Root Component (App.tsx / App.jsx)

**Top-Level Composition**:
- Provider nesting order: [list providers from outer to inner]
  - Example: BrowserRouter → AuthProvider → ThemeProvider → QueryClientProvider
- Layout structure: [header, sidebar, main, footer arrangement]
- Routing: [route definitions, path patterns, lazy loading]
- Global state initialization: [context setup, store creation]

**Component Hierarchy**:
```
App
├── [ProviderName]
│   ├── [LayoutComponent]
│   │   ├── Header (if present)
│   │   ├── Sidebar (if present)
│   │   ├── Main Content
│   │   │   └── Routes/Children
│   │   └── Footer (if present)
```

**Example Description**: "App.tsx sets up BrowserRouter, wraps with AuthProvider for session management, renders ChatContainer as main content filling full viewport - no traditional header/footer/sidebar layout, pure chat interface"

---

### Build Configuration (vite.config.ts / webpack.config.js)

**Build Tool**: [Vite / Webpack / Next.js / etc.]

**Configuration**:
- Plugins: [list plugins with purpose]
  - Example: @vitejs/plugin-react for JSX transformation
- Dev server:
  - Port: [port number]
  - Proxy: [API proxy rules if any]
  - Host: [localhost / 0.0.0.0]
  - HTTPS: [yes/no]
- Build output:
  - Directory: [dist, build, .next]
  - Format: [ES modules, CommonJS]
  - Minification: [enabled/disabled]
- Path aliases: [if using @ or ~ imports]

**Example**: "Vite 5.x with React plugin, dev server on port 5173, proxies /api to http://localhost:8000 with changeOrigin:true, builds to dist/, no custom aliases"

---

### TypeScript Configuration (tsconfig.json)

**Compiler Options**:
- Target: [ES2020, ES2022, ESNext]
- Module: [ESNext, CommonJS]
- JSX: [react-jsx, react, preserve]
- Strict mode: [enabled/disabled + specific flags]
- Module resolution: [bundler, node]
- Base URL & Paths: [if path mapping used]

**Include/Exclude**:
- Include: [src/**/* patterns]
- Exclude: [node_modules, dist, etc.]

**Example**: "Target ES2020, module ESNext, jsx: react-jsx, strict mode fully enabled, includes src/**/*.ts and src/**/*.tsx, excludes node_modules and dist"

---

## Database/Data Layer

### [Module 5: Models/Schema]

**Purpose**: [database models/schema definition]

**Interface**:
```[language]
[Schema definition, table structure, relationships]
```

**Key Entities**:
- Entity1: [fields and purpose]
- Entity2: [fields and purpose]

**Relationships**: [how entities relate]

**Migrations**: [tool and location]

---

## Capability Implementation Mapping

[Map each capability from meta.yaml to specific files/functions]

| Capability | Backend Implementation | Frontend Implementation |
|------------|----------------------|------------------------|
| [capability_1] | [file.py:ClassName.method] | [Component.tsx] |
| [capability_2] | [file.py:function] | [Hook.ts:useHook] |
| [capability_3] | [file.py:ClassName] | [Component.tsx] |

---

## Error Handling Patterns

**Backend Pattern**:
```python
# Standard error handling across services
try:
    # Operation
    conn.commit()
except Exception as e:
    conn.rollback()
    logger.error(f"Error: {e}")
    return {'error': str(e)}
finally:
    # Cleanup
```

**Frontend Pattern**:
```typescript
// Standard error handling in components
try {
  await apiCall();
} catch (error) {
  setError(error.message);
  toast.error(error.message);
}
```

---

## Security Patterns

**Backend**:
- Authentication: [JWT, session, OAuth - describe pattern]
- Authorization: [Role-based, claims - describe pattern]
- Input Validation: [Approach used]
- SQL Injection Prevention: [Parameterized queries, ORM]
- Password Security: [Hashing algorithm, salt]

**Frontend**:
- Token Storage: [localStorage, httpOnly cookie]
- XSS Prevention: [Sanitization approach]
- CSRF Protection: [Token approach]

**Code Example** (if complex auth flow):
```[language]
[Show complex security implementation if non-standard]
```

---

## Integration Points

**Backend → Database**:
- Connection: [pool, direct]
- ORM: [tool if used]
- Migrations: [tool and location]

**Frontend → Backend**:
- Protocol: [REST, GraphQL, WebSocket]
- Auth: [Bearer token, session cookie]
- Real-time: [SSE, WebSocket, polling]

**Backend → External Services**:
- [Service]: [integration pattern]
- [Service]: [integration pattern]

---

## Testing Patterns (if applicable)

**Backend Tests** (location: [path]):
- Unit tests: [framework and approach]
- Integration tests: [approach]

**Frontend Tests** (location: [path]):
- Component tests: [framework]
- Hook tests: [approach]

---

**NOTES**:
- **Interface signatures should list ALL methods** (including private ones), not just main methods
- **Complete Flow section**: Use for complex modules - describe step-by-step algorithm
- **All Behaviors**: Complete list including edge cases, not just "key" behaviors
- **Constants**: Include module-level constants with explanations and units
- **Template Strings**: Include FULL TEXT of large strings (prompts, templates, etc.) - exception to "no code" rule
- **Iteration Logic**: For loops/recursion, describe conditions, state updates, base cases
- **Advanced Error Patterns**: Map error types to detection/response/recovery
- **Algorithm Details**: Pseudocode for complex, non-obvious algorithms
- Keep actual names from codebase (no placeholders like "MyService")
- Standard patterns (CRUD, basic React, JWT auth) = descriptions only
- Complex patterns (streaming, custom algorithms, integrations) = full code if needed
- **Mark sections as "N/A" or omit if not applicable** (e.g., simple utility functions don't need iteration logic)
