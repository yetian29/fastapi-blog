import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.services import ICodeService, ISendService
from src.helper.exc import fail
from src.service.exc import (
    CodeHasExpiredException,
    CodeIsNotFoundException,
    CodesAreNotEqualException,
)


@dataclass(frozen=True)
class DummyCodeService(ICodeService):
    cache: dict = field(default_factory=dict)

    async def generate_code(self, user: UserAuth) -> str:
        code = str(random.randint(100000, 999999))
        time_out = timedelta(minutes=1)
        cached_data = {"code": code, "ttl": datetime.now() + time_out}
        if user.phone_number:
            self.cache[user.phone_number] = cached_data
        else:
            self.cache[user.email] = cached_data
        return code

    async def validate_code(self, user: UserAuth, code: str) -> None:
        if user.phone_number:
            cached_data = self.cache.get(user.phone_number)
            if not cached_data:
                del self.cache[user.phone_number]
                fail(CodeIsNotFoundException)
            if code != cached_data.get("code"):
                del self.cache[user.phone_number]
                fail(CodesAreNotEqualException)
            if datetime.now() > cached_data.get("ttl"):
                del self.cache[user.phone_number]
                fail(CodeHasExpiredException)
            del self.cache[user.phone_number]
        else:
            cached_data = self.cache.get(user.email)
            if not cached_data:
                del self.cache[user.email]
                fail(CodeIsNotFoundException)
            if code != cached_data.get("code"):
                del self.cache[user.email]
                fail(CodesAreNotEqualException)
            if datetime.now() > cached_data.get("ttl"):
                del self.cache[user.email]
                fail(CodeHasExpiredException)
            del self.cache[user.email]


class DummySendService(ISendService):
    pass
