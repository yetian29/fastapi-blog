import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.user_auth.entities import User
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserService,
)
from src.helper.errors import fail
from src.services.errors import (
    CodeExpiredException,
    CodeNotFoundException,
    CodesNotEqualException,
)
from tests.mocks.user_auth.factories import UserFactory


@dataclass
class DummyCodeService(ICodeService):
    caches: dict[str, dict] = field(default_factory=dict)

    async def generate_code(self, phone_number: str) -> str:
        code = str(random.randint(100000, 999999))
        code_expire_time = timedelta(minutes=1)
        cached_data = {"code": code, "expire_time": datetime.now() + code_expire_time}
        self.caches[phone_number] = cached_data
        return code

    async def validate_code(self, phone_number: str, code: str) -> None:
        cached_data = self.caches.get(phone_number)

        if not cached_data:
            fail(CodeNotFoundException())

        if datetime.now() > cached_data.get("expire_time"):
            fail(CodeExpiredException())
            del self.caches[phone_number]

        if code != cached_data.get("code"):
            fail(CodesNotEqualException())
            del self.caches[phone_number]

        del self.caches[phone_number]


class DummySendService(ISendService):
    async def send_code(self, phone_number: str, code: str) -> None:
        print(f"The code <{code}> has been sent to phone number: <{phone_number}>.")


class DummyLoginService(ILoginService):
    async def activate_and_generate_token(self, user: User) -> str:
        user.is_active = True
        user.token = str(uuid4())
        return user.token


class DummyUserService(IUserService):
    async def get(self, phone_number: str) -> User:
        return UserFactory.build(phone_number=phone_number)

    async def get_or_create(self, user: User) -> User:
        return user
    
    async def update(self, user: User) -> User:
        return user
