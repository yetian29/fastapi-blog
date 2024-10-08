from dataclasses import dataclass

from src.domain.user_profile.entities import UserProfile


@dataclass
class CreateUserProfileCommand:
    user_profile: UserProfile

@dataclass
class UpdateUserProfileCommand:
    user_profile: UserProfile

@dataclass
class GetUserProfileCommand:
    oid: str
