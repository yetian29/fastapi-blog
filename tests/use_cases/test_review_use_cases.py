import pytest

from src.domain.review.use_cases import (
    CreateOrUpdateReviewUseCase,
    DeleteReviewUseCase,
)
from src.domain.user_auth.use_cases import AuthorizeUserUseCase, LoginUserUseCase
from tests.mocks.review.factories import (
    CreateOrUpdateReviewCommandFactory,
    DeleteReviewCommandFactory,
)
from tests.mocks.user_auth.factories import (
    AuthorizeUserCommandFactory,
    LoginUserCommandFactory,
)


@pytest.fixture(scope="function")
def mock_authorize_user_use_case(mock_test_container):
    return mock_test_container.resolve(AuthorizeUserUseCase)


@pytest.fixture(scope="function")
def mock_login_user_use_case(mock_test_container):
    return mock_test_container.resolve(LoginUserUseCase)


@pytest.fixture(scope="function")
def mock_create_or_update_review_use_case(mock_test_container):
    return mock_test_container.resolve(CreateOrUpdateReviewUseCase)


@pytest.fixture(scope="function")
def mock_delete_review_use_case(mock_test_container):
    return mock_test_container.resolve(DeleteReviewUseCase)


async def test_create_or_update_review_use_case(
    mock_authorize_user_use_case,
    mock_login_user_use_case,
    mock_create_or_update_review_use_case,
):
    command1 = AuthorizeUserCommandFactory.build()
    code = await mock_authorize_user_use_case.execute(command1)
    command2 = LoginUserCommandFactory.build(
        phone_number=command1.user.phone_number, code=code
    )
    token = await mock_login_user_use_case.execute(command2)
    command3 = CreateOrUpdateReviewCommandFactory.build()
    review = await mock_create_or_update_review_use_case.execute(
        check=token, command=command3
    )
    assert review.user_id == command3.review.user_id
    assert review.post_id == command3.review.post_id


async def test_delete_review_use_case(mock_delete_review_use_case):
    command = DeleteReviewCommandFactory.build()
    review = await mock_delete_review_use_case.execute(command)
    assert review.oid == command.oid
