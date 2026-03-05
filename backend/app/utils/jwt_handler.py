"""
JWT token creation and verification utilities.
"""


from jose import JWTError, jwt

from app.config import settings


def create_access_token(data: dict) -> str:
    """Create a permanent JWT access token (no expiration)."""
    to_encode = data.copy()
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT token. Returns payload or None if invalid."""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
