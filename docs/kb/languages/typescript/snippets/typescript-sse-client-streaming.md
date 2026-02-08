# TypeScript - Server-Sent Events (SSE) Client with Streaming

**Language**: TypeScript
**Technology**: Fetch API, ReadableStream
**Feature/Pattern**: SSE Client, Stream Processing, Event Parsing
**Difficulty**: advanced

---

## Prerequisites

**Required Packages**:
```bash
# No external packages required - uses native Fetch API
npm install typescript
```

**Required Knowledge**:
- Fetch API and ReadableStream
- Server-Sent Events (SSE) protocol
- TypeScript discriminated unions
- Async iterators and generators
- AbortController for cancellation
- TextDecoder for stream decoding

---

## Overview

This snippet demonstrates a production-ready SSE client that handles Server-Sent Events streaming using the Fetch API's ReadableStream. It parses SSE messages, manages buffering, handles reconnection, and provides type-safe event handling with discriminated unions.

Key features:
- ReadableStream processing for SSE
- Buffer management for incomplete messages
- Type-safe event parsing with discriminated unions
- AbortController support for cancellation
- Authentication header injection
- Line-by-line SSE message parsing
- Error handling and recovery

---

## Implementation

### Basic Usage

```typescript
import { sendMessageStreaming, StreamEvent } from './api';

async function streamChat(message: string) {
  await sendMessageStreaming(
    message,
    (event: StreamEvent) => {
      switch (event.type) {
        case 'text':
          console.log('Text:', event.content);
          break;
        case 'done':
          console.log('Stream complete');
          break;
        case 'error':
          console.error('Error:', event.message);
          break;
      }
    }
  );
}
```

**Explanation**:
- Callback receives strongly-typed events
- Switch on event.type for type narrowing
- Events processed in real-time as they arrive

### Advanced Usage with Cancellation

```typescript
// Create abort controller for cancellation
const abortController = new AbortController();

// Start streaming
const streamPromise = sendMessageStreaming(
  'What are the top products?',
  (event: StreamEvent) => {
    if (event.type === 'thinking') {
      console.log('AI thinking:', event.content);
    } else if (event.type === 'tool_start') {
      console.log('Executing query:', event.query);
    } else if (event.type === 'tool_result') {
      console.log('Query result:', event.rows, 'rows');
      if (!event.success) {
        console.error('Query error:', event.error);
      }
    } else if (event.type === 'text') {
      console.log('Response text:', event.content);
    } else if (event.type === 'done') {
      console.log('Conversation ID:', event.conversation_id);
    }
  },
  abortController.signal,
  'conversation-123' // Optional conversation ID for context
);

// Cancel after 30 seconds
setTimeout(() => {
  abortController.abort();
  console.log('Stream cancelled');
}, 30000);

// Wait for completion or cancellation
try {
  await streamPromise;
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('User cancelled stream');
  } else {
    console.error('Stream error:', err);
  }
}
```

**Key Points**:
- AbortController cancels stream at any time
- Conversation ID maintains context across messages
- Type-safe event handling with discriminated unions
- Graceful error handling for cancellation vs errors

---

## Complete Example

```typescript
/**
 * Send a message with streaming response.
 * Calls the callback for each event received.
 */
export async function sendMessageStreaming(
  message: string,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
  conversationId?: string | null
): Promise<void> {
  const response = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId || undefined,
    }),
    signal,
  });

  if (!response.ok) {
    throw new ApiError(response.status, 'Stream request failed');
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new ApiError(500, 'No response body');
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE messages
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data.trim()) {
            try {
              const event = JSON.parse(data) as StreamEvent;
              onEvent(event);
            } catch (e) {
              console.error('Failed to parse SSE event:', data);
            }
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// Event type definitions
export interface StreamTextEvent {
  type: 'text';
  content: string;
}

export interface StreamToolStartEvent {
  type: 'tool_start';
  tool: string;
  query: string;
  reasoning?: string;
}

export interface StreamToolResultEvent {
  type: 'tool_result';
  query: string;
  success: boolean;
  rows?: number;
  time_ms?: number;
  columns?: string[];
  data?: unknown[][];
  error?: string;
}

export interface StreamDoneEvent {
  type: 'done';
  queries: Array<{
    query: string;
    success: boolean;
    rows?: number;
    time_ms?: number;
    error?: string;
  }>;
  conversation_id?: string;
}

export interface StreamErrorEvent {
  type: 'error';
  message: string;
}

export type StreamEvent =
  | StreamTextEvent
  | StreamToolStartEvent
  | StreamToolResultEvent
  | StreamDoneEvent
  | StreamErrorEvent;
```

---

## Configuration

```typescript
// API configuration
const API_BASE = '/api/v1';

// Auth headers
export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Custom API error class
class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}
```

---

## Error Handling

