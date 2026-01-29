# UI Description

## Application Type

**Single-Page Application (SPA)** with real-time streaming chat interface.

---

## UI Structure

### Main Layout

```
┌────────────────────────────────────────────────────────────┐
│  Header: Logo + User Profile + Logout                     │
├─────────────┬──────────────────────────────────────────────┤
│             │                                              │
│   Sidebar   │         Main Content Area                    │
│             │                                              │
│  - Chats    │    (Chat Container / Auth Page /            │
│  - Admin    │     Admin Viewer / Data Viewer)             │
│             │                                              │
│             │                                              │
│             │                                              │
│             │                                              │
└─────────────┴──────────────────────────────────────────────┘
```

**Evidence**: App.tsx:50-200 (main layout structure with sidebar and router)

---

## Pages & Views

### 1. Authentication Page (Login/Register)

**Route**: `/` (when not authenticated)

**Components**:
- Centered auth form with logo
- Email and password inputs
- Password visibility toggle
- Submit button
- Error message display (top of form)

**Layout**:
```
        ┌─────────────────┐
        │    IT Logo      │
        │ Ipswich Town    │
        │ Fan Data Insights│
        └─────────────────┘

        Sign In / Create Account

        Email
        [___________________]

        Password
        [_________________] 👁

        [   Sign In Button   ]

        (Error message here if any)
```

**User Flow**:
1. User enters email and password
2. Clicks "Sign In" or "Create Account"
3. On success: JWT saved to localStorage, redirect to chat
4. On error: Show error message above form

**Evidence**: AuthPage.tsx:10-104 (auth form with toggle), App.tsx:70-80 (routing)

---

### 2. Chat Interface (Main View)

**Route**: `/` (when authenticated)

**Layout**:
```
┌────────────────┬─────────────────────────────────────────────┐
│  Sidebar       │   Chat Area                                 │
│                │                                             │
│  📊 Schema     │   ┌───────────────────────────────────┐   │
│    Tables:     │   │  Message: User                    │   │
│    - access    │   │  "How many fans went to the       │   │
│    - ticket    │   │   Coventry game?"                 │   │
│                │   └───────────────────────────────────┘   │
│  💬 Chats      │   ┌───────────────────────────────────┐   │
│    - Coventry  │   │  Message: Assistant               │   │
│      Analysis  │   │  [Thinking deeply...]             │   │
│    - Top Fans  │   │  "I found 2 Coventry games.       │   │
│                │   │   Which one do you mean?"         │   │
│  👥 Admin      │   │  [ Coventry - Dec 6, 2024 (Home) ]│   │
│    (if admin)  │   │  [ Coventry - Dec 18, 2024 (Away)]│   │
│                │   └───────────────────────────────────┘   │
│                │                                             │
│                │   ─────────────────────────────────────    │
│                │   [Type a question...            ] [Send]  │
└────────────────┴─────────────────────────────────────────────┘
```

**Components**:
- **Left Sidebar** (collapsible):
  - Schema tab: Database tables with columns
  - Chats tab: List of saved conversations
  - Admin tab: All conversations (admin only)

- **Chat Area**:
  - Message list (scrollable)
  - Streaming indicators
  - Query result tables
  - Charts (expandable)

- **Input Area**:
  - Textarea with auto-resize
  - Suggestion dropdown (history + templates)
  - Send button

**Evidence**: App.tsx:50-200 (main layout), ChatContainer.tsx:63-356 (chat area), SidebarTabs.tsx:172-253 (sidebar)

---

### 3. Empty State (No Messages)

**When**: User opens app with no chat history

**UI**:
```
        🗨️
    Welcome to Fan Data Insights

    Ask questions about your data in natural language.
    Claude will analyze and query the database for you.

    ┌──────────────────┬──────────────────┬──────────────────┐
    │ 📊 Count access  │ 📋 View access   │ 🔍 Explore fan_id│
    └──────────────────┴──────────────────┴──────────────────┘

           (or type a question below)
```

**Clickable Suggestion Chips**:
- "Count access"
- "View access"
- "Explore fan_id"
- "List tables"

**Evidence**: ChatContainer.tsx:99-166 (empty state with clickable chips)

