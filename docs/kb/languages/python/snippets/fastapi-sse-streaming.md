# Python + FastAPI - Server-Sent Events (SSE) Streaming

**Language**: Python
**Technology**: FastAPI
**Feature/Pattern**: Server-Sent Events for real-time data streaming
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
pip install fastapi uvicorn
```

**Required Knowledge**:
- FastAPI StreamingResponse
- Python generators and yield
- Server-Sent Events (SSE) protocol
- JSON serialization
- Async/await patterns

---

## Overview

This snippet demonstrates how to implement Server-Sent Events (SSE) streaming with FastAPI. SSE allows the server to push real-time updates to the client over a single HTTP connection. This is ideal for streaming LLM responses, progress updates, or any continuous data flow.

Key features:
- Generator functions for streaming data
- Proper SSE formatting with `data:` prefix and double newlines
- Multiple event types (text, tool results, errors, completion)
- Connection management headers (no-cache, keep-alive)
- Error handling with graceful stream termination

---

## Implementation

### Basic Usage

#### Simple SSE Endpoint

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import time

app = FastAPI()

@app.get("/stream")
async def stream_events():
    """Basic SSE endpoint that streams events."""

    def generate():
        for i in range(10):
            # Format as SSE: "data: <json>\n\n"
            event = {"type": "counter", "value": i}
            yield f"data: {json.dumps(event)}\n\n"
            time.sleep(0.5)  # Simulate work

        # Send completion event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

**Explanation**:
- Line 9: Generator function yields data chunks (doesn't load all into memory)
- Line 12: SSE format requires `data: ` prefix and `\n\n` suffix
- Line 17: StreamingResponse wraps generator for HTTP streaming
- Line 18: `text/event-stream` is the standard SSE media type

#### Client-Side Usage (JavaScript)

```javascript
const eventSource = new EventSource('/stream');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);

    if (data.type === 'done') {
        eventSource.close();
    }
};

eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    eventSource.close();
};
```

### Advanced Usage

#### SSE with Multiple Event Types

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json
from typing import Generator

@app.post("/chat/stream")
async def stream_chat(request: Request):
    """
    Stream chat responses with multiple event types.

    Event types:
    - text: Incremental text content
    - tool_start: Tool execution beginning
    - tool_result: Tool execution results
    - done: Stream completion
    - error: Error occurred
    """

    def generate_events() -> Generator[str, None, None]:
        try:
            # Simulate streaming text response
            text_chunks = ["Hello", " ", "world", "!", " ", "How", " ", "can", " ", "I", " ", "help?"]

            for chunk in text_chunks:
                event = {
                    "type": "text",
                    "content": chunk
                }
                yield f"data: {json.dumps(event)}\n\n"

            # Simulate tool execution
            yield f"data: {json.dumps({
                'type': 'tool_start',
                'tool': 'execute_sql',
                'query': 'SELECT COUNT(*) FROM users'
            })}\n\n"

            # Simulate tool result
            yield f"data: {json.dumps({
                'type': 'tool_result',
                'success': True,
                'rows': 42,
                'execution_time': '0.15s'
            })}\n\n"

            # Send completion
            yield f"data: {json.dumps({
                'type': 'done',
                'conversation_id': '12345'
            })}\n\n"

        except Exception as e:
            # Send error event
            yield f"data: {json.dumps({
                'type': 'error',
                'message': str(e)
            })}\n\n"

            # Always send done event
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
```

**Key Points**:
- Multiple event types allow rich client-side handling
- Always send `done` event to signal completion
- Error handling ensures stream doesn't hang
- Headers prevent caching and buffering

---

## Complete Example

### Full LLM Streaming Endpoint

