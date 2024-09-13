from dataclasses import dataclass

from src.domain.common.base import BaseOid, BaseTime


@dataclass
class User(BaseOid, BaseTime):
    phone_number: str
    token: str | None
    is_active: bool
