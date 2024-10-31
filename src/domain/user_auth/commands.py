from dataclasses import dataclass

from src.domain.user_auth.entities import UserAuth


@dataclass(frozen=True)
class AuthorizeUserAuthCommand:
    user: UserAuth


@dataclass(frozen=True)
class LoginUserAuthCommand:
    phone_number: str
    email: str
    code: str


@dataclass(frozen=True)
class DeleteUserAuthCommand:
    oid: str
