import pytest
import punq

from src.core.configs.containers import get_container
from src.domain.post.services import IPostService
from tests.mocks.post.services import DummyPostService


@pytest.fixture(scope="session")
def mock_test_container() -> punq.Container:
    container = get_container()
    container.register(IPostService, DummyPostService)
    return container
