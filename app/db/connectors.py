from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional
from asyncio import get_event_loop

class MongoConnector:
    _client: Optional[AsyncIOMotorClient] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                settings.MONGODB_URI, io_loop=get_event_loop()
            )
        return cls._client

def get_user_collection():
    client = MongoConnector.get_client()
    db = client[settings.MONGODB_DB]
    return db["users"]
