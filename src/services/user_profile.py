from dataclasses import dataclass
from datetime import datetime

from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.services import IUserProfileService
from src.infrastructure.dto.user_profile import UserProfileDto
from src.infrastructure.repositories.user_profile import IUserProfileRepository


@dataclass
class UserProfileService(IUserProfileService):
    repository: IUserProfileRepository

    async def create(self, user: UserProfile) -> UserProfile:
        dto = UserProfileDto.from_entity(user)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, user: UserProfile) -> UserProfile:
        dto = UserProfileDto.from_entity(user)
        dto = await self.repository.update(dto)
        return dto.to_entity()

    async def get_by_phone_number(self, phone_number: str) -> UserProfile:
        dto = await self.repository.get_by_phone_number(phone_number)
        if not dto:
            return None
        return dto.to_entity()
    
    async def create_or_update(self, user: UserProfile) -> UserProfile:
        existing_user_profile = await self.get_by_phone_number(
            oid=user.oid
        )
        if existing_user_profile:
            existing_user_profile.username = user.username
            existing_user_profile.date_of_birth = user.date_of_birth
            existing_user_profile.updated_at = datetime.now()
            return await self.update(existing_user_profile)

        return await self.create(user)
