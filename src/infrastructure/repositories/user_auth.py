from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from pymongo import ReturnDocument

from src.infrastructure.db import Database
from src.infrastructure.dto.user_auth import UserAuthDto


@dataclass(frozen=True)
class IUserAuthRepository(ABC):
    database: Database
    collection_name: str = "user_auth"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get_by_oid(self, oid: str) -> Optional[UserAuthDto]:
        pass

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> Optional[UserAuthDto]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserAuthDto]:
        pass

    @abstractmethod
    async def create(self, user: UserAuthDto) -> UserAuthDto:
        pass

    @abstractmethod
    async def update(self, user: UserAuthDto) -> Optional[UserAuthDto]:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass


class MongoUserAuthRepository(IUserAuthRepository):
    async def get_by_oid(self, oid: str) -> Optional[UserAuthDto]:
        doc = await self.collection.find_one({"oid": oid})
        return doc

    async def get_by_phone_number(self, phone_number: str) -> Optional[UserAuthDto]:
        doc = await self.collection.find_one({"phone_number": phone_number})
        return doc

    async def get_by_email(self, email: str) -> Optional[UserAuthDto]:
        doc = await self.collection.find_one({"email": email})
        return doc

    async def create(self, user: UserAuthDto) -> UserAuthDto:
        doc = await self.collection.insert_one(user.dump())
        doc = await self.collection.find_one({"_id": doc.inserted_id})
        return UserAuthDto.load(doc)

    async def update(self, user: UserAuthDto) -> Optional[UserAuthDto]:
        doc = await self.collection.find_one_and_update(
            {"oid": user.oid},
            {"$set": user.dump()},
            return_document=ReturnDocument.AFTER,
        )
        return UserAuthDto.load(doc)

    async def delete(self, oid: str) -> None:
        await self.collection.delete_one({"oid": oid})
