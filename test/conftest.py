import punq
import pytest

from src.core.config.container import get_container
from src.domain.post.services import IPostService
from test.mock.service.post import DummyPostService


@pytest.fixture(scope="session")
def mock_test_container() -> punq.Container:
    container = get_container()
    container.register(IPostService, DummyPostService)
    return container
