# TypeScript + React - Custom Hook for SSE Streaming Chat

**Language**: TypeScript
**Technology**: React
**Feature/Pattern**: SSE Streaming with React Hooks, State Management
**Difficulty**: advanced

---

## Prerequisites

**Required Packages**:
```bash
npm install react typescript
npm install --save-dev @types/react
```

**Required Knowledge**:
- React hooks (useState, useEffect, useCallback, useRef)
- TypeScript interfaces and discriminated unions
- Server-Sent Events (SSE)
- Async/await patterns
- AbortController for cancellation

---

## Overview

This snippet demonstrates a production-ready custom React hook for managing chat state with Server-Sent Events (SSE) streaming. It handles real-time streaming responses, progress tracking, query execution status, thinking indicators, clarification requests, and conversation history.

Key features:
- Real-time SSE event processing with discriminated union types
- Streaming state management with progress stages
- Query execution tracking with success/error states
- Elapsed time tracking with intervals
- Abort controller for cancellation
- Conversation loading and persistence
- Error handling with user-friendly messages

---

## Implementation

### Basic Usage

```typescript
import { useChat } from './hooks/useChat';

function ChatComponent() {
  const {
    messages,
    isLoading,
    error,
    sendUserMessage,
    clearChat
  } = useChat();

  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id}>{msg.content}</div>
      ))}
      <button onClick={() => sendUserMessage("Hello!")}>
        Send
      </button>
    </div>
  );
}
```

**Explanation**:
- The hook provides reactive state for messages, loading, and errors
- `sendUserMessage` handles SSE streaming automatically
- Messages update in real-time as events arrive

### Advanced Usage with Streaming State

```typescript
function AdvancedChatComponent() {
  const {
    messages,
    streamingState,
    sendUserMessage,
    cancelStream,
    selectClarificationOption
  } = useChat();

  return (
    <div>
      {/* Show thinking indicator */}
      {streamingState.isThinking && (
        <div className="thinking">
          <span>Thinking...</span>
          <p>{streamingState.thinkingText}</p>
        </div>
      )}

      {/* Show query execution status */}
      {streamingState.currentQuery && (
        <div className={`query-${streamingState.queryStatus}`}>
          <code>{streamingState.currentQuery}</code>
          <span>Status: {streamingState.queryStatus}</span>
        </div>
      )}

      {/* Show streaming text */}
      {streamingState.isStreaming && streamingState.currentText && (
        <div className="streaming">
          {streamingState.currentText}
          <span className="elapsed">
            {(streamingState.elapsedMs / 1000).toFixed(1)}s
          </span>
        </div>
      )}

      {/* Show clarification request */}
      {streamingState.clarification && (
        <div className="clarification">
          <p>{streamingState.clarification.question}</p>
          {streamingState.clarification.options.map(option => (
            <button
              key={option}
              onClick={() => selectClarificationOption(option)}
            >
              {option}
            </button>
          ))}
        </div>
      )}

      {/* Cancel button */}
      {streamingState.isStreaming && (
        <button onClick={cancelStream}>Cancel</button>
      )}
    </div>
  );
}
```

**Key Points**:
- `streamingState` provides granular control over UI indicators
- Progress stages: connecting → thinking → generating_sql → executing_query → processing_results
- Query status tracks SQL execution: idle → executing → success/error
- Elapsed time updates every 100ms during streaming
- Clarification support for interactive queries

---

## Complete Example

