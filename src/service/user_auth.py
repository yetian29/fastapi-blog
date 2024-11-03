import pickle
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi_cache import FastAPICache

from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)
from src.helper.exc import fail
from src.infrastructure.dto.user_auth import UserAuthDto
from src.infrastructure.repositories.user_auth import IUserAuthRepository
from src.service.exc import (
    CodeHasExpiredException,
    CodeIsNotFoundException,
    CodesAreNotEqualException,
    UserAuthIsNotFoundException,
)


class CodeService(ICodeService):
    cache = FastAPICache.get_backend()

    def generate_code(self, user: UserAuth) -> str:
        code = random.randint(100000, 999999)
        ttl = timedelta(minutes=1)
        cached_data = {"code": code, "ttl": datetime.now() + ttl}
        cached_data = pickle.dumps(cached_data)  # convert data dict to bytes
        if user.phone_number:
            self.cache.set(user.phone_number, cached_data)
        else:
            self.cache.set(user.email, cached_data)
        return code

    def validate_code(self, user: UserAuth, code: str) -> None:
        if user.phone_number:
            cached_data = self.cache.get(user.phone_number)
            if not cached_data:
                self.cache.clear(user.phone_number)
                fail(CodeIsNotFoundException)
            cached_data = pickle.loads(cached_data)
            if code != cached_data.get("code"):
                self.cache.clear(user.phone_number)
                fail(CodesAreNotEqualException)
            if datetime.now() > cached_data.get("ttl"):
                self.cache.clear(user.phone_number)
                fail(CodeHasExpiredException)
        else:
            cached_data = self.cache.get(user.email)
            if not cached_data:
                self.cache.clear(user.email)
                fail(CodeIsNotFoundException)
            cached_data = pickle.loads(cached_data)
            if code != cached_data.get("code"):
                self.cache.clear(user.email)
                fail(CodesAreNotEqualException)
            if datetime.now() > cached_data.get("ttl"):
                self.cache.clear(user.email)
                fail(CodeHasExpiredException)


class SendService(ISendService):
    def send_code(self, user: UserAuth, code: str) -> None:
        if user.phone_number:
            print(
                f"The code <{code}> has been send to phone number <{user.phone_number}>"
            )
        else:
            print(f"The code <{code}> has been send to email <{user.email}>")


class LoginService(ILoginService):
    def active_and_generate_token(self, user) -> str:
        user.is_active = True
        user.token = str(uuid4())
        return user.token


@dataclass(frozen=True)
class UserAuthService(IUserAuthService):
    repository: IUserAuthRepository

    async def get_by_oid(self, oid: str) -> UserAuth:
        dto = await self.repository.get_by_id(oid)
        if not dto:
            fail(UserAuthIsNotFoundException)
        return dto.to_entity()

    async def get_or_create(self, user: UserAuth) -> UserAuth:
        dto = UserAuthDto.from_entity(user)
        try:
            return await self.get_by_oid(dto.oid)
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
        return await self.get_by_id(oid)
