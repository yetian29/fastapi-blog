

from dataclasses import dataclass
from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.errors import UserProfileNotFoundException
from src.domain.user_profile.services import IUserProfileService
from src.helper.errors import fail
from src.infrastructure.repositories.user_profile import IUserProfileRepository

@dataclass
class UserProfileService(IUserProfileService):
    repository: IUserProfileRepository
    
    async def create(self, user: UserProfile) -> UserProfile:
        dto = UserProfile.from_entity(user)
        dto = await self.repository.create(dto)
        return dto.to_entity()
    
    async def update(self, user: UserProfile) -> UserProfile:
        dto = UserProfile.from_entity(user)
        dto = await self.repository.update(dto)
        return dto.to_entity()
    
    async def get_by_id(self, oid: str) -> UserProfile:
        dto = await self.repository.get_by_id(oid)
        if not dto:
            fail(UserProfileNotFoundException())
        return dto.to_entity()