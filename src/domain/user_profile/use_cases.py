

from dataclasses import dataclass
from src.domain.user_profile.commands import CreateUserProfileCommand, GetUserProfileCommand, UpdateUserProfileCommand
from src.domain.user_profile.entities import UserProfile
from src.domain.user_profile.services import IUserProfileService

@dataclass
class CreateUserProfileUseCase:
    service: IUserProfileService

    async def execute(self, command: CreateUserProfileCommand) -> UserProfile:
        return await self.service.create(user=command.user)

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
    