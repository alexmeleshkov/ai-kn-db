# TypeScript - Discriminated Union Types for Streaming Events

**Language**: TypeScript
**Technology**: TypeScript Type System
**Feature/Pattern**: Discriminated Unions, Type-Safe Event Handling, Tagged Unions
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
npm install typescript
```

**Required Knowledge**:
- TypeScript interfaces
- Union types
- Type narrowing with discriminated unions
- Literal types
- Type guards
- Switch statements with exhaustiveness checking

---

## Overview

This snippet demonstrates production-ready discriminated union types for type-safe event handling in streaming systems. Discriminated unions (also called tagged unions) use a common property (discriminant) to enable exhaustive type checking and type narrowing in switch statements.

Key features:
- Type-safe event handling with discriminant property
- Exhaustive switch statement checking
- IntelliSense support for event properties
- Compile-time guarantees for event processing
- Prevents accessing properties that don't exist on event type
- Self-documenting event structure

---

## Implementation

### Basic Usage

```typescript
import type { StreamEvent } from './api';

function handleEvent(event: StreamEvent) {
  switch (event.type) {
    case 'text':
      // TypeScript knows event.content exists
      console.log('Text:', event.content);
      break;

    case 'tool_start':
      // TypeScript knows event.query and event.tool exist
      console.log('Running tool:', event.tool);
      console.log('Query:', event.query);
      break;

    case 'done':
      // TypeScript knows event.conversation_id exists
      console.log('Done! ID:', event.conversation_id);
      break;

    case 'error':
      // TypeScript knows event.message exists
      console.error('Error:', event.message);
      break;

    default:
      // TypeScript ensures all cases handled
      const _exhaustive: never = event;
      return _exhaustive;
  }
}
```

**Explanation**:
- Switch on `event.type` narrows type automatically
- Each case has access to case-specific properties
- Default case catches unhandled event types at compile time

### Advanced Usage with Type Guards

```typescript
// Type guard functions
function isTextEvent(event: StreamEvent): event is StreamTextEvent {
  return event.type === 'text';
}

function isToolEvent(event: StreamEvent): event is StreamToolStartEvent | StreamToolResultEvent {
  return event.type === 'tool_start' || event.type === 'tool_result';
}

function isErrorEvent(event: StreamEvent): event is StreamErrorEvent {
  return event.type === 'error';
}

// Usage with type guards
function processEvent(event: StreamEvent) {
  if (isTextEvent(event)) {
    // event is StreamTextEvent
    updateTextDisplay(event.content);
  } else if (isToolEvent(event)) {
    // event is StreamToolStartEvent | StreamToolResultEvent
    updateToolDisplay(event.query);
  } else if (isErrorEvent(event)) {
    // event is StreamErrorEvent
    showError(event.message);
  }
}

// Filter events by type
function filterTextEvents(events: StreamEvent[]): StreamTextEvent[] {
  return events.filter(isTextEvent);
}

// Map over specific event types
function extractAllQueries(events: StreamEvent[]): string[] {
  return events
    .filter((e): e is StreamToolStartEvent => e.type === 'tool_start')
    .map(e => e.query);
}
```

**Key Points**:
- Type guards enable type narrowing in if statements
- Filter with type guard maintains type information
- Inline type guards work in array methods
- Type predicates (`event is Type`) enable flow analysis

---

## Complete Example

```typescript
/**
 * Streaming event type definitions with discriminated unions.
 */

// Thinking events
export interface StreamThinkingStartEvent {
  type: 'thinking_start';
}

export interface StreamThinkingEvent {
  type: 'thinking';
  content: string;
}

export interface StreamThinkingEndEvent {
  type: 'thinking_end';
}

// Text streaming event
export interface StreamTextEvent {
  type: 'text';
  content: string;
}

// Tool execution events
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

// Error event
export interface StreamErrorEvent {
  type: 'error';
  message: string;
}

// Completion event
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

// Keep-alive event
export interface StreamHeartbeatEvent {
  type: 'heartbeat';
}

// Clarification events
export interface StreamClarificationEvent {
  type: 'clarification_needed';
  question: string;
  options: string[];
  context?: string;
}

export interface StreamWaitingForClarificationEvent {
  type: 'waiting_for_clarification';
  question: string;
  options: string[];
}

// Discriminated union of all event types
export type StreamEvent =
  | StreamThinkingStartEvent
  | StreamThinkingEvent
  | StreamThinkingEndEvent
  | StreamTextEvent
  | StreamToolStartEvent
  | StreamToolResultEvent
  | StreamErrorEvent
  | StreamDoneEvent
  | StreamHeartbeatEvent
  | StreamClarificationEvent
  | StreamWaitingForClarificationEvent;

// ============ Usage Examples ============

