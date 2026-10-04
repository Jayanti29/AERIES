import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AERIS - Adaptive Air Operations & Resource Intelligence System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "aeris-government-grade-super-secret-key-32-bytes!!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Short-lived access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    IDLE_TIMEOUT_MINUTES: int = 15
    IDLE_WARNING_SECONDS: int = 60

    # Database & Cache
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aeris.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://localhost:8200")
    VAULT_TOKEN: str = os.getenv("VAULT_TOKEN", "aeris-dev-root-token")

    # Security & CORS
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:80", "http://localhost:3000", "http://localhost:5173"]
    HANDLING_BANNER: str = "SYNTHETIC DATA - SIMULATION"
    EMERGENCY_READ_ONLY: bool = False

    class Config:
        case_sensitive = True

settings = Settings()
