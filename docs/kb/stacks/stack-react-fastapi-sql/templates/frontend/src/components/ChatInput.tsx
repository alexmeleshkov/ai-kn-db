/**
 * ChatInput component - User input field with submit button.
 * Based on db-chat-nl modules.md:178-183 (ChatInput component)
 */
import React, { useState, useRef, KeyboardEvent } from 'react';

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

/**
 * ChatInput provides a text area with auto-resize and Enter key handling.
 * Based on modules.md:179-183 (textarea, submit button, Enter key handling)
 */
export const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  disabled = false,
  placeholder = 'Ask a question...'
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea based on content
  // Based on modules.md:180 (auto-resize)
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const textarea = e.target;
    setMessage(textarea.value);

    // Reset height to auto to get the correct scrollHeight
    textarea.style.height = 'auto';
    // Set height to scrollHeight to fit content
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  };

  // Handle form submission
  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();

    const trimmedMessage = message.trim();
    if (!trimmedMessage || disabled) {
      return;
    }

    onSubmit(trimmedMessage);
    setMessage('');

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  // Handle Enter key press
  // Based on modules.md:182 (Enter key handling)
  // Enter = submit, Shift+Enter = new line
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="chat-input-container">
      <form onSubmit={handleSubmit} className="chat-input-form">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className="chat-input-textarea"
          rows={1}
        />

        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="chat-input-submit"
        >
          Send
        </button>
      </form>

      <style>{`
        .chat-input-container {
          border-top: 1px solid #e0e0e0;
          background-color: white;
          padding: 16px;
        }

        .chat-input-form {
          display: flex;
          gap: 12px;
          align-items: flex-end;
        }

        .chat-input-textarea {
          flex: 1;
          min-height: 44px;
          max-height: 200px;
          padding: 12px;
          border: 1px solid #ccc;
          border-radius: 8px;
          font-family: inherit;
          font-size: 14px;
          line-height: 1.5;
          resize: none;
          overflow-y: auto;
          transition: border-color 0.2s;
        }

        .chat-input-textarea:focus {
          outline: none;
          border-color: #007bff;
        }

        .chat-input-textarea:disabled {
          background-color: #f5f5f5;
          cursor: not-allowed;
        }

        .chat-input-submit {
          padding: 12px 24px;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s;
          white-space: nowrap;
        }

        .chat-input-submit:hover:not(:disabled) {
          background-color: #0056b3;
        }

        .chat-input-submit:disabled {
          background-color: #ccc;
          cursor: not-allowed;
        }

        .chat-input-submit:active:not(:disabled) {
          transform: scale(0.98);
        }
      `}</style>
    </div>
  );
};
