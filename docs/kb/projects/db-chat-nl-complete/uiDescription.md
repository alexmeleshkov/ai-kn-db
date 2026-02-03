# UI Structure & User Experience

> **Purpose**: Document UI structure, component hierarchy, and user flows.
> Focus on WHAT to build (structure, behavior), not HOW to style it.

## Page Structure Overview

**Total pages/screens**: 1 (Single-Page Application)
**Layout pattern**: Single-page app with conditional rendering

**Core pages**:
- `/` - Main application (Auth gate → Chat interface)

---

## Navigation Structure

**Navigation type**: Sidebar tabs (not top navigation)

**Primary navigation items** (sidebar):
- **Query History** - List of past conversations
- **Database Info** - Schema browser with table/column list
- **Suggestions** - Auto-generated query templates

**No top navigation**: User menu (logout) in top-right corner only

**Breadcrumbs**: No (single page app)

---

## Layout Patterns

### Overall Layout Structure
```
┌─────────────────────────────────────────────────────┐
│ Header: Logo + Database Status + User Menu          │
├─────────────┬───────────────────────────────────────┤
│ Sidebar     │ Main Content Area                     │
│ (tabs)      │                                       │
│             │ [ChatContainer or AuthPage]           │
│ - History   │                                       │
│ - Database  │ Messages scroll area                  │
│ - Suggest   │                                       │
│             │ ┌─────────────────────────────────┐   │
│             │ │ ChatInput (fixed at bottom)      │   │
│             │ └─────────────────────────────────┘   │
└─────────────┴───────────────────────────────────────┘
```

**Header**:
- Logo/title: "ITFC Analysis" or app name
- Database connection status indicator
- User email display
- Logout button

**Sidebar** (collapsible):
- Tab navigation (History | Database | Suggestions)
- Content area shows selected tab component
- Initially collapsed on mobile

**Main content area**:
- Authenticated: ChatContainer with messages + input
- Unauthenticated: AuthPage with login/register forms

**Footer**: None

---

## Key Pages/Screens

### Page 1: Authentication Page (Unauthenticated State)

**Route/URL**: `/` (when not logged in)
**Purpose**: User login or registration

**Layout sections**:
1. **Logo/Title** - App branding at top
2. **Tab Selector** - "Login" | "Register" tabs
3. **Form Area** - Email + password fields + submit button
4. **Error Display** - Red error message if login/registration fails

**Key components**:
- **AuthPage** - Container with tab switching logic
- **LoginForm** - Email + password + submit
- **RegisterForm** - Email + password + confirm password + submit
- **ErrorMessage** - Red text for error feedback

**Interactions**:
- Tab click → Switch between Login and Register forms
- Submit login → POST /auth/login → on success: store token + redirect to chat → on error: show error message
- Submit register → POST /auth/register → on success: store token + redirect to chat → on error: show error message

**Navigation from this page**:
- Success → Main chat interface (authenticated state)

---

### Page 2: Main Chat Interface (Authenticated State)

**Route/URL**: `/` (when logged in)
**Purpose**: Chat with database using natural language

**Layout sections**:
1. **Sidebar** - Query History, Database Info, or Suggestions (tab-based)
2. **Chat Messages Area** - Scrollable list of user/assistant messages
3. **Chat Input** - Fixed at bottom, text area + send button

**Key components**:
- **ChatContainer** - Main orchestrator, handles SSE streaming
- **ChatMessage** - Individual message display (user or assistant)
- **ChatInput** - Text area with send button and enter-to-send
- **DataViewer** - Query result display (table or chart)
- **QueryChart** - Bar/line/pie chart for numeric data
- **SidebarTabs** - Tab navigation for sidebar content
- **QueryHistory** - List of conversations with titles and timestamps
- **DatabaseInfo** - Database schema tree view
- **SuggestionList** - Query template suggestions (from useSuggestions hook)

**Interactions**:
- Type message + Enter or click Send → POST /chat/stream (SSE) → stream events:
  - **thinking** event → Show "Thinking..." indicator
  - **text** event → Accumulate assistant response incrementally
  - **tool_start** event → Show "Executing query..." indicator
  - **tool_result** event → Display query results (table or chart)
  - **done** event → Stop streaming, enable input
  - **error** event → Display error message
- Click conversation in history → Load conversation messages
- Click suggestion → Insert query template into input
- Scroll messages → Auto-scroll to latest message on new content
- Click database table → Expand to show columns

**Navigation from this page**:
- Logout → Clear token → AuthPage

---

## Component Hierarchy

