# Sidebar Navigation

**Category**: Layout
**Related Projects**: [[db-chat-nl-master]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Backend Features**: [[conversation-history]], [[admin-access]]

---

## Overview

A left-side collapsible sidebar that provides navigation between saved conversations and admin views. Users can browse their conversation history, switch between chats, delete old conversations, and (if admin) view all users' conversations.

**Key characteristics**:
- Tabbed interface with "Chats" and "Admin" tabs (admin-only)
- Conversation list with title, date, and delete button
- Real-time refresh when new conversations are created
- Empty state guidance for new users
- Compact, scannable list format with relative timestamps

---

## Layout Structure

### Visual Arrangement

```
┌─────────────────────────────────┐
│     Sidebar Navigation          │
│                                 │
│  ┌───────────────────────────┐ │
│  │ [Chats] 3  [Admin]        │ │  ← Tab Header
│  └───────────────────────────┘ │
│                                 │
│  ┌───────────────────────────┐ │
│  │ Conversation Title        │ │  ← Chat Item
│  │ 2 days ago            [×] │ │
│  ├───────────────────────────┤ │
│  │ Another Chat              │ │
│  │ Today                 [×] │ │
│  ├───────────────────────────┤ │
│  │ User query about data     │ │
│  │ Yesterday             [×] │ │
│  └───────────────────────────┘ │
│                                 │
│  OR (Admin Tab)                 │
│                                 │
│  ┌───────────────────────────┐ │
│  │ [user@example.com]        │ │  ← Admin Item
│  │ Conversation Title        │ │
│  │ 3 days ago                │ │
│  ├───────────────────────────┤ │
│  │ [admin@company.com]       │ │
│  │ Another conversation      │ │
│  │ Today                     │ │
│  └───────────────────────────┘ │
│                                 │
│  OR (Empty State)               │
│                                 │
│  ┌───────────────────────────┐ │
│  │   No saved chats          │ │
│  │                           │ │
│  │   Start a conversation    │ │
│  │   and it will be saved    │ │
│  │   here                    │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

**Components**:
- **Tabs Header**: Horizontal tab buttons at top, shows active tab with visual indicator and count badge
- **Chats List**: Scrollable list of user's own conversations
- **Admin List**: Scrollable list of all conversations with user email badges (admin-only)
- **Empty State**: Centered message when no conversations exist
- **Loading State**: Spinner with "Loading..." text

**Placement**: Fixed left sidebar, spans full height, approximately 280-320px wide

---

## Visual Elements

### Main Components

**Tabs Header** (SidebarTabs.tsx:213-235):
- **Location**: Top of sidebar
- **Contains**: Two tab buttons ("Chats" and "Admin"), each with icon, label, and optional badge count
- **Purpose**: Switch between personal chats and admin view
- **Visual style**:
  - Horizontal flex layout
  - Active tab: Bold, underline or background highlight
  - Badge: Small circle with conversation count
  - Admin tab: Only visible if user.isAdmin === true

**Chat Item** (SidebarTabs.tsx:67-88):
- **Location**: Stacked vertically in chats list
- **Contains**: Title (truncated), formatted date, delete button (×)
- **Purpose**: Represents a saved conversation, clickable to load
- **Visual style**:
  - Padding: 12px
  - Title: Bold or medium weight, truncated with ellipsis
  - Date: Smaller, lighter gray text (e.g., "Today", "2 days ago", "Jan 5")
  - Delete button: Small × in top-right corner, appears on hover
  - Hover: Background highlight (light gray)
  - Cursor: Pointer

**Admin Item** (SidebarTabs.tsx:158-167):
- **Location**: Stacked vertically in admin list
- **Contains**: User email badge, conversation title, formatted date
- **Purpose**: Shows conversation from any user, clickable to view (read-only)
- **Visual style**:
  - User badge: Small pill/chip at top (e.g., "user@example.com")
  - Title: Same styling as chat item
  - Date: Same relative format
  - Hover: Background highlight
  - No delete button (admin view is read-only)

**Empty State** (SidebarTabs.tsx:46-50, 149-152):
- **Location**: Centered in tab content area when no conversations
- **Contains**: Icon or emoji, primary text, hint text
- **Purpose**: Guides users when list is empty
- **Visual style**:
  - Centered text
  - Primary text: "No saved chats" or "No conversations yet"
  - Hint: Lighter gray, smaller font (e.g., "Start a conversation and it will be saved here")

**Loading State** (SidebarTabs.tsx:35-41, 129-135):
- **Location**: Centered in tab content area during fetch
- **Contains**: Spinning icon, "Loading..." text
- **Purpose**: Shows data is being fetched
- **Visual style**: Spinner animation + inline text

**Error State** (SidebarTabs.tsx:139-144):
- **Location**: Centered in admin tab content area
- **Contains**: Error message, "Retry" button
- **Purpose**: Allows recovery from failed fetch
- **Visual style**: Error text + secondary button

### Interactive Elements

**Tab Buttons** (SidebarTabs.tsx:214-233):
- **Click**: Switches active tab, updates content area
- **Visual feedback**: Active state (bold, highlight, or underline)
- **Badge**: Shows conversation count for "Chats" tab

**Chat Item Click** (SidebarTabs.tsx:71):
- **Click anywhere on item**: Loads conversation into main chat area (onSelectConversation callback)
- **Visual feedback**: Hover background, cursor pointer

**Delete Button** (SidebarTabs.tsx:75-85):
- **Click**: Shows confirmation dialog ("Delete this conversation?"), then deletes
- **Event**: stopPropagation to prevent loading conversation when clicking delete
- **Visual feedback**: Button visible on hover, confirmation dialog

**Admin Item Click** (SidebarTabs.tsx:161):
- **Click anywhere on item**: Opens read-only conversation view in main area (onViewAdminConversation callback)
- **Visual feedback**: Hover background, cursor pointer

**Retry Button** (SidebarTabs.tsx:142):
- **Click**: Re-fetches admin conversations after error
- **Visual feedback**: Button hover state

**User Actions**:
- **Click "Chats" tab**: View own conversations
- **Click "Admin" tab**: View all conversations (if admin)
- **Click chat item**: Load conversation into main chat
- **Click delete (×)**: Delete conversation after confirmation
- **Click admin item**: View read-only conversation in admin viewer
- **Click "Retry"**: Re-attempt failed data fetch

**Visual States**:
- **Default**: Tabs header + conversation list
- **Loading**: Spinner + "Loading..." centered
- **Empty (Chats)**: "No saved chats" with hint text
- **Empty (Admin)**: "No conversations yet"
- **Error (Admin)**: Error message + "Retry" button
- **Hover (item)**: Background highlight
- **Hover (delete)**: Delete button visible (may be hidden by default)
- **Active tab**: Visual indicator (bold, underline, or background)

---

## Responsive Behavior

**Desktop (>1024px)**:
- Sidebar fixed width (280-320px)
- Full height spanning viewport
- Conversation titles show full text (with ellipsis if too long)
- Hover effects active

**Tablet (768-1024px)**:
- Sidebar width may reduce slightly (240-280px)
- Titles may truncate sooner
- Touch-friendly tap targets

**Mobile (<768px)**:
- Sidebar may collapse to icon-only or hamburger menu
- Tabs may stack vertically or become dropdown
- Full-width overlay when opened
- Conversation list stacks with full titles
- Delete button always visible (no hover-only)

---

## User Flows

### Browse and Load Conversation

1. User sees "Chats" tab with list of conversations
2. User scans titles and dates
3. User clicks conversation item
4. Main chat area loads conversation messages
5. User can continue conversation or browse back to another

### Delete Old Conversation

1. User hovers over conversation item
2. Delete button (×) appears in top-right
3. User clicks delete button
4. Confirmation dialog: "Delete this conversation?"
5. User confirms
6. Conversation removed from list immediately
7. If conversation was loaded in main area, it may clear or show empty state

### Admin View All Conversations

1. Admin user sees "Admin" tab in header
2. Admin clicks "Admin" tab
3. List loads with all conversations across users
4. Each item shows user email badge + title + date
5. Admin clicks conversation item
6. Main area displays read-only admin conversation viewer
7. Admin can browse messages but cannot reply or delete

### Handle Empty State (New User)

1. New user opens sidebar for first time
2. "Chats" tab shows empty state: "No saved chats"
3. Hint text: "Start a conversation and it will be saved here"
4. User starts conversation in main chat
5. After sending first message, conversation appears in sidebar
6. User can now click to reload it later

### Error Recovery (Admin)

1. Admin opens "Admin" tab
2. Network error or auth failure occurs
3. Error state displays: "Failed to load conversations"
4. "Retry" button appears
5. Admin clicks "Retry"
6. System re-fetches conversation list
7. On success, list populates

---

## Integration Points

**Backend Features Used**:
- [[conversation-history]] - Fetch user's saved conversations (getConversations API, SidebarTabs.tsx:186)
- [[admin-access]] - Fetch all conversations if admin (getAdminConversations API, SidebarTabs.tsx:107)
- [[conversation-crud]] - Delete conversation (deleteConversation API, SidebarTabs.tsx:195-201)
- [[authentication]] - Check user role (isAdmin flag, SidebarTabs.tsx:177)

**Technologies**:
- [[react-hooks]] - useState for active tab, conversations list, loading state (SidebarTabs.tsx:178-180)
- [[react-hooks]] - useEffect for fetching on mount and refresh trigger (SidebarTabs.tsx:205-207)
- [[react-hooks]] - useCallback for optimized fetch and delete handlers (SidebarTabs.tsx:182-202)
- [[react-hooks]] - memo for performance optimization (SidebarTabs.tsx:172)
- [[typescript]] - Type-safe props, conversation types, tab types (SidebarTabs.tsx:15-21)

**Data Flow**:
- **Input**: Component mounts or refreshTrigger prop changes
- **Fetch**: useAuth provides isAuthenticated and isAdmin → fetchConversations() calls API
- **Display**: Conversations array mapped to ChatsList or AdminPanel components
- **Output**: onSelectConversation(id) or onViewAdminConversation(id) callbacks when user clicks item
- **Delete**: handleDeleteConversation(id) → API call → filter local state → list updates

---

## Component Hierarchy

```
SidebarTabs
├── TabsHeader (div)
│   ├── ChatsTabButton
│   │   ├── Icon (SVG)
│   │   ├── Label ("Chats")
│   │   └── Badge (count)
│   └── AdminTabButton (if isAdmin)
│       ├── Icon (SVG)
│       └── Label ("Admin")
└── TabsContent (div)
    ├── ChatsList (if activeTab === 'chats')
    │   ├── LoadingState (if loading)
    │   │   ├── LoadingSpinner
    │   │   └── LoadingText
    │   ├── EmptyState (if no conversations)
    │   │   ├── EmptyText
    │   │   └── HintText
    │   └── ChatItems[]
    │       ├── ChatTitle
    │       ├── ChatDate
    │       └── DeleteButton (×)
    └── AdminPanel (if activeTab === 'admin' && isAdmin)
        ├── LoadingState (if loading)
        ├── ErrorState (if error)
        │   ├── ErrorText
        │   └── RetryButton
        ├── EmptyState (if no conversations)
        └── AdminItems[]
            ├── UserBadge
            ├── ChatTitle
            └── ChatDate
```

---

## Visual Design Patterns

**Color Usage**:
- Primary: Blue accent for active tab indicator
- Secondary: Gray for inactive tabs and secondary text
- Background: Light gray or white for sidebar background
- Text: Dark gray for titles, lighter gray for dates and hints
- Hover: Subtle gray background highlight on items
- Badge: Blue background with white text for count and user email

**Typography**:
- Tab labels: 14px, medium weight, uppercase or regular
- Conversation titles: 14-15px, medium weight
- Dates: 12px, lighter weight, gray
- User badges: 11-12px, medium weight, uppercase
- Empty/hint text: 13-14px, light weight, gray

**Spacing**:
- Tab padding: 12px horizontal, 8px vertical
- Item padding: 12px all sides
- Item margins: 2-4px between items or no margin with borders
- Badge margin: 4px left of tab label
- List padding: 8px top/bottom for scrollable area

**Visual Effects**:
- Borders: Bottom border on active tab or divider between tabs
- Shadows: None or subtle shadow if sidebar elevated
- Animations:
  - Smooth tab transition (underline slide or content fade)
  - Hover background fade-in (150-200ms)
  - Loading spinner rotation
- Scrolling: Smooth scroll with momentum on touch devices

---

## Accessibility

**Keyboard Navigation**:
- **Tab**: Navigate between tab buttons, conversation items, delete buttons
- **Enter/Space**: Activate selected tab or conversation
- **Arrow Left/Right**: Switch between tabs
- **Arrow Up/Down**: Navigate conversation list
- **Delete/Backspace**: Delete selected conversation (with confirmation)

**Screen Reader Support**:
- Tab buttons: ARIA role="tab", aria-selected="true/false", aria-controls="tabpanel-id"
- Tab panels: ARIA role="tabpanel", aria-labelledby="tab-id"
- Conversation items: Semantic button or link, label includes title and date
- Delete button: ARIA label "Delete conversation [title]"
- Empty state: ARIA live region for dynamic messages
- Badge count: Announced as "[N] conversations"

**Focus Management**:
- Focus visible indicator on all interactive elements
- Focus trapped within confirmation dialog when deleting
- Focus returns to delete button if dialog is cancelled
- Focus moves to next conversation item if deleted conversation was focused
- Tab order: Tabs → conversation items → delete buttons

---

## Code Snippets

**Implementation**: See [[language/snippets/react-tabbed-sidebar.md]]

**Key patterns used**:
- **Controlled Tab State**: useState for activeTab, conditional rendering based on tab (SidebarTabs.tsx:178, 239-249)
- **Fetch on Mount Pattern**: useEffect with empty dependency array triggers initial load (SidebarTabs.tsx:205-207)
- **Refresh Trigger Pattern**: refreshTrigger prop in useEffect deps causes re-fetch (SidebarTabs.tsx:175, 207)
- **Optimistic Update on Delete**: Filter local state immediately after delete API call (SidebarTabs.tsx:198)
- **Relative Time Formatting**: Format dates as "Today", "2 days ago", or locale date (SidebarTabs.tsx:53-63, 117-127)
- **Conditional Rendering**: Show admin tab only if isAdmin flag is true (SidebarTabs.tsx:224-234)

---

## Alternatives & Variations

**Similar UI Patterns**:
- **Hamburger Menu**: Collapsible menu icon, sidebar slides in on mobile (Pros: saves space; Cons: less discoverable)
- **Tree View**: Nested folders for conversations by date/topic (Pros: organized; Cons: more complex)
- **Dropdown List**: Single dropdown instead of sidebar (Pros: minimal space; Cons: harder to scan)
- **Bottom Tabs (Mobile)**: Tabs at bottom like iOS apps (Pros: thumb-friendly; Cons: desktop/mobile inconsistency)

**When to Use**:
- Use tabbed sidebar when users have multiple "modes" (personal vs admin, or different data types)
- Use simple list when only one conversation type exists
- Use search/filter when conversation count is very high (100+)
- Use infinite scroll when conversation count exceeds 50-100

---

## Related

**UI Features**: [[chat-interface]], [[admin-panel]], [[authentication-page]]
**Backend Features**: [[conversation-history]], [[admin-access]], [[conversation-crud]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Code Examples**: [[language/snippets/react-tabbed-sidebar.md]]
**Projects Using This**: [[db-chat-nl-master]]

---

## Notes

- Conversation list refreshes when refreshTrigger prop changes (parent increments this after creating new conversation)
- Delete confirmation uses browser's native confirm() dialog (could be replaced with custom modal)
- Admin view is read-only by design - admin cannot delete or modify conversations from this interface
- Relative date formatting handles today, yesterday, days ago, and absolute dates for older items
- Empty state hint text helps new users understand the feature ("Start a conversation and it will be saved here")
- Component uses React.memo optimization to prevent unnecessary re-renders when props haven't changed
- fetchConversations wrapped in useCallback to stabilize reference for useEffect dependency array
- User authentication state (isAuthenticated, isAdmin) comes from useAuth hook, manages visibility of admin tab
