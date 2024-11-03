from polyfactory.factories import DataclassFactory

from src.domain.user_auth.commands import AuthorizeUserAuthCommand, LoginUserAuthCommand
from src.domain.user_auth.entities import UserAuth


class UserAuthFactory(DataclassFactory[UserAuth]):
    __model__ = UserAuth


class AuthorizeUserAuthCommandFactory(DataclassFactory[AuthorizeUserAuthCommand]):
    __model__ = AuthorizeUserAuthCommand


class LoginUserAuthCommandFactory(DataclassFactory[LoginUserAuthCommand]):
    __model__ = LoginUserAuthCommand