### High-Level Component Tree
```
App
├── AuthPage (if !authenticated)
│   ├── LoginForm
│   └── RegisterForm
└── Main Layout (if authenticated)
    ├── Header
    │   ├── Logo
    │   ├── DatabaseStatus
    │   └── UserMenu (logout button)
    ├── Sidebar
    │   └── SidebarTabs
    │       ├── QueryHistory (tab content)
    │       ├── DatabaseInfo (tab content)
    │       └── SuggestionList (tab content)
    └── ChatContainer
        ├── ChatMessage[] (list)
        │   ├── MessageHeader (role + timestamp)
        │   ├── MessageContent (markdown + SQL)
        │   └── DataViewer (if has query result)
        │       ├── Table (if tabular data)
        │       └── QueryChart (if numeric data)
        └── ChatInput (fixed at bottom)
            ├── TextArea
            └── SendButton
```

---

## Reusable Components

### Component Name 1: ChatMessage

**Purpose**: Display individual chat message (user or assistant)
**Where used**: ChatContainer (repeated for each message)

**Content/Structure**:
- Message role indicator (User or Assistant avatar/label)
- Timestamp (e.g., "2 minutes ago")
- Message content (markdown rendered)
- SQL query code block (if present)
- Query result display (DataViewer if has result)

**Interactive elements**:
- None (display only)

**Variants**:
- User message: Blue background, right-aligned
- Assistant message: Gray background, left-aligned, may include SQL and results
- Thinking indicator: Animated "..." during streaming

---

### Component Name 2: DataViewer

**Purpose**: Display query results as table or chart
**Where used**: ChatMessage (when assistant message has query result)

**Content/Structure**:
- Auto-detection: If numeric columns → chart, else → table
- Table: Header row + data rows (max 20 visible, scroll for more)
- Chart: Bar, line, or pie based on data shape

**Interactive elements**:
- Table sorting: Click column header to sort (optional)
- Chart legend: Click to toggle series (optional)

**States**: Loading | Success (table/chart) | Error (error message)

---

### Component Name 3: ChatInput

**Purpose**: Text input for user messages with send button
**Where used**: ChatContainer (fixed at bottom)

**Content/Structure**:
- Multi-line text area (auto-resize up to 5 lines)
- Send button (paper airplane icon or "Send" text)
- Disabled state while streaming response

**Interactive elements**:
- Type text → Enable send button when text present
- Enter key → Send message (Shift+Enter for new line)
- Click Send → Submit message, clear input

**States**: Enabled | Disabled (while streaming)

---

## UI States

### Loading States

**Where used**:
- Message streaming: "Thinking..." animated indicator in message area
- Query execution: "Executing query..." indicator below message
- Initial load: No loading indicator (immediate render)

**Pattern**: Inline text with animated ellipsis (CSS animation)

---

### Error States

**Where displayed**:
- Login/registration errors: Red text below form
- Chat errors: Red error message in chat message (from assistant)
- Connection errors: Toast notification (optional)

**Error types handled**:
- Authentication failure → "Invalid email or password"
- Token expired → "Session expired, please log in again" → redirect to login
- Query execution error → Claude's error message with context
- Network error → "Connection failed, please try again"

**Recovery actions**:
- Retry button (for network errors)
- Logout and re-login (for auth errors)
- Modify query (for SQL errors)

---

### Empty States

**Where used**:
- New conversation: "Start a conversation by asking a question about your database"
- No query history: "No conversations yet. Start chatting to see history here."
- No suggestions: "Loading suggestions..." or "No suggestions available"

**Pattern**: Centered text with icon (optional)

---

### Success States

**Where used**:
- Login success: Immediate redirect to chat (no explicit feedback)
- Message sent: Immediate "Thinking..." indicator (no toast)
- Query executed: Results displayed inline

**Pattern**: Inline feedback (no toast notifications)

---

## User Flows

### Flow 1: User Authentication and First Query

**Trigger**: User visits app for first time

**Steps**:
1. User lands on AuthPage (sees login form)
2. User clicks "Register" tab
3. User enters email + password, clicks "Register"
4. System creates account, generates JWT, stores token in localStorage
5. User sees main chat interface (empty conversation)
6. User types "How many fans are there?" in ChatInput
7. User presses Enter or clicks Send
8. System streams response:
   - Shows "Thinking..." indicator
   - Shows "Executing query..." when tool called
   - Displays SQL query in code block
   - Displays results table below query
   - Shows "Generated SQL: SELECT COUNT(*) FROM fan" summary
9. User sees complete response with query and results

**Success endpoint**: User viewing first query results in chat
**Failure handling**: Error message shown inline, user can retry

---

### Flow 2: Loading Conversation History

**Trigger**: User clicks conversation in Query History sidebar

**Steps**:
1. User clicks "Query History" tab in sidebar
2. System displays list of conversations (title + timestamp)
3. User clicks conversation "Fan Analysis - 2 hours ago"
4. System fetches conversation with messages (GET /conversations/{id})
5. Chat area clears and loads historical messages
6. User sees full conversation history (user + assistant messages with results)

**Success endpoint**: Historical conversation displayed in chat area
**Failure handling**: Error message "Failed to load conversation" with retry button

