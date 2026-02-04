# Server-Sent Events (SSE)

**Technology**: SSE Protocol (text/event-stream)
**Category**: Protocol

---

## Overview

HTTP-based streaming protocol for server-to-client real-time updates.

---

## Usage Files

- `backend/app/api/routes.py`
- `backend/app/services/chat.py`
- `frontend/src/services/api.ts`
- `frontend/src/hooks/useChat.ts`

---

## Complete Usage Patterns

### Backend SSE Endpoint (routes.py)

**Pattern**:
```python
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(request: ChatRequest):
    async def event_generator():
        for event in chat_service.stream_chat(...):
            yield f"data: {json.dumps(event)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Event Format**:
```
data: {"type": "text", "content": "Hello"}\n\n
data: {"type": "done"}\n\n
```

### Frontend SSE Client (api.ts)

**Pattern**:
```typescript
const response = await fetch('/chat', {
  method: 'POST',
  body: JSON.stringify({ content: question }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  buffer += decoder.decode(value, { stream: true });
  const lines = buffer.split('\n\n');
  buffer = lines.pop() || '';

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const event = JSON.parse(line.slice(6));
      onEvent(event);
    }
  }
}
```

**All Behaviors**:
- Text-based protocol (text/event-stream)
- Events delimited by \n\n
- Data lines start with "data: "
- Client-side parsing with buffering
- Automatic reconnection on disconnect

---

## Configuration

```python
media_type="text/event-stream"
headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
```
