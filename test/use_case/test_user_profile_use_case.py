import pytest

from src.domain.user_profile.use_case import (
    CreateUserProfileUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
)
from test.mock.factory.user_profile import (
    CreateUserProfileCommandFactory,
    GetUserProfileCommandFactory,
    UpdateUserProfileCommandFactory,
)


@pytest.fixture
def mock_create_user_profile_use_case(mock_test_container):
    return mock_test_container.resolve(CreateUserProfileUseCase)


@pytest.fixture
def mock_update_user_profile_use_case(mock_test_container):
    return mock_test_container.resolve(UpdateUserProfileUseCase)


@pytest.fixture
def mock_get_user_profile_use_case(mock_test_container):
    return mock_test_container.resolve(GetUserProfileUseCase)


async def test_create_user_profile_use_case(mock_create_user_profile_use_case):
    command = CreateUserProfileCommandFactory.build()
    user_profile = await mock_create_user_profile_use_case.execute(command)
    assert user_profile == command.user_profile


async def test_update_user_profile_use_case(mock_update_user_profile_use_case):
    command = UpdateUserProfileCommandFactory.build()
    user_profile = await mock_update_user_profile_use_case.execute(command)
    assert user_profile == command.user_profile


async def test_get_user_profile_use_case(mock_get_user_profile_use_case):
    command = GetUserProfileCommandFactory.build()
    user_profile = await mock_update_user_profile_use_case.execute(command)
    assert user_profile.oid == command.oid
