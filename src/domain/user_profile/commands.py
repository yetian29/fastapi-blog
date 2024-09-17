from dataclasses import dataclass

from src.domain.user_auth.entities import User
from src.domain.user_profile.entities import UserProfile


@dataclass
class CreateUserProfileCommand:
    user_token: str
    user: User   
    user_profile: UserProfile


@dataclass
class UpdateUserProfileCommand:
    user: User
    user: UserProfile


@dataclass
class GetUserProfileCommand:
    user: User
    oid: str
