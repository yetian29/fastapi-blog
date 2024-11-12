import pickle
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi_cache import FastAPICache

from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.errors import (
    CodeHasExpiredException,
    CodeIsNotFoundException,
    CodesAreNotEqualException,
    UserAuthIsNotFoundException,
)
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)
from src.helper.errors import fail
from src.infrastructure.dto.user_auth import UserAuthDto
from src.infrastructure.repositories.user_auth import IUserAuthRepository


@dataclass(frozen=True)
class CodeService(ICodeService):
    async def generate_code(self, user: UserAuth) -> str:
        cache = FastAPICache.get_backend()
        code = str(random.randint(100000, 999999))
        time_out = timedelta(minutes=1)
        cached_data = {"code": code, "ttl": datetime.now() + time_out}
        cached_data = pickle.dumps(cached_data)  # convert data dict to bytes
        key = user.phone_number if user.phone_number else user.email
        await cache.set(key, cached_data)
        return code

    async def validate_code(self, user: UserAuth, code: str) -> None:
        cache = FastAPICache.get_backend()
        key = user.phone_number if user.phone_number else user.email
        cached_data = await cache.get(key)
        if not cached_data:
            await cache.clear(key)
            fail(CodeIsNotFoundException)
        cached_data = pickle.loads(cached_data)
        if code != cached_data.get("code"):
            await cache.clear(key)
            fail(CodesAreNotEqualException)
        if datetime.now() > cached_data.get("ttl"):
            await cache.clear(key)
            fail(CodeHasExpiredException)
        await cache.clear(key)


class SendService(ISendService):
    def send_code(self, user: UserAuth, code: str) -> None:
        key = user.phone_number if user.phone_number else user.email
        print(f"The code <{code}> has been send to phone number or email <{key}>")


class LoginService(ILoginService):
    def active_and_generate_token(self, user) -> str:
        user.is_active = True
        user.token = str(uuid4())
        return user.token


@dataclass(frozen=True)
class UserAuthService(IUserAuthService):
    repository: IUserAuthRepository

    async def get_by_oid(self, oid: str) -> UserAuth:
        dto = await self.repository.get_by_oid(oid)
        if not dto:
            fail(UserAuthIsNotFoundException)
        return dto.to_entity()

    async def get_by_phone_number_or_email(
        self, phone_number: Optional[str], email: Optional[str]
    ) -> UserAuth:
        if phone_number:
            dto = await self.repository.get_by_phone_number(phone_number)
        else:
            dto = await self.repository.get_by_email(email)
        if not dto:
            fail(UserAuthIsNotFoundException)
        return dto.to_entity()

    async def get_by_token(self, token: str) -> UserAuth:
        dto = await self.repository.get_by_token(token)
        if not dto:
            fail(UserAuthIsNotFoundException)
        return dto.to_entity()

    async def get_or_create(self, user: UserAuth) -> UserAuth:
        try:
            return await self.get_by_phone_number_or_email(
                phone_number=user.phone_number, email=user.email
            )
        except UserAuthIsNotFoundException:
            return await self.create(user)

    async def create(self, user: UserAuth) -> UserAuth:
        dto = UserAuthDto.from_entity(user)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, user: UserAuth) -> UserAuth:
        dto = UserAuthDto.from_entity(user)
        dto = await self.repository.update(dto)
        if not dto:
            fail(UserAuthIsNotFoundException)
        return dto.to_entity()

    async def delete(self, oid: str) -> UserAuth:
        await self.repository.delete(oid)
        return await self.get_by_oid(oid)
