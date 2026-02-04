# UI Structure & User Experience

> **Purpose**: Document UI structure, component hierarchy, and user flows.
> Focus on WHAT to build (structure, behavior), not HOW to style it.

## Page Structure Overview

**Total pages/screens**: 2 main views + authentication
**Layout pattern**: Single-page application with view mode switching

**Core pages**:
- `/` (authenticated) - Main application with chat interface
- `/` (unauthenticated) - Login/register page
- View modes: Chat, Data Viewer, Admin Viewer (within authenticated app)

---

## Navigation Structure

**Navigation type**: Left sidebar with tabbed navigation

**Primary navigation items** (Sidebar tabs):
- **Chats** - List of user's conversations
- **History** - Recent query history with timestamps
- **Schema** - Database schema browser with table/column details
- **Admin** - Cross-user conversation viewer (admin only, shown if user.is_admin=true)

**Secondary navigation**:
- **New Chat** button - Top of sidebar, creates new conversation
- **User menu** - Bottom of sidebar with email and logout button
- **Logo** - Top of sidebar, Ipswich Town FC branding

**Breadcrumbs**: No

---

## Layout Patterns

### Overall Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Unauthenticated                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Auth Page (centered)                 │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Logo + Title                                    │  │  │
│  │  │  Email input                                     │  │  │
│  │  │  Password input                                  │  │  │
│  │  │  [Login] or [Register] button                    │  │  │
│  │  │  Toggle: "Need an account?" / "Have an account?" │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     Authenticated                           │
│  ┌──────────┬──────────────────────────────────────────┐   │
│  │ Sidebar  │          Main Content Area               │   │
│  │ (300px)  │                                           │   │
│  │          │                                           │   │
│  │ [Logo]   │  ┌────────────────────────────────────┐  │   │
│  │          │  │                                    │  │   │
│  │ [New     │  │   ChatContainer (view=chat)        │  │   │
│  │  Chat]   │  │      OR                            │  │   │
│  │          │  │   DataViewer (view=data)           │  │   │
│  │ ┌──────┐ │  │      OR                            │  │   │
│  │ │Tabs: │ │  │   AdminConversationViewer          │  │   │
│  │ │Chat  │ │  │      (view=admin-view)             │  │   │
│  │ │Hist  │ │  │                                    │  │   │
│  │ │Schema│ │  └────────────────────────────────────┘  │   │
│  │ │Admin*│ │                                           │   │
│  │ └──────┘ │                                           │   │
│  │          │                                           │   │
│  │ [User]   │                                           │   │
│  │ [Logout] │                                           │   │
│  └──────────┴──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Sidebar** (left, 300px width):
- Logo section (circular icon + "Ipswich Town Fan Data Insights" text)
- New Chat button (blue accent, full width)
- Tabbed navigation (pills-style tabs with badges)
- Tab content area (scrollable lists)
- User menu (bottom, fixed position)

**Main Content Area** (flex: 1, fills remaining width):
- Switches between ChatContainer, DataViewer, AdminConversationViewer based on view mode state
- Full height, scrollable content

---

## Key Pages/Screens

### Authentication Page

**Route/URL**: `/` (when not authenticated)
**Purpose**: User login and registration

**Layout sections**:
1. **Centered card** - White background, rounded corners, shadow
2. **Logo** - Large circular Ipswich Town FC icon
3. **Title** - "Sign in to your account" or "Create a new account"
4. **Form** - Email and password inputs
5. **Submit button** - "Sign In" or "Create Account"
6. **Toggle** - Link to switch between login and register modes
7. **Error display** - Red banner for authentication errors

**Key components**:
- **AuthPage component** - Manages mode state (login vs register)
- **Email input** - Pydantic EmailStr validation on backend
- **Password input** - Type="password", no client-side validation
- **Submit button** - Calls /auth/login or /auth/register API
- **Mode toggle link** - Changes between "Sign In" and "Create Account"

**Interactions**:
- Click "Create Account" → Call /auth/register → Receive JWT → Navigate to main app
- Click "Sign In" → Call /auth/login → Receive JWT → Navigate to main app
- Click "Need an account?" → Toggle to register mode
- Click "Already have an account?" → Toggle to login mode
- Error response → Display error message in red banner

**Navigation from this page**:
- Successful auth → Main app (chat interface)

---

### Main Application (Chat View)

**Route/URL**: `/` (when authenticated, default view)
**Purpose**: Chat interface for natural language database querying

**Layout sections**:
1. **Sidebar** (left):
   - Logo and new chat button
   - Tabbed navigation (Chats, History, Schema, Admin*)
   - Tab content (conversation list, query history, schema tree, admin list)
   - User menu (email + logout)

2. **Main content** (right):
   - Chat header (conversation title if exists)
   - Message list (scrollable, auto-scroll to bottom)
   - Chat input (textarea with autocomplete)

**Key components**:

