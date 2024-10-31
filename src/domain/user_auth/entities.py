from dataclasses import dataclass
from typing import Optional
from xml.dom.minidom import Entity


@dataclass
class UserAuth(Entity):
    phone_number: Optional[str]
    email: Optional[str]
    token: str
    is_active: bool
