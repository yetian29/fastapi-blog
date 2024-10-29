import pytest

from src.domain.post.use_case import CreatePostUseCase
from test.mock.factory.post import CreatePostCommandFactory


@pytest.fixture
def mock_create_post_use_case(mock_test_container):
    return mock_test_container.resolve(CreatePostUseCase)


async def test_create_post_use_case(mock_create_post_use_case):
    command = CreatePostCommandFactory.build()
    post = await mock_create_post_use_case.execute(command)
    assert post == command.post
