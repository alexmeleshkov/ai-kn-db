# UI Structure & User Flows

> **Purpose**: Document UI organization, navigation, and user interaction patterns.
> This file informs layout generation and component hierarchy decisions.

## UI Overview

**Interface Type**: [Web App / Mobile App / Desktop App / CLI / Dashboard / Admin Panel]

**Target Devices**: [Desktop-first / Mobile-first / Desktop-only / Mobile-only / Cross-platform]

**Navigation Pattern**: [Sidebar navigation / Top navbar / Tabs / Bottom navigation / Command palette / Multi-panel]

**Layout Approach**: [Single page / Multi-page / Modal-heavy / Drawer-based / Split panes]

---

## Main UI Sections

### [Section 1 Name - e.g., Navigation/Header/Sidebar]

**Purpose**: [What this section provides - e.g., primary navigation, user menu, branding]

**Location**: [Where it appears - e.g., left sidebar, top bar, fixed header]

**Contents**:
- [Element 1 - e.g., Logo/brand]
- [Element 2 - e.g., Main navigation links]
- [Element 3 - e.g., User profile dropdown]
- [Element 4 - e.g., Search bar]

**Behavior**:
- [Interaction 1 - e.g., collapsible on mobile]
- [Interaction 2 - e.g., highlights active page]
- [Interaction 3 - e.g., sticky on scroll]

**Visibility**: [Always visible / Hidden on mobile / Context-dependent]

---

### [Section 2 Name - e.g., Main Content Area/Dashboard]

**Purpose**: [Primary user workspace]

**Layout**: [Single column / Multi-column / Grid / List view / Card layout]

**Key Components**:
- [Component 1 with brief purpose]
- [Component 2 with brief purpose]
- [Component 3 with brief purpose]

**Responsive Behavior**:
- Desktop: [Layout description]
- Tablet: [How it adapts]
- Mobile: [How it adapts]

---

### [Section 3 Name - e.g., Sidebar Panel/Details Pane]

**Purpose**: [Contextual information, filters, settings]

**Location**: [Right side / Left side / Slide-out drawer]

**Shows**: [What information is displayed]

**Trigger**: [How user accesses it - e.g., click button, automatic, always visible]

---

## Component Hierarchy

```
[Show visual hierarchy - adapt format to your app structure]

Example formats:

Web App:
AppLayout
├── Navigation
│   ├── Logo
│   ├── MenuItems
│   └── UserMenu
├── MainContent
│   ├── PageHeader
│   ├── ContentArea
│   │   ├── [Feature Components]
│   │   └── [Data Display Components]
│   └── Footer
└── Sidebar (optional)
    ├── Filters
    └── QuickActions

Dashboard:
DashboardLayout
├── TopBar (AppBar/Header)
├── SideNav (Drawer)
└── MainArea
    ├── WidgetGrid
    └── DetailPanel

Mobile App:
RootNavigator
├── BottomTabNavigator
│   ├── HomeScreen
│   ├── SearchScreen
│   └── ProfileScreen
└── ModalStack
```

---

## Key User Flows

### Flow 1: [Primary User Journey - e.g., Complete Core Task]

**Entry Point**: [How user starts - e.g., clicks button, navigates to page]

**Steps**:
1. [Action 1] → [Screen/Component shown]
2. [Action 2] → [What happens, what's displayed]
3. [Action 3] → [Feedback provided]
4. [Action 4] → [Success state/result]

**UI Components Involved**:
- [Component 1] - [Role in flow]
- [Component 2] - [Role in flow]
- [Component 3] - [Role in flow]

**Visual Feedback**:
- [Loading states]
- [Progress indicators]
- [Success/error messages]

**Exit Points**: [How flow completes or can be abandoned]

---

### Flow 2: [Secondary Journey]

**Entry Point**: [Starting action]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**UI Components**: [List relevant components]

---

### Flow 3: [Error/Edge Case Flow]

**Trigger**: [What causes this flow]

**Steps**: [How error is handled in UI]

**Recovery**: [How user gets back on track]

---

## Navigation Patterns

### Primary Navigation

**Type**: [Sidebar / Top bar / Bottom tabs / Breadcrumbs]

**Items**:
- [Nav item 1] → [Destination]
- [Nav item 2] → [Destination]
- [Nav item 3] → [Destination]

**Active State Indication**: [How current page is shown]

### Secondary Navigation

**Type**: [Tabs / Sub-menu / Dropdown / Step indicator]

**Context**: [When it appears]

**Items**: [List navigation options]

---

## Modal/Overlay Patterns

### [Modal Type 1 - e.g., Confirmation Dialog]

**Trigger**: [When it appears]

**Content**: [What it shows]

**Actions**: [Button options - e.g., Confirm/Cancel]

**Dismissal**: [How user closes it]

---

### [Modal Type 2 - e.g., Form Dialog]

**Purpose**: [What it's for]

**Layout**: [Single form / Multi-step / Tabbed]

**Validation**: [Inline / On submit / Real-time]

---

## Responsive Behavior

### Desktop (> 1024px)
- [Layout characteristic 1]
- [Layout characteristic 2]
- [Layout characteristic 3]

### Tablet (768px - 1024px)
- [Adaptation 1]
- [Adaptation 2]
- [Adaptation 3]

### Mobile (< 768px)
- [Adaptation 1]
- [Adaptation 2]
- [Adaptation 3]

---

## State Management in UI

### Global States
- [State 1 - e.g., User authentication status]
  - Affects: [Which components]
  - Shown as: [UI indication]

- [State 2 - e.g., Active filters]
  - Affects: [Which components]
  - Shown as: [UI indication]

### Local Component States
- [State 1 - e.g., Form validation]
- [State 2 - e.g., Loading indicators]
- [State 3 - e.g., Expanded/collapsed sections]

---

## Loading & Empty States

### Loading States
**During data fetch**: [What user sees - e.g., skeleton screens, spinners, progress bars]

**During action**: [What user sees - e.g., button disabled + spinner, overlay]

### Empty States
**No data**: [Message and action shown]

**No search results**: [Message and suggested actions]

**First-time user**: [Onboarding or empty state with guidance]

---

## Error Handling in UI

### Error Display Patterns
- **Inline validation**: [Where and how shown]
- **Toast notifications**: [Positioning and duration]
- **Error pages**: [Full page error states]
- **Inline alerts**: [Contextual error messages]

### Recovery Actions
- [What actions user can take to fix errors]
- [Links to help/support if applicable]

---

## Accessibility Considerations

- **Keyboard Navigation**: [Tab order, shortcuts]
- **Screen Reader Support**: [ARIA labels, announcements]
- **Focus Management**: [Focus trapping in modals, focus restoration]
- **Color Contrast**: [Meeting WCAG standards]
- **Interactive Element Size**: [Minimum touch targets]

---
