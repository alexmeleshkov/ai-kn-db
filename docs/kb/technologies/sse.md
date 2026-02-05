# SSE (Server-Sent Events)

**Category**: Real-time Communication / Streaming
**Website**: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
**Specification**: https://html.spec.whatwg.org/multipage/server-sent-events.html

---

## Overview

Server-Sent Events (SSE) is a server push technology enabling servers to send real-time updates to clients over HTTP. Unlike WebSockets, SSE is unidirectional (server → client) and uses simple HTTP connections.

---

## Key Features

**HTTP-based**: Uses standard HTTP (no special protocol)
**Automatic Reconnection**: Browser automatically reconnects if connection drops
**Text-based**: Events sent as UTF-8 text
**Event IDs**: Supports resuming from last received event
**Named Events**: Multiple event types on same connection
**Simple API**: Native browser EventSource API

---

## Protocol Format

**Content-Type**: `text/event-stream`

**Basic Event**:
```
data: This is a message\n\n
```

**Event with ID**:
```
id: 123\n
data: Message with ID\n\n
```

**Named Event**:
```
event: user-joined\n
data: {"user": "Alice"}\n\n
```

**Multi-line Data**:
```
data: First line\n
data: Second line\n\n
```

**Heartbeat** (keep connection alive):
```
: heartbeat\n\n
```

---

## Common Use Cases

- **Live feeds**: News updates, social media streams
- **Notifications**: Real-time alerts and messages
- **Progress updates**: File uploads, task processing
- **Chat applications**: One-way message streaming
- **Monitoring dashboards**: Metrics and logs
- **AI streaming**: LLM text generation, thinking preview

---

## Server Implementation Examples

### Python/FastAPI
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

@app.get("/events")
async def stream_events():
    async def event_generator():
        # Send named events
        yield f"event: thinking\n"
        yield f"data: {json.dumps({'content': 'Processing...'})}\n\n"
        await asyncio.sleep(1)

        yield f"event: result\n"
        yield f"data: {json.dumps({'answer': 'Hello!'})}\n\n"

        yield f"event: done\n"
        yield f"data: {json.dumps({})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

### Node.js/Express
```javascript
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream')
  res.setHeader('Cache-Control', 'no-cache')
  res.setHeader('Connection', 'keep-alive')

  const sendEvent = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`)
  }

  sendEvent({ type: 'connected' })

  // Send heartbeat every 15s
  const interval = setInterval(() => {
    res.write(': heartbeat\n\n')
  }, 15000)

  req.on('close', () => {
    clearInterval(interval)
  })
})
```

---

## Client Implementation

### Browser EventSource API
```javascript
const eventSource = new EventSource('/api/events')

eventSource.onmessage = (event) => {
  console.log('Message:', event.data)
}

eventSource.addEventListener('thinking', (event) => {
  const data = JSON.parse(event.data)
  console.log('Thinking:', data.content)
})

eventSource.addEventListener('done', () => {
  eventSource.close()
})

eventSource.onerror = (error) => {
  console.error('Connection error:', error)
  eventSource.close()
}
```

### Fetch API (More Control)
```typescript
// Allows custom headers, POST, cancellation
const controller = new AbortController()

const response = await fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ question: 'Hello' }),
  signal: controller.signal
})

const reader = response.body!.getReader()
const decoder = new TextDecoder()
let buffer = ''

while (true) {
  const { done, value } = await reader.read()
  if (done) break

  buffer += decoder.decode(value, { stream: true })
  const events = buffer.split('\n\n')
  buffer = events.pop() || ''  // Keep incomplete event

  for (const eventText of events) {
    const match = eventText.match(/^data: (.+)$/m)
    if (match) {
      const data = JSON.parse(match[1])
      onEvent(data)
    }
  }
}

// Cancel stream
controller.abort()
```

---

## Best Practices

**Connection Management**:
- Send heartbeat every 15-30s to prevent timeouts
- Handle reconnection gracefully
- Close connections when done
- Limit connections per user

**Performance**:
- Use HTTP/2 for multiple concurrent streams
- Disable proxy buffering (nginx: `proxy_buffering off`)
- Keep events small (split large data into chunks)
- Use compression for text data

**Security**:
- Validate all event data
- Implement authentication (cookies or tokens)
- Rate limit connections
- Sanitize data before rendering in UI

---

## Proxy Configuration

### Nginx
```nginx
location /api/events {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
    proxy_read_timeout 3600s;
}
```

### Platform Timeouts
- **Heroku**: 55-second timeout → send heartbeat every 15s
- **AWS ALB**: 60-second idle timeout
- **Cloudflare**: 100-second timeout

---

## SSE vs WebSockets

**SSE Advantages**:
- ✅ Simpler (HTTP-based)
- ✅ Automatic reconnection
- ✅ Event IDs for resuming
- ✅ Works through most proxies
- ✅ Better for one-way updates

**SSE Limitations**:
- ❌ Unidirectional only (server → client)
- ❌ Text-only (no binary)
- ❌ HTTP/1.1 connection limits (6 per domain)
- ❌ No custom headers with EventSource

**Use SSE for**: Live feeds, notifications, progress updates, LLM streaming
**Use WebSockets for**: Chat (bidirectional), gaming, collaborative editing

---

## Error Handling

```javascript
let reconnectAttempts = 0
const maxReconnects = 5

function connect() {
  const eventSource = new EventSource('/api/events')

  eventSource.onopen = () => {
    console.log('Connected')
    reconnectAttempts = 0
  }

  eventSource.onerror = () => {
    eventSource.close()

    if (reconnectAttempts < maxReconnects) {
      reconnectAttempts++
      const delay = Math.min(1000 * 2 ** reconnectAttempts, 30000)
      console.log(`Reconnecting in ${delay}ms...`)
      setTimeout(connect, delay)
    } else {
      console.error('Max reconnect attempts reached')
    }
  }
}

connect()
```

---

## Testing

### Manual Test
```bash
curl -N http://localhost:8000/events
```

### Python Test
```python
import httpx

async def test_sse():
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', 'http://localhost:8000/events') as response:
            async for line in response.aiter_lines():
                if line.startswith('data:'):
                    print(line)
```

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[data-streaming]], [[real-time-updates]]
**Code snippets**: See `languages/python/snippets/`, `languages/typescript/snippets/`
**Alternatives**: [[websockets]], [[long-polling]], [[grpc-streaming]]
**Often used with**: [[fastapi]], [[react-hooks]], [[asyncio]]
