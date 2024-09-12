from dataclasses import dataclass
from src.domain.user_auth.entities import User
from src.domain.user_auth.services import ICodeService, IUserService
from src.infrastructure.repositories.user import IUserRepository


class CacheCodeService(ICodeService):
    async def generate_code()




@dataclass
class UserService(IUserService):
    repository: IUserRepository
    
    async def get_or_create(self, user: User) -> User:
        dto = await self.repository.get_or_create(user)
        return dto.to_entity()
        
        
        