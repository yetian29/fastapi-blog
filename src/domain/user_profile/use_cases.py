from dataclasses import dataclass

from src.domain.user_auth.errors import UserInvalidException
from src.domain.user_auth.services import IUserService
from src.domain.user_profile.commands import (
    CreateOrUpdateUserProfileCommand,
    GetUserProfileCommand,
)
from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.services import IUserProfileService
from src.helper.errors import fail


@dataclass
class CreateOrUpdateUserProfileUseCase:
    service: IUserProfileService
    user_service: IUserService

    async def execute(self, check: str, command: CreateOrUpdateUserProfileCommand) -> UserProfile:
        user = await self.user_service.get_by_id(oid=command.user_profile.user_id)
        if user.token == check:
            return await self.service.create_or_update(user=command.user_profile)
        else:
            fail(UserInvalidException())




@dataclass
class GetUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: GetUserProfileCommand) -> UserProfile:
        return await self.service.get_by_id(oid=command.oid)
