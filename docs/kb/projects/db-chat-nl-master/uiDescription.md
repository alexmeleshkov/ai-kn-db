# UI Structure & User Experience

> **Purpose**: Document UI structure, component hierarchy, and user flows.
> Focus on WHAT to build (structure, behavior), not HOW to style it.

## Page Structure Overview

**Total pages/screens**: 2 main pages (AuthPage, Chat Application with sidebar)
**Layout pattern**: Single-page app (SPA) with tab-based navigation after login

**Core pages**:
- `/login` - Authentication page with login form
- `/` - Main chat application with database sidebar and conversation tabs

---

## Navigation Structure

**Navigation type**: Tabs in sidebar (Chats view / Admin view)

**Primary navigation items**:
- Chats tab - User's personal conversation history
- Admin tab - Admin-only view of all conversations (requires is_admin=true)
- Database Info - Always-visible sidebar showing schema and upload

**Breadcrumbs**: No breadcrumbs used

---

## Layout Patterns

### Overall Layout Structure
```
┌──────────────────────────────────────────────────────┐
│  AuthPage (full screen centered)                     │
│  ┌────────────────────────────────────────────────┐  │
│  │  Logo (IT circle)                              │  │
│  │  "Ipswich Town Fan Data Insights"              │  │
│  │  Email input                                   │  │
│  │  Password input (with show/hide toggle)       │  │
│  │  Login button                                  │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘

After Login:
┌──────────────────────────────────────────────────────┐
│ Sidebar (left)  │  Main Chat Area (center/right)     │
├─────────────────┼──────────────────────────────────────┤
│ Database Info   │  ChatContainer                      │
│ - Status        │  - Empty state with suggestions OR  │
│ - Upload        │  - Message list with streaming      │
│ - S3 files      │  - Streaming indicators             │
│ - Tables        │  - Clarification UI                 │
│   (expandable)  │  - Error messages                   │
│                 │                                     │
│ SidebarTabs     │  ChatInput                          │
│ - Chats         │  - Autocomplete suggestions         │
│ - Admin         │  - Textarea                         │
│ - Query History │  - Send button                      │
└─────────────────┴──────────────────────────────────────┘
```

**Sidebar**: Fixed left panel with collapsible database schema and conversation tabs
- DatabaseInfo: Schema viewer (always visible at top)
- SidebarTabs: Chats/Admin/Query History tabs
- QueryHistory: Recent queries (collapsible)

**Main content area**: Chat interface with message display and input
- ChatContainer: Message history and streaming responses
- ChatInput: Textarea with autocomplete at bottom

---

## Key Pages/Screens

### Authentication Page

**Route/URL**: `/login`
**Purpose**: User login with JWT authentication

**Layout sections**:
1. Logo section - Ipswich Town FC circular logo
2. Title - "Ipswich Town Fan Data Insights"
3. Login form - Email, password, submit

**Key components**:
- AuthPage - Container component
- Email input - HTML5 email validation
- Password input - Show/hide toggle with emoji (🙈/👁️)
- Submit button - Disabled during submission

**Interactions**:
- User enters email/password → validation (email format, password min 6 chars)
- User clicks submit → POST /auth/login, JWT token stored, redirect to chat
- User toggles password visibility → input type switches text/password

**Navigation from this page**:
- Successful login → Main chat application

**CSS Classes**: auth-page, auth-container, auth-logo, auth-form, auth-error, form-group, password-input-wrapper, password-toggle, auth-submit

---

### Main Chat Application

**Route/URL**: `/`
**Purpose**: Natural language query interface with database schema sidebar

**Layout sections**:
1. Sidebar (left) - Database schema, conversation history, admin panel
2. Chat area (center/right) - Message display and streaming responses
3. Input area (bottom) - Query input with autocomplete

**Key components**:
- DatabaseInfo - Schema viewer with upload/delete
- SidebarTabs - Chats/Admin tabs
- ChatContainer - Message display with streaming
- ChatInput - Query input with suggestions
- ChatMessage - Individual message with markdown/tables/charts
- QueryChart - Chart.js visualization
- DataViewer - Modal table data viewer
- QueryHistory - Recent queries (collapsible sidebar)
- AdminConversationViewer - Read-only admin view

