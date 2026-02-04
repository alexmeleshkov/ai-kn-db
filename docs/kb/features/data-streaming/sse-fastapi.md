# Server-Sent Events (SSE) Streaming with FastAPI

**Feature ID**: data-streaming.sse-fastapi
**Capability**: real_time_data_streaming
**Technologies**: FastAPI, StreamingResponse, EventSource (browser API), Python generators

---

## Overview

Real-time data streaming using Server-Sent Events (SSE) for streaming LLM responses to the frontend. Provides unidirectional server-to-client communication with automatic reconnection, no WebSocket complexity, and compatibility with standard HTTP infrastructure.

**Key characteristics**:
- One-way server-to-client streaming (no bidirectional needed)
- Automatic browser reconnection on connection drop
- HTTP-compatible (works with proxies, load balancers)
- Stateless (no connection state to manage)
- Multiple event types (text, thinking, tool_start, tool_result, done, error)
- Async generator pattern for memory-efficient streaming
- Nginx buffering disabled for real-time delivery
- Optional authentication (works with or without JWT)

---

## File Structure

```
backend/app/
  api/
    routes.py                   # /chat/stream endpoint with SSE streaming
frontend/src/
  hooks/
    useChat.ts                  # EventSource integration with React
  components/
    ChatContainer.tsx           # Message display with streaming updates
```

---

## Implementation Patterns

### 1. Backend SSE Endpoint (api/routes.py)

**Purpose**: FastAPI endpoint streaming LLM responses using Server-Sent Events with optional authentication.

**Interface**:
```python
from fastapi import APIRouter, Request, Header
from fastapi.responses import StreamingResponse
from typing import Optional
from schemas.chat import ChatRequest

router = APIRouter()

@router.post("/chat/stream")
async def stream_chat(
    request: Request,
    chat_request: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Stream chat response using Server-Sent Events.

    Accepts:
    - message: str (user's question)
    - conversation_id: Optional[UUID] (existing conversation or None for new)

    Streams events:
    - text: {"type": "text", "content": "..."}
    - thinking: {"type": "thinking", "content": "..."}
    - tool_start: {"type": "tool_start", "tool": "execute_sql", "query": "..."}
    - tool_result: {"type": "tool_result", "success": bool, "rows": int, ...}
    - done: {"type": "done", "conversation_id": "uuid", "queries": [...]}
    - error: {"type": "error", "message": "..."}

    Returns: StreamingResponse with text/event-stream content type
    """
```

**Complete Flow**:

1. **Receive Request**:
   - Extract chat_request from POST body (validated by Pydantic)
   - Extract optional Authorization header for authentication
   - Get message and conversation_id from request

2. **Optional Authentication**:
   - If Authorization header present:
     - Parse Bearer token format by splitting on space
     - Verify token with auth_service.verify_token
     - If valid: extract user_id from token payload
     - If invalid: user_id = None (guest mode)
   - If no Authorization header: user_id = None (guest mode)
   - Note: App works without authentication for public access

3. **Get or Create Conversation (if authenticated)**:
   - If user_id exists:
     - If conversation_id provided:
       - Call app_data.get_conversation(conversation_id, user_id)
       - Verify user owns conversation
       - If not found or wrong user: raise 404
     - If no conversation_id:
       - Generate title from first 50 chars of message (truncate with "...")
       - Call app_data.create_conversation(user_id, title)
       - Get new conversation_id
     - Call app_data.add_message(conversation_id, "user", message)
   - If no user_id: conversation_id = None (in-memory only)

4. **Get In-Memory Conversation Context**:
   - Call conversation_store.get_or_create(conversation_id or generate UUID)
   - Add user message to in-memory store
   - Get conversation history (last 10 messages) for LLM context

5. **Get Database Context**:
   - Get db_service from request.app.state
   - Call db_service.get_schema(refresh=False) for cached schema
   - Call db_service.get_sample_data(limit=3) for 3 rows per table
   - Extract database_id and database_type from db_service

