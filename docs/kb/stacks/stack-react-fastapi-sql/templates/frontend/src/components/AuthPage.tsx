/**
 * Authentication page with login and registration forms.
 * Based on db-chat-nl architecture.md:46 (AuthPage.tsx)
 */
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

/**
 * AuthPage component displays login/register forms.
 * Based on structure.md:27 (Login/register UI)
 */
export const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, register, error, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(username, email, password);
      }
      // Navigation handled by App.tsx routing
    } catch (err) {
      // Error displayed via context
      console.error('Auth error:', err);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setUsername('');
    setEmail('');
    setPassword('');
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-title">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h1>
          <p className="auth-subtitle">
            {isLogin
              ? 'Sign in to continue to your chat'
              : 'Sign up to start using the chat interface'}
          </p>

          <form onSubmit={handleSubmit} className="auth-form">
            {!isLogin && (
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your username"
                  required
                  disabled={isLoading}
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                disabled={isLoading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="password-input-wrapper">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="submit-button"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : isLogin ? 'Sign In' : 'Sign Up'}
            </button>
          </form>

          <div className="auth-toggle">
            <p>
              {isLogin ? "Don't have an account?" : 'Already have an account?'}
              {' '}
              <button
                type="button"
                onClick={toggleMode}
                className="toggle-link"
                disabled={isLoading}
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>
      </div>

      <style>{`
        .auth-page {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 100vh;
          background: linear-gradient(135deg, var(--primary-base, #1a365d) 0%, var(--primary-dark, #142850) 100%);
        }

        .auth-container {
          width: 100%;
          max-width: 400px;
          padding: 20px;
        }

        .auth-card {
          background: white;
          border-radius: 12px;
          padding: 40px;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }

        .auth-title {
          font-size: 28px;
          font-weight: 700;
          color: var(--primary-base, #1a365d);
          margin-bottom: 8px;
          text-align: center;
        }

        .auth-subtitle {
          font-size: 14px;
          color: #666;
          text-align: center;
          margin-bottom: 32px;
        }

        .auth-form {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-group label {
          font-size: 14px;
          font-weight: 600;
          color: #333;
        }

        .form-group input {
          padding: 12px;
          font-size: 16px;
          border: 1px solid #ddd;
          border-radius: 6px;
          transition: border-color 0.2s;
        }

        .form-group input:focus {
          outline: none;
          border-color: var(--accent-base, #3182ce);
        }

        .form-group input:disabled {
          background-color: #f5f5f5;
          cursor: not-allowed;
        }

        .password-input-wrapper {
          position: relative;
          display: flex;
        }

        .password-input-wrapper input {
          flex: 1;
          padding-right: 70px;
        }

        .password-toggle {
          position: absolute;
          right: 8px;
          top: 50%;
          transform: translateY(-50%);
          padding: 6px 12px;
          background: transparent;
          border: none;
          color: var(--accent-base, #3182ce);
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: opacity 0.2s;
        }

        .password-toggle:hover:not(:disabled) {
          opacity: 0.7;
        }

        .password-toggle:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

        .error-message {
          padding: 12px;
          background-color: #fee;
          color: var(--error, #e53e3e);
          border: 1px solid #fcc;
          border-radius: 6px;
          font-size: 14px;
        }

        .submit-button {
          padding: 14px;
          font-size: 16px;
          font-weight: 600;
          color: white;
          background-color: var(--accent-base, #3182ce);
          border: none;
          border-radius: 6px;
          cursor: pointer;
          transition: background-color 0.2s;
        }

        .submit-button:hover:not(:disabled) {
          background-color: var(--primary-base, #1a365d);
        }

        .submit-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .auth-toggle {
          margin-top: 24px;
          text-align: center;
        }

        .auth-toggle p {
          font-size: 14px;
          color: #666;
        }

        .toggle-link {
          background: none;
          border: none;
          color: var(--accent-base, #3182ce);
          font-weight: 600;
          cursor: pointer;
          text-decoration: none;
          transition: opacity 0.2s;
        }

        .toggle-link:hover:not(:disabled) {
          opacity: 0.7;
          text-decoration: underline;
        }

        .toggle-link:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

        @media (max-width: 768px) {
          .auth-container {
            padding: 16px;
          }

          .auth-card {
            padding: 32px 24px;
          }

          .auth-title {
            font-size: 24px;
          }
        }
      `}</style>
    </div>
  );
};
