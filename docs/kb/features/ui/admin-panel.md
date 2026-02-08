# Admin Panel

**Category**: Interface
**Related Projects**: [[db-chat-nl-master]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Backend Features**: [[admin-access]], [[conversation-history]]

---

## Overview

A read-only conversation viewer for administrators to monitor and review any user's conversations. Admins can browse a list of all conversations across users, select one, and view the full message history without the ability to reply or modify.

**Key characteristics**:
- Read-only conversation display with "Admin View" badge
- User email and metadata prominently displayed
- Full message history with timestamps
- Back navigation to return to chat list
- Clear visual distinction from regular chat interface

---

## Layout Structure

### Visual Arrangement

```
┌──────────────────────────────────────────────────────┐
│  [← Back to Chat]      ADMIN VIEW (READ-ONLY)        │
│                                                      │
│  Conversation Title                                  │
│  user@example.com | Jan 5, 2026 10:30 AM            │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ User                    10:30 AM           │    │
│  │ How many users are in the database?       │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ Assistant                10:30 AM          │    │
│  │ Let me check that for you...              │    │
│  │ [SQL Query displayed]                     │    │
│  │ There are 1,245 users in the database.   │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ User                    10:31 AM           │    │
│  │ What about active users?                  │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │ Assistant                10:31 AM          │    │
│  │ [Response content...]                     │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Components**:
- **Admin Header**: Back button, "Admin View" badge, conversation title, user metadata
- **Message Thread**: Scrollable list of all messages in chronological order
- **Message Items**: Role label (User/Assistant), timestamp, message content
- **Empty State**: Message when conversation has no messages
- **Loading State**: Spinner while fetching conversation

**Placement**: Replaces main chat area when admin selects a conversation from admin tab

---

## Visual Elements

### Main Components

**Admin Viewer Container** (AdminConversationViewer.tsx:66-104):
- **Location**: Full-width main content area
- **Contains**: Header section, scrollable messages section
- **Purpose**: Displays read-only conversation for admin review
- **Visual style**: Similar to chat interface but with distinct header and no input field

**Admin Header** (AdminConversationViewer.tsx:68-83):
- **Location**: Top of viewer, fixed or sticky
- **Contains**: Back button with arrow icon, "Admin View (Read-only)" badge, conversation title (h2), user email, creation date
- **Purpose**: Identifies conversation context and provides navigation
- **Visual style**:
  - Badge: Pill-shaped, distinct color (yellow/orange) to indicate admin mode
  - Title: Large heading (h2)
  - Metadata: Email + date in smaller, lighter text below title
  - Back button: Icon + "Back to Chat" text on left

**Back Button** (AdminConversationViewer.tsx:69-74):
- **Location**: Top-left of admin header
- **Contains**: Arrow-left SVG icon, "Back to Chat" text
- **Purpose**: Return to main chat interface
- **Visual style**: Secondary button, icon + text inline

**Admin View Badge** (AdminConversationViewer.tsx:76):
- **Location**: Top of header, above title
- **Contains**: Text "Admin View (Read-only)"
- **Purpose**: Clearly indicates restricted mode
- **Visual style**: Pill/chip shape, contrasting color (e.g., orange/yellow background)

**Conversation Metadata** (AdminConversationViewer.tsx:77-81):
- **Location**: Below conversation title in header
- **Contains**: User email, formatted creation date
- **Purpose**: Shows who owns the conversation and when it started
- **Visual style**: Smaller font, lighter gray, inline with separator (|)

**Messages Section** (AdminConversationViewer.tsx:85-103):
- **Location**: Below header, scrollable
- **Contains**: List of message items or empty state
- **Purpose**: Displays full conversation history
- **Visual style**: White background, vertical stack of message bubbles

**Message Item** (AdminConversationViewer.tsx:90-101):
- **Location**: Stacked vertically in messages section
- **Contains**: Role badge (User/Assistant), timestamp, message content
- **Purpose**: Displays individual conversation turn
- **Visual style**:
  - Role-based class: `.user` or `.assistant` for styling
  - Header: Role + timestamp in flex layout
  - Content: Plain text (no markdown rendering in this view)
  - Padding: 12-16px internal spacing
  - Border or background to distinguish messages

**Empty State** (AdminConversationViewer.tsx:87):
- **Location**: Centered in messages section when no messages
- **Contains**: Text "No messages in this conversation"
- **Purpose**: Indicates empty conversation
- **Visual style**: Centered, light gray text

**Loading State** (AdminConversationViewer.tsx:45-52):
- **Location**: Full admin viewer area
- **Contains**: Spinner, "Loading conversation..." text
- **Purpose**: Feedback while fetching conversation data
- **Visual style**: Centered spinner + text

**Error State** (AdminConversationViewer.tsx:55-63):
- **Location**: Full admin viewer area
- **Contains**: Error message ("Conversation not found" or custom error), "Go Back" button
- **Purpose**: Handle failed fetches or missing conversations
- **Visual style**: Centered error text + secondary button

### Interactive Elements

**Back Button** (AdminConversationViewer.tsx:69-74):
- **Click**: Calls onClose() callback, returns to main chat
- **Visual feedback**: Hover state, cursor pointer

**Go Back Button (Error)** (AdminConversationViewer.tsx:60):
- **Click**: Calls onClose() callback, exits error state
- **Visual feedback**: Secondary button hover

**User Actions**:
- **Click "Back to Chat"**: Return to main chat interface
- **Scroll messages**: Browse full conversation history
- **Click "Go Back" (error)**: Exit viewer on error

**Visual States**:
- **Loading**: Spinner + "Loading conversation..."
- **Loaded**: Header + message thread displayed
- **Empty**: Header + "No messages in this conversation"
- **Error**: Error message + "Go Back" button
- **Read-only**: No input field, no reply button, no delete actions

---

## Responsive Behavior

**Desktop (>1024px)**:
- Full-width main content area
- Header with back button, badge, title, and metadata in single row or stacked
- Messages display with comfortable margins
- Timestamps visible on all messages

**Tablet (768-1024px)**:
- Header may stack: back button on top row, title/metadata below
- Messages adjust width but maintain readability
- Timestamps may wrap or abbreviate

**Mobile (<768px)**:
- Header stacks vertically: back button, badge, title, metadata each on own line
- Messages full-width with minimal margins
- Timestamps abbreviated or moved below content
- Scrolling optimized for touch

---

## User Flows

### View User Conversation (Admin)

1. Admin clicks conversation in admin tab of sidebar
2. Main area transitions to AdminConversationViewer
3. Loading state appears: spinner + "Loading conversation..."
4. Conversation data fetches (user email, title, messages)
5. Header displays with "Admin View" badge, user email, title, date
6. Messages render in chronological order
7. Admin scrolls to read full conversation
8. Admin clicks "Back to Chat" to return

### Handle Empty Conversation

1. Admin clicks conversation that has no messages
2. Viewer loads successfully
3. Header displays with conversation metadata
4. Messages section shows "No messages in this conversation"
5. Admin clicks "Back to Chat" to return

### Handle Error State

1. Admin clicks conversation
2. Fetch fails (network error, auth issue, conversation deleted)
3. Error state displays: "Conversation not found" or error message
4. "Go Back" button appears
5. Admin clicks "Go Back" to return to chat

---

## Integration Points

**Backend Features Used**:
- [[admin-access]] - Verify user has admin privileges to access viewer
- [[conversation-history]] - Fetch full conversation with messages (getAdminConversation API, AdminConversationViewer.tsx:26)
- [[authentication]] - Ensure only admins can access this view

**Technologies**:
- [[react-hooks]] - useState for conversation data, loading, error states (AdminConversationViewer.tsx:14-16)
- [[react-hooks]] - useEffect for fetching on conversationId change (AdminConversationViewer.tsx:18-20)
- [[typescript]] - Type-safe props and conversation types (AdminConversationViewer.tsx:8-11)

**Data Flow**:
- **Input**: conversationId prop from parent (sidebar admin item click)
- **Fetch**: useEffect triggers loadConversation() → getAdminConversation(conversationId)
- **Display**: Conversation object (title, user_email, messages[]) renders in UI
- **Output**: onClose() callback when "Back to Chat" or "Go Back" clicked

---

## Component Hierarchy

```
AdminConversationViewer
├── LoadingState (if isLoading)
│   ├── LoadingSpinner
│   └── LoadingText
├── ErrorState (if error || !conversation)
│   ├── ErrorText
│   └── GoBackButton
└── AdminViewer (if loaded successfully)
    ├── AdminViewerHeader
    │   ├── BackButton
    │   │   ├── ArrowIcon (SVG)
    │   │   └── BackText
    │   └── AdminViewerInfo
    │       ├── AdminViewerBadge ("Admin View (Read-only)")
    │       ├── Title (h2)
    │       └── AdminViewerMeta
    │           ├── UserEmail
    │           └── Date
    └── AdminViewerMessages
        ├── EmptyState (if messages.length === 0)
        └── AdminViewerMessage[] (for each message)
            ├── AdminViewerMessageHeader
            │   ├── RoleLabel (User/Assistant)
            │   └── Timestamp
            └── AdminViewerMessageContent
```

---

## Visual Design Patterns

**Color Usage**:
- Primary: Standard brand colors for header and text
- Badge: Yellow/orange background with dark text to indicate admin mode
- Background: White for messages, light gray for page
- Text: Dark gray for content, lighter gray for timestamps
- Borders: Light borders around messages or header

**Typography**:
- Heading (title): 20-24px, bold
- Badge: 12px, uppercase or medium weight
- User email: 14px, medium weight
- Message role: 12-14px, bold or uppercase
- Message content: 14-16px, regular
- Timestamps: 12px, light weight, gray

**Spacing**:
- Header padding: 16-24px
- Message padding: 12-16px internal
- Message margins: 12-16px between messages
- Badge margin: 8px below badge, above title
- Metadata margin: 8px above metadata, below title

**Visual Effects**:
- Shadows: Subtle shadow on header if sticky/elevated
- Borders: Bottom border on header, light borders around messages
- Animations:
  - Smooth scroll in messages area
  - Fade-in on component mount
  - Loading spinner rotation
- Hover: Subtle hover on back button

---

## Accessibility

**Keyboard Navigation**:
- **Tab**: Navigate to back button
- **Enter/Space**: Activate back button
- **Arrow Up/Down**: Scroll messages (browser default)
- **Escape**: Could close viewer (if implemented)

**Screen Reader Support**:
- Header: Announced as "Admin View (Read-only)"
- Conversation title: Announced as heading (h2)
- User metadata: Announced as "Conversation with [email] on [date]"
- Messages: Each message role and content announced sequentially
- Timestamps: Read with message context
- Empty state: "No messages in this conversation" announced
- Loading state: "Loading conversation" announced
- Error state: Error message announced, button labeled "Go Back"

**Focus Management**:
- Focus visible on back button
- Focus can scroll through messages (if messages are focusable)
- Focus returns to previous location when exiting viewer (ideally)

---

## Code Snippets

**Implementation**: See [[language/snippets/react-read-only-viewer.md]]

**Key patterns used**:
- **Fetch on Prop Change**: useEffect with conversationId dependency triggers re-fetch (AdminConversationViewer.tsx:18-20)
- **Loading/Error/Success States**: Conditional rendering based on isLoading, error, conversation state (AdminConversationViewer.tsx:44-64)
- **Date Formatting**: Format timestamp as "Jan 5, 2026 10:30 AM" using toLocaleDateString + toLocaleTimeString (AdminConversationViewer.tsx:36-42)
- **Callback Props**: onClose prop for navigation back to parent view (AdminConversationViewer.tsx:69, 60)

---

## Alternatives & Variations

**Similar UI Patterns**:
- **Modal Overlay**: Display conversation in modal instead of replacing main area (Pros: context preserved; Cons: limited space)
- **Split View**: Show admin list and conversation side-by-side (Pros: faster browsing; Cons: less space for messages)
- **Inline Expansion**: Expand conversation in sidebar itself (Pros: compact; Cons: hard to read long conversations)
- **New Tab/Window**: Open conversation in separate browser tab (Pros: multi-task; Cons: window management)

**When to Use**:
- Use full-area viewer when conversations are long and need full attention
- Use modal when quick glance is sufficient
- Use split view when admins need to compare conversations or browse quickly
- Use new tab when admins need to reference multiple conversations simultaneously

---

## Related

**UI Features**: [[sidebar-navigation]], [[chat-interface]], [[authentication-page]]
**Backend Features**: [[admin-access]], [[conversation-history]], [[authentication]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Code Examples**: [[language/snippets/react-read-only-viewer.md]]
**Projects Using This**: [[db-chat-nl-master]]

---

## Notes

- Viewer is strictly read-only by design - no input field, no reply button, no edit/delete actions
- Admin View badge is prominently displayed to avoid confusion with regular chat mode
- Message content is plain text (no markdown rendering), unlike regular chat messages which use ReactMarkdown
- Date formatting uses full date + time (e.g., "Jan 5, 2026 10:30 AM") for admin auditing purposes
- Component re-fetches conversation data whenever conversationId prop changes (allows browsing multiple conversations)
- Error handling covers both network failures and missing/deleted conversations
- No pagination implemented - all messages load at once (may need pagination for very long conversations)
- User email prominently displayed for admin to identify conversation owner
- No real-time updates - viewer shows snapshot at load time (admin must reload to see new messages)