```typescript
/**
 * Custom hook for managing chat state with streaming support.
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types/chat';
import { sendMessageStreaming, StreamEvent, getConversation } from '../services/api';

type ProgressStage = 'connecting' | 'thinking' | 'generating_sql' | 'executing_query' | 'processing_results';

interface ClarificationRequest {
  question: string;
  options: string[];
  context?: string;
}

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

interface UseChatResult {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string | null;
  streamingState: StreamingState;
  sendUserMessage: (content: string) => Promise<void>;
  clearChat: () => void;
  cancelStream: () => void;
  loadConversation: (id: string) => Promise<void>;
  clearError: () => void;
  selectClarificationOption: (option: string) => void;
}

export function useChat(): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [streamingState, setStreamingState] = useState<StreamingState>({
    isStreaming: false,
    currentText: '',
    currentQuery: null,
    queryStatus: 'idle',
    isThinking: false,
    thinkingText: '',
    elapsedMs: 0,
    progressStage: 'connecting',
    clarification: null,
  });

  const abortControllerRef = useRef<AbortController | null>(null);
  const startTimeRef = useRef<number | null>(null);
  const timerRef = useRef<number | null>(null);

  // Elapsed time timer
  useEffect(() => {
    if (streamingState.isStreaming && startTimeRef.current) {
      timerRef.current = window.setInterval(() => {
        const elapsed = Date.now() - (startTimeRef.current || Date.now());
        setStreamingState(prev => ({ ...prev, elapsedMs: elapsed }));
      }, 100);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [streamingState.isStreaming]);

  const cancelStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  const sendUserMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Cancel any existing stream
    cancelStream();

    // Add user message immediately
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    // Create new abort controller
    abortControllerRef.current = new AbortController();

    // Initialize streaming state and timer
    startTimeRef.current = Date.now();
    setStreamingState({
      isStreaming: true,
      currentText: '',
      currentQuery: null,
      queryStatus: 'idle',
      isThinking: false,
      thinkingText: '',
      elapsedMs: 0,
      progressStage: 'connecting',
      clarification: null,
    });

    // Collect the full response
    let fullText = '';
    const executedQueries: Array<{
      query: string;
      success: boolean;
      rows?: number;
      error?: string;
      columns?: string[];
      data?: unknown[][];
    }> = [];

    // Capture current conversationId for the closure
    const currentConversationId = conversationId;

    try {
      await sendMessageStreaming(
        content.trim(),
        (event: StreamEvent) => {
          switch (event.type) {
            case 'thinking_start':
              setStreamingState(prev => ({
                ...prev,
                isThinking: true,
                thinkingText: '',
                progressStage: 'thinking',
              }));
              break;

            case 'thinking':
              setStreamingState(prev => ({
                ...prev,
                thinkingText: prev.thinkingText + (event.content || ''),
              }));
              break;

            case 'thinking_end':
              setStreamingState(prev => ({
                ...prev,
                isThinking: false,
                progressStage: 'generating_sql',
              }));
              break;

            case 'text':
              fullText += event.content;
              setStreamingState(prev => ({
                ...prev,
                currentText: fullText,
                isThinking: false,
                progressStage: 'processing_results',
              }));
              break;

            case 'tool_start':
              setStreamingState(prev => ({
                ...prev,
                currentQuery: event.query,
                queryStatus: 'executing',
                progressStage: 'executing_query',
              }));
              break;

            case 'tool_result':
              executedQueries.push({
                query: event.query,
                success: event.success,
                rows: event.rows,
                error: event.error,
                columns: event.columns,
                data: event.data,
              });
              setStreamingState(prev => ({
                ...prev,
                queryStatus: event.success ? 'success' : 'error',
                progressStage: event.success ? 'processing_results' : 'generating_sql',
              }));
              break;

            case 'error':
              setError(event.message);
              break;

            case 'done':
              // Store conversation_id for memory
              if (event.conversation_id) {
                setConversationId(event.conversation_id);
              }

              // Build final message - text only, queries stored separately
              const assistantMessage: ChatMessage = {
                id: crypto.randomUUID(),
                role: 'assistant',
                content: fullText,
                timestamp: new Date().toISOString(),
                executedQueries: executedQueries.length > 0 ? executedQueries : undefined,
              };

              setMessages(prev => [...prev, assistantMessage]);
              startTimeRef.current = null;
              setStreamingState({
                isStreaming: false,
                currentText: '',
                currentQuery: null,
                queryStatus: 'idle',
                isThinking: false,
                thinkingText: '',
                elapsedMs: 0,
                progressStage: 'connecting',
                clarification: null,
              });
              break;

            case 'heartbeat':
              // Keep-alive event - ignore
              break;

            case 'clarification_needed':
              // AI is asking for clarification
              setStreamingState(prev => ({
                ...prev,
                clarification: {
                  question: event.question || '',
                  options: event.options || [],
                  context: event.context,
                },
                progressStage: 'processing_results',
              }));
              break;

            case 'waiting_for_clarification':
              // Stop streaming, keep clarification visible
              startTimeRef.current = null;
              setStreamingState(prev => ({
                ...prev,
                isStreaming: false,
              }));
              setIsLoading(false);
              break;
          }
        },
        abortControllerRef.current.signal,
        currentConversationId
      );
    } catch (err) {
      startTimeRef.current = null;
      if ((err as Error).name === 'AbortError') {
        // Stream was cancelled
        setStreamingState({
          isStreaming: false,
          currentText: '',
          currentQuery: null,
          queryStatus: 'idle',
          isThinking: false,
          thinkingText: '',
          elapsedMs: 0,
          progressStage: 'connecting',
          clarification: null,
        });
      } else {
        // Provide user-friendly error messages
        let errorMessage = err instanceof Error ? err.message : 'Failed to send message';

        // Map common errors to friendly messages
        if (errorMessage.includes('timed out') || errorMessage.includes('timeout')) {
          errorMessage = 'This question needs a lot of data processing. Try being more specific, like "Show top 10..." or "How many... in 2024?"';
        } else if (errorMessage.includes('network') || errorMessage.includes('fetch')) {
          errorMessage = 'Connection was interrupted. This can happen with complex queries. Please try again.';
        } else if (errorMessage.includes('Stream request failed')) {
          errorMessage = 'Having trouble connecting. Please try again in a moment.';
        }

        setError(errorMessage);

        // Add error message if we have partial content
        if (fullText) {
          const partialMessage: ChatMessage = {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: fullText + `\n\n*Error: ${errorMessage}*`,
            timestamp: new Date().toISOString(),
          };
          setMessages(prev => [...prev, partialMessage]);
        }

        setStreamingState({
          isStreaming: false,
          currentText: '',
          currentQuery: null,
          queryStatus: 'idle',
          isThinking: false,
          thinkingText: '',
          elapsedMs: 0,
          progressStage: 'connecting',
          clarification: null,
        });
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [cancelStream, conversationId]);

  const clearChat = useCallback(() => {
    cancelStream();
    startTimeRef.current = null;
    setMessages([]);
    setConversationId(null);
    setError(null);
    setStreamingState({
      isStreaming: false,
      currentText: '',
      currentQuery: null,
      queryStatus: 'idle',
      isThinking: false,
      thinkingText: '',
      elapsedMs: 0,
      progressStage: 'connecting',
      clarification: null,
    });
  }, [cancelStream]);

  // Handle user selecting a clarification option
  const selectClarificationOption = useCallback((option: string) => {
    // Clear clarification state
    setStreamingState(prev => ({
      ...prev,
      clarification: null,
    }));
    // Send the selected option as a user message
    sendUserMessage(option);
  }, [sendUserMessage]);

  const loadConversation = useCallback(async (id: string) => {
    cancelStream();
    setIsLoading(true);
    setError(null);

    try {
      const conversation = await getConversation(id);
      setConversationId(id);

      // Convert conversation messages to chat messages
      const chatMessages: ChatMessage[] = conversation.messages.map(msg => ({
        id: msg.id,
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        timestamp: msg.created_at,
      }));

      setMessages(chatMessages);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load conversation';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [cancelStream]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    conversationId,
    streamingState,
    sendUserMessage,
    clearChat,
    cancelStream,
    loadConversation,
    clearError,
    selectClarificationOption,
  };
}
```