**Interactions**:
- User types query → autocomplete suggestions appear (history/template/column)
- User submits query → SSE streaming begins, progress indicators show
- Claude executes SQL → Query results display with table/chart
- Claude requests clarification → Buttons appear with options
- User clicks suggestion chip → Query populates input
- User clicks table in schema → Modal opens with paginated data
- User uploads JSON file → New table created in database
- Admin views conversation → Read-only view with all messages

**Navigation from this page**:
- Click conversation in sidebar → Load conversation messages
- Click admin tab → View all conversations
- Click table view button → Modal opens with DataViewer

**CSS Classes**: chat-container, chat-messages, empty-state, welcome-chips, message (user/assistant), streaming, progress-indicator, thinking-status, tool-status, clarification-request, chat-input-wrapper, suggestions-dropdown, database-info, table-section, sidebar-tabs

---

## Component Hierarchy

### High-Level Component Tree
```
App
├── AuthPage (unauthenticated)
│   ├── Logo
│   ├── Form
│   │   ├── Email Input
│   │   ├── Password Input (with show/hide toggle)
│   │   └── Submit Button
│   └── Error Message
│
└── Main Application (authenticated)
    ├── Sidebar
    │   ├── DatabaseInfo
    │   │   ├── Status Indicator
    │   │   ├── Upload Section
    │   │   ├── S3 Files List
    │   │   └── Tables List (expandable)
    │   │       ├── Table Header (name, row count, view/delete buttons)
    │   │       └── Columns List (name, type, primary key indicator)
    │   ├── SidebarTabs
    │   │   ├── Chats Tab (user conversations)
    │   │   ├── Admin Tab (all conversations, admin only)
    │   │   └── Conversation List Items
    │   └── QueryHistory (collapsible)
    │       └── Query Items (recent 10)
    │
    ├── ChatContainer
    │   ├── Empty State (with suggestion chips)
    │   ├── Message List
    │   │   └── ChatMessage[]
    │   │       ├── Message Header (role + time)
    │   │       ├── Message Content (markdown)
    │   │       ├── Executed Queries[]
    │   │       │   ├── SQL Code Block
    │   │       │   ├── Query Table (thead + tbody)
    │   │       │   ├── CSV Download Button
    │   │       │   └── QueryChart
    │   │       └── Query Error
    │   ├── Streaming Indicator
    │   │   ├── Progress Message (time-based)
    │   │   ├── Extended Thinking Status (with preview)
    │   │   ├── Streaming Text (with cursor)
    │   │   └── Tool Status (executing/success/error)
    │   ├── Clarification Request
    │   │   ├── Question
    │   │   ├── Context
    │   │   └── Option Buttons[]
    │   └── Error Message (with retry button)
    │
    ├── ChatInput
    │   ├── Suggestions Dropdown[]
    │   │   ├── Suggestion Icon (history/template/column)
    │   │   ├── Suggestion Text
    │   │   └── Suggestion Hint (type label)
    │   ├── Textarea
    │   └── Send Button
    │
    └── Modals
        ├── DataViewer (table data pagination)
        │   ├── Header (title + close button)
        │   ├── Data Table (scrollable)
        │   └── Pagination (Previous/Next, page info)
        └── AdminConversationViewer (read-only conversation)
            ├── Header (back button, "Read-only" badge, user email, date)
            └── Messages List[]
```

---

## Reusable Components

### ChatMessage

**Purpose**: Renders individual message with markdown, SQL results, tables, charts, CSV export
**Where used**: ChatContainer message list

**Content/Structure**:
- Message header: role label ("You" or "Assistant") + timestamp
- Message content: ReactMarkdown with GFM support
- Executed queries: SQL code block, result table, chart visualization, CSV download
- NULL value styling: null cells get special styling
- Error display: red error message for failed queries