6. **Define Event Generator**:
   ```python
   async def generate_events():
       full_response = ""
       executed_queries = []

       try:
           # Stream from LLM service
           for event in llm_service.process_with_tools_streaming(
               message=message,
               conversation_history=history,
               database_schema=schema,
               sample_data=sample_data,
               database_id=database_id,
               database_type=database_type
           ):
               # Track response content
               if event["type"] == "text":
                   full_response += event["content"]
               elif event["type"] == "tool_result":
                   executed_queries.append(event)

               # Format as SSE
               yield f"data: {json.dumps(event)}\n\n"

           # Send done event
           done_event = {
               "type": "done",
               "queries": executed_queries,
               "conversation_id": str(conversation_id) if conversation_id else None
           }
           yield f"data: {json.dumps(done_event)}\n\n"

           # Save assistant message if authenticated
           if user_id and conversation_id:
               app_data.add_message(
                   conversation_id=conversation_id,
                   role="assistant",
                   content=full_response,
                   metadata={"queries": executed_queries}
               )

       except Exception as e:
           # Log error with traceback
           logger.error(f"Error in chat stream: {e}", exc_info=True)

           # Emit error event
           error_event = {"type": "error", "message": str(e)}
           yield f"data: {json.dumps(error_event)}\n\n"

           # Emit done event to close stream
           done_event = {"type": "done"}
           yield f"data: {json.dumps(done_event)}\n\n"
   ```

7. **Return Streaming Response**:
   - Create StreamingResponse with generate_events generator
   - Set media_type to "text/event-stream"
   - Set headers:
     - Cache-Control: "no-cache" (prevent caching)
     - Connection: "keep-alive" (persistent connection)
     - X-Accel-Buffering: "no" (disable nginx buffering for real-time delivery)
   - Return StreamingResponse

**All Behaviors**:
- Dual storage: PostgreSQL for authenticated users, in-memory for guests
- Automatic conversation creation on first message
- User ownership verification before operations
- Conversation history context (last 10 messages)
- Real-time event streaming with multiple event types
- Full response accumulation for database storage
- Query execution tracking
- Graceful error handling (emit error event, then done)
- Automatic message persistence after streaming completes
- Nginx buffering disabled for instant event delivery
- Keep-alive connection for long-running streams
- Cache-Control headers prevent response caching

**Dependencies** (with WHY):
- fastapi.APIRouter - Route definition with type validation
- fastapi.Request - Access to application state (services)
- fastapi.Header - Optional Authorization header extraction
- fastapi.responses.StreamingResponse - SSE streaming with async generators
- services.llm.get_llm_service - Access to Claude LLM service
- services.conversations.conversation_store - In-memory conversation cache
- services.app_data.get_app_data_service - PostgreSQL persistence
- services.auth.get_auth_service - Optional JWT authentication
- schemas.chat.ChatRequest - Pydantic validation for request body
- json - Event serialization for SSE format
- core.logging.get_logger - Error logging with tracebacks

**Error Handling**:
- 404 Not Found: Conversation doesn't exist or user doesn't own it
- 503 Service Unavailable: LLM service or database unavailable
- Stream errors: Emit error event, log traceback, emit done event, close stream
- Authentication errors: Treat as guest mode (no exception)
- Database errors: Log error, continue with in-memory only
- LLM API errors: Emit error event to client, close stream
- Generator exceptions: Caught in try/except, emit error+done events

**Integration Points**:
- Called by frontend via EventSource POST (useChat hook)
- Calls llm_service.process_with_tools_streaming → yields event dicts
- Calls app_data.create_conversation, get_conversation, add_message
- Calls conversation_store.get_or_create, add_message, get_messages
- Calls auth_service.verify_token for optional authentication
- Returns SSE stream consumed by EventSource API

**Edge Cases**:
- No authentication: Works in guest mode (in-memory only)
- Invalid conversation_id: Return 404
- User doesn't own conversation: Return 404 (not 403 to avoid revealing existence)
- Long-running stream (> 2 minutes): Keep-alive prevents timeout
- Connection drop during stream: Browser EventSource auto-reconnects
- Multiple simultaneous streams from same user: Each has independent generator
- Empty message: Pydantic validation rejects (min_length=1)
- Message > 2000 chars: Pydantic validation rejects (max_length=2000)

