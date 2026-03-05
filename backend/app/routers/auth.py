"""Authentication routes."""

from fastapi import APIRouter

from app.controllers.auth_controller import handle_login
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse, summary="Login & get JWT token")
def login(body: LoginRequest):
    return handle_login(body)