---

## Error Handling

```typescript
// Error handling in useChat hook
try {
  await sendMessageStreaming(content, onEvent, signal, conversationId);
} catch (err) {
  if ((err as Error).name === 'AbortError') {
    // User cancelled - reset streaming state
    setStreamingState({
      isStreaming: false,
      currentText: '',
      // ... reset other fields
    });
  } else {
    // Map error to user-friendly message
    let errorMessage = err instanceof Error ? err.message : 'Failed to send message';

    if (errorMessage.includes('timeout')) {
      errorMessage = 'Query took too long. Try being more specific.';
    } else if (errorMessage.includes('network')) {
      errorMessage = 'Connection interrupted. Please try again.';
    }

    setError(errorMessage);

    // Save partial response if available
    if (fullText) {
      const partialMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: fullText + `\n\n*Error: ${errorMessage}*`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, partialMessage]);
    }
  }
}
```

**Common Errors**:
1. **AbortError**: User cancelled stream - gracefully reset state without showing error
2. **Timeout**: Query exceeded time limit - suggest more specific query
3. **Network Error**: Connection interrupted - advise retry
4. **Stream Request Failed**: Backend unavailable - general connection error

---

## Performance Considerations

- **Timer Management**: Elapsed time timer runs every 100ms only during streaming, automatically cleaned up
- **useCallback Dependencies**: All callbacks memoized with correct dependencies to prevent unnecessary re-renders
- **Ref Usage**: AbortController and timers stored in refs to avoid triggering re-renders
- **State Batching**: Multiple state updates in event handlers are batched by React 18+
- **Memory Management**: Cleanup functions in useEffect prevent memory leaks from intervals
- **Partial Messages**: Saves partial responses on error to avoid losing user context

---

## Security Considerations

- **Input Validation**: Empty messages are rejected before sending
- **Token Cancellation**: AbortController ensures streams can always be cancelled
- **Error Sanitization**: User-friendly error messages avoid exposing internal details
- **UUID Generation**: Uses crypto.randomUUID() for secure message IDs
- **Conversation ID**: Captured in closure to prevent race conditions with state updates

---

## Related

**Feature**: [[nl-to-sql/claude-tool-use]], [[conversation/postgresql-crud]], [[data-streaming/sse-fastapi]]
**Technology**: [[react]], [[typescript]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[typescript-sse-client-streaming.md]]
