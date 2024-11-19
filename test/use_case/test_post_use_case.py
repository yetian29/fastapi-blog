import pytest

from src.domain.post.use_case import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    UpdatePostUseCase,
)
from test.mock.factory.post import (
    CreatePostCommandFactory,
    DeletePostCommandFactory,
    GetPostCommandFactory,
    GetPostListCommandFactory,
    UpdatePostCommandFactory,
)


@pytest.fixture
def mock_create_post_use_case(mock_test_container):
    return mock_test_container.resolve(CreatePostUseCase)


@pytest.fixture
def mock_update_post_use_case(mock_test_container):
    return mock_test_container.resolve(UpdatePostUseCase)


@pytest.fixture
def mock_delete_post_use_case(mock_test_container):
    return mock_test_container.resolve(DeletePostUseCase)


@pytest.fixture
def mock_get_post_use_case(mock_test_container):
    return mock_test_container.resolve(GetPostUseCase)


@pytest.fixture
def mock_find_many_use_case(mock_test_container):
    return mock_test_container.resolve(GetPostListUseCase)


@pytest.fixture
def mock_count_many_use_case(mock_test_container):
    return mock_test_container.resolve(GetPostListUseCase)


async def test_create_post_use_case(mock_create_post_use_case):
    command = CreatePostCommandFactory.build()
    post = await mock_create_post_use_case.execute(command)
    assert post == command.post


async def test_update_post_use_case(mock_update_post_use_case):
    command = UpdatePostCommandFactory.build()
    post = await mock_update_post_use_case.execute(command)
    assert post == command.post


async def test_delete_post_use_case(mock_delete_post_use_case):
    command = DeletePostCommandFactory.build()
    post = await mock_delete_post_use_case.execute(command)
    assert post.oid == command.oid


async def test_get_post_use_case(mock_get_post_use_case):
    command = GetPostCommandFactory.build()
    post = await mock_get_post_use_case.execute(command)
    assert post.oid == command.oid


async def test_find_many_use_case(mock_find_many_use_case):
    command = GetPostListCommandFactory.build()
    posts, count = await mock_find_many_use_case.execute(command)
    assert len(posts) <= command.pagination.limit
    assert count <= 1000