**Interactive elements**:
- CSV download button: Exports query results to CSV file
- Table scrolling: Horizontal scroll for wide tables
- Chart toggle: Automatic chart rendering for chartable data

**States**: Normal, with query results, with error, with chart

**CSS Classes**: chat-message, message-header, message-role, message-time, message-content, executed-queries, query-result, query-header, sql-code, query-stats, query-table-wrapper, query-table, null-value, table-truncated, query-error, csv-download-btn

---

### ChatInput

**Purpose**: Query input with autocomplete suggestions and keyboard navigation
**Where used**: Bottom of ChatContainer

**Content/Structure**:
- Suggestions dropdown: Positioned above input (absolute)
- Textarea: 2 rows, auto-expanding
- Send button: Disabled when empty or submitting

**Interactive elements**:
- Autocomplete: Shows suggestions (history/template/column) based on input
- Keyboard navigation: ArrowUp/Down to select, Tab/Enter to apply, Escape to dismiss
- Submit: Enter to send (Shift+Enter for newline)
- Focus management: Shows suggestions on focus, hides on blur (150ms delay)

**States**: Empty, with suggestions, submitting, disabled

**CSS Classes**: chat-input-wrapper, suggestions-dropdown, suggestion-item (.selected, .history, .template, .column), suggestion-icon, suggestion-text, suggestion-hint, chat-input-form, chat-input, send-button

---

### DatabaseInfo

**Purpose**: Database schema viewer with table/column display, file upload, S3 integration
**Where used**: Top of sidebar (always visible)

**Content/Structure**:
- Status indicator: Green (connected) / Red (disconnected)
- Upload section: File input (JSON only) + upload button
- S3 files section: File list with name, size (GB/MB), loaded status (✓/○)
- Tables list: Expandable table sections with columns

**Interactive elements**:
- Table expand/collapse: Click header to toggle columns
- View table button: Opens DataViewer modal with paginated data
- Delete table button: Confirmation dialog, then deletes table
- Upload button: Triggers hidden file input
- File upload: Uploads JSON, creates table, refreshes schema

**States**: Loading, loaded, error, no tables

**CSS Classes**: database-info (.loading, .error), database-info-header, status-indicator (.connected, .disconnected), upload-section, upload-button, upload-error, s3-storage-section, s3-header, s3-files, s3-file-item, database-tables, table-section, table-header, expand-icon, table-name, table-row-count, view-table-btn, delete-table-btn, table-columns, column-item, column-name, column-type, no-tables

---

### QueryChart

**Purpose**: Automatic chart visualization for query results using Chart.js
**Where used**: Inside ChatMessage after successful query with chartable data

