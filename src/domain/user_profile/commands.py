from dataclasses import dataclass

from src.domain.user_profile.entities import UserProfile


@dataclass(frozen=True)
class CreateUserProfileCommand:
    user_profile: UserProfile


@dataclass(frozen=True)
class UpdateUserProfileCommand:
    user_profile: UserProfile


@dataclass(frozen=True)
class GetUserProfileCommand:
    oid: str