---

## Streaming States

### 1. Thinking State (Extended Thinking)

**Visual**:
```
┌───────────────────────────────────────┐
│ 🧠 Thinking deeply...                 │
│ [Analyzing schema relationships...]   │
└───────────────────────────────────────┘
```

**When**: Claude is using Extended Thinking to reason about complex queries

**Evidence**: ChatContainer.tsx:199-215 (thinking indicator)

---

### 2. Executing Query State

**Visual**:
```
┌───────────────────────────────────────┐
│ ⚙️ Executing SQL query...             │
│ (5s)                                  │
└───────────────────────────────────────┘
```

**When**: SQL query is being executed (can take several seconds)

**Evidence**: ChatContainer.tsx:224-240 (query execution indicator with elapsed time)

---

### 3. Streaming Text State

**Visual**:
```
┌───────────────────────────────────────┐
│ There are 15,234 fans who attended   │
│ the Coventry City match on December  │
│ 6th, 2024▋                            │
└───────────────────────────────────────┘
```

**Cursor blinks** to show live streaming

**Evidence**: ChatContainer.tsx:217-223 (streaming text with cursor)

---

### 4. Clarification Request State

**Visual**:
```
┌───────────────────────────────────────────────────┐
│ ❓ Which Coventry game do you mean?              │
│ Found 2 Coventry games in the database           │
│                                                   │
│ ┌───────────────────────────────────────────┐   │
│ │ Coventry City - Dec 6, 2024 (Home)        │   │
│ └───────────────────────────────────────────┘   │
│ ┌───────────────────────────────────────────┐   │
│ │ Coventry City - Dec 18, 2024 (Away)       │   │
│ └───────────────────────────────────────────┘   │
└───────────────────────────────────────────────────┘
```

**User Action**: Click one of the option buttons

**Evidence**: ChatContainer.tsx:256-280 (clarification UI with options)

---

### 5. Progress Indicators by Stage

**Stages and Messages**:
- `connecting` → "Connecting..."
- `thinking` → "Analyzing your question..."
- `generating_sql` → "Generating query..."
- `executing_query` → "Executing query... (Xs)"
- `processing_results` → "Processing results..."

**Time-based overrides**:
- 5s+ → "Analyzing data... (Xs)"
- 10s+ → "Processing large dataset... (Xs)"
- 15s+ → "Taking longer than usual, almost there... (Xs)" + "Try simpler question" button
- 20s+ → "This query is complex, still working... (Xs)"

**Evidence**: ChatContainer.tsx:28-61 (getProgressMessage function)

---

## Sidebar Components

### Schema Tab

**UI**:
```
Databases ⚫ (connected)

[ + Upload JSON File ]

━━━━━━━━━━━━━━━━━━━━━━

▼ access (15,234 rows)        👁 ×
  🔑 id INTEGER
     fan_id VARCHAR
     entry_datetime TIMESTAMP
     product_start_datetime TIMESTAMP
     product_opponent_name VARCHAR

▼ ticket (8,921 rows)          👁 ×
  🔑 id INTEGER
     fan_id_beneficiary VARCHAR
     transaction_datetime TIMESTAMP
     product_location VARCHAR
```

**Interactions**:
- Click table name → Expand/collapse columns
- Click 👁 → Open data viewer modal
- Click × → Delete table (with confirmation)
- Click "+ Upload JSON File" → File picker

**Evidence**: DatabaseInfo.tsx:129-241 (schema tree with expand/collapse)

---

### Chats Tab

**UI**:
```
💬 Chats

┌────────────────────────────────────┐
│ Coventry game attendance           │
│ Today                          × │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ Top 10 fans by ticket purchases    │
│ Yesterday                      × │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ How many fans from USA?            │
│ 2 days ago                     × │
└────────────────────────────────────┘
```

**Interactions**:
- Click conversation → Load in main area
- Click × → Delete conversation (with confirmation)

**Evidence**: SidebarTabs.tsx:66-89 (chat list)

---

### Admin Tab (Admin Only)

**UI**:
```
👥 Admin

┌────────────────────────────────────┐
│ 📧 john@example.com                │
│ "Show me fan demographics"         │
│ Today                              │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ 📧 sarah@example.com               │
│ "Coventry ticket sales"            │
│ Yesterday                          │
└────────────────────────────────────┘
```

