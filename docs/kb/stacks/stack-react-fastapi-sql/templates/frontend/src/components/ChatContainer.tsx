/**
 * ChatContainer component - Main chat interface with message list.
 * Based on db-chat-nl modules.md:171-176 (ChatContainer component)
 */
import React, { useEffect, useRef } from 'react';
import { Message } from '../types/chat';

interface ChatContainerProps {
  messages: Message[];
  isLoading?: boolean;
  error?: string | null;
}

/**
 * ChatContainer displays the message history with auto-scroll.
 * Based on modules.md:172-175 (message list, auto-scroll, loading states)
 */
export const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  isLoading = false,
  error = null
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  // Based on modules.md:173 (auto-scroll to bottom)
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="messages-list">
        {messages.length === 0 && !isLoading && (
          <div className="empty-state">
            <p>No messages yet. Start a conversation!</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
          >
            <div className="message-header">
              <span className="message-role">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </span>
              <span className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>

            <div className="message-content">
              {/* TODO: Add markdown rendering with react-markdown */}
              {/* Based on modules.md:187-190 (Markdown rendering) */}
              <p>{message.content}</p>
            </div>

            {/* Display SQL query if present */}
            {message.sql && (
              <div className="message-sql">
                <strong>SQL Query:</strong>
                <pre>
                  <code>{message.sql}</code>
                </pre>
              </div>
            )}

            {/* Display query results if present */}
            {message.results && (
              <div className="message-results">
                <strong>Results ({message.results.rowCount} rows):</strong>
                {/* TODO: Use DataViewer component for table display */}
                {/* Based on modules.md:212-217 (DataViewer component) */}
                <div className="results-preview">
                  <p>Results table would be displayed here</p>
                </div>
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="message assistant loading">
            <div className="message-header">
              <span className="message-role">Assistant</span>
            </div>
            <div className="message-content">
              <div className="loading-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </div>
            </div>
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="message error">
            <div className="message-header">
              <span className="message-role">Error</span>
            </div>
            <div className="message-content">
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      <style>{`
        .chat-container {
          display: flex;
          flex-direction: column;
          height: 100%;
          overflow: hidden;
        }

        .messages-list {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #666;
        }

        .message {
          padding: 12px 16px;
          border-radius: 8px;
          max-width: 80%;
        }

        .message.user {
          align-self: flex-end;
          background-color: #007bff;
          color: white;
        }

        .message.assistant {
          align-self: flex-start;
          background-color: #f1f3f5;
          color: #333;
        }

        .message.error {
          align-self: center;
          background-color: #fee;
          color: #c33;
          border: 1px solid #fcc;
        }

        .message-header {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          font-size: 12px;
          opacity: 0.8;
        }

        .message-role {
          font-weight: 600;
        }

        .message-timestamp {
          font-size: 11px;
        }

        .message-content {
          line-height: 1.5;
        }

        .message-sql,
        .message-results {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid rgba(0, 0, 0, 0.1);
        }

        .message-sql pre {
          background-color: #282c34;
          color: #abb2bf;
          padding: 12px;
          border-radius: 4px;
          overflow-x: auto;
          margin-top: 8px;
        }

        .message-sql code {
          font-family: 'Courier New', monospace;
          font-size: 13px;
        }

        .results-preview {
          margin-top: 8px;
          padding: 12px;
          background-color: white;
          border: 1px solid #ddd;
          border-radius: 4px;
        }

        .loading-dots {
          display: flex;
          gap: 4px;
        }

        .loading-dots span {
          animation: blink 1.4s infinite;
        }

        .loading-dots span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .loading-dots span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes blink {
          0%, 80%, 100% {
            opacity: 0;
          }
          40% {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};
