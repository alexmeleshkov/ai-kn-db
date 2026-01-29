# UI Structure & User Experience

> **Purpose**: Document UI structure, component hierarchy, and user flows.
> Focus on WHAT to build (structure, behavior), not HOW to style it.
> **OPTIONAL**: Only needed for projects with significant UI/frontend components.

## Page Structure Overview

**Total pages/screens**: [number]
**Layout pattern**: [single-page app / multi-page / hybrid]

**Core pages**:
- `[page/route]` - [purpose and content]
- `[page/route]` - [purpose and content]
- `[page/route]` - [purpose and content]

---

## Navigation Structure

**Navigation type**: [top nav / sidebar / mobile drawer / tabs / other]

**Primary navigation items**:
- [item 1] - [links to]
- [item 2] - [links to]
- [item 3] - [links to]

**Secondary navigation** (if applicable):
- [item 1] - [context and purpose]
- [item 2] - [context and purpose]

**Breadcrumbs**: [yes/no - where used]

---

## Layout Patterns

### Overall Layout Structure
```
[Describe layout hierarchy using ASCII or text structure]
Example:
┌─────────────────────────────────────┐
│ Header (logo, nav, user menu)       │
├──────────┬──────────────────────────┤
│ Sidebar  │ Main Content Area        │
│ (nav)    │                          │
│          │                          │
└──────────┴──────────────────────────┘
```

**Header**: [components present]
- [element 1]
- [element 2]
- [element 3]

**Sidebar** (if applicable): [components present]
- [element 1]
- [element 2]

**Main content area**: [typical structure]
- [pattern description]

**Footer** (if applicable): [components present]
- [element 1]
- [element 2]

---

## Key Pages/Screens

### [Page 1: name]

**Route/URL**: `[path]`
**Purpose**: [what this page does]

**Layout sections**:
1. [Section name] - [content/purpose]
2. [Section name] - [content/purpose]
3. [Section name] - [content/purpose]

**Key components**:
- [Component name] - [purpose and behavior]
- [Component name] - [purpose and behavior]
- [Component name] - [purpose and behavior]

**Interactions**:
- [User action] → [system response]
- [User action] → [system response]

**Navigation from this page**:
- [Link/button] → [destination]
- [Link/button] → [destination]

---

### [Page 2: name]

**Route/URL**: `[path]`
**Purpose**: [what this page does]

**Layout sections**:
1. [Section name] - [content/purpose]
2. [Section name] - [content/purpose]

**Key components**:
- [Component name] - [purpose and behavior]
- [Component name] - [purpose and behavior]

**Interactions**:
- [User action] → [system response]
- [User action] → [system response]

**Navigation from this page**:
- [Link/button] → [destination]

---

### [Page 3: name]

**Route/URL**: `[path]`
**Purpose**: [what this page does]

**Layout sections**:
1. [Section name] - [content/purpose]
2. [Section name] - [content/purpose]

**Key components**:
- [Component name] - [purpose and behavior]
- [Component name] - [purpose and behavior]

**Interactions**:
- [User action] → [system response]

---

## Component Hierarchy

### High-Level Component Tree
```
[Show component nesting/hierarchy]
Example:
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   └── UserMenu
│   ├── Sidebar (optional)
│   └── MainContent
│       ├── [PageComponent1]
│       └── [PageComponent2]
└── Footer
```

---

## Reusable Components

### [Component Name 1]

**Purpose**: [what it does]
**Where used**: [list pages/contexts]

**Content/Structure**:
- [element 1]
- [element 2]
- [element 3]

**Interactive elements**:
- [interaction description]
- [interaction description]

**Variants** (if any):
- [variant 1] - [difference]
- [variant 2] - [difference]

---

### [Component Name 2]

**Purpose**: [what it does]
**Where used**: [list pages/contexts]

**Content/Structure**:
- [element 1]
- [element 2]

**Interactive elements**:
- [interaction description]

**States**: [loading / error / success / empty]

---

### [Component Name 3]

**Purpose**: [what it does]
**Where used**: [list pages/contexts]

**Content/Structure**:
- [element 1]
- [element 2]

**Interactive elements**:
- [interaction description]

---

## UI States

### Loading States

**Where used**:
- [Context 1] - [loading indicator type]
- [Context 2] - [loading indicator type]
- [Context 3] - [loading indicator type]

**Pattern**: [skeleton / spinner / progress bar / text]

---

### Error States

**Where displayed**:
- [Context 1] - [error display approach]
- [Context 2] - [error display approach]

**Error types handled**:
- [Error type 1] - [user-facing message approach]
- [Error type 2] - [user-facing message approach]
- [Error type 3] - [user-facing message approach]

**Recovery actions**:
- [Action 1]
- [Action 2]

---

### Empty States

**Where used**:
- [Context 1] - [message and actions shown]
- [Context 2] - [message and actions shown]

**Pattern**: [message + illustration / CTA / help text]

---

### Success States

**Where used**:
- [Context 1] - [success feedback approach]
- [Context 2] - [success feedback approach]