// Exhaustive event handler with type narrowing
function handleStreamEvent(event: StreamEvent): void {
  switch (event.type) {
    case 'thinking_start':
      console.log('AI started thinking');
      break;

    case 'thinking':
      console.log('Thinking:', event.content);
      break;

    case 'thinking_end':
      console.log('AI finished thinking');
      break;

    case 'text':
      console.log('Text:', event.content);
      break;

    case 'tool_start':
      console.log('Tool:', event.tool);
      console.log('Query:', event.query);
      if (event.reasoning) {
        console.log('Reasoning:', event.reasoning);
      }
      break;

    case 'tool_result':
      if (event.success) {
        console.log('Success:', event.rows, 'rows');
        console.log('Time:', event.time_ms, 'ms');
      } else {
        console.error('Failed:', event.error);
      }
      break;

    case 'error':
      console.error('Error:', event.message);
      break;

    case 'done':
      console.log('Conversation:', event.conversation_id);
      console.log('Queries executed:', event.queries.length);
      break;

    case 'heartbeat':
      // Keep-alive - no action needed
      break;

    case 'clarification_needed':
      console.log('Question:', event.question);
      console.log('Options:', event.options);
      break;

    case 'waiting_for_clarification':
      console.log('Waiting for user to select:', event.options);
      break;

    default:
      // Exhaustiveness check - TypeScript error if case missing
      const _exhaustive: never = event;
      return _exhaustive;
  }
}

// React component using discriminated unions
import { useState } from 'react';

function StreamingDisplay() {
  const [events, setEvents] = useState<StreamEvent[]>([]);

  const handleEvent = (event: StreamEvent) => {
    setEvents(prev => [...prev, event]);

    // Type-safe event handling
    switch (event.type) {
      case 'text':
        updateTextContent(event.content);
        break;

      case 'tool_start':
        showQueryExecuting(event.query);
        break;

      case 'tool_result':
        showQueryResult(event.success, event.rows, event.error);
        break;

      case 'clarification_needed':
        showClarificationPrompt(event.question, event.options);
        break;

      case 'done':
        finalize(event.conversation_id);
        break;
    }
  };

  return (
    <div>
      {events.map((event, i) => (
        <EventDisplay key={i} event={event} />
      ))}
    </div>
  );
}

// Component that renders different UI based on event type
function EventDisplay({ event }: { event: StreamEvent }) {
  switch (event.type) {
    case 'text':
      return <div className="text">{event.content}</div>;

    case 'tool_start':
      return (
        <div className="tool-start">
          <strong>{event.tool}</strong>
          <code>{event.query}</code>
        </div>
      );

    case 'tool_result':
      return (
        <div className={event.success ? 'success' : 'error'}>
          {event.success ? (
            <span>{event.rows} rows in {event.time_ms}ms</span>
          ) : (
            <span>Error: {event.error}</span>
          )}
        </div>
      );

    case 'clarification_needed':
      return (
        <div className="clarification">
          <p>{event.question}</p>
          {event.options.map(opt => (
            <button key={opt}>{opt}</button>
          ))}
        </div>
      );

    case 'error':
      return <div className="error">{event.message}</div>;

    case 'thinking':
    case 'thinking_start':
    case 'thinking_end':
    case 'heartbeat':
    case 'done':
    case 'waiting_for_clarification':
      return null;

    default:
      // Exhaustiveness check
      const _exhaustive: never = event;
      return _exhaustive;
  }
}
```

---

## Configuration

```typescript
// Event grouping with type aliases
export type ThinkingEvent =
  | StreamThinkingStartEvent
  | StreamThinkingEvent
  | StreamThinkingEndEvent;

export type ToolEvent =
  | StreamToolStartEvent
  | StreamToolResultEvent;

export type ClarificationEvent =
  | StreamClarificationEvent
  | StreamWaitingForClarificationEvent;

// Type guard factories
function isThinkingEvent(event: StreamEvent): event is ThinkingEvent {
  return event.type.startsWith('thinking');
}

function isToolEvent(event: StreamEvent): event is ToolEvent {
  return event.type.startsWith('tool');
}

function isClarificationEvent(event: StreamEvent): event is ClarificationEvent {
  return event.type.includes('clarification');
}

// Event filtering
function filterByCategory(events: StreamEvent[]) {
  return {
    thinking: events.filter(isThinkingEvent),
    tools: events.filter(isToolEvent),
    clarifications: events.filter(isClarificationEvent),
    text: events.filter((e): e is StreamTextEvent => e.type === 'text'),
    errors: events.filter((e): e is StreamErrorEvent => e.type === 'error'),
  };
}
```

---

## Error Handling

```typescript
// Safe event parsing with validation
function parseStreamEvent(data: string): StreamEvent | null {
  try {
    const parsed = JSON.parse(data) as Partial<StreamEvent>;

    // Validate discriminant exists
    if (!parsed.type) {
      console.error('Event missing type:', data);
      return null;
    }

    // Validate event type is known
    const validTypes = [
      'thinking_start', 'thinking', 'thinking_end',
      'text', 'tool_start', 'tool_result',
      'error', 'done', 'heartbeat',
      'clarification_needed', 'waiting_for_clarification'
    ];

    if (!validTypes.includes(parsed.type)) {
      console.warn('Unknown event type:', parsed.type);
      return null;
    }

    // Type assertion after validation
    return parsed as StreamEvent;
  } catch (err) {
    console.error('Failed to parse event:', err);
    return null;
  }
}

