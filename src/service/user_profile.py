from dataclasses import dataclass

from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.service import IUserProfileService
from src.helper.exc import fail
from src.infrastructure.dto.user_profile import UserProfileDto
from src.infrastructure.repositories.user_profile import IUserProfileRepository
from src.service.exc import UserProfileIsNotFoundException


@dataclass(frozen=True)
class UserProfileService(IUserProfileService):
    repository: IUserProfileRepository

    async def get_by_oid(self, oid: str) -> UserProfile:
        dto = await self.repository.get_by_oid(oid)
        if not dto:
            fail(UserProfileIsNotFoundException)
        return dto.to_entity()

    async def create(self, user_profile: UserProfile) -> UserProfile:
        dto = UserProfileDto.from_entity(user_profile)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, user_profile: UserProfile) -> UserProfile:
        dto = UserProfileDto.from_entity(user_profile)
        dto = await self.repository.update(dto)
        if not dto:
            fail(UserProfileIsNotFoundException)
        return dto.to_entity()