**Content/Structure**:
- Chart.js canvas: Bar, line, or pie chart
- Legend: Automatic legend generation
- Color palette: 8-color Ipswich Town scheme (#0E4C92 blue, #FFFFFF white, #D4AF37 gold, etc.)

**Interactive elements**:
- Chart type detection: Auto-detects bar/line/pie based on data structure
- Hover tooltips: Shows data values on hover
- Legend toggle: Click legend to show/hide datasets

**Variants**:
- Bar chart: For categorical data with numeric values
- Line chart: For time series or sequential data
- Pie chart: For proportional data (single dataset, small row count)

**CSS Classes**: query-chart, chart-container

---

### DataViewer

**Purpose**: Modal table data viewer with pagination (50 rows per page)
**Where used**: Opens when clicking "view" button on table in DatabaseInfo

**Content/Structure**:
- Header: Table name + subtitle + close button
- Data table: thead with columns, tbody with rows
- Pagination: Previous/Next buttons, page number, row count

**Interactive elements**:
- Pagination: Navigate 50 rows at a time
- Close button: Closes modal, returns to main view
- Scrolling: Horizontal/vertical scroll for large tables

**States**: Loading (spinner), loaded (data table), error (error message), empty (no data)

**CSS Classes**: data-viewer, data-viewer-header, data-viewer-title, data-viewer-subtitle, data-viewer-close, data-viewer-content, data-viewer-loading, data-viewer-error, data-viewer-table-wrapper, data-viewer-table, null-value, data-viewer-pagination, data-viewer-empty

---

### SidebarTabs

**Purpose**: Tab navigation for Chats (user conversations), Admin (all conversations), and conversation list
**Where used**: Sidebar below DatabaseInfo

**Content/Structure**:
- Tab buttons: Chats, Admin (if is_admin)
- Conversation list: Scrollable list of conversations
- New chat button: Creates new conversation
- Conversation items: Title, timestamp, delete button

**Interactive elements**:
- Tab switching: Click to switch between Chats/Admin views
- Conversation click: Loads conversation messages
- Delete conversation: Confirmation, then DELETE request
- New chat: Clears current conversation, starts fresh

**States**: Chats view, Admin view, loading, empty

**CSS Classes**: sidebar-tabs, tab-buttons, tab-button (.active), conversations-list, conversation-item (.active), conversation-title, conversation-date, delete-conversation-btn, new-chat-btn

---

### AdminConversationViewer

**Purpose**: Read-only admin view of any user's conversation with messages
**Where used**: Opens when admin clicks conversation in Admin tab

**Content/Structure**:
- Header: Back button, "Read-only" badge, conversation title, user email, date
- Messages list: All messages in conversation (user + assistant)
- Message items: Role label, timestamp, content

**Interactive elements**:
- Back button: Returns to admin conversation list
- No editing: Read-only view (no input, no actions)

**States**: Loading (spinner), loaded (messages), error (error message), empty (no messages)

**CSS Classes**: admin-viewer, admin-viewer-loading, loading-spinner, admin-viewer-error, admin-viewer-header, admin-viewer-close, admin-viewer-info, admin-viewer-badge, admin-viewer-meta, admin-viewer-user, admin-viewer-date, admin-viewer-messages, admin-viewer-empty, admin-viewer-message (.user, .assistant), admin-viewer-message-header, admin-viewer-message-role, admin-viewer-message-time, admin-viewer-message-content

---

### QueryHistory

**Purpose**: Collapsible sidebar section showing recent queries (max 10 visible)
**Where used**: Sidebar below SidebarTabs

**Content/Structure**:
- Header: "Recent Queries" + collapse button
- Query items: Query text (truncated), relative timestamp
- Clear button: Clears all history

**Interactive elements**:
- Collapse toggle: Show/hide query list
- Query click: Populates input with query text
- Clear history: Removes all queries from localStorage

**States**: Collapsed, expanded, empty (no queries)

**CSS Classes**: query-history, query-history-header, collapse-btn, query-list, query-item, query-text, query-time, clear-history-btn, no-queries

---

## UI States

### Loading States

**Where used**:
- ChatContainer - "Analyzing schema...", "Connecting to Claude..."
- DatabaseInfo - Spinner + "Loading schema..."
- DataViewer - Spinner + "Loading data..."
- AdminConversationViewer - Spinner + "Loading conversation..."

**Pattern**: Spinner (rotating icon) + descriptive text

**Spinner animation**: CSS rotation animation, 360deg infinite linear

---

### Error States

**Where displayed**:
- ChatContainer - Error message + "Retry" button
- ChatInput - Red border + error text
- DatabaseInfo - "Failed to load schema" message
- DataViewer - "Failed to load data" message
- AuthPage - Red error message below form

**Error types handled**:
- Network errors - "Could not connect to server"
- Authentication errors - "Invalid email or password"
- Database errors - SQL execution errors with error message
- Timeout errors - "Query took too long (>30s)"

**Recovery actions**:
- Retry button - Resends last request
- Clear error - Click to dismiss error
- Auto-clear - Errors clear on new action

---

### Empty States

**Where used**:
- ChatContainer - Welcome message + suggestion chips ("How many...", "View all tables", etc.)
- DatabaseInfo - "No databases loaded. Upload a JSON file to get started."
- QueryHistory - "No query history yet"
- SidebarTabs (Chats) - "No conversations yet"

**Pattern**: Icon + message + helpful CTA or suggestion chips

**Empty state suggestions**: Based on first table in schema ("How many [table] records?")

---

### Success States

**Where used**:
- Query execution - Green checkmark + "Success" in tool status
- File upload - "File uploaded successfully"
- Login - Redirect to main application

**Pattern**: Green checkmark icon + success message (inline or toast)

---

## User Flows

### Primary User Journey: Natural Language Query

**Trigger**: User types question in chat input

**Steps**:
1. User types query (e.g., "How many fans bought tickets?")
2. System shows autocomplete suggestions (history/templates/columns)
3. User presses Enter or clicks Send button
4. System sends POST /chat with SSE streaming
5. Progress indicator shows "Analyzing schema..." → "Thinking..." → "Generating SQL..." → "Executing query..."
6. Extended thinking (if enabled): Pulse icon + thought preview
7. Tool execution: "Executing SQL..." with spinner
8. Results display: Table with columns/rows, NULL styling, CSV download button
9. Chart visualization: Automatic chart rendering if data is chartable
10. Success: Green checkmark + "Success" in tool status

**Success endpoint**: Query results displayed with table and optional chart
**Failure handling**: Error message + "Retry" button, error context from QueryValidator

---

### Secondary User Journey: Clarification Flow

**Trigger**: Claude API calls ask_clarification tool (ambiguous query)

**Steps**:
1. User asks ambiguous question (e.g., "How many fans went to the Coventry game?")
2. System detects multiple matches (discovery query finds 2+ games)
3. Claude calls ask_clarification tool
4. Streaming stops, clarification UI appears
5. Question: "Which Coventry game?"
6. Context: "Multiple matches found"
7. Option buttons: "Coventry Home (2023-10-15)", "Coventry Away (2024-03-22)"
8. User clicks option button
9. System sends POST /chat with selected option
10. Claude generates specific query with selected date
11. Results display as normal

**Success endpoint**: Query results with correct game data
**Failure handling**: If clarification fails, user can rephrase query

---

### User Journey: Database Schema Exploration

**Trigger**: User wants to see database structure or upload data

**Steps**:
1. User views DatabaseInfo sidebar (always visible)
2. Status indicator shows "Connected" (green) or "Disconnected" (red)
3. User clicks table header to expand columns
4. Columns list shows: column name, type, primary key indicator (🔑)
5. User clicks "View" button (👁) on table
6. DataViewer modal opens with first 50 rows
7. User navigates with Previous/Next pagination
8. User closes modal with × button

**Alternative flow (Upload)**:
1. User clicks "Upload JSON" button
2. File input dialog opens (accept=".json")
3. User selects JSON file
4. System uploads file, creates table
5. Schema refreshes, new table appears
6. Success message or error message displays

**Success endpoint**: Schema visible with expandable tables, or new table created

---

### Admin Journey: View User Conversation

**Trigger**: Admin clicks "Admin" tab in sidebar (requires is_admin=true)

**Steps**:
1. Admin clicks Admin tab
2. System fetches GET /admin/conversations (limit=200)
3. Conversation list displays with user email + date
4. Admin clicks conversation item
5. AdminConversationViewer opens
6. Header shows: "Read-only" badge, user email, date
7. Messages list shows all messages (user + assistant)
8. Admin reviews conversation (no editing)
9. Admin clicks "Back" button
10. Returns to admin conversation list

**Success endpoint**: Read-only view of any user's conversation
**Failure handling**: 403 error if user is not admin, 404 if conversation not found

---

## Forms & Input

### Login Form

**Location**: AuthPage (full screen centered)
**Purpose**: User authentication with JWT tokens

**Fields**:
- Email - email type - HTML5 email validation, required
- Password - password/text (toggle) - minLength=6, required

**Validation approach**: Client-side (HTML5) + server-side (FastAPI)
**Error display**: Inline below form (auth-error class)

**Submit behavior**:
- Success: JWT token stored, redirect to main app
- Error: "Invalid email or password" or "User not found"

**CSS Classes**: auth-form, form-group, password-input-wrapper, password-toggle, auth-submit, auth-error

---

### Chat Input Form

**Location**: Bottom of ChatContainer
**Purpose**: Natural language query input with autocomplete

**Fields**:
- Query textarea - text - 2 rows, auto-expanding

**Validation approach**: Client-side (non-empty check)
**Error display**: None (send button disabled if empty)

**Submit behavior**:
- Success: SSE streaming begins, input clears
- Error: Error message displays with retry button

**CSS Classes**: chat-input-form, chat-input, send-button

---

## Modals & Overlays

### DataViewer Modal

**Trigger**: Click "View" button (👁) on table in DatabaseInfo
**Purpose**: View table data with pagination (50 rows per page)

**Content**:
- Header: Table name + "Table Data" subtitle + close button (×)
- Data table: Scrollable table with columns and rows
- Pagination: Previous/Next buttons + page info

**Actions**:
- Previous button → Load previous page (offset -= 50)
- Next button → Load next page (offset += 50)
- Close button (×) → Close modal

**Dismissal**: Click close button (× icon)

**CSS Classes**: data-viewer, data-viewer-header, data-viewer-title, data-viewer-subtitle, data-viewer-close, data-viewer-content, data-viewer-table-wrapper, data-viewer-table, data-viewer-pagination

---

### AdminConversationViewer Modal

**Trigger**: Admin clicks conversation in Admin tab
**Purpose**: Read-only view of user conversation

**Content**:
- Header: Back button (←), "Read-only" badge, user email, date
- Messages list: All messages (user + assistant)

**Actions**:
- Back button (←) → Return to admin conversation list

**Dismissal**: Click back button

**CSS Classes**: admin-viewer, admin-viewer-header, admin-viewer-close, admin-viewer-info, admin-viewer-badge, admin-viewer-meta, admin-viewer-messages, admin-viewer-message

---

## Data Display Patterns

### Query Result Tables

**Where used**: ChatMessage component after successful SQL execution

**Display pattern**: HTML table with thead/tbody

**Columns/Fields shown**:
- Dynamic based on SQL query columns
- NULL values get special styling (gray italic "NULL")
- Objects serialized to JSON string

**Sorting**: No sorting (results as returned by SQL)
**Filtering**: No filtering (use SQL WHERE clause)
**Pagination**: Truncation notice if >100 rows returned

**Row actions**:
- CSV export button: Downloads all rows as CSV file
- Chart visualization: Automatic if data is chartable

**CSS Classes**: query-table-wrapper, query-table, null-value, table-truncated

---

### Conversation Lists

**Where used**: SidebarTabs (Chats/Admin views)

**Display pattern**: Vertical list of conversation items

**Columns/Fields shown**:
- Conversation title (first user message or auto-generated)
- Timestamp (relative: "2 hours ago")
- Delete button (× icon, Chats view only)

**Sorting**: Reverse chronological (newest first)
**Filtering**: No filtering (separate tabs for Chats/Admin)
**Pagination**: Scroll to load more (if implemented)

**Row actions**:
- Click conversation → Load messages
- Click delete (×) → Confirm dialog, DELETE request

**CSS Classes**: conversations-list, conversation-item (.active), conversation-title, conversation-date, delete-conversation-btn

---

## Real-time Updates

**Where used**: ChatContainer during query execution

**Update mechanism**: Server-Sent Events (SSE) - unidirectional server→client streaming

**Visual feedback**:
- Progress indicator: Spinner + descriptive message (time-based)
- Extended thinking: Pulse icon + thought preview (last 100 chars)
- Streaming text: Text appears with blinking cursor
- Tool status: "Executing SQL...", "Success" (green ✓), "Error" (red ✗)

**Examples**:
- Query execution: Real-time progress ("Analyzing schema...", "Executing query...")
- Extended thinking: Thought preview updates as Claude thinks
- Clarification requests: Stops streaming, shows option buttons

**SSE Event Types**:
- `text`: Assistant response text
- `thinking`: Extended thinking content
- `tool_start`: Tool execution begins
- `tool_result`: Tool execution result (data or error)
- `done`: Streaming complete
- `error`: Error occurred

---

## Responsive Behavior

**Breakpoints approach**: Mobile-first (evidence: 768px breakpoint in CSS)

**Mobile adaptations**:
- Sidebar → Hamburger menu or slide-over drawer (likely)
- Tables → Horizontal scroll
- Charts → Resize to fit container
- Input → Full-width bottom bar

**Touch interactions**:
- Touch-friendly button sizes (minimum 44x44px)
- Swipe gestures (not implemented in scanned code, but common for mobile)

---

## Accessibility Considerations

**Keyboard navigation**: Supported in ChatInput (ArrowUp/Down, Tab, Enter, Escape)

**Screen reader support**:
- Semantic HTML (button, input, textarea, table elements)
- Role labels (message-role: "You", "Assistant")
- Status indicators (status-indicator with text)

**Focus management**:
- Input auto-focus after suggestions applied
- Modal focus trap (close button accessible)
- Escape key to dismiss modals/suggestions

**ARIA labels**: Not explicitly mentioned in scanned code, should be added for icons and status indicators

---

## Branding & Visual Identity

**Color Scheme**: Ipswich Town FC colors (evidence: index.css, QueryChart.tsx)
- Primary blue: #0E4C92 (Ipswich Town blue)
- White: #FFFFFF
- Gold accent: #D4AF37 (Ipswich Town gold)
- Chart palette: 8 colors including blue, gold, red, green, orange, purple, pink, teal

**Logo**: Ipswich Town FC circular logo (IT circle) - displayed on AuthPage

**Typography**: Not specified in scanned patterns, but likely sans-serif for readability

**Styling Methodology**: CSS classes with BEM-like naming (component-element pattern)

**Animations**:
- Spinner rotation: 360deg infinite linear
- Pulse animation: Extended thinking indicator
- Cursor blink: Streaming text cursor

---

## Key User Interactions

### Autocomplete Suggestion Selection

**Context**: User typing in ChatInput
**User action**: Types query, suggestions appear, uses ArrowUp/Down to select, presses Tab or Enter
**System response**: Selected suggestion highlighted (blue background)
**Result**: Suggestion text populates input, suggestions hide, input focuses

---

### Query Execution with Streaming

**Context**: User submits query in ChatInput
**User action**: Presses Enter or clicks Send button
**System response**:
- Input clears
- SSE streaming begins
- Progress indicator shows "Analyzing schema..." (0-5s), "Longer than usual..." (15s), "Complex query..." (20s)
- Extended thinking shows pulse icon + thought preview
- Tool execution shows spinner + "Executing SQL..."
**Result**: Query results display with table, optional chart, CSV download button

---

### Clarification Option Selection

**Context**: Claude requests clarification during query execution
**User action**: Clicks one of the option buttons
**System response**:
- Selected option sent to backend
- SSE streaming resumes
- Specific query executes with selected context
**Result**: Query results display with correct data

---

## Onboarding/First-Time Experience

**Approach**: Empty state with suggestion chips

**Flow**:
1. User logs in for first time
2. Empty state displays: "Ask me anything about your data!"
3. Suggestion chips show examples based on first table: "How many [table]?", "View all tables", "Explore [table]", etc.
4. User clicks suggestion chip or types own query
5. Results display with table/chart
6. User learns by example

**No formal tutorial**: Learning through suggestion chips and real-time feedback

---

## Search & Discovery

**Where available**: Not implemented (no search bar)

**Discovery mechanism**:
- Database schema sidebar (tables/columns)
- Query suggestions (autocomplete)
- Recent query history

**Search alternative**: Natural language queries act as search (e.g., "Find all fans who...")

---

## Notifications & Feedback

**Notification types**:
- Success - Green checkmark in tool status ("Success")
- Error - Red error message with retry button
- Info - Progress indicators (spinner + text)
- Clarification - Yellow/orange clarification request UI

**Display patterns**:
- Inline message: Error/success in ChatContainer
- Progress indicator: Time-based messages during query execution
- Tool status: Icon + label (executing/success/error)

**No toast/snackbar**: All feedback inline within relevant component

---