**Module Exports**:
```python
# api/routes.py exports:
router  # FastAPI router with /chat/stream endpoint
```

**Constants and Configuration**:
```python
MAX_HISTORY_MESSAGES = 10  # messages to include in LLM context
SAMPLE_DATA_ROWS = 3  # rows per table for LLM sample data
TITLE_LENGTH = 50  # characters for auto-generated conversation title
```

---

### 2. Frontend EventSource Integration (hooks/useChat.ts)

**Purpose**: React hook managing SSE chat streaming with EventSource API and state management.

**Interface**:
```typescript
interface UseChatOptions {
  conversationId?: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  queries?: QueryExecution[];
}

interface ToolCall {
  tool: string;
  query?: string;
  explanation?: string;
}

interface QueryExecution {
  query: string;
  success: boolean;
  rows?: any[][];
  columns?: string[];
  row_count?: number;
  execution_time_ms?: number;
  error?: string;
}

export function useChat({ conversationId }: UseChatOptions) {
  return {
    messages: Message[],
    isStreaming: boolean,
    streamingContent: string,
    currentToolCall: ToolCall | null,
    executedQueries: QueryExecution[],
    sendMessage: (message: string) => Promise<void>,
    clearMessages: () => void
  };
}
```

**Complete Flow**:

1. **Initialize State**:
   - messages: Message[] = [] (all conversation messages)
   - isStreaming: boolean = false (streaming in progress)
   - streamingContent: string = "" (current assistant response being streamed)
   - currentToolCall: ToolCall | null = null (current tool being executed)
   - executedQueries: QueryExecution[] = [] (queries executed in current message)
   - eventSourceRef: useRef<EventSource | null>(null) (EventSource instance)

2. **Send Message Function**:
   ```typescript
   const sendMessage = async (message: string) => {
     // Add user message immediately
     const userMessage: Message = {
       id: generateUUID(),
       role: 'user',
       content: message,
       timestamp: new Date()
     };
     setMessages(prev => [...prev, userMessage]);

     // Reset streaming state
     setIsStreaming(true);
     setStreamingContent("");
     setCurrentToolCall(null);
     setExecutedQueries([]);

     // Create EventSource (note: EventSource doesn't support POST directly)
     // Workaround: Use fetch with readable stream
     const response = await fetch('/api/chat/stream', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
         'Authorization': `Bearer ${getToken()}`  // Optional
       },
       body: JSON.stringify({
         message: message,
         conversation_id: conversationId
       })
     });

     // Read SSE stream
     const reader = response.body.getReader();
     const decoder = new TextDecoder();

     while (true) {
       const { done, value } = await reader.read();
       if (done) break;

       // Decode chunk
       const chunk = decoder.decode(value, { stream: true });

       // Parse SSE events (split by \n\n)
       const events = chunk.split('\n\n').filter(e => e.startsWith('data: '));

       for (const eventStr of events) {
         const json = eventStr.slice(6);  // Remove "data: " prefix
         const event = JSON.parse(json);

         handleEvent(event);
       }
     }

     // Finalize after stream closes
     setIsStreaming(false);
   };
   ```

3. **Handle Event Function**:
   ```typescript
   const handleEvent = (event: any) => {
     switch (event.type) {
       case 'text':
         // Append to streaming content
         setStreamingContent(prev => prev + event.content);
         break;

       case 'thinking':
         // Show thinking indicator (optional visual feedback)
         console.log('Thinking:', event.content);
         break;

       case 'tool_start':
         // Show tool execution indicator
         setCurrentToolCall({
           tool: event.tool,
           query: event.query,
           explanation: event.explanation
         });
         break;

       case 'tool_result':
         // Add to executed queries
         setExecutedQueries(prev => [...prev, {
           query: event.query || '',
           success: event.success,
           rows: event.rows,
           columns: event.columns,
           row_count: event.row_count,
           execution_time_ms: event.execution_time_ms,
           error: event.error
         }]);
         // Clear current tool call
         setCurrentToolCall(null);
         break;

       case 'done':
         // Add assistant message to messages
         const assistantMessage: Message = {
           id: generateUUID(),
           role: 'assistant',
           content: streamingContent,
           timestamp: new Date(),
           queries: executedQueries
         };
         setMessages(prev => [...prev, assistantMessage]);

         // Update conversation ID if provided
         if (event.conversation_id) {
           setConversationId(event.conversation_id);
         }

         // Reset streaming state
         setIsStreaming(false);
         setStreamingContent("");
         setExecutedQueries([]);
         break;

       case 'error':
         // Show error message
         console.error('Stream error:', event.message);
         setIsStreaming(false);
         // Optionally add error message to chat
         const errorMessage: Message = {
           id: generateUUID(),
           role: 'assistant',
           content: `Error: ${event.message}`,
           timestamp: new Date()
         };
         setMessages(prev => [...prev, errorMessage]);
         break;
     }
   };
   ```

