import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)
from src.helper.errors import fail
from src.service.exc import (
    CodeHasExpiredException,
    CodeIsNotFoundException,
    CodesAreNotEqualException,
    UserAuthIsNotFoundException,
)
from test.mock.factory.user_auth import UserAuthFactory


@dataclass(frozen=True)
class DummyCodeService(ICodeService):
    cache: dict[str, dict] = field(default_factory=dict)

    async def generate_code(self, user: UserAuth) -> str:
        code = str(random.randint(100000, 999999))
        time_out = timedelta(minutes=1)
        cached_data = {"code": code, "ttl": datetime.now() + time_out}
        key = user.phone_number if user.phone_number else user.email
        self.cache[key] = cached_data
        return code

    async def validate_code(self, user: UserAuth, code: str) -> None:
        key = user.phone_number if user.phone_number else user.email
        cached_data = self.cache.get(key)
        if not cached_data:
            del self.cache[key]
            fail(CodeIsNotFoundException)
        if code != cached_data.get("code"):
            del self.cache[key]
            fail(CodesAreNotEqualException)
        if datetime.now() > cached_data.get("ttl"):
            del self.cache[key]
            fail(CodeHasExpiredException)
        del self.cache[key]


class DummySendService(ISendService):
    def send_code(self, user: UserAuth, code: str) -> None:
        key = user.phone_number if user.phone_number else user.email
        print(f"The code <{code}> has been sent to phone number or email <{key}>")


class DummyLoginService(ILoginService):
    def active_and_generate_token(self, user: UserAuth) -> str:
        user.is_active = True
        user.token = str(uuid4())
        return user.token


class DummyUserAuthService(IUserAuthService):
    async def get_by_oid(self, oid: str) -> UserAuth:
        return UserAuthFactory.build(oid=oid)

    async def get_by_phone_number_or_email(
        self, phone_number: Optional[str], email: Optional[str]
    ) -> UserAuth:
        if phone_number:
            return UserAuthFactory.build(phone_number=phone_number)
        return UserAuthFactory.build(email=email)

    async def get_by_token(self, token: str) -> UserAuth:
        return UserAuthFactory.build(token=token)

    async def create(self, user: UserAuth) -> UserAuth:
        user.oid = str(uuid4())
        user.created_at = datetime.now()
        user.updated_at = datetime.now()
        return user

    async def get_or_create(self, user: UserAuth) -> UserAuth:
        try:
            return await self.get_by_phone_number_or_email(
                phone_number=user.phone_number, email=user.email
            )
        except UserAuthIsNotFoundException:
            return await self.create(user)

    async def update(self, user: UserAuth) -> UserAuth:
        return user

    async def delete(self, oid: str) -> UserAuth:
        return UserAuthFactory.build(oid=oid)
