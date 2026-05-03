"""
MongoDB connection (async).
Fails fast if config is missing.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

if not settings.MONGO_URL:
    raise RuntimeError("MONGO_URL is not set")

_client = AsyncIOMotorClient(settings.MONGO_URL)
db = _client[settings.DB_NAME]