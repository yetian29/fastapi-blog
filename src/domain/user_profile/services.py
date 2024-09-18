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
    async def create_or_update(self, user: UserProfile) -> UserProfile:
        pass
    
    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> UserProfile:       
        pass
