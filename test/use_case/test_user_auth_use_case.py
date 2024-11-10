from uuid import UUID

import pytest

from src.domain.user_auth.use_case import AuthorizeUseAuthUseCase, LoginUserAuthUseCase
from test.mock.factory.user_auth import (
    AuthorizeUserAuthCommandFactory,
    LoginUserAuthCommandFactory,
)


@pytest.fixture
def mock_authorize_user_auth_use_case(mock_test_container):
    return mock_test_container.resolve(AuthorizeUseAuthUseCase)


@pytest.fixture
def mock_login_user_auth_use_case(mock_test_container):
    return mock_test_container.resolve(LoginUserAuthUseCase)


async def test_login_user_auth_use_case(
    mock_authorize_user_auth_use_case, mock_login_user_auth_use_case
):
    command1 = AuthorizeUserAuthCommandFactory.build()
    code = await mock_authorize_user_auth_use_case.execute(command1)
    command2 = LoginUserAuthCommandFactory.build(
        phone_number=command1.user.phone_number, email=command1.user.email, code=code
    )
    token = await mock_login_user_auth_use_case.execute(command2)
    assert isinstance(code, str)
    assert len(code) == 6
    assert code.isdigit()
    assert isinstance(token, str)
    assert UUID(token, version=4)
