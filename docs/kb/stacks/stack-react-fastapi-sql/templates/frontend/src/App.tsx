/**
 * Main App component - Overrides default Vite template.
 * Based on db-chat-nl architecture.md:6-10 (Frontend structure with chat interface)
 */
import React from 'react';
import { ChatContainer } from './components/ChatContainer';
import { ChatInput } from './components/ChatInput';
import { useChat } from './hooks/useChat';

/**
 * App component integrating ChatContainer and ChatInput.
 * This replaces the default Vite template with a functional chat interface.
 */
function App() {
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat();

  return (
    <div className="app">
      <header className="app-header">
        <h1>Chat Interface</h1>
        <div className="header-actions">
          <button
            onClick={clearMessages}
            className="clear-button"
            disabled={messages.length === 0}
          >
            Clear Chat
          </button>
        </div>
      </header>

      <main className="app-main">
        <ChatContainer
          messages={messages}
          isLoading={isLoading}
          error={error}
        />
      </main>

      <footer className="app-footer">
        <ChatInput
          onSubmit={sendMessage}
          disabled={isLoading}
          placeholder="Ask a question about your database..."
        />
      </footer>

      <style>{`
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
            'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
            sans-serif;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }

        .app {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background-color: #f8f9fa;
        }

        .app-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 24px;
          background-color: white;
          border-bottom: 1px solid #e0e0e0;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .app-header h1 {
          font-size: 24px;
          font-weight: 700;
          color: #333;
        }

        .header-actions {
          display: flex;
          gap: 12px;
        }

        .clear-button {
          padding: 8px 16px;
          background-color: transparent;
          color: #666;
          border: 1px solid #ccc;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .clear-button:hover:not(:disabled) {
          background-color: #f5f5f5;
          border-color: #999;
        }

        .clear-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .app-main {
          flex: 1;
          overflow: hidden;
          display: flex;
          flex-direction: column;
        }

        .app-footer {
          background-color: white;
        }

        @media (max-width: 768px) {
          .app-header h1 {
            font-size: 20px;
          }

          .app-header {
            padding: 12px 16px;
          }
        }
      `}</style>
    </div>
  );
}

export default App;
