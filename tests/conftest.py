import punq
import pytest

from src.core.configs.containers import get_container
from src.domain.post.services import IPostService
from src.domain.review.services import IReviewService
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserService,
)
from src.domain.user_profile.services import IUserProfileService
from tests.mocks.post.services import DummyPostService
from tests.mocks.review.services import DummyReviewService
from tests.mocks.user_auth.services import (
    DummyCodeService,
    DummyLoginService,
    DummySendService,
    DummyUserService,
)
from tests.mocks.user_profile.services import DummyUserProfileService


@pytest.fixture(scope="session")
def mock_test_container() -> punq.Container:
    container = get_container()
    # post
    container.register(IPostService, DummyPostService)

    # user
    container.register(ICodeService, DummyCodeService, scope=punq.Scope.singleton)
    container.register(ISendService, DummySendService)
    container.register(ILoginService, DummyLoginService)
    container.register(IUserService, DummyUserService)

    # review
    container.register(IReviewService, DummyReviewService)

    # user profile
    container.register(IUserProfileService, DummyUserProfileService)

    return container