**Interactions**:
- Click conversation → Open read-only admin viewer

**Evidence**: SidebarTabs.tsx:94-170 (admin panel), AdminConversationViewer.tsx:13-106 (read-only viewer)

---

## Message Components

### User Message

**UI**:
```
┌─────────────────────────────────────────┐
│ You                            10:23 AM │
│                                         │
│ How many fans went to the Coventry     │
│ game on December 6th?                  │
└─────────────────────────────────────────┘
```

**Evidence**: ChatMessage.tsx:122-135 (user message rendering)

---

### Assistant Message

**UI with Query Results**:
```
┌──────────────────────────────────────────────────────┐
│ Assistant                                   10:23 AM │
│                                                      │
│ There were 15,234 fans who attended the Coventry    │
│ City match at Portman Road on December 6th, 2024.   │
│                                                      │
│ ─────────────────────────────────────────────────── │
│                                                      │
│ SQL Query                            [ ↓ CSV ]      │
│ ┌──────────────────────────────────────────────┐   │
│ │ SELECT COUNT(DISTINCT [access.fan_id])       │   │
│ │ FROM access                                  │   │
│ │ WHERE [access.product_opponent_name]         │   │
│ │   LIKE '%Coventry%'                          │   │
│ │ AND CAST([access.product_start_datetime]     │   │
│ │   AS DATE) = '2024-12-06'                    │   │
│ │ AND [access.entry_datetime] IS NOT NULL      │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ 15,234 rows returned                                │
│                                                      │
│ ┌────────────────────┬──────────────────────┐      │
│ │ count              │ 15234                │      │
│ └────────────────────┴──────────────────────┘      │
│                                                      │
│ [ Show Chart ]                                      │
└──────────────────────────────────────────────────────┘
```

**Features**:
- Markdown rendering (bold, italic, lists, tables)
- SQL code block with syntax highlighting
- Query stats (row count, execution time)
- Result table (scrollable, truncated at 1000 rows)
- CSV download button
- Optional chart visualization

**Evidence**: ChatMessage.tsx:51-152 (query result display with table and chart)

---

## Chart Visualization

**UI** (when "Show Chart" clicked):
```
┌──────────────────────────────────────────────┐
│ [ Bar ] [ Line ] [ Pie ]                     │
│                                              │
│     ▁▂▃▄▅▆█                                  │
│     ▔▔▔▔▔▔▔                                  │
│     Bar Chart Visualization                   │
│     (auto-generated from query results)      │
│                                              │
│ [ Hide Chart ]                               │
└──────────────────────────────────────────────┘
```

**Chart Types**:
- **Bar**: For categorical data with numeric values
- **Line**: For time series or ordered data
- **Pie**: For single numeric column (percentage breakdown)

**Auto-detection**:
- First string column → labels
- Numeric columns → data series
- Multiple numeric columns → multiple bars/lines

**Evidence**: QueryChart.tsx:92-192 (chart rendering with type selection)

---

## Input Component

### Chat Input with Suggestions

**UI**:
```
┌─────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────┐ │
│ │ 🔍 Recent                                     │ │
│ │    How many fans went to the Coventry game?   │ │
│ │                                               │ │
│ │ 📋 Suggested                                  │ │
│ │    Count access by product_opponent_name      │ │
│ │                                               │ │
│ │ 🗃️ Column                                      │ │
│ │    Show access by fan_id                      │ │
│ └───────────────────────────────────────────────┘ │
│                                                   │
│ ┌─────────────────────────────────────────────┐ │
│ │ Ask a question about your data...           │ │
│ │                                             │ │
│ │                                             │ │
│ └─────────────────────────────────────────────┘ │
│                                       [ Send ]   │
└─────────────────────────────────────────────────────┘
```

**Suggestion Types**:
- **Recent** (🔍): From localStorage query history
- **Suggested** (📋): Template-based suggestions (e.g., "Count {table}")
- **Column** (🗃️): Column-based queries (e.g., "Show {table} by {column}")