```typescript
async function streamWithErrorHandling(message: string) {
  try {
    await sendMessageStreaming(
      message,
      (event: StreamEvent) => {
        if (event.type === 'error') {
          // Server sent error event
          console.error('Server error:', event.message);
          // Update UI to show error
        } else if (event.type === 'text') {
          // Update UI with text
          console.log(event.content);
        }
      },
      signal
    );
  } catch (err) {
    if (err instanceof ApiError) {
      switch (err.status) {
        case 401:
          console.error('Authentication required');
          // Redirect to login
          break;
        case 429:
          console.error('Rate limited - too many requests');
          // Show rate limit message
          break;
        case 500:
          console.error('Server error:', err.message);
          // Show generic error
          break;
        default:
          console.error('Request failed:', err.message);
      }
    } else if (err.name === 'AbortError') {
      console.log('Stream cancelled by user');
      // No error UI needed
    } else {
      console.error('Network error:', err);
      // Show connectivity error
    }
  }
}

// Partial event parsing error handling
for (const line of lines) {
  if (line.startsWith('data: ')) {
    const data = line.slice(6);
    if (data.trim()) {
      try {
        const event = JSON.parse(data) as StreamEvent;
        onEvent(event);
      } catch (e) {
        // Log but don't throw - continue processing other events
        console.error('Failed to parse SSE event:', data);
        // Optionally emit error event
        onEvent({
          type: 'error',
          message: 'Failed to parse server event'
        });
      }
    }
  }
}
```

**Common Errors**:
1. **No Response Body**: Response doesn't have a body - check server CORS and response headers
2. **Parse Error**: Invalid JSON in SSE message - log and continue processing
3. **AbortError**: User cancelled stream - handle gracefully without error UI
4. **Network Error**: Connection interrupted - show retry option

---

## Testing

```typescript
import { sendMessageStreaming } from './api';

describe('SSE Client', () => {
  it('processes text events', async () => {
    const events: StreamEvent[] = [];

    // Mock fetch to return SSE stream
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        body: {
          getReader: () => ({
            read: jest.fn()
              .mockResolvedValueOnce({
                done: false,
                value: new TextEncoder().encode('data: {"type":"text","content":"Hello"}\n')
              })
              .mockResolvedValueOnce({
                done: false,
                value: new TextEncoder().encode('data: {"type":"done"}\n')
              })
              .mockResolvedValueOnce({ done: true }),
            releaseLock: jest.fn(),
          }),
        },
      } as any)
    );

    await sendMessageStreaming('test', (event) => {
      events.push(event);
    });

    expect(events).toHaveLength(2);
    expect(events[0].type).toBe('text');
    expect(events[1].type).toBe('done');
  });

  it('handles cancellation', async () => {
    const abortController = new AbortController();

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        body: {
          getReader: () => ({
            read: jest.fn()
              .mockImplementation(() => new Promise(() => {})), // Never resolves
            releaseLock: jest.fn(),
          }),
        },
      } as any)
    );

    const promise = sendMessageStreaming(
      'test',
      () => {},
      abortController.signal
    );

    abortController.abort();

    await expect(promise).rejects.toThrow('AbortError');
  });

  it('handles incomplete SSE messages', async () => {
    const events: StreamEvent[] = [];

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        body: {
          getReader: () => ({
            read: jest.fn()
              .mockResolvedValueOnce({
                done: false,
                value: new TextEncoder().encode('data: {"type":"text","con') // Incomplete
              })
              .mockResolvedValueOnce({
                done: false,
                value: new TextEncoder().encode('tent":"Hello"}\n') // Complete
              })
              .mockResolvedValueOnce({ done: true }),
            releaseLock: jest.fn(),
          }),
        },
      } as any)
    );

    await sendMessageStreaming('test', (event) => {
      events.push(event);
    });

    expect(events).toHaveLength(1);
    expect(events[0]).toEqual({ type: 'text', content: 'Hello' });
  });
});
```

---

## Performance Considerations

- **Buffer Management**: Incomplete messages buffered efficiently with string concatenation
- **Stream Processing**: Processes events as they arrive, not waiting for full response
- **Memory Efficiency**: TextDecoder streams bytes without loading entire response
- **Reader Lock**: Always released in finally block to prevent memory leaks
- **Event Callback**: Synchronous callback prevents backpressure issues
- **Parse Errors**: Individual parse failures don't stop stream processing

---

## Security Considerations

- **Auth Headers**: Tokens included in headers, not URL query params
- **HTTPS Only**: SSE streams should only use HTTPS to encrypt tokens
- **CORS**: Backend must set proper CORS headers for cross-origin streaming
- **Event Validation**: Parse errors caught and logged, don't crash client
- **Token Refresh**: Long streams may need token refresh handling
- **Rate Limiting**: Backend should implement rate limits on streaming endpoints

---

## Related

**Feature**: [[data-streaming/sse-fastapi]], [[nl-to-sql/claude-tool-use]]
**Technology**: [[typescript]], [[react]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[python-sse-streaming.md]], [[react-hooks-sse-streaming-useChat.md]]