```python
from fastapi import APIRouter, Request, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@router.post("/chat/stream")
async def stream_chat(
    request: Request,
    chat_request: ChatRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Stream a chat response using Server-Sent Events (SSE).

    Events:
    - text: {"type": "text", "content": "..."}
    - tool_start: {"type": "tool_start", "tool": "execute_sql", "query": "..."}
    - tool_result: {"type": "tool_result", "success": bool, "rows": int, ...}
    - done: {"type": "done", "queries": [...], "conversation_id": "..."}
    - error: {"type": "error", "message": "..."}
    """
    llm_service = request.app.state.llm_service
    db_service = request.app.state.db_service

    # Authenticate user (optional)
    user_id = None
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
            # Verify token and extract user_id (implementation not shown)
            user_id = verify_token(token)

    # Get or create conversation
    conversation_id = chat_request.conversation_id or generate_conversation_id()

    def generate_events():
        full_response = ""
        executed_queries = []

        try:
            # Get database schema for LLM context
            schema = db_service.get_schema()
            sample_data = db_service.get_all_samples_for_prompt(limit_per_table=3)

            # Stream LLM response with tool use
            for event in llm_service.process_with_tools_streaming(
                user_question=chat_request.message,
                schema=schema,
                execute_sql_func=db_service.execute_query,
                sample_data=sample_data
            ):
                # Track full response text
                if event.get("type") == "text":
                    full_response += event.get("content", "")

                # Track executed queries
                elif event.get("type") == "tool_result":
                    executed_queries.append(event)

                # Add conversation_id to done event
                elif event.get("type") == "done":
                    event["conversation_id"] = conversation_id

                    # Save to database (if authenticated)
                    if user_id:
                        save_conversation(
                            user_id=user_id,
                            conversation_id=conversation_id,
                            user_message=chat_request.message,
                            assistant_message=full_response,
                            executed_queries=executed_queries
                        )

                # Format as SSE and yield
                yield f"data: {json.dumps(event)}\n\n"

        except Exception as e:
            import traceback
            print(f"Stream error: {e}")
            print(f"Traceback: {traceback.format_exc()}")

            # Send error event
            yield f"data: {json.dumps({
                'type': 'error',
                'message': str(e)
            })}\n\n"

            # Always send done event
            yield f"data: {json.dumps({
                'type': 'done',
                'queries': [],
                'conversation_id': conversation_id
            })}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
```

### Client-Side Handler (TypeScript/React)

```typescript
async function streamChat(message: string, conversationId?: string) {
    const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message, conversation_id: conversationId })
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    let buffer = '';
    let fullText = '';

    while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process complete SSE messages
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || ''; // Keep incomplete message in buffer

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const jsonStr = line.slice(6); // Remove "data: " prefix
                const event = JSON.parse(jsonStr);

                switch (event.type) {
                    case 'text':
                        fullText += event.content;
                        updateUI(fullText);
                        break;

                    case 'tool_start':
                        showToolExecution(event.tool, event.query);
                        break;

                    case 'tool_result':
                        showToolResult(event);
                        break;

                    case 'done':
                        console.log('Stream complete:', event.conversation_id);
                        break;

                    case 'error':
                        showError(event.message);
                        break;
                }
            }
        }
    }
}
```

---

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # SSE Configuration
    sse_keep_alive_timeout: int = 60  # seconds
    sse_max_buffer_size: int = 1024 * 1024  # 1MB

    # CORS for SSE
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

# Apply CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Error Handling

```python
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def generate_events_with_error_handling():
    """Generator with comprehensive error handling."""
    try:
        # Main streaming logic
        for i in range(10):
            # Simulate potential error
            if i == 5:
                raise ValueError("Simulated error")

            yield f"data: {json.dumps({'type': 'text', 'content': f'Item {i}'})}\n\n"

        # Success completion
        yield f"data: {json.dumps({'type': 'done', 'status': 'success'})}\n\n"

    except GeneratorExit:
        # Client disconnected - cleanup
        logger.info("Client disconnected during stream")
        # Perform cleanup (close DB connections, etc.)

    except Exception as e:
        logger.error(f"Stream error: {e}", exc_info=True)

        # Send error to client
        yield f"data: {json.dumps({
            'type': 'error',
            'message': str(e),
            'code': 'STREAM_ERROR'
        })}\n\n"

        # Always send done event
        yield f"data: {json.dumps({'type': 'done', 'status': 'error'})}\n\n"
```

