from dataclasses import dataclass

from src.domain.common.base import BaseOid, BaseTime


@dataclass
class UserProfile(BaseOid, BaseTime):
    phone_number: str
    username: str
    date_of_birth: str
