"""Controller for authentication – bridges HTTP layer with auth service."""

from fastapi import HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import authenticate_user


def handle_login(body: LoginRequest) -> LoginResponse:
    """Validate credentials and return JWT token or raise 401."""
    token = authenticate_user(body.username, body.password)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
        )

    return LoginResponse(access_token=token, username=body.username)
