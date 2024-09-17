from polyfactory.factories import DataclassFactory

from src.domain.user_profile.commands import (
    CreateUserProfileCommand,
    GetUserProfileCommand,
    UpdateUserProfileCommand,
)
from src.domain.user_profile.entities import UserProfile


class UserProfileFactory(DataclassFactory[UserProfile]):
    __model__ = UserProfile


class CreateUserProfileCommandFactory(DataclassFactory[CreateUserProfileCommand]):
    __model__ = CreateUserProfileCommand


class UpdateUserProfileCommandFactory(DataclassFactory[UpdateUserProfileCommand]):
    __model__ = UpdateUserProfileCommand


class GetUserProfileCommandFactory(DataclassFactory[GetUserProfileCommand]):
    __model__ = GetUserProfileCommand
