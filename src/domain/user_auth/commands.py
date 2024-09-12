


from dataclasses import dataclass
from src.domain.user_auth.entities import User

@dataclass
class AuthorizeUserCommand:
    user: User
    
    
@dataclass
class LoginUserCommand:
    phone_number: str
    code: str
    