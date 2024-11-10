from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from pymongo import ReturnDocument

from src.infrastructure.db import Database
from src.infrastructure.dto.user_profile import UserProfileDto


@dataclass(frozen=True)
class IUserProfileRepository(ABC):
    database: Database
    collection_name: str = "user_profile"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get_by_oid(self, oid: str) -> Optional[UserProfileDto]:
        pass

    @abstractmethod
    async def create(self, user_profile: UserProfileDto) -> UserProfileDto:
        pass

    @abstractmethod
    async def update(self, user_profile: UserProfileDto) -> Optional[UserProfileDto]:
        pass


class MongoUserProfileRepository(IUserProfileRepository):
    async def get_by_oid(self, oid: str) -> Optional[UserProfileDto]:
        doc = await self.collection.find_one({"oid": oid})
        return UserProfileDto.load(doc)

    async def create(self, user_profile: UserProfileDto) -> UserProfileDto:
        doc = await self.collection.insert_one(user_profile.dump())
        doc = await self.collection.find_one({"_id": doc.inserted_id})
        return UserProfileDto.load(doc)

    async def update(self, user_profile: UserProfileDto) -> Optional[UserProfileDto]:
        doc = await self.collection.find_one_and_update(
            {"oid": user_profile.oid},
            {"$set": user_profile.dump()},
            return_document=ReturnDocument.AFTER,
        )
        return UserProfileDto.load(doc)
