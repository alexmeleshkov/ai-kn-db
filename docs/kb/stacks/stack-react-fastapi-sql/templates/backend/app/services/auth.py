"""
Authentication service for user registration and login.
Based on db-chat-nl modules.md:5-36 (auth.py service pattern)
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt


# TODO: Replace with actual settings from app.core.config
class Settings:
    """Temporary settings stub. Replace with real config."""
    JWT_SECRET: str = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24


settings = Settings()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Based on modules.md:30-31 (bcrypt hashing pattern)

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password as string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    Based on modules.md:14 (password validation)

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(user_id: int) -> str:
    """
    Generate JWT access token for authenticated user.
    Based on modules.md:21-27 (JWT token generation pattern)

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT token string
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> Optional[int]:
    """
    Decode and validate JWT token.
    Based on modules.md:16 (token verification)

    Args:
        token: JWT token string to verify

    Returns:
        User ID from token if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        return user_id
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        return None


# TODO: Implement database integration for user management
# Based on structure.md:26 (User model with SQLAlchemy)
#
# Example stub functions that need database implementation:
#
# def create_user(username: str, email: str, password: str) -> dict:
#     """Register new user with hashed password."""
#     hashed = hash_password(password)
#     # TODO: Save to database with SQLAlchemy User model
#     return {"id": 1, "username": username, "email": email}
#
# def get_user_by_email(email: str) -> Optional[dict]:
#     """Retrieve user by email address."""
#     # TODO: Query database
#     return None
#
# def authenticate_user(email: str, password: str) -> Optional[dict]:
#     """Validate credentials and return user if valid."""
#     user = get_user_by_email(email)
#     if user and verify_password(password, user['password_hash']):
#         return user
#     return None
