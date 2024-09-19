from abc import ABC, abstractmethod
from dataclasses import dataclass

from pymongo import ReturnDocument

from src.domain.user_profile.errors import (
    CreateUserProfileNotSuccessException,
    UpdateUserProfileNotSuccessException,
    UserProfileNotFoundException,
)
from src.helper.errors import fail
from src.infrastructure.database import Database
from src.infrastructure.dto.user_profile import UserProfileDto


@dataclass
class IUserProfileRepository(ABC):
    database: Database
    collection_name: str = "profiles"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get_by_id(self, oid: str) -> UserProfileDto:
        pass
    
    @abstractmethod
    async def create(self, user: UserProfileDto) -> UserProfileDto:
        pass

    @abstractmethod
    async def update(self, user: UserProfileDto) -> UserProfileDto:
        pass



class MongoUserProfileRepository(IUserProfileRepository):
    async def get_by_id(self, oid: str) -> UserProfileDto:
        try:
            doc = await self.collection.find_one({"oid": oid})
        except:
            fail(UserProfileNotFoundException())
        else:
            return UserProfileDto.load(doc)

    async def create(self, user: UserProfileDto) -> UserProfileDto:
        try:
            new_user_profile = await self.collection.insert_one(user.dump())
        except:
            fail(CreateUserProfileNotSuccessException())
        else:
            created_user_profile = await self.collection.find_one(
                {"_id": new_user_profile.inserted_id}
            )
            return UserProfileDto.load(created_user_profile)

    async def update(self, user: UserProfileDto) -> UserProfileDto:
        try:
            updated_user = await self.collection.find_one_and_update(
                {"oid": user.oid},
                {"$set": user.dump()},
                return_document=ReturnDocument.AFTER,
            )
        except:
            fail(UpdateUserProfileNotSuccessException())
        else:
            return UserProfileDto.load(updated_user)
