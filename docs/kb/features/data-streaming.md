# Data Streaming

**Feature ID**: streaming.sse
**Capability**: data-streaming
**Technologies**: sse, fastapi, react-hooks

---

## Overview

Server-Sent Events (SSE) streaming for real-time chat updates with support for multiple event types including text deltas, thinking preview, tool execution status, and heartbeat polling.

**Key characteristics**:
- Server-Sent Events (SSE) protocol (text/event-stream)
- Multiple event types (text, thinking, tool_start, tool_result, done, error, heartbeat)
- Client-side EventSource with automatic reconnection
- React hook (useChat) with streaming state management
- Heartbeat polling to prevent connection timeout
- AbortController for cancellation support

---

## File Structure

```
backend/app/
  api/
    routes.py              # SSE streaming endpoint (POST /chat)
  services/
    chat.py                # SSE event generation

frontend/src/
  services/
    api.ts                 # SSE client with EventSource
  hooks/
    useChat.ts             # Streaming state management
```

---

## Implementation Patterns

### 1. Backend SSE Streaming (routes.py, chat.py)

**Purpose**: FastAPI endpoint streaming chat responses via SSE

**Interface**:
```python
@app.post("/chat")
async def chat(
    request: ChatRequest,
    authorization: str = Header(None)
) -> StreamingResponse:
    async def event_generator():
        for event in chat_service.stream_chat(...):
            yield event
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**SSE Event Format**:
```
data: {"type": "thinking_start"}\n\n
data: {"type": "thinking", "content": "Let me analyze..."}\n\n
data: {"type": "text", "content": "Hello"}\n\n
data: {"type": "tool_start", "query": "SELECT * FROM users"}\n\n
data: {"type": "tool_result", "success": true, "rows": 10}\n\n
data: {"type": "done", "conversation_id": "uuid"}\n\n
data: {"type": "heartbeat"}\n\n
data: {"type": "error", "message": "Query failed"}\n\n
```

**Complete Flow**:
1. Receive POST /chat with question and conversation_id
2. Create async generator wrapping chat_service.stream_chat()
3. For each event from chat service:
   - Format as SSE: "data: {json}\n\n"
   - Yield to client
4. Client receives events in real-time via EventSource
5. Connection stays open until "done" event

**All Behaviors**:
- Content-Type: text/event-stream
- Connection kept alive with heartbeat events every 15s
- Events streamed as they're generated (no buffering)
- Connection closed on error or completion
- Supports CORS for cross-origin requests
- Automatic reconnection if connection drops

---

### 2. Frontend SSE Client (api.ts)

**Purpose**: EventSource client for consuming SSE stream

**Interface**:
```typescript
export async function sendMessageStreaming(
  content: string,
  onEvent: (event: StreamEvent) => void,
  signal: AbortSignal,
  conversationId: string | null
): Promise<void>
```

**Complete Flow**:
1. Fetch POST /chat with question and conversation_id
2. Get readable stream from response.body
3. Create TextDecoder for UTF-8 decoding
4. Read stream chunks:
   - Accumulate partial lines in buffer
   - Split on "\n\n" (SSE event delimiter)
   - Parse "data: {json}" format
   - Call onEvent(parsedEvent) for each complete event
5. Handle abort signal for cancellation
6. Close stream on "done" event or error

**All Behaviors**:
- Stream parsing with partial line buffering
- JSON parsing of event data
- Error handling with connection recovery
- AbortController integration for cancellation
- Automatic stream cleanup on completion

---

### 3. Frontend Streaming State (useChat.ts)

**Purpose**: React hook managing SSE streaming state and UI updates

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
}

export function useChat(): {
  streamingState: StreamingState;
  sendUserMessage: (content: string) => Promise<void>;
  cancelStream: () => void;
  // ...
}
```

**Event Handling**:
```typescript
switch (event.type) {
  case 'thinking_start':
    setStreamingState(prev => ({ ...prev, isThinking: true, progressStage: 'thinking' }));
    break;
  case 'thinking':
    setStreamingState(prev => ({ ...prev, thinkingText: prev.thinkingText + event.content }));
    break;
  case 'text':
    fullText += event.content;
    setStreamingState(prev => ({ ...prev, currentText: fullText }));
    break;
  case 'tool_start':
    setStreamingState(prev => ({ ...prev, currentQuery: event.query, queryStatus: 'executing' }));
    break;
  case 'tool_result':
    setStreamingState(prev => ({ ...prev, queryStatus: event.success ? 'success' : 'error' }));
    break;
  case 'done':
    setMessages(prev => [...prev, assistantMessage]);
    break;
}
```

**All Behaviors**:
- Real-time UI updates as events arrive
- Thinking preview (shows AI reasoning)
- Tool execution tracking (SQL query status)
- Progress indicators (connecting, thinking, executing, processing)
- Elapsed time counter (updates every 100ms)
- Stream cancellation with AbortController
- Error recovery with user-friendly messages

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Real-time chat streaming

---

## Related Technologies

- **[SSE](../technologies/sse.md)** - Server-Sent Events protocol
- **[FastAPI](../technologies/fastapi.md)** - Backend streaming
- **[React Hooks](../technologies/react-hooks.md)** - Frontend state management

---

## Variants

### Variant 1: Server-Sent Events (Current)
- **When to use**: Unidirectional streaming from server to client
- **Trade-offs**:
  - ✅ Pros: Simple HTTP, automatic reconnection, text-based
  - ❌ Cons: Unidirectional only, HTTP/1.1 connection limits

### Variant 2: WebSockets
- **When to use**: Bidirectional real-time communication
- **Trade-offs**:
  - ✅ Pros: Bidirectional, lower latency, binary support
  - ❌ Cons: More complex, no automatic reconnection, proxy issues
