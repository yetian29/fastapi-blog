import pytest
from src.domain.post.use_cases import CreatePostUseCase, DeletePostUseCase, GetPostListUseCase, GetPostUseCase, UpdatePostUseCase
from tests.mocks.post.factories import CreatePostCommandFactory, DeletePostCommandFactory, GetPostCommandFactory, GetPostListCommandFactory, UpdatePostCommandFactory



@pytest.fixture(scope="function")
def mock_create_post_use_case(mock_test_container):
    return mock_test_container.resolve(CreatePostUseCase)
    
@pytest.fixture(scope="function")
def mock_update_post_use_case(mock_test_container):
    return mock_test_container.resolve(UpdatePostUseCase)

@pytest.fixture(scope="function")
def mock_delete_post_use_case(mock_test_container):
    return mock_test_container.resolve(DeletePostUseCase)

@pytest.fixture(scope="function")
def mock_get_by_id_use_case(mock_test_container):
    return mock_test_container.resolve(GetPostUseCase)

@pytest.fixture(scope="function")
def mock_find_many_use_case(mock_test_container):
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
    
async def test_get_by_id_use_case(mock_get_by_id_use_case):
    command = GetPostCommandFactory.build()
    post = await mock_get_by_id_use_case.execute(command)
    assert post.oid == command.oid
   
async def test_find_many_use_case(mock_find_many_use_case):
    command = GetPostListCommandFactory.build() 
    posts, count = await mock_find_many_use_case.execute(command)
    assert len(posts) < command.pagination.limit
    assert count < 1000
    
    