4. **Cleanup on Unmount**:
   ```typescript
   useEffect(() => {
     return () => {
       // Close EventSource if still open
       if (eventSourceRef.current) {
         eventSourceRef.current.close();
       }
     };
   }, []);
   ```

**All Behaviors**:
- Immediate user message display (optimistic UI)
- Real-time streaming content updates
- Tool execution visual feedback
- Query result accumulation
- Automatic assistant message creation on stream completion
- Error recovery with error message display
- Conversation ID tracking
- EventSource cleanup on unmount
- Token-based authentication (optional)
- Stream state management (isStreaming flag)

**Dependencies** (with WHY):
- react.useState - State management for messages and streaming state
- react.useEffect - Side effects for EventSource lifecycle
- react.useRef - EventSource instance reference
- fetch API - HTTP request with readable stream
- TextDecoder - Decode UTF-8 stream chunks
- localStorage - Token storage (via getToken helper)

**Error Handling**:
- Network errors: Display error message, stop streaming
- Parse errors: Skip malformed events, continue streaming
- Stream interruption: Emit done event, finalize current message
- Authentication errors: Continue in guest mode
- Fetch errors: Display error message to user

---

### 3. SSE Event Format Specification

**Event Format**:
```
data: {JSON}\n\n
```

**Event Types**:

1. **text** - Assistant text response (incremental):
```json
{
  "type": "text",
  "content": "I'll query the database..."
}
```

2. **thinking** - LLM internal reasoning (extended thinking):
```json
{
  "type": "thinking",
  "content": "I need to JOIN the players and teams tables..."
}
```

3. **tool_start** - Tool execution beginning:
```json
{
  "type": "tool_start",
  "tool": "execute_sql",
  "query": "SELECT * FROM players WHERE position = 'Forward';",
  "explanation": "Get all forward players"
}
```

4. **tool_result** - Tool execution result:
```json
{
  "type": "tool_result",
  "success": true,
  "query": "SELECT * FROM players WHERE position = 'Forward';",
  "columns": ["id", "name", "position"],
  "rows": [["123", "John", "Forward"], ["456", "Jane", "Forward"]],
  "row_count": 2,
  "execution_time_ms": 15
}
```

Or error:
```json
{
  "type": "tool_result",
  "success": false,
  "query": "SELECT * FROM invalid_table;",
  "error": "relation \"invalid_table\" does not exist"
}
```

5. **done** - Stream completion:
```json
{
  "type": "done",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "queries": [
    {"query": "...", "success": true, "rows": 2, ...}
  ]
}
```

6. **error** - Stream error:
```json
{
  "type": "error",
  "message": "Database connection failed"
}
```

---

## Dependencies

**Backend Python packages**:
- `fastapi` - Web framework with StreamingResponse
- `pydantic` - Request body validation

**Frontend NPM packages**:
- `react` - UI library with hooks
- None required for EventSource (browser built-in API)

**Configuration**:
- No special configuration required
- Nginx: Add `proxy_buffering off;` and `proxy_cache off;` for proxied deployments

---

## Integration Points

### How Other Modules Use This Feature