**Keyboard Navigation**:
- ↓/↑ → Navigate suggestions
- Tab/Enter → Accept suggestion
- Esc → Close suggestions
- Shift+Enter → New line (without sending)
- Enter → Send message

**Evidence**: ChatInput.tsx:16-191 (input with suggestions and keyboard nav), useSuggestions.ts:19-173 (suggestion generation)

---

## Modals & Overlays

### Data Viewer Modal

**When**: User clicks 👁 icon next to table name

**UI**:
```
┌──────────────────────────────────────────────────────┐
│  access - Table Data                           [×] │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌───────┬──────────┬─────────────┬──────────────┐ │
│  │ id    │ fan_id   │ entry_dt    │ opponent     │ │
│  ├───────┼──────────┼─────────────┼──────────────┤ │
│  │ 1     │ F001     │ 2024-12-06  │ Coventry     │ │
│  │ 2     │ F002     │ 2024-12-06  │ Coventry     │ │
│  │ ...   │ ...      │ ...         │ ...          │ │
│  └───────┴──────────┴─────────────┴──────────────┘ │
│                                                      │
│  [ Previous ]   Page 1 (50 rows)   [ Next ]        │
└──────────────────────────────────────────────────────┘
```

**Features**:
- Full-screen modal
- Pagination (50 rows per page)
- Horizontal scroll for wide tables
- NULL value highlighting
- Close button (×)

**Evidence**: DataViewer.tsx:19-147 (modal with pagination)

---

### Admin Conversation Viewer

**When**: Admin clicks conversation in Admin tab

**UI**:
```
┌──────────────────────────────────────────────────────┐
│  [ ← Back to Chat ]                                  │
│                                                      │
│  [ Admin View (Read-only) ]                         │
│  Coventry game attendance                           │
│  john@example.com · Dec 6, 2024                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ User                         10:20 AM      │    │
│  │ How many fans went to Coventry?           │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ Assistant                    10:20 AM      │    │
│  │ There were 15,234 fans...                 │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Features**:
- Read-only view (no input)
- Full conversation history
- User email shown
- Back button returns to regular chat

**Evidence**: AdminConversationViewer.tsx:13-106 (read-only conversation view)

---

## Responsive Design

### Mobile Breakpoints

**< 768px (Mobile)**:
- Sidebar collapses to overlay
- Hamburger menu button
- Single-column layout
- Full-width messages
- Sticky input at bottom

**768px - 1024px (Tablet)**:
- Narrow sidebar (icons only)
- Expand on hover
- Two-column layout maintained

**> 1024px (Desktop)**:
- Full sidebar visible
- Three-column layout (sidebar | chat | metadata)
- Optimal reading width (max 800px for chat)

**Evidence**: Responsive CSS in frontend/src/styles/index.css

---

## Color Scheme & Theming

### Brand Colors

- **Primary Blue**: `#1A365D` (Ipswich Town)
- **Accent Blue**: `#3182CE`
- **Success Green**: `#38A169`
- **Warning Yellow**: `#D69E2E`
- **Error Red**: `#E53E3E`

### UI States

- **Background**: `#F7FAFC` (light gray)
- **Card Background**: `#FFFFFF` (white)
- **Border**: `#E2E8F0` (light gray)
- **Text Primary**: `#2D3748` (dark gray)
- **Text Secondary**: `#718096` (medium gray)
- **Text Muted**: `#A0AEC0` (light gray)

### Message Colors

- **User Message**: `#EBF8FF` (light blue background)
- **Assistant Message**: `#F7FAFC` (light gray background)
- **Streaming Cursor**: `#3182CE` (animated blink)

**Evidence**: frontend/src/styles/index.css (CSS variables and color definitions)

---

## Animation & Transitions

### Loading States

- **Spinner**: Rotating circle (0.6s linear infinite)
- **Thinking Pulse**: Pulsing icon (1.5s ease-in-out infinite)
- **Cursor Blink**: Blinking cursor (1s step-end infinite)

### Transitions

- **Sidebar Toggle**: 0.3s ease-in-out
- **Message Fade-in**: 0.2s ease-in
- **Button Hover**: 0.15s ease
- **Modal Open**: 0.2s ease-out (scale + fade)