**Sidebar Components**:
- **Logo** - Circular icon, "Ipswich Town Fan Data Insights" text
- **New Chat Button** - Increments chatKey, resets conversation
- **SidebarTabs** - Tabbed navigation with badges
  - Chats tab: List of conversations sorted by updated_at DESC
  - History tab: Recent queries with timestamps
  - Schema tab: Collapsible database tables with columns
  - Admin tab: All conversations across all users (admin only)
- **User Menu** - Display email, logout button

**Chat Components**:
- **ChatContainer** - Main chat interface
  - Receives conversationId prop to load existing conversation
  - Receives chatKey prop to force remount on new chat
- **Message List** - Scrollable container for ChatMessage components
- **ChatMessage** - Individual message bubbles
  - User messages: Right-aligned, blue background
  - Assistant messages: Left-aligned, white background
  - Markdown rendering with syntax highlighting
  - Query result tables with CSV download
  - Chart visualization toggle button
  - Streaming cursor animation during LLM response
- **ChatInput** - Textarea with autocomplete
  - Table name suggestions (triggered by typing)
  - Column name suggestions (triggered after ".")
  - Template suggestions (common query patterns)
  - Keyboard navigation (arrow keys, Enter, Escape)
  - Enter to send, Shift+Enter for newline
  - Disabled during streaming

**Interactions**:
- Type message → Show autocomplete suggestions → Select suggestion → Insert into textarea
- Press Enter → Send message → Stream SSE events → Display response
- Click query result → Expand table view
- Click "Show Chart" → Display bar/line/pie chart with column selectors
- Click "Download CSV" → Export query results as CSV file
- Click conversation in sidebar → Load conversation → Display messages
- Click "New Chat" → Clear current chat → Start fresh conversation
- Streaming response → Show thinking indicator, tool calls, query execution, final text
- Tool execution → Show SQL query, execution time, row count, success/error

**Navigation from this page**:
- Click conversation → Load conversation in chat view
- Click table in Schema tab → Switch to Data Viewer
- Click admin conversation → Switch to Admin Viewer
- Click Logout → Return to auth page

---

### Data Viewer

**Route/URL**: `/` (view mode = "data")
**Purpose**: Browse table data with pagination

**Layout sections**:
1. **Header** - Table name, close button
2. **Table** - HTML table with sticky header
3. **Pagination** - Page controls, row count

**Key components**:
- **DataViewer component** - Fetches and displays table data
- **Table header** - Column names, sticky position
- **Table rows** - Data rows, zebra striping
- **Pagination controls** - Previous/Next buttons, page number, total rows
- **Close button** - Returns to chat view

**Interactions**:
- Load → Fetch first page from /database/tables/{name}
- Click Next → Fetch next page
- Click Previous → Fetch previous page
- Click Close → Return to chat view

**Navigation from this page**:
- Close button → Chat view

---

### Admin Conversation Viewer

**Route/URL**: `/` (view mode = "admin-view", admin only)
**Purpose**: View any conversation from any user

**Layout sections**:
1. **Header** - Conversation title, user email, close button
2. **Message list** - All messages in conversation (read-only)

**Key components**:
- **AdminConversationViewer component** - Fetches conversation by ID
- **Header** - Shows conversation owner's email
- **Message list** - ChatMessage components in read-only mode
- **Close button** - Returns to chat view

**Interactions**:
- Load → Fetch /admin/conversations/{id}
- Display messages → Render all messages
- Click Close → Return to chat view

**Navigation from this page**:
- Close button → Chat view

---

## Component Hierarchy

```
App
├── AuthProvider (context)
│   └── AuthWrapper
│       ├── AuthPage (if not authenticated)
│       └── AppContent (if authenticated)
│           ├── Sidebar
│           │   ├── Logo
│           │   ├── New Chat Button
│           │   ├── SidebarTabs
│           │   │   ├── Chats Tab
│           │   │   │   └── Conversation List
│           │   │   ├── History Tab
│           │   │   │   └── QueryHistory component
│           │   │   ├── Schema Tab
│           │   │   │   └── DatabaseInfo component
│           │   │   └── Admin Tab (if admin)
│           │   │       └── Admin Conversation List
│           │   └── User Menu
│           └── Main Content
│               ├── ChatContainer (if view=chat)
│               │   ├── Message List
│               │   │   └── ChatMessage (multiple)
│               │   │       ├── Markdown content
│               │   │       ├── Query result table
│               │   │       └── QueryChart (if show chart)
│               │   └── ChatInput
│               ├── DataViewer (if view=data)
│               │   ├── Table header
│               │   ├── Table rows
│               │   └── Pagination
│               └── AdminConversationViewer (if view=admin-view)
│                   ├── Header
│                   └── Message List
```

---

## State Management

**Global State** (AuthContext):
- `user`: User object with id, email, is_admin
- `isAuthenticated`: Boolean
- `isLoading`: Boolean during auth check
- `login(email, password)`: Login function
- `logout()`: Logout function
- `token`: JWT token stored in localStorage

**App State** (AppContent component):
- `chatKey`: Number, incremented to force ChatContainer remount
- `viewMode`: "chat" | "data" | "admin-view"
- `selectedTable`: Table name for DataViewer
- `tables`: Database schema for autocomplete
- `selectedConversationId`: Conversation to load
- `adminViewConversationId`: Admin-viewed conversation