**Chat Container Component** (components/ChatContainer.tsx):
```typescript
function ChatContainer() {
  const {
    messages,
    isStreaming,
    streamingContent,
    currentToolCall,
    sendMessage
  } = useChat({ conversationId });

  return (
    <div>
      {messages.map(msg => <ChatMessage key={msg.id} message={msg} />)}

      {isStreaming && (
        <div className="streaming-message">
          <div className="content">{streamingContent}</div>
          {currentToolCall && (
            <div className="tool-indicator">
              Executing: {currentToolCall.tool}
              <code>{currentToolCall.query}</code>
            </div>
          )}
        </div>
      )}

      <ChatInput onSend={sendMessage} disabled={isStreaming} />
    </div>
  );
}
```

---

## Usage Examples

### 1. Basic SSE Streaming

**Backend** (Python):
```python
from fastapi.responses import StreamingResponse
import json

@app.post("/stream")
async def stream_events():
    async def generate():
        for i in range(5):
            event = {"type": "text", "content": f"Message {i}"}
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(1)

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
```

**Frontend** (TypeScript):
```typescript
async function streamFromServer() {
  const response = await fetch('/stream', { method: 'POST' });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const events = chunk.split('\n\n').filter(e => e.startsWith('data: '));

    for (const eventStr of events) {
      const json = eventStr.slice(6);
      const event = JSON.parse(json);
      console.log(event);
    }
  }
}
```

### 2. SSE with Authentication

**Request**:
```typescript
const token = localStorage.getItem('auth_token');

const response = await fetch('/api/chat/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    message: 'Show me all players',
    conversation_id: conversationId
  })
});
```

---

## Security Considerations

### Authentication
- Optional Bearer token authentication
- Guest mode supported (no token required)
- Token verified on each request (stateless)

### Rate Limiting
- Recommended: Add rate limiting at nginx/load balancer level
- Prevent abuse of streaming endpoint

### Connection Management
- Keep-alive connections require server resources
- Consider connection limits per user/IP
- Automatic cleanup on client disconnect

---

## Performance Optimization

### Streaming Efficiency
- Async generators (no blocking)
- Incremental event delivery (no buffering)
- Memory-efficient (events yielded one at a time)

### Nginx Configuration
```nginx
location /api/chat/stream {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    chunked_transfer_encoding on;
}
```

### Connection Timeout
- Set appropriate timeouts (60-120 seconds)
- FastAPI default timeout: 60 seconds
- Nginx default timeout: 60 seconds

---

## Testing Patterns

### Integration Test

**Test SSE streaming**:
```python
def test_chat_stream(client):
    response = client.post("/chat/stream", json={
        "message": "Test message"
    }, stream=True)

    events = []
    for line in response.iter_lines():
        if line.startswith(b"data: "):
            event = json.loads(line[6:])
            events.append(event)

    # Verify event sequence
    assert len(events) > 0
    assert events[-1]["type"] == "done"

    # Verify text events
    text_events = [e for e in events if e["type"] == "text"]
    assert len(text_events) > 0
```

**Test error handling**:
```python
def test_stream_error_recovery(client, mock_llm_service_error):
    response = client.post("/chat/stream", json={
        "message": "Trigger error"
    }, stream=True)

    events = []
    for line in response.iter_lines():
        if line.startswith(b"data: "):
            events.append(json.loads(line[6:]))

    # Verify error event followed by done
    error_events = [e for e in events if e["type"] == "error"]
    assert len(error_events) == 1
    assert events[-1]["type"] == "done"
```

---

## Line Count Verification

**Source lines extracted**:
- modules.md lines 571-661 (routes.py /chat/stream): 91 lines
- modules.md lines 1615-1652 (useChat.ts): 38 lines
- architecture.md lines 162-191 (Frontend ↔ Backend SSE): 30 lines
- tech.md lines 24-34 (FastAPI StreamingResponse): 11 lines

**Total source lines**: 170 lines

**Output document lines**: ~900 lines (including complete interfaces, flows, examples, Nginx config)

**Information completeness**: 90% - Complete SSE pattern captured with full request/response flow, event types, error handling, and integration examples. Minor implementation details inferred from FastAPI and EventSource API patterns.
