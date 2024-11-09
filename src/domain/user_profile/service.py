from abc import ABC, abstractmethod

from src.domain.user_profile.entities import UserProfile


class IUserProfileService(ABC):
    @abstractmethod
    async def get_by_oid(self, oid: str) -> UserProfile:
        pass

    @abstractmethod
    async def create(self, user_profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    async def update(self, user_profile: UserProfile) -> UserProfile:
        pass
