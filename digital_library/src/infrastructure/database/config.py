from pydantic import BaseSettings, Field
from typing import List, Optional
from pathlib import Path
from functools import lru_cache
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Configuration settings for the Digital Library Management Platform.

    This class loads configuration settings from environment variables and provides
    a central location for accessing these values throughout the application.

    Attributes:
        PROJECT_NAME (str): The name of the project.
        DATABASE_URL (str): The connection URL for the PostgreSQL database.
        SECRET_KEY (str): A secret key for JWT token generation.
        API_V1_STR (str): The prefix for API v1 routes.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
        REFRESH_TOKEN_EXPIRE_MINUTES (int): The expiration time for refresh tokens in minutes.
        ALGORITHM (str): The algorithm used for signing JWT tokens.
        PORT (int): The port on which the application runs.
        CORS_ALLOWED_ORIGINS (List[str]): A list of allowed origins for CORS requests.
        REDIS_HOST (str): The host for the Redis cache.
        REDIS_PORT (int): The port for the Redis cache.
        REDIS_DB (int): The Redis database index.
        CACHE_PREFIX (str): Prefix for Redis cache keys.
        LOG_LEVEL (str): The logging level for the application.
    """

    PROJECT_NAME: str = "Digital Library Management Platform"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/database")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM = "HS256"
    PORT: int = os.getenv("PORT", 8000)
    CORS_ALLOWED_ORIGINS: List[str] = ["*"]
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)
    REDIS_DB: int = os.getenv("REDIS_DB", 0)
    CACHE_PREFIX: str = "digital_library:"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings():
    """
    Retrieves the application settings.

    Returns:
        Settings: The application settings object.
    """
    return Settings()

settings = get_settings()