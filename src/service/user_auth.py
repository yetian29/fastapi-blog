import pickle
import random
from datetime import datetime, timedelta

from fastapi_cache import FastAPICache

from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.services import ICodeService, ISendService
from src.helper.exc import fail
from src.service.exc import (
    CodeHasExpiredException,
    CodeIsNotFoundException,
    CodesAreNotEqualException,
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
