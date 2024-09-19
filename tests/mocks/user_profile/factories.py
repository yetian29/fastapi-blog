from polyfactory.factories import DataclassFactory

from src.domain.user_profile.commands import (
    CreateOrUpdateUserProfileCommand,
    GetUserProfileCommand,
)
from src.domain.user_profile.entities import UserProfile


class UserProfileFactory(DataclassFactory[UserProfile]):
    __model__ = UserProfile


class CreateOrUpdateUserProfileCommandFactory(
    DataclassFactory[CreateOrUpdateUserProfileCommand]
):
    __model__ = CreateOrUpdateUserProfileCommand


class GetUserProfileCommandFactory(DataclassFactory[GetUserProfileCommand]):
    __model__ = GetUserProfileCommand
