

from dataclasses import dataclass
from src.domain.user_profile.entities import UserProfile

@dataclass
class CreateUserProfileCommand:
    user: UserProfile
    
    
@dataclass
class UpdateUserProfileCommand:
    user: UserProfile
    
@dataclass
class GetUserProfileCommand:
    oid: str