**Chat State** (useChat hook):
- `messages`: Array of Message objects
- `isStreaming`: Boolean during SSE streaming
- `streamingContent`: Accumulated text during stream
- `currentToolCall`: Tool call being executed (SQL query)
- `executedQueries`: Array of query executions
- `sendMessage(message)`: Send message function
- `clearMessages()`: Clear chat function

**Query History State** (useQueryHistory hook):
- `history`: Array of HistoryItem objects
- `addToHistory(query, result)`: Add query to history
- `clearHistory()`: Clear all history

---

## User Flows

### New User Registration

1. User lands on auth page (not authenticated)
2. Click "Create Account"
3. Enter email and password
4. Click "Create Account" button
5. Frontend calls POST /auth/register
6. Backend creates user, generates JWT token
7. Frontend stores token in localStorage
8. Frontend updates AuthContext (authenticated)
9. AuthWrapper shows AppContent (main app)
10. User sees chat interface with empty conversation

### Existing User Login

1. User lands on auth page
2. Enter email and password
3. Click "Sign In" button
4. Frontend calls POST /auth/login
5. Backend verifies credentials, generates JWT token
6. Frontend stores token in localStorage
7. Frontend updates AuthContext (authenticated)
8. AuthWrapper shows AppContent
9. User sees chat interface
10. Sidebar loads user's conversations

### Chat Query Flow

1. User types question in ChatInput
2. User presses Enter
3. Frontend creates EventSource to /chat/stream
4. Frontend sends POST with message + optional conversation_id
5. Backend authenticates (optional)
6. Backend saves user message to PostgreSQL
7. Backend gets conversation history
8. Backend gets database schema + sample data
9. Backend streams to Claude with schema + message
10. Claude generates SQL via Tool Use
11. Backend executes SQL query
12. Backend returns results to Claude
13. Claude generates natural language response
14. Backend streams events to frontend:
    - "text" events → Append to streamingContent
    - "tool_start" → Show SQL query being executed
    - "tool_result" → Display query results in table
    - "done" → Save assistant message, close stream
15. Frontend displays complete response with query results
16. User can download CSV or show chart

### Admin Viewing Conversation

1. Admin user clicks Admin tab in sidebar
2. Frontend calls GET /admin/conversations
3. Backend returns all conversations with user emails
4. Frontend displays conversation list with user emails
5. Admin clicks on a conversation
6. Frontend calls GET /admin/conversations/{id}
7. Backend returns conversation with all messages
8. Frontend switches to admin-view mode
9. AdminConversationViewer displays messages
10. Admin can read messages (read-only)
11. Admin clicks Close
12. Frontend returns to chat view

---

## Responsive Design

**Desktop** (>768px):
- Sidebar 300px fixed width
- Main content fills remaining space
- Chat input single row with send button inline

**Mobile** (<768px):
- Sidebar becomes full width (toggle with hamburger menu)
- Main content full width when sidebar hidden
- Chat input stacks vertically (textarea above send button)
- Tables scroll horizontally
- Charts scale to viewport width

---

## Styling Approach

**Design System**:
- CSS custom properties (variables) for colors, spacing, radius, transitions
- Ipswich Town FC branding (navy blue primary color #1a365d)
- BEM-style naming for component-specific styles
- Utility classes for common patterns

**Color Palette**:
- Primary: Navy blue (#1a365d)
- Accent: Blue (#3182ce)
- Success: Green (#38a169)
- Error: Red (#e53e3e)
- Background: Light gray (#f7fafc)
- Text: Dark gray (#2d3748)

**Typography**:
- Font family: System fonts (Apple, Segoe UI, Roboto)
- Monospace: SF Mono, Fira Code (for code and SQL)
- Font sizes: 0.625rem to 2rem range

**Spacing System**:
- xs: 0.25rem
- sm: 0.5rem
- md: 1rem (most common)
- lg: 1.5rem
- xl: 2rem

**Animations**:
- Spin (loading spinners)
- Pulse (thinking indicator)
- Blink (streaming cursor)
- FadeIn (modals)
- SlideUp (modal content)
- Transitions: 150ms fast, 300ms normal

---

## Accessibility Features

- **Keyboard navigation**: Tab through interactive elements, Enter to submit
- **Focus states**: Visible focus outlines on buttons and inputs
- **Alt text**: Images have descriptive alt text
- **ARIA labels**: Screen reader labels on icons and buttons
- **Color contrast**: WCAG AA compliant (primary navy on white)
- **Error messages**: Descriptive errors for form validation
- **Loading states**: Visual feedback during async operations

**Note**: Full accessibility audit not performed in scanned repository (reference project).

---

## Browser Support

**Supported browsers**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Required features**:
- EventSource API (SSE streaming)
- CSS custom properties (variables)
- ES2020 (fetch, async/await, optional chaining)
- localStorage API

---

*This UI description covers structure, components, interactions, and user flows for the DB Chat NL v2 application.*