**Common Errors**:
1. **Client Disconnect**: GeneratorExit raised when client closes connection - handle cleanup
2. **Buffering Issues**: Use `X-Accel-Buffering: no` header for nginx
3. **CORS Errors**: Ensure proper CORS headers for cross-origin SSE
4. **Timeout**: Long-running streams may timeout - send periodic keep-alive messages
5. **Memory Issues**: Large responses can cause memory problems - use generators to stream

---

## Testing

```python
import pytest
from fastapi.testclient import TestClient

def test_sse_stream(client: TestClient):
    """Test SSE streaming endpoint."""
    response = client.get("/stream", stream=True)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"

    events = []
    for line in response.iter_lines():
        if line.startswith(b"data: "):
            data = json.loads(line[6:])  # Remove "data: " prefix
            events.append(data)

    assert len(events) > 0
    assert events[-1]["type"] == "done"

def test_sse_chat_stream(client: TestClient):
    """Test chat streaming with events."""
    response = client.post(
        "/chat/stream",
        json={"message": "Hello"},
        stream=True
    )

    assert response.status_code == 200

    text_events = []
    done_event = None

    for line in response.iter_lines():
        if line.startswith(b"data: "):
            event = json.loads(line[6:])

            if event["type"] == "text":
                text_events.append(event["content"])
            elif event["type"] == "done":
                done_event = event

    assert len(text_events) > 0
    assert done_event is not None
    assert "conversation_id" in done_event

def test_sse_error_handling(client: TestClient):
    """Test error handling in SSE stream."""
    response = client.post(
        "/chat/stream",
        json={"message": "trigger error"},  # Assume this triggers an error
        stream=True
    )

    error_event = None
    done_event = None

    for line in response.iter_lines():
        if line.startswith(b"data: "):
            event = json.loads(line[6:])

            if event["type"] == "error":
                error_event = event
            elif event["type"] == "done":
                done_event = event

    assert error_event is not None
    assert done_event is not None  # Always sends done even on error
```

---

## Performance Considerations

- **Generator Efficiency**: Use generators (yield) instead of loading all data into memory
- **Chunk Size**: Send events as they're ready (don't wait to accumulate large batches)
- **Keep-Alive**: Send periodic ping/heartbeat messages for long-running streams (every 15-30s)
- **Connection Limits**: Monitor concurrent SSE connections (they're long-lived)
- **Buffering**: Disable buffering in reverse proxies (nginx, CloudFlare) for real-time delivery
- **Error Recovery**: Client should reconnect with Last-Event-ID for resumable streams

**Keep-Alive Example**:
```python
import asyncio

async def generate_with_keepalive():
    last_event_time = asyncio.get_event_loop().time()

    while processing:
        # Send actual events
        yield f"data: {json.dumps(event)}\n\n"
        last_event_time = asyncio.get_event_loop().time()

        # Send keep-alive if no events for 15 seconds
        if asyncio.get_event_loop().time() - last_event_time > 15:
            yield f": keep-alive\n\n"  # Comment line (ignored by client)
            last_event_time = asyncio.get_event_loop().time()
```

---

## Security Considerations

- **Authentication**: Verify Bearer tokens for protected SSE endpoints
- **Rate Limiting**: Limit concurrent SSE connections per user to prevent resource exhaustion
- **CORS**: Configure allowed origins carefully for cross-origin SSE
- **Input Validation**: Validate all request parameters before streaming
- **Timeout**: Implement maximum stream duration to prevent infinite connections
- **Resource Cleanup**: Ensure connections are properly closed and resources freed on errors
- **Message Size**: Limit individual event size to prevent memory issues
- **Injection**: JSON-encode all data to prevent SSE injection attacks

---

## Related

**Feature**: [[streaming]], [[real-time-updates]]
**Technology**: [[fastapi]], [[sse]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[websockets-streaming.md]], [[graphql-subscriptions.md]]
