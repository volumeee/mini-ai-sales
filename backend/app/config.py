"""
Application configuration using Pydantic BaseSettings.
Loads from environment variables with sensible defaults.
"""

from pathlib import Path

from pydantic_settings import BaseSettings

# Project root: backend/app/config.py → backend/ → project-root/
_APP_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _APP_DIR.parent
_PROJECT_ROOT = _BACKEND_DIR.parent


class Settings(BaseSettings):
    """Centralized application settings."""

    # JWT
    JWT_SECRET: str = "mini-ai-sales-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"

    # Data paths (override via env vars for Docker)
    CSV_PATH: str = str(_PROJECT_ROOT / "data" / "sales_data.csv")
    MODEL_PATH: str = str(_PROJECT_ROOT / "ml" / "model.joblib")
    ENCODER_PATH: str = str(_PROJECT_ROOT / "ml" / "label_encoder.joblib")

    # Dummy users (username: password)
    DUMMY_USERS: dict = {
        "admin": "admin123",
        "user": "user123",
    }

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
