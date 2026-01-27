/**
 * TypeScript type definitions for chat functionality.
 * Based on db-chat-nl modules.md:275-281 (Type definitions)
 */

/**
 * Message interface representing a single chat message.
 * Based on modules.md:154-158 (Chat schemas)
 */
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sql?: string;
  results?: QueryResult;
}

/**
 * Query result interface for database query responses.
 * Based on modules.md:156 (QueryResult schema)
 */
export interface QueryResult {
  columns: string[];
  rows: Record<string, any>[];
  rowCount: number;
}

/**
 * Conversation interface for chat history.
 * Based on modules.md:158 (Conversation schema)
 */
export interface Conversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  messageCount?: number;
}

/**
 * SSE event types from the streaming endpoint.
 * Based on architecture.md:76-77 (SSE Streaming Pattern)
 */
export type SSEEventType =
  | 'connected'
  | 'status'
  | 'message'
  | 'sql'
  | 'results'
  | 'heartbeat'
  | 'error'
  | 'done';

/**
 * SSE event data structure.
 */
export interface SSEEvent {
  type: SSEEventType;
  content?: string;
  message?: string;
  query?: string;
  data?: QueryResult;
}