---

### Flow 3: Database Schema Exploration

**Trigger**: User wants to see available tables

**Steps**:
1. User clicks "Database Info" tab in sidebar
2. System displays database schema tree
3. User sees tables list (e.g., "fan", "ticket", "communication")
4. User clicks "fan" table to expand
5. System shows columns (e.g., "[fan.id] - int", "[fan.email] - varchar")
6. User sees row count: "~50,000 rows"
7. User uses this info to craft better questions

**Success endpoint**: User understands database structure
**Failure handling**: "Failed to load schema" error message

---

## Forms & Input

### Form 1: Login Form

**Location**: AuthPage (Login tab)
**Purpose**: Authenticate existing user

**Fields**:
- Email - email type - required, email format validation
- Password - password type - required, min 6 chars

**Validation approach**: Client-side (HTML5) + server-side (Pydantic)
**Error display**: Inline below form (red text)

**Submit behavior**:
- Success: Store token in localStorage → redirect to chat
- Error: Show error message ("Invalid email or password")

---

### Form 2: Register Form

**Location**: AuthPage (Register tab)
**Purpose**: Create new user account

**Fields**:
- Email - email type - required, email format validation
- Password - password type - required, min 6 chars
- Confirm Password - password type - required, must match password

**Validation approach**: Client-side (HTML5) + server-side (Pydantic)
**Error display**: Inline below form (red text)

**Submit behavior**:
- Success: Store token in localStorage → redirect to chat
- Error: Show error message ("Email already registered")

---

## Real-time Updates

**Where used**: Chat messages during streaming

**Update mechanism**: Server-Sent Events (EventSource)

**Visual feedback**:
- Thinking indicator: Animated "..." appended to message content incrementally
- Text accumulation: Assistant message grows character by character
- Tool execution: "Executing SQL query..." indicator
- Results appear: Table or chart rendered when tool_result event received

**Examples**:
- Chat streaming: Text accumulates incrementally as SSE events arrive
- Query execution: Results appear when tool execution completes

---

## Responsive Behavior

**Breakpoints approach**: Mobile-first with CSS media queries

**Mobile adaptations** (< 768px):
- Sidebar: Hidden by default, toggle button in header
- Chat messages: Full-width, no left/right margins
- Tables: Horizontal scroll for wide tables
- Charts: Responsive canvas, legend below chart

**Touch interactions**:
- Tap to send message (instead of click)
- Swipe to open/close sidebar (optional)
- Pinch-to-zoom on charts (native browser behavior)

---

## Accessibility Considerations

**Keyboard navigation**: Enter to send message, Tab to navigate form fields

**Screen reader support**:
- ARIA labels on buttons ("Send message", "Logout")
- Alt text on images/icons (if any)
- Role attributes on chat message list

**Focus management**: Focus returns to input after message sent

**ARIA labels**: aria-label on icon buttons, aria-live on streaming message content

---

## Key User Interactions

### Interaction Pattern 1: Sending a Chat Message

**Context**: User in main chat interface with empty input
**User action**: Types message, presses Enter or clicks Send
**System response**:
1. Disable input (prevent duplicate sends)
2. Add user message to chat (blue bubble, right-aligned)
3. Show "Thinking..." indicator immediately
4. Stream SSE events, update assistant message incrementally
5. Re-enable input when streaming completes

**Result**: User sees full response with SQL and results, can send next message

---

### Interaction Pattern 2: Viewing Query Results

**Context**: Assistant message has query result
**User action**: Scrolls to see full table or chart
**System response**:
1. Auto-detect data type (numeric → chart, text → table)
2. Render table with scrollable container (max 20 rows visible)
3. Or render chart (bar/line/pie based on data shape)
4. Show row count: "Showing 20 of 156 rows" below table

**Result**: User understands query results visually

---

### Interaction Pattern 3: Using Query Suggestions

**Context**: User clicks "Suggestions" tab in sidebar
**User action**: Clicks suggestion "Count fans by country"
**System response**:
1. Insert suggestion text into ChatInput
2. Focus input (cursor at end of text)
3. User can edit or send immediately

**Result**: User sends pre-written query with minimal effort

---

## Onboarding/First-Time Experience

**Approach**: Empty state CTAs

**Flow**:
1. User logs in for first time
2. Sees empty chat with message: "Start a conversation by asking a question about your database"
3. Sidebar shows "Database Info" tab with schema (user can explore)
4. User can click "Suggestions" tab to see example queries
5. User sends first message, sees how system works

---

## Notifications & Feedback

**Notification types**:
- Error messages - inline in chat or below forms - red text
- Success messages - none (implicit via immediate response)
- Loading indicators - inline "Thinking..." and "Executing query..."

**Display patterns**:
- Inline message: Errors and status updates in chat message area
- No toast/snackbar: All feedback is contextual (inline)

---