**Pattern**: [toast / modal / inline message / redirect]

---

## User Flows

### [Flow 1: Primary User Journey]

**Trigger**: [what starts this flow]

**Steps**:
1. User [action] on [page/component]
2. System [response]
3. User [action]
4. System [response]
5. User sees [result/feedback]

**Success endpoint**: [where user ends up]
**Failure handling**: [what happens on error]

---

### [Flow 2: Secondary User Journey]

**Trigger**: [what starts this flow]

**Steps**:
1. User [action]
2. System [response]
3. User [action]
4. System [response]

**Success endpoint**: [where user ends up]
**Failure handling**: [what happens on error]

---

### [Flow 3: User Journey]

**Trigger**: [what starts this flow]

**Steps**:
1. User [action]
2. System [response]
3. User [action]

**Success endpoint**: [where user ends up]

---

## Forms & Input

### [Form 1: name]

**Location**: [where this form appears]
**Purpose**: [what it accomplishes]

**Fields**:
- [Field name] - [type] - [validation rules]
- [Field name] - [type] - [validation rules]
- [Field name] - [type] - [validation rules]

**Validation approach**: [client-side / server-side / both]
**Error display**: [inline / summary / both]

**Submit behavior**:
- Success: [what happens]
- Error: [what happens]

---

### [Form 2: name]

**Location**: [where this form appears]
**Purpose**: [what it accomplishes]

**Fields**:
- [Field name] - [type] - [validation rules]
- [Field name] - [type] - [validation rules]

**Validation approach**: [client-side / server-side / both]

**Submit behavior**:
- Success: [what happens]
- Error: [what happens]

---

## Modals & Overlays

### [Modal 1: name]

**Trigger**: [what opens this modal]
**Purpose**: [what it's for]

**Content**:
- [element 1]
- [element 2]

**Actions**:
- [Primary action] → [result]
- [Secondary action] → [result]
- [Close/cancel] → [result]

**Dismissal**: [click outside / close button / ESC key]

---

### [Modal 2: name]

**Trigger**: [what opens this modal]
**Purpose**: [what it's for]

**Content**:
- [element 1]
- [element 2]

**Actions**:
- [Primary action] → [result]
- [Cancel] → [result]

---

## Data Display Patterns

### Lists/Tables

**Where used**: [locations]

**Display pattern**: [table / cards / list items]

**Columns/Fields shown**:
- [Field 1]
- [Field 2]
- [Field 3]

**Sorting**: [yes/no - which columns]
**Filtering**: [yes/no - which fields]
**Pagination**: [yes/no - approach]

**Row/Item actions**:
- [Action 1]
- [Action 2]

---

### Cards/Panels

**Where used**: [locations]
**Purpose**: [what they display]

**Content structure**:
- [element 1]
- [element 2]
- [element 3]

**Actions available**:
- [Action 1]
- [Action 2]

---

## Real-time Updates

**Where used**: [list pages/components with live data]

**Update mechanism**: [WebSocket / polling / SSE / other]

**Visual feedback**: [how user knows data updated]

**Examples**:
- [Context 1] - [what updates in real-time]
- [Context 2] - [what updates in real-time]

---

## Responsive Behavior

**Breakpoints approach**: [mobile-first / desktop-first / adaptive]

**Mobile adaptations**:
- [Navigation] → [mobile pattern]
- [Sidebar] → [mobile pattern]
- [Tables/Complex layouts] → [mobile pattern]

**Touch interactions**: [list touch-specific behaviors]

---

## Accessibility Considerations

**Keyboard navigation**: [how it's supported]

**Screen reader support**:
- [Support area 1]
- [Support area 2]

**Focus management**: [how focus is handled in modals/overlays]

**ARIA labels**: [where used]

---

## Key User Interactions

### [Interaction Pattern 1]

**Context**: [where this happens]
**User action**: [what user does]
**System response**: [immediate feedback]
**Result**: [final outcome]

---

### [Interaction Pattern 2]

**Context**: [where this happens]
**User action**: [what user does]
**System response**: [immediate feedback]
**Result**: [final outcome]

---

### [Interaction Pattern 3]

**Context**: [where this happens]
**User action**: [what user does]
**System response**: [immediate feedback]

---

## Onboarding/First-Time Experience

**Approach**: [tutorial / tooltips / empty state CTAs / documentation links]

**Flow**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Search & Discovery

**Where available**: [locations]

**Search scope**: [what can be searched]

**Search behavior**:
- Input method: [text / voice / filters]
- Results display: [instant / on-submit]
- Filtering options: [list available filters]

**No results state**: [what's shown]

---

## Notifications & Feedback

**Notification types**:
- [Type 1] - [when shown] - [display method]
- [Type 2] - [when shown] - [display method]
- [Type 3] - [when shown] - [display method]

**Display patterns**:
- Toast/Snackbar: [when used]
- Modal: [when used]
- Inline message: [when used]
- Badge/Indicator: [when used]

---
