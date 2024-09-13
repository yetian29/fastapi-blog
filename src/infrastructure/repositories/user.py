from abc import ABC, abstractmethod
from dataclasses import dataclass

from pymongo import ReturnDocument

from src.domain.user_auth.errors import (
    CreateUserNotSuccessException,
    UpdateUserNotSuccessException,
    UserNotFoundException,
)
from src.helper.errors import fail
from src.infrastructure.database import Database
from src.infrastructure.dto.user import UserDto


@dataclass
class IUserRepository(ABC):
    database: Database
    collection_name: str = "users"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get(self, phone_number: str) -> UserDto:
        pass

    @abstractmethod
    async def create(self, user: UserDto) -> UserDto:
        pass
    
    @abstractmethod
    async def update(self, user: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def get_or_create(self, user: UserDto) -> UserDto:
        pass


class MongoUserRepository(IUserRepository):
    async def get(self, phone_number: str) -> UserDto:
        try:
            doc = await self.collection.find_one({"phone_number": phone_number})
        except:
            fail(UserNotFoundException())
        else:
            return UserDto.load(doc)

    async def create(self, user: UserDto) -> UserDto:
        try:
            new_user = await self.collection.insert_one(user.dump())
        except:
            fail(CreateUserNotSuccessException())
        else:
            created_user = await self.collection.find_one({"_id": new_user.inserted_id})
            return UserDto.load(created_user)

    async def update(self, user: UserDto) -> UserDto:
        try:
            updated_user = await self.collection.find_one_and_update(
                {"oid": user.oid},
                {"$set": user.dump()},
                return_document=ReturnDocument.AFTER
            )
        except:
            fail(UpdateUserNotSuccessException())
        else:
            return UserDto.load(updated_user)
        
    async def get_or_create(self, user: UserDto) -> UserDto:
        dto = await self.get(phone_number=user.phone_number)
        return dto or await self.create(user)
