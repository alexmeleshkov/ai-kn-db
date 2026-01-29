# UI Structure & User Flows

## UI Overview

**Interface Type**: Web App (SPA)
**Target Devices**: Desktop-first, mobile-responsive
**Navigation Pattern**: Sidebar navigation with main content area
**Layout Approach**: Split panes (sidebar + main chat)

## Main UI Sections

### 1. Sidebar (Left, 300px wide)
**Purpose**: Navigation, history, schema viewer

**Location**: Fixed left side, collapsible on mobile

**Contents**:
- Logo (ITFC circle)
- New Chat button
- Tabs: Conversations, Schema
- User menu (logout)

**Behavior**:
- Sticky on scroll
- Highlights active conversation
- Collapsible on mobile (<768px)

### 2. Main Content Area
**Purpose**: Chat interface and query results

**Layout**: Vertical flex (messages + input)

**Key Components**:
- ChatMessage list (auto-scroll)
- DataViewer (query results table)
- QueryChart (auto-generated charts)
- ChatInput (text area + send button)

**Responsive Behavior**:
- Desktop: Sidebar visible, full chart width
- Mobile: Sidebar hidden, tap to open

## Component Hierarchy

```
App
├── AuthPage (if not authenticated)
│   ├── Login form
│   └── Register form
└── Main Layout (if authenticated)
    ├── Sidebar
    │   ├── Logo
    │   ├── New Chat button
    │   ├── SidebarTabs
    │   │   ├── Conversations (QueryHistory)
    │   │   └── Schema (DatabaseInfo)
    │   └── User menu
    └── ChatContainer
        ├── Messages (ChatMessage[])
        ├── DataViewer (query results)
        ├── QueryChart (visualizations)
        └── ChatInput
```

## Key User Flows

### Flow 1: User Login
1. User navigates to app
2. Sees AuthPage with login form
3. Enters email + password
4. JWT token stored in localStorage
5. Redirected to chat interface

**UI Components**: AuthPage, useAuth hook

### Flow 2: Ask Question
1. User types in ChatInput
2. Clicks send or presses Enter
3. SSE connection opens, streaming begins
4. Progress messages display ("Thinking...", "Executing query...")
5. Results display in DataViewer + QueryChart
6. User can ask follow-up

**UI Components**: ChatInput, ChatContainer, ChatMessage, DataViewer, QueryChart

### Flow 3: View History
1. User clicks "Conversations" tab in sidebar
2. List of past conversations displays
3. User clicks conversation
4. Messages load in ChatContainer
5. User can continue conversation

**UI Components**: SidebarTabs, QueryHistory, ChatContainer

## Navigation Patterns

**Primary Navigation**: Sidebar tabs (Conversations, Schema)
**Active State**: Blue highlight on selected tab

## Responsive Behavior

### Desktop (> 1024px)
- Sidebar visible (300px)
- Chat full width
- Charts responsive

### Tablet (768px - 1024px)
- Sidebar 250px
- Slightly narrower chat

### Mobile (< 768px)
- Sidebar hidden (hamburger menu)
- Chat full width
- Charts stack vertically

## Loading & Empty States

**Loading States**:
- Streaming: "Thinking..." with elapsed time
- Query execution: "Executing query... (5s)"

**Empty States**:
- No conversations: "Ask your first question"
- No results: "Query returned no rows"

## Error Handling

**Display Patterns**:
- Error banner (red background)
- Inline error messages
- Retry button for failed queries

**Recovery Actions**:
- Edit generated SQL and re-run
- Ask clarification question
- Start new conversation
