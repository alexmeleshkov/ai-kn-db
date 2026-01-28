/**
 * Main App component with authentication and routing.
 * Based on db-chat-nl architecture.md:64 (App.tsx with routing)
 */
import React from 'react';
import { ChatContainer } from './components/ChatContainer';
import { ChatInput } from './components/ChatInput';
import { AuthPage } from './components/AuthPage';
import { Sidebar } from './components/Sidebar';
import { useChat } from './hooks/useChat';
import { AuthProvider, useAuth } from './hooks/useAuth';

/**
 * Protected chat interface component.
 * Only accessible when user is authenticated.
 */
function ChatInterface() {
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat();

  const handleNewChat = () => {
    clearMessages();
  };

  return (
    <div className="chat-interface">
      <Sidebar onNewChat={handleNewChat} />

      <div className="chat-main">
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
      </div>
    </div>
  );
}

/**
 * App router component that handles authentication state.
 * Based on structure.md:27 (AuthProvider wrapper with routing)
 */
function AppRouter() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage />;
  }

  return <ChatInterface />;
}

/**
 * Root App component with AuthProvider.
 * Based on architecture.md:64 (App.tsx root component)
 */
function App() {
  return (
    <AuthProvider>
      <AppRouter />

      <style>{`
        :root {
          --primary-base: #1a365d;
          --primary-dark: #142850;
          --accent-base: #3182ce;
          --success: #38a169;
          --error: #e53e3e;
        }

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

        .loading-screen {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100vh;
          background-color: #f8f9fa;
        }

        .loading-spinner {
          font-size: 18px;
          color: var(--primary-base);
          font-weight: 600;
        }

        .chat-interface {
          display: flex;
          height: 100vh;
          background-color: #f8f9fa;
        }

        .chat-main {
          flex: 1;
          display: flex;
          flex-direction: column;
          overflow: hidden;
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

          .chat-interface {
            flex-direction: column;
          }
        }
      `}</style>
    </AuthProvider>
  );
}

export default App;
