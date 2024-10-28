from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config.database import settings


class Database:
    def __init__(self) -> None:
        self._client = AsyncIOMotorClient(settings.MONGO_URI)
        self._db = self._client.get_database(settings.MONGO_DB)

    @property
    def connection(self):
        return self._db
