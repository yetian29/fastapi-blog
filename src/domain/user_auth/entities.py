from dataclasses import dataclass
from typing import Optional

from src.domain.base.entities import BaseEntity


@dataclass
class UserAuth(BaseEntity):
    phone_number: Optional[str]
    email: Optional[str]
    token: Optional[str]
    is_active: bool = False
