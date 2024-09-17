

from abc import ABC, abstractmethod

from src.domain.user_profile.entities import UserProfile


class IUserProfileService(ABC):
    @abstractmethod
    async def create(self, user: UserProfile) -> UserProfile:
        pass
    
    @abstractmethod
    async def update(self, user: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    async def get_by_id(self, oid: str) -> UserProfile:
        pass