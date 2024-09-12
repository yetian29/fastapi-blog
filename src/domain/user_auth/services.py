


from abc import ABC, abstractmethod
import random

from src.domain.user_auth.entities import User

class ICodeService(ABC):
    @abstractmethod
    async def generate_code(self, phone_number: str) -> str:
        pass

    @abstractmethod
    async def validate_code(self, phone_number: str, code: str) -> None:
        pass

class ISendSerivce(ABC):
    @abstractmethod
    async def send_code(self, phone_number: str) -> None:
        pass        
 
class ILoginService(ABC):
    @abstractmethod
    async def activate_and_generate_token(self, user: User) -> str:
        pass

     
class IUserService(ABC):
    @abstractmethod
    async def get_or_create(self, user: User):
        pass
    