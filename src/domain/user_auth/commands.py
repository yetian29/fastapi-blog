from dataclasses import dataclass
from typing import Optional

from src.domain.user_auth.entities import UserAuth


@dataclass(frozen=True)
class AuthorizeUserAuthCommand:
    user: UserAuth


@dataclass(frozen=True)
class LoginUserAuthCommand:
    phone_number: Optional[str]
    email: Optional[str]
    code: str


@dataclass(frozen=True)
class DeleteUserAuthCommand:
    oid: str
