from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pickle
import random
from uuid import uuid4

from fastapi_cache import FastAPICache
from src.domain.user_auth.entities import User
from src.domain.user_auth.services import ICodeService, ILoginService, ISendService, IUserService
from src.helper.errors import fail
from src.infrastructure.repositories.user import IUserRepository
from src.services.errors import CodeExpiredException, CodeNotFoundException, CodesNotEqualException



class CacheCodeService(ICodeService):    
    async def generate_code(self, phone_number: str) -> str:
        caches = FastAPICache.get_backend()
        code = str(random.randint(100000, 999999))
        code_expire_time = timedelta(minutes=1)
        cached_data = {
            "code": code,
            "expire_time": datetime.now() + code_expire_time
            
        }
        cached_data = pickle.dumps(cached_data)
        caches.set(phone_number, cached_data)
        return code
    
    async def validate_code(self, phone_number: str, code: str) -> None:
        caches = FastAPICache.get_backend()
        data = caches.get(phone_number)
        cached_data = pickle.loads(data)
        if not cached_data:
            fail(CodeNotFoundException())
            
        if datetime.now() > cached_data.get("expire_time"):
            fail(CodeExpiredException())
            caches.clear(phone_number)
        
        if code != cached_data.get("code"):
            fail(CodesNotEqualException())
            caches.clear(phone_number)
        
        caches.clear(phone_number)
        
        
class SMSSendService(ISendService):
    async def send_code(self, phone_number: str, code: str) -> None:
        print(f"The code <{code}> has been sent to phone number: <{phone_number}>.")
    

class LoginService(ILoginService):
    async def activate_and_generate_token(self, user: User) -> str:
        user.is_active = True
        user.token = str(uuid4())
        return user.token


@dataclass
class UserService(IUserService):
    repository: IUserRepository
          
    
    async def get_or_create(self, user: User) -> User:
        dto = await self.repository.get_or_create(user)
        return dto.to_entity()
        
    async def get(self, phone_number: str) -> User:
        dto = await self.repository.get(phone_number)
        return dto.to_entity()
        
        