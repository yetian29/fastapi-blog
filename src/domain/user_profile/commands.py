from dataclasses import dataclass

from src.domain.user_profile.entities import UserProfile


@dataclass
class CreateOrUpdateUserProfileCommand:
    user_profile: UserProfile



@dataclass
class GetUserProfileCommand:
    oid: str
