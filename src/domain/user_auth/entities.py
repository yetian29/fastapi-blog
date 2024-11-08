from dataclasses import dataclass
from typing import Optional

from src.domain.base.entities import BaseEntity


@dataclass
class UserAuth(BaseEntity):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    token: Optional[str] = None
    is_active: bool = False