// Usage in SSE handler
for (const line of lines) {
  if (line.startsWith('data: ')) {
    const data = line.slice(6);
    const event = parseStreamEvent(data);

    if (event) {
      handleStreamEvent(event);
    }
  }
}

// Error recovery in event handler
function safeHandleEvent(event: StreamEvent): void {
  try {
    switch (event.type) {
      case 'tool_result':
        if (!event.query) {
          console.error('tool_result missing query');
          return;
        }
        processToolResult(event);
        break;

      case 'text':
        if (typeof event.content !== 'string') {
          console.error('text event has invalid content');
          return;
        }
        processText(event.content);
        break;

      // ... other cases
    }
  } catch (err) {
    console.error('Error handling event:', event.type, err);
  }
}
```

**Common Errors**:
1. **Missing Discriminant**: Event has no `type` field - validation catches before type assertion
2. **Unknown Event Type**: New event type not in union - safely ignored or logged
3. **Missing Required Fields**: Event missing expected fields - runtime validation needed
4. **Type Mismatch**: Field has wrong type (e.g., number instead of string) - validate before processing

---

## Testing

```typescript
import type { StreamEvent, StreamTextEvent, StreamToolResultEvent } from './api';

describe('StreamEvent discriminated unions', () => {
  it('narrows type in switch statement', () => {
    const event: StreamEvent = {
      type: 'text',
      content: 'Hello',
    };

    switch (event.type) {
      case 'text':
        // TypeScript knows event.content exists
        expect(event.content).toBe('Hello');
        break;
      default:
        fail('Should not reach default');
    }
  });

  it('works with type guards', () => {
    const events: StreamEvent[] = [
      { type: 'text', content: 'Hello' },
      { type: 'tool_start', tool: 'query', query: 'SELECT 1' },
      { type: 'done', queries: [] },
    ];

    const textEvents = events.filter(
      (e): e is StreamTextEvent => e.type === 'text'
    );

    expect(textEvents).toHaveLength(1);
    expect(textEvents[0].content).toBe('Hello');
  });

  it('validates event structure', () => {
    const validEvent: StreamEvent = {
      type: 'tool_result',
      query: 'SELECT 1',
      success: true,
      rows: 5,
    };

    expect(validEvent.type).toBe('tool_result');
    if (validEvent.type === 'tool_result') {
      expect(validEvent.success).toBe(true);
      expect(validEvent.rows).toBe(5);
    }
  });

  it('handles unknown events safely', () => {
    const unknownData = '{"type":"unknown","data":"test"}';
    const parsed = parseStreamEvent(unknownData);

    expect(parsed).toBeNull();
  });
});

// Type-level tests (compile-time only)
function typeLevelTests() {
  const event: StreamEvent = { type: 'text', content: 'test' };

  // This compiles
  if (event.type === 'text') {
    const content: string = event.content;
  }

  // This would cause TypeScript error
  // if (event.type === 'text') {
  //   const query: string = event.query; // Error: Property 'query' does not exist
  // }

  // Exhaustiveness check catches missing cases
  function handleEvent(e: StreamEvent) {
    switch (e.type) {
      case 'text':
      case 'tool_start':
      case 'tool_result':
      case 'done':
      case 'error':
      case 'thinking_start':
      case 'thinking':
      case 'thinking_end':
      case 'heartbeat':
      case 'clarification_needed':
      case 'waiting_for_clarification':
        return true;
      default:
        // If a case is missing, this line causes compile error
        const _exhaustive: never = e;
        return _exhaustive;
    }
  }
}
```

---

## Performance Considerations

- **Zero Runtime Cost**: Discriminated unions are compile-time only, no runtime overhead
- **Switch Optimization**: Modern JS engines optimize switch statements on string literals
- **Type Narrowing**: No runtime type checking needed after narrowing
- **Inline Functions**: Small handler functions inline well for performance
- **Event Parsing**: JSON parsing is the bottleneck, not type checking

---

## Security Considerations

- **Runtime Validation**: Always validate events from untrusted sources (network)
- **Type Assertions**: Only assert types after validation
- **Unknown Events**: Safely ignore unknown event types to prevent crashes
- **Field Validation**: Check required fields exist before accessing
- **Error Handling**: Don't expose internal errors in event messages

---

## Related

**Feature**: [[data-streaming/sse-fastapi]], [[nl-to-sql/claude-tool-use]]
**Technology**: [[typescript]], [[react]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[python-pydantic-models.md]] (runtime validation with Pydantic)
