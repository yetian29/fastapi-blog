from dataclasses import dataclass

from src.domain.user_auth.errors import UserInvalidException
from src.domain.user_auth.services import IUserService
from src.domain.user_profile.commands import (
    CreateUserProfileCommand,
    GetUserProfileCommand,
    UpdateUserProfileCommand,
)
from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.services import IUserProfileService
from src.helper.errors import fail


@dataclass
class CreateUserProfileUseCase:
    service: IUserProfileService
    user_service: IUserService

    async def execute(self, command: CreateUserProfileCommand) -> UserProfile:
        user = await self.user_service.get_by_id(oid=command.user.oid)
        if user.token == command.user_token:          
            return await self.service.create(user=command.user_profile)
        else:
            fail(UserInvalidException())


@dataclass
class UpdateUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: UpdateUserProfileCommand) -> UserProfile:
        return await self.service.update(user=command.user)


@dataclass
class GetUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: GetUserProfileCommand) -> UserProfile:
        return await self.service.get_by_id(oid=command.oid)
