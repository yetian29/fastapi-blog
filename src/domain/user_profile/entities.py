from dataclasses import dataclass, field

from src.domain.base.entities import BaseEntity
from src.domain.user_auth.entities import UserAuth
from src.domain.user_profile.value_object import NotLoaded


@dataclass
class UserProfile(BaseEntity):
    username: str = ""
    date_of_birth: str = ""
    user: UserAuth | NotLoaded = field(default_factory=NotLoaded)
