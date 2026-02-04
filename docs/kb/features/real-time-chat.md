# Real-Time Chat

**Feature ID**: chat.realtime
**Capability**: real-time-chat
**Technologies**: react-hooks, sse, typescript

---

## Overview

Real-time chat interface with SSE streaming, extended thinking preview, tool execution tracking, clarification handling, and progress indicators.

**Key characteristics**:
- SSE-based streaming (text/event-stream)
- Extended thinking preview (shows AI reasoning)
- Tool execution status (SQL query progress)
- Clarification UI (multiple-choice questions from AI)
- Progress stages (connecting, thinking, generating, executing, processing)
- Elapsed time counter
- Stream cancellation support

---

## File Structure

```
frontend/src/
  components/
    ChatContainer.tsx      # Main chat UI
    ChatMessage.tsx        # Message rendering
    ChatInput.tsx          # Input with suggestions
  hooks/
    useChat.ts             # Chat state management
```

---

## Implementation Patterns

### 1. Chat Container (ChatContainer.tsx)

**Purpose**: Main chat UI component integrating message display, streaming status, and clarification UI

**Interface**:
```typescript
export function ChatContainer(): JSX.Element
```

**Complete Flow**:
1. Initialize useChat() hook
2. Render message list (user and assistant messages)
3. Show streaming indicators during active stream:
   - Thinking preview (if isThinking)
   - Current query (if queryStatus = 'executing')
   - Progress stage indicator
   - Elapsed time counter
4. Show clarification UI if clarification request present
5. Render ChatInput at bottom

**All Behaviors**:
- Scrolls to bottom on new messages
- Shows welcome chips for first-time users
- Displays streaming progress with visual indicators
- Clarification UI with selectable options
- "Try simpler question" button after 30s
- Loading spinner during initial connection
- Error display with retry option

---

### 2. Chat Message (ChatMessage.tsx)

**Purpose**: Renders individual chat messages with markdown, SQL results, CSV export, and chart visualization

**Interface**:
```typescript
interface ChatMessageProps {
  message: ChatMessage;
}

export function ChatMessage({ message }: ChatMessageProps): JSX.Element
```

**All Behaviors**:
- User messages: right-aligned, blue background
- Assistant messages: left-aligned, gray background
- Markdown rendering with react-markdown
- SQL results displayed as tables
- CSV export button for query results
- Chart.js visualization for chartable data
- Copy button for SQL queries
- Timestamp display (relative or absolute)

---

### 3. Chat Input (ChatInput.tsx)

**Purpose**: Textarea with autocomplete suggestions and keyboard navigation

**Interface**:
```typescript
export function ChatInput({
  onSubmit,
  isDisabled,
}: ChatInputProps): JSX.Element
```

**All Behaviors**:
- Multi-line textarea with auto-resize
- Suggestions dropdown below input
- Keyboard navigation:
  - ArrowDown/ArrowUp: navigate suggestions
  - Tab: select highlighted suggestion
  - Enter: submit (Shift+Enter for newline)
  - Escape: close suggestions
- Submit button with loading state
- Disabled state during streaming
- Focus management (auto-focus on mount)

---

### 4. Chat State Hook (useChat.ts)

**Purpose**: React hook managing chat state with SSE streaming

**Interface**:
```typescript
interface StreamingState {
  isStreaming: boolean;
  currentText: string;
  currentQuery: string | null;
  queryStatus: 'idle' | 'executing' | 'success' | 'error';
  isThinking: boolean;
  thinkingText: string;
  elapsedMs: number;
  progressStage: ProgressStage;
  clarification: ClarificationRequest | null;
}

export function useChat(): {
  messages: ChatMessage[];
  streamingState: StreamingState;
  sendUserMessage: (content: string) => Promise<void>;
  // ...
}
```

**Complete Flow**:
1. sendUserMessage(content):
   - Add user message to messages array
   - Create AbortController for cancellation
   - Initialize streaming state
   - Start elapsed time timer
   - Call sendMessageStreaming() with SSE event handler
2. Process SSE events:
   - thinking_start: set isThinking=true
   - thinking: append to thinkingText
   - text: append to currentText
   - tool_start: show query in UI
   - tool_result: update query status
   - clarification_needed: show clarification UI
   - done: add assistant message, reset state
3. On completion: stop timer, reset streaming state

**All Behaviors**:
- Real-time state updates as events arrive
- Thinking preview accumulation
- Tool execution tracking
- Progress stage transitions
- Elapsed time counter (100ms interval)
- Stream cancellation with AbortController
- Error recovery with user-friendly messages
- Clarification handling (pause stream, wait for user selection)

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Chat interface

---

## Related Technologies

- **[React Hooks](../technologies/react-hooks.md)** - State management
- **[SSE](../technologies/sse.md)** - Streaming protocol
- **[TypeScript](../technologies/typescript.md)** - Type safety
