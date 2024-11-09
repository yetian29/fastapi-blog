from dataclasses import dataclass

from src.domain.user_profile.commands import (
    CreateUserProfileCommand,
    GetUserProfileCommand,
    UpdateUserProfileCommand,
)
from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.service import IUserProfileService


@dataclass(frozen=True)
class CreateUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: CreateUserProfileCommand) -> UserProfile:
        return await self.service.create(user_profile=command.user_profile)


@dataclass(frozen=True)
class UpdateUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: UpdateUserProfileCommand) -> UserProfile:
        return await self.service.update(user_profile=command.user_profile)


@dataclass(frozen=True)
class GetUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: GetUserProfileCommand) -> UserProfile:
        return await self.service.get_by_oid(oid=command.oid)
