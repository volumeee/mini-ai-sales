"""Authentication service – validates credentials and issues tokens."""

from app.config import settings
from app.utils.jwt_handler import create_access_token


def authenticate_user(username: str, password: str) -> str | None:
    """
    Validate username/password against dummy users.
    Returns JWT access token on success, None on failure.
    """
    stored_password = settings.DUMMY_USERS.get(username)

    if stored_password is None or stored_password != password:
        return None

    token = create_access_token(data={"sub": username})
    return token
