from uuid import UUID

import pytest

from src.domain.user_auth.use_cases import AuthorizeUserUseCase, LoginUserUseCase
from tests.mocks.user.factories import (
    AuthorizeUserCommandFactory,
    LoginUserCommandFactory,
)


@pytest.fixture(scope="function")
def mock_authorize_user_use_case(mock_test_container):
    return mock_test_container.resolve(AuthorizeUserUseCase)


@pytest.fixture(scope="function")
def mock_login_user_use_case(mock_test_container):
    return mock_test_container.resolve(LoginUserUseCase)


async def test_authorize_and_login_user_use_case(
    mock_authorize_user_use_case, mock_login_user_use_case
):
    command1 = AuthorizeUserCommandFactory.build()
    code = await mock_authorize_user_use_case.execute(command1)
    assert isinstance(code, str)
    assert code.isdigit()
    assert len(code) == 6

    command2 = LoginUserCommandFactory.build(
        phone_number=command1.user.phone_number, code=code
    )
    token = await mock_login_user_use_case.execute(command2)
    assert isinstance(token, str)
    assert UUID(token, version=4)
