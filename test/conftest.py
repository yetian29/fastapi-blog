import punq
import pytest

from src.core.config.container import get_container
from src.domain.post.services import IPostService
from src.domain.review.service import IReviewService
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)
from src.domain.user_profile.service import IUserProfileService
from test.mock.service.post import DummyPostService
from test.mock.service.review import DummyReviewService
from test.mock.service.user_auth import (
    DummyCodeService,
    DummyLoginService,
    DummySendService,
    DummyUserAuthService,
)
from test.mock.service.user_profile import DummyUserProfileService


@pytest.fixture(scope="session")
def mock_test_container() -> punq.Container:
    container = get_container()

    # User Profile
    container.register(IUserProfileService, DummyUserProfileService)

    # Review
    container.register(IReviewService, DummyReviewService)

    # User Auth
    container.register(ICodeService, DummyCodeService, scope=punq.Scope.singleton)
    container.register(ISendService, DummySendService)
    container.register(ILoginService, DummyLoginService)
    container.register(
        IUserAuthService, DummyUserAuthService, scope=punq.Scope.singleton
    )

    # Post
    container.register(IPostService, DummyPostService)

    return container
