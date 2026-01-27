/**
 * useChat hook - Chat state management with SSE streaming.
 * Based on db-chat-nl modules.md:242-248 (useChat hook)
 */
import { useState, useCallback, useRef } from 'react';
import { Message, SSEEvent } from '../types/chat';

interface UseChatResult {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
}

/**
 * Custom hook for managing chat state and SSE connections.
 * Based on modules.md:243-248 (SSE connection handling, message state, loading states)
 */
export const useChat = (apiUrl: string = '/api/v1/chat/stream'): UseChatResult => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  /**
   * Send a message and establish SSE connection for streaming response.
   * Based on architecture.md:76-77 (SSE Streaming Pattern)
   */
  const sendMessage = useCallback(async (messageText: string) => {
    // Clear previous error
    setError(null);
    setIsLoading(true);

    // Add user message immediately
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: messageText,
      timestamp: new Date()
    };

    setMessages((prev) => [...prev, userMessage]);

    // Prepare assistant message (will be updated as stream arrives)
    const assistantMessageId = `assistant-${Date.now()}`;
    let assistantContent = '';
    let assistantSql: string | undefined;
    let assistantResults: any = undefined;

    try {
      // TODO: Replace with actual SSE connection
      // Based on modules.md:245 (SSE connection handling)

      // For now, use fetch with streaming
      // In production, use EventSource or fetch with ReadableStream
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          conversation_id: null  // TODO: Add conversation management
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      // Read SSE stream
      // Based on tech.md:46-51 (SSE streaming with heartbeat)
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);

            try {
              const event: SSEEvent = JSON.parse(data);

              // Handle different event types
              // Based on architecture.md:96 (SSE response streaming)
              switch (event.type) {
                case 'connected':
                  console.log('SSE connection established');
                  break;

                case 'status':
                  console.log('Status:', event.message);
                  break;

                case 'message':
                  assistantContent = event.content || '';
                  // Update assistant message
                  setMessages((prev) => {
                    const filtered = prev.filter(m => m.id !== assistantMessageId);
                    return [
                      ...filtered,
                      {
                        id: assistantMessageId,
                        role: 'assistant',
                        content: assistantContent,
                        timestamp: new Date(),
                        sql: assistantSql,
                        results: assistantResults
                      }
                    ];
                  });
                  break;

                case 'sql':
                  assistantSql = event.query;
                  break;

                case 'results':
                  assistantResults = event.data;
                  break;

                case 'heartbeat':
                  // Heartbeat to keep connection alive
                  // Based on tech.md:63-64 (Heroku timeout prevention)
                  console.log('Heartbeat received');
                  break;

                case 'error':
                  setError(event.message || 'An error occurred');
                  break;

                case 'done':
                  console.log('Stream complete');
                  break;
              }
            } catch (parseError) {
              console.error('Failed to parse SSE event:', parseError);
            }
          }
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [apiUrl]);

  /**
   * Clear all messages from chat history.
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);

    // Close any active SSE connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages
  };
};
