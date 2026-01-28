/**
 * Sidebar component with user profile and navigation.
 * Based on db-chat-nl architecture.md:51 (SidebarTabs.tsx)
 */
import React from 'react';
import { useAuth } from '../hooks/useAuth';

interface SidebarProps {
  onNewChat?: () => void;
}

/**
 * Sidebar displays user profile, navigation, and actions.
 * Based on structure.md:49 (Navigation & history)
 */
export const Sidebar: React.FC<SidebarProps> = ({ onNewChat }) => {
  const { currentUser, logout } = useAuth();

  const handleNewChat = () => {
    if (onNewChat) {
      onNewChat();
    }
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      logout();
    }
  };

  // Generate avatar initials from username
  const getInitials = (username: string): string => {
    return username
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Chat App</h2>
      </div>

      <div className="sidebar-actions">
        <button className="new-chat-button" onClick={handleNewChat}>
          <span className="button-icon">+</span>
          New Chat
        </button>
      </div>

      <div className="sidebar-content">
        {/* TODO: Add conversation history list */}
        {/* Based on structure.md:48-49 (conversation_history capability) */}
        <div className="conversations-section">
          <h3 className="section-title">Recent Conversations</h3>
          <div className="conversation-list">
            <p className="empty-message">No conversations yet</p>
          </div>
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="user-avatar">
            {currentUser && getInitials(currentUser.username)}
          </div>
          <div className="user-info">
            <div className="user-name">{currentUser?.username}</div>
            <div className="user-email">{currentUser?.email}</div>
          </div>
        </div>
        <button className="logout-button" onClick={handleLogout} title="Logout">
          Logout
        </button>
      </div>

      <style>{`
        .sidebar {
          display: flex;
          flex-direction: column;
          width: 260px;
          height: 100vh;
          background-color: var(--primary-base, #1a365d);
          color: white;
          border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-header {
          padding: 20px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-title {
          font-size: 20px;
          font-weight: 700;
          margin: 0;
          color: white;
        }

        .sidebar-actions {
          padding: 16px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .new-chat-button {
          width: 100%;
          padding: 12px;
          background-color: var(--accent-base, #3182ce);
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }

        .new-chat-button:hover {
          background-color: var(--primary-dark, #142850);
        }

        .button-icon {
          font-size: 20px;
          font-weight: 300;
        }

        .sidebar-content {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
        }

        .conversations-section {
          margin-bottom: 20px;
        }

        .section-title {
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 12px;
          opacity: 0.7;
        }

        .conversation-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .empty-message {
          font-size: 14px;
          color: rgba(255, 255, 255, 0.5);
          text-align: center;
          padding: 20px 0;
        }

        .sidebar-footer {
          padding: 16px;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .user-profile {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: linear-gradient(135deg, var(--accent-base, #3182ce), var(--primary-dark, #142850));
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 16px;
          font-weight: 700;
          color: white;
          flex-shrink: 0;
        }

        .user-info {
          flex: 1;
          min-width: 0;
        }

        .user-name {
          font-size: 14px;
          font-weight: 600;
          color: white;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .user-email {
          font-size: 12px;
          color: rgba(255, 255, 255, 0.7);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .logout-button {
          width: 100%;
          padding: 10px;
          background-color: transparent;
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          border-radius: 6px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .logout-button:hover {
          background-color: rgba(255, 255, 255, 0.1);
          border-color: rgba(255, 255, 255, 0.5);
        }

        @media (max-width: 768px) {
          .sidebar {
            width: 100%;
            height: auto;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            transform: translateX(-100%);
            transition: transform 0.3s;
          }

          .sidebar.open {
            transform: translateX(0);
          }
        }
      `}</style>
    </div>
  );
};