### Scroll Behavior

- **Auto-scroll on new message**: Smooth scroll to bottom
- **Manual scroll**: Disable auto-scroll temporarily
- **Scroll restoration**: Restore position on navigation

**Evidence**: frontend/src/styles/index.css (animation keyframes), ChatContainer.tsx:76-78 (auto-scroll)

---

## Accessibility

### Keyboard Navigation

- **Tab**: Navigate through interactive elements
- **Enter**: Submit forms, activate buttons
- **Escape**: Close modals, dismiss suggestions
- **Arrow Keys**: Navigate suggestions
- **Space**: Toggle checkboxes

### Screen Reader Support

- **ARIA labels**: All interactive elements labeled
- **Role attributes**: Proper semantic roles (button, dialog, list)
- **Focus management**: Focus trapped in modals
- **Status announcements**: Streaming updates announced

### Visual Accessibility

- **Contrast ratio**: WCAG AA compliant (4.5:1 minimum)
- **Focus indicators**: Visible outline on keyboard focus
- **Text sizing**: Responsive font sizes (rem units)
- **Color-blind friendly**: Not relying solely on color for info

**Evidence**: Component props with aria-* attributes throughout codebase

---

## User Flows

### 1. First-Time User Flow

```
1. User opens app → See login page
2. Click "Create Account" (sign up disabled in this version)
3. Enter email + password → Click "Sign In"
4. JWT saved → Redirect to chat
5. See welcome message + suggestion chips
6. Click "Count access" chip → Auto-fill input
7. Press Enter → See streaming response
8. Results shown with table + chart option
```

### 2. Returning User Flow

```
1. User opens app → Auto-login (JWT from localStorage)
2. See previous conversations in sidebar
3. Click conversation → Load history
4. Continue chatting
```

### 3. Admin Flow

```
1. Admin user logs in (is_admin=true in JWT)
2. See "Admin" tab in sidebar
3. Click Admin tab → See all users' conversations
4. Click any conversation → Open read-only viewer
5. Review conversation → Click "Back to Chat"
6. Return to own chat interface
```

---

## Error States

### Network Error

```
┌────────────────────────────────────────┐
│ ⚠️ Connection was interrupted          │
│ This can happen with complex queries.  │
│ Please try again.                      │
│                                        │
│ [ Try Again ]                          │
└────────────────────────────────────────┘
```

### Authentication Error

```
┌────────────────────────────────────────┐
│ ⚠️ Invalid email or password           │
└────────────────────────────────────────┘
```

### Query Timeout Error

```
┌────────────────────────────────────────┐
│ ⚠️ This question needs a lot of data   │
│ processing. Try being more specific,   │
│ like "Show top 10..." or "How many...  │
│ in 2024?"                              │
│                                        │
│ [ Try Again ]                          │
└────────────────────────────────────────┘
```

**Evidence**: useChat.ts:269-326 (error handling with user-friendly messages)

---

## Performance Optimizations

### Frontend

- **Code splitting**: Routes lazy-loaded
- **Memoization**: React.memo on ChatMessage, QueryHistory
- **Debouncing**: Suggestion generation debounced (300ms)
- **Virtual scrolling**: Large tables virtualized (future enhancement)

### Backend

- **Streaming**: SSE prevents timeout on long queries
- **Connection pooling**: PostgreSQL connections reused
- **Schema caching**: Database schema cached (refreshed on demand)
- **Query result limiting**: Max 1000 rows per query

**Evidence**: ChatMessage.tsx:121 (React.memo), llm.py:707-1054 (streaming), database_base.py (connection pooling)

---

## Summary

The db-chat-nl UI is a modern, real-time chat interface for database querying with:

- **Streaming AI responses** with live progress indicators
- **Clarification requests** when ambiguity detected
- **Multi-database support** (DuckDB, PostgreSQL, Azure SQL)
- **Admin panel** for monitoring all conversations
- **Chart visualization** for query results
- **Responsive design** for mobile, tablet, desktop
- **Keyboard navigation** and accessibility support
- **Error handling** with user-friendly messages

The interface prioritizes **clarity**, **feedback**, and **usability** to make natural language database querying accessible to non-technical users.
