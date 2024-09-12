from polyfactory.factories import DataclassFactory

from src.domain.user_auth.commands import AuthorizeUserCommand, LoginUserCommand
from src.domain.user_auth.entities import User



class UserFactory(DataclassFactory[User]):
    __model__ = User
    
    
class AuthorizeUserCommandFactory(DataclassFactory[AuthorizeUserCommand]):
    __model__ = AuthorizeUserCommand
    

class LoginUserCommandFactory(DataclassFactory[LoginUserCommand]):
    __model__ = LoginUserCommand