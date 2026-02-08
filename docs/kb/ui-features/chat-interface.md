# Chat Interface

**Category**: Interface
**Related Projects**: [[db-chat-nl-master]]
**Technologies**: [[react]], [[typescript]], [[react-markdown]], [[server-sent-events]]
**Backend Features**: [[real-time-chat]], [[streaming-responses]], [[nl-to-sql]], [[clarification-system]]

---

## Overview

A real-time chat interface that enables users to ask questions about their database in natural language. The interface displays a conversation-style message thread with streaming AI responses, query execution progress, and interactive clarification prompts.

**Key characteristics**:
- Streaming text responses with live progress indicators
- Real-time query execution feedback with elapsed time tracking
- Intelligent clarification system with clickable options
- Welcome screen with contextual query suggestions
- Empty state handling and error recovery

---

## Layout Structure

### Visual Arrangement

```
┌──────────────────────────────────────────────────────┐
│                   Chat Container                     │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │          Chat Messages Area                │    │
│  │  (Scrollable conversation history)         │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────┐     │    │
│  │  │ User Message                     │     │    │
│  │  │ "How many users are there?"      │     │    │
│  │  └──────────────────────────────────┘     │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────┐     │    │
│  │  │ Assistant Response               │     │    │
│  │  │ [SQL Query]                      │     │    │
│  │  │ [Data Table]                     │     │    │
│  │  │ [Chart - Optional]               │     │    │
│  │  └──────────────────────────────────┘     │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────┐     │    │
│  │  │ Streaming Response               │     │    │
│  │  │ ⚡ Executing query... (5s)       │     │    │
│  │  │ "The results show..."▋           │     │    │
│  │  └──────────────────────────────────┘     │    │
│  │                                            │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  [Suggestions dropdown - if triggered]     │    │
│  ├────────────────────────────────────────────┤    │
│  │ [Textarea: "Ask a question..."]  [Send]    │    │
│  └────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

**Components**:
- **Message Thread**: Scrollable area displaying user and assistant messages in chronological order
- **Streaming Indicator**: Dynamic progress display with spinner, stage text, and elapsed time
- **Clarification Prompt**: Interactive question with clickable option buttons
- **Welcome Screen**: Empty state with contextual suggestion chips based on available tables
- **Input Area**: Textarea with suggestion dropdown and send button at bottom

**Placement**: Main content area of the application, occupying the central and right portion of the screen

---

## Visual Elements

### Main Components

**Chat Messages Container** (ChatContainer.tsx:98-346):
- **Location**: Main scrollable area, fills vertical space above input
- **Contains**: Message list, streaming responses, loading indicators, error messages, auto-scroll anchor
- **Purpose**: Displays conversation history and live responses
- **Visual style**: Clean white background, messages separated by subtle spacing

**Welcome Screen** (ChatContainer.tsx:100-166):
- **Location**: Centered in empty chat area
- **Contains**: Chat icon (SVG), welcome heading, description text, clickable suggestion chips
- **Purpose**: Guides new users with contextual query examples
- **Visual style**: Centered layout with icon, large heading "Welcome to Fan Data Insights", and 4 suggestion chips with emoji icons

**Chat Message Bubble** (ChatMessage.tsx:125-151):
- **Location**: Left-aligned for assistant, right-aligned for user
- **Contains**: Role label, timestamp, message content, optional query results
- **Purpose**: Displays individual conversation turns
- **Visual style**:
  - User messages: Simple paragraph text, blue accent
  - Assistant messages: Markdown-rendered content, SQL code blocks, data tables, charts

**Streaming Response** (ChatContainer.tsx:176-283):
- **Location**: Appears at bottom of message list during AI response
- **Contains**: Progress spinner, stage text, elapsed timer, partial text with cursor, query status badges
- **Purpose**: Provides real-time feedback during query processing
- **Visual style**: Animated spinner, monospace cursor (▋), color-coded status badges

**Progress Indicator** (ChatContainer.tsx:180-196):
- **Location**: Top of streaming message
- **Contains**: Spinning icon, dynamic stage text, elapsed time in seconds/minutes
- **Purpose**: Shows current processing stage and duration
- **Visual style**: Inline layout with spinner + text, changes message based on elapsed time

**Query Status Badges** (ChatContainer.tsx:224-254):
- **Location**: Below progress text during query execution
- **Contains**: Icon (spinner/checkmark/X), status text, elapsed time
- **Purpose**: Shows SQL query execution state
- **Visual style**:
  - Executing: Spinning icon + "Executing SQL query... (Ns)"
  - Success: Green checkmark + "Query executed successfully"
  - Error: Red X + "Query failed, retrying..."

**Thinking Indicator** (ChatContainer.tsx:200-215):
- **Location**: Within streaming message during extended thinking
- **Contains**: Pulsing clock icon, "Thinking deeply..." label, preview of thinking text
- **Purpose**: Indicates AI is using extended reasoning
- **Visual style**: Pulsing animation, truncated preview (last 100 chars)

**Clarification Request** (ChatContainer.tsx:257-280, 286-313):
- **Location**: Within streaming message or as standalone message
- **Contains**: Question icon, question text, optional context, button options
- **Purpose**: Requests user input when query is ambiguous
- **Visual style**: Question icon (❓), multiple clickable option buttons in horizontal layout

**Query Result Display** (ChatMessage.tsx:51-118):
- **Location**: Below assistant message text
- **Contains**: SQL code block, row count, data table, CSV download button, optional chart
- **Purpose**: Shows executed SQL and returned data
- **Visual style**:
  - Header: "SQL Query" label + CSV download button
  - Code: Monospace pre/code block
  - Table: Striped rows, scrollable wrapper, NULL values styled
  - Stats: "N rows returned" below code

### Interactive Elements (ChatInput.tsx)

**Input Textarea** (ChatInput.tsx:169-180):
- **Location**: Bottom of chat container, fixed position
- **Contains**: Multi-line textarea (2 rows), placeholder text
- **Purpose**: User enters natural language questions
- **Visual style**: Rounded corners, border, grows with content

**Send Button** (ChatInput.tsx:181-187):
- **Location**: Right side of input field
- **Contains**: Text "Send" or "Processing..."
- **Purpose**: Submits user message
- **Visual style**: Primary button style, disabled when loading or empty

**Suggestions Dropdown** (ChatInput.tsx:128-166):
- **Location**: Above input field when focused and suggestions available
- **Contains**: List of suggestion items with icons, text, and type hints
- **Purpose**: Autocomplete queries based on history, templates, or column names
- **Visual style**:
  - Dropdown panel above input
  - Each item: Icon (history/template/column) + text + hint label
  - Keyboard navigable with arrow keys
  - Selected item highlighted

**Suggestion Chips (Welcome)** (ChatContainer.tsx:124-157):
- **Location**: Center of welcome screen
- **Contains**: Emoji icon + query text
- **Purpose**: One-click query examples based on database schema
- **Visual style**: Rounded chip buttons, icon + text layout, hover effect

**User Actions**:
- **Type in input**: Shows suggestions dropdown if available
- **Press Enter**: Sends message
- **Press Shift+Enter**: New line in textarea
- **Arrow keys**: Navigate suggestions
- **Tab/Enter on suggestion**: Select suggestion
- **Escape**: Close suggestions
- **Click suggestion chip**: Sends pre-built query
- **Click clarification option**: Responds to clarification request
- **Click CSV download**: Exports query results as CSV file

**Visual States**:
- **Default**: Empty input with placeholder, send button disabled
- **Typing**: Send button enabled, suggestions may appear
- **Loading**: Input disabled, "Processing..." on button, streaming response visible
- **Streaming**: Progress indicator animates, text streams with cursor
- **Query executing**: Spinning badge with elapsed time
- **Query success**: Green checkmark badge
- **Query error**: Red X badge, error message, retry button
- **Clarification**: Question with option buttons, awaiting user selection
- **Error**: Red warning icon, error text, "Try Again" button
- **Empty chat**: Welcome screen with suggestion chips
- **Long query (15s+)**: "Try simpler question" button appears

---

## Responsive Behavior

**Desktop (>1024px)**:
- Full-width chat container with comfortable margins
- Message bubbles max-width for readability
- Data tables scrollable horizontally if wide
- Input field spans full width with send button inline

**Tablet (768-1024px)**:
- Slightly reduced margins
- Messages maintain readability
- Tables may require horizontal scrolling
- Input remains full-width

**Mobile (<768px)**:
- Messages stack full-width
- Suggestion chips wrap vertically
- Input field and button stack or compress
- Tables scroll horizontally in viewport
- Welcome screen icon and text scale down

---

## User Flows

### Ask a Question Flow

1. User sees empty chat with welcome screen and suggestion chips
2. User types question in input field or clicks suggestion chip
3. Input field disabled, "Processing..." appears
4. Progress indicator appears: "Connecting..." → "Analyzing your question..." → "Generating query..."
5. SQL query executes: "Executing query... (Ns)" with elapsed timer
6. Query succeeds: Green checkmark badge appears
7. Streaming text response begins with cursor (▋)
8. Full response completes, query results appear (SQL + table)
9. Chart visualization option appears if data is chartable
10. Input re-enabled, user can ask follow-up

### Clarification Flow

1. User asks ambiguous question: "Show sales"
2. Progress indicator appears
3. Clarification prompt displays: "Which table do you mean?"
4. Options appear as buttons: ["sales_data", "monthly_sales", "sales_summary"]
5. User clicks option
6. Processing resumes with selected option
7. Query executes and results display

### Error Recovery Flow

1. User sends query
2. Query execution fails (timeout, syntax error, etc.)
3. Red X badge appears: "Query failed, retrying..."
4. System attempts retry
5. If still fails: Error message appears with "Try Again" button
6. User clicks "Try Again" to retry last query
7. Or user clicks "Try simpler question" (if 15s+ elapsed)

### Long Query Flow

1. User asks complex question
2. Progress indicator shows elapsed time
3. At 5s: "Analyzing data... (5s)"
4. At 10s: "Processing large dataset... (10s)"
5. At 15s: "Taking longer than usual, almost there... (15s)" + "Try simpler question" button appears
6. At 20s+: "This query is complex, still working... (20s)"
7. User can wait or click "Try simpler question" to cancel and start over

### Extended Thinking Flow

1. User asks complex analytical question
2. "Thinking deeply..." indicator appears with pulsing clock icon
3. Thinking text preview shows last 100 chars of reasoning
4. Thinking completes, regular streaming response begins

---

## Integration Points

**Backend Features Used**:
- [[real-time-chat]] - Server-sent events (SSE) for streaming responses (ChatContainer.tsx:68)
- [[nl-to-sql]] - Converts natural language to SQL queries
- [[query-execution]] - Runs SQL against database and returns results
- [[clarification-system]] - Handles ambiguous queries with user prompts (ChatContainer.tsx:257-313)
- [[streaming-responses]] - Progressive text generation with progress stages

**Technologies**:
- [[react-hooks]] - useState, useEffect, useCallback, useRef, useMemo for state management
- [[typescript]] - Type-safe props, message types, streaming state
- [[react-markdown]] - Renders formatted assistant responses with remarkGfm (ChatMessage.tsx:137)
- [[server-sent-events]] - Real-time streaming via useChat hook
- [[chart-js]] - Data visualization via QueryChart component

**Data Flow**:
- **Input**: User types question → ChatInput validates → onSend callback → sendUserMessage
- **Processing**: useChat hook opens SSE stream → receives progress events → updates streamingState
- **Display**: streamingState renders progress/text/queries → message added to messages array → ChatMessage renders
- **Output**: Query results (columns, data) embedded in message → QueryResultDisplay renders table + chart option

---

## Component Hierarchy

```
ChatContainer
├── ChatMessages (scrollable div)
│   ├── EmptyState (if no messages)
│   │   ├── WelcomeIcon (SVG)
│   │   ├── WelcomeText (h2 + p)
│   │   └── SuggestionChips (button[])
│   ├── ChatMessage[] (for each message)
│   │   ├── MessageHeader (role + timestamp)
│   │   ├── MessageContent
│   │   │   ├── ReactMarkdown (assistant messages)
│   │   │   └── QueryResultDisplay[]
│   │   │       ├── QueryHeader (label + CSV button)
│   │   │       ├── SQLCode (pre/code)
│   │   │       ├── QueryStats (row count)
│   │   │       ├── QueryTable (table)
│   │   │       └── QueryChart (optional)
│   ├── StreamingMessage (if streaming)
│   │   ├── ProgressIndicator
│   │   │   ├── ProgressSpinner (SVG)
│   │   │   ├── ProgressText (stage + elapsed)
│   │   │   └── SimplifyButton (if >15s)
│   │   ├── ThinkingStatus (if extended thinking)
│   │   │   ├── ThinkingIcon (pulsing SVG)
│   │   │   ├── ThinkingLabel
│   │   │   └── ThinkingPreview
│   │   ├── StreamingText (with cursor)
│   │   ├── QueryStatusBadge (executing/success/error)
│   │   └── ClarificationRequest
│   │       ├── ClarificationQuestion
│   │       ├── ClarificationContext
│   │       └── ClarificationOptions (button[])
│   ├── LoadingIndicator (fallback)
│   ├── ErrorMessage
│   │   ├── ErrorIcon
│   │   ├── ErrorText
│   │   └── RetryButton
│   └── AutoScrollAnchor (ref)
└── ChatInput
    ├── SuggestionsDropdown
    │   └── SuggestionItem[]
    │       ├── SuggestionIcon (SVG)
    │       ├── SuggestionText
    │       └── SuggestionHint
    └── ChatInputForm
        ├── Textarea
        └── SendButton
```

---

## Visual Design Patterns

**Color Usage**:
- Primary: Blue accent for user messages and primary buttons
- Secondary: Gray for assistant messages and secondary elements
- Background: White for messages, light gray for page background
- Text: Dark gray for body, lighter gray for timestamps/hints
- Status: Green (success), red (error), yellow (warning), blue (processing)

**Typography**:
- Headings: Large, bold for welcome screen (h2)
- Body text: 14-16px, regular weight for message content
- Labels: 12px, uppercase or bold for message roles, timestamps
- Code: Monospace for SQL queries and query results
- Hints: Smaller, lighter weight for suggestions and metadata

**Spacing**:
- Message padding: Comfortable internal padding (12-16px)
- Message margins: Clear separation between messages (16px vertical)
- Input padding: 12px inside textarea
- Chip gaps: 8px between suggestion chips
- Table cells: Compact padding (8px) for data density

**Visual Effects**:
- Shadows: Subtle box-shadow on messages and input for depth
- Borders: Light borders on input, tables, and suggestion items
- Animations:
  - Spinner rotation (continuous)
  - Cursor blink (▋)
  - Smooth scroll to bottom on new messages
  - Pulsing clock icon during thinking
  - Hover effects on buttons and clickable items

---

## Accessibility

**Keyboard Navigation**:
- **Tab**: Navigate between input, send button, and interactive elements
- **Enter**: Send message (without Shift)
- **Shift+Enter**: New line in textarea
- **Arrow Up/Down**: Navigate suggestions
- **Tab/Enter**: Select highlighted suggestion
- **Escape**: Close suggestions dropdown
- **Space/Enter**: Activate buttons (send, clarification options, chips)

**Screen Reader Support**:
- Message roles announced ("You", "Assistant")
- Timestamps read for each message
- Loading states announced ("Processing...", "Executing query...")
- Error messages read when they appear
- Button labels clear ("Send", "Try Again", "Download CSV")
- Suggestion type hints ("Recent", "Suggested", "Column")

**Focus Management**:
- Input field auto-focused on page load
- Focus returns to input after sending message
- Focus remains on input when suggestions appear
- Focus indicators visible on all interactive elements
- Tab order follows logical visual flow

---

## Code Snippets

**Implementation**: See [[language/snippets/react-chat-streaming.md]]

**Key patterns used**:
- **SSE Streaming Pattern**: useChat hook manages EventSource connection, parses events, updates state (ChatContainer.tsx:68)
- **Auto-scroll Pattern**: useEffect with messagesEndRef.scrollIntoView on message changes (ChatContainer.tsx:76-78)
- **Progressive Feedback Pattern**: streamingState tracks stage, elapsed time, current text (ChatContainer.tsx:29-60)
- **Controlled Input Pattern**: useState for input value, onSend callback lifts state up (ChatInput.tsx:23-49)
- **Suggestion Dropdown Pattern**: Keyboard navigation with arrow keys and selection (ChatInput.tsx:60-102)
- **Memo Optimization**: ChatMessage memoized to prevent unnecessary re-renders (ChatMessage.tsx:121)

---

## Alternatives & Variations

**Similar UI Patterns**:
- **Discord-style threading**: Group messages by day/topic with collapsible sections (Pros: organized history; Cons: more complex navigation)
- **Slack-style threading**: Reply threads for follow-ups (Pros: better conversation context; Cons: harder to implement clarifications)
- **Traditional form-based**: Submit button, full page reload (Pros: simpler; Cons: no streaming, poor UX for long queries)
- **Split-pane**: Input at top, results below (Pros: more screen space for results; Cons: non-standard chat UX)

**When to Use**:
- Use streaming chat pattern when queries take >2s and users need feedback
- Use clarification system when domain has ambiguous terms or multiple similar entities
- Use suggestion chips when users need onboarding or common queries are known
- Use traditional form when queries are instant (<500ms) and streaming adds no value

---

## Related

**UI Features**: [[sidebar-navigation]], [[data-visualization]], [[authentication-page]]
**Backend Features**: [[real-time-chat]], [[nl-to-sql]], [[query-execution]], [[clarification-system]]
**Technologies**: [[react]], [[typescript]], [[react-markdown]], [[server-sent-events]], [[chart-js]]
**Code Examples**: [[language/snippets/react-chat-streaming.md]], [[language/snippets/sse-client.md]]
**Projects Using This**: [[db-chat-nl-master]]

---

## Notes

- Streaming implementation uses EventSource (SSE) for one-way server → client communication
- Progress messages adapt based on elapsed time for better user reassurance during long queries
- Clarification system can interrupt streaming to request user input
- CSV export converts query results to downloadable file client-side (no server round-trip)
- Auto-scroll behavior triggers on both new messages AND streaming text updates
- Input is disabled during processing to prevent multiple concurrent queries
- Error recovery retries last user message automatically
- Welcome screen suggestions dynamically generated from database schema (tables[0].name, columns[0].name)
- NULL values in query results styled distinctly from empty strings
- Extended thinking preview shows last 100 characters to give users insight into reasoning without overwhelming UI
