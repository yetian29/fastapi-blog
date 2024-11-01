import random
from datetime import datetime, timedelta

from src.domain.user_auth.services import ICodeService


class CodeService(ICodeService):
    def generate_code(self, user) -> str:
        cache = {}
        code = random.randint(100000, 999999)
        ttl = timedelta(minutes=1)
        cached_data = {"code": code, "ttl": datetime.now() + ttl}
        if user.phone_number:
            cache[user.phone_number] = cached_data

        else:
            cache[user.email] = cached_data

        return code
