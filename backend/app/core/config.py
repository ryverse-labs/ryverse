"""
Centralized configuration.
Loads env variables once and exposes typed settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

    # Database
    MONGO_URL: str = os.getenv("MONGO_URL")
    DB_NAME: str = os.getenv("DB_NAME", "ryverse")

    # App
    APP_NAME: str = "RyVerse API"
    ENV: str = os.getenv("ENV", "development")


settings = Settings()