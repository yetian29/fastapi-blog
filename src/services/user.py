import pickle
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi_cache import FastAPICache

from src.domain.user_auth.entities import User
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserService,
)
from src.helper.errors import fail
from src.infrastructure.dto.user import UserDto
from src.infrastructure.repositories.user import IUserRepository
from src.services.errors import (
    CodeExpiredException,
    CodeNotFoundException,
    CodesNotEqualException,
)


class CacheCodeService(ICodeService):
    async def generate_code(self, phone_number: str) -> str:
        caches = FastAPICache.get_backend()
        code = str(random.randint(100000, 999999))
        code_expire_time = timedelta(minutes=1)
        cached_data = {"code": code, "expire_time": datetime.now() + code_expire_time}
        data_bytes = pickle.dumps(cached_data)
        await caches.set(phone_number, data_bytes)
        return code

    async def validate_code(self, phone_number: str, code: str) -> None:
        caches = FastAPICache.get_backend()
        data = await caches.get(phone_number)

        if not data:
            fail(CodeNotFoundException())

        cached_data = pickle.loads(data)

        if datetime.now() > cached_data.get("expire_time"):
            fail(CodeExpiredException())
            await caches.clear(phone_number)

        if code != cached_data.get("code"):
            fail(CodesNotEqualException())
            await caches.clear(phone_number)

        await caches.clear(phone_number)


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
        dto = UserDto.from_entity(user)
        dto = await self.repository.get_or_create(dto)
        return dto.to_entity()

    async def get(self, phone_number: str) -> User:
        dto = await self.repository.get(phone_number)
        return dto.to_entity()
