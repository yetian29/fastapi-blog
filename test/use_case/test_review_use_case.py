import pytest

from src.domain.review.use_case import (
    CreateReviewUseCase,
    DeleteReviewUseCase,
    GetReviewListUseCase,
    GetReviewUseCase,
    UpdateReviewUseCase,
)
from test.mock.factory.review import (
    CreateReviewCommandFactory,
    DeleteReviewCommandFactory,
    GetReviewCommandFactory,
    GetReviewListCommandFactory,
    UpdateReviewCommandFactory,
)


@pytest.fixture
def mock_create_review_use_case(mock_test_container):
    return mock_test_container.resolve(CreateReviewUseCase)


@pytest.fixture
def mock_update_review_use_case(mock_test_container):
    return mock_test_container.resolve(UpdateReviewUseCase)


@pytest.fixture
def mock_delete_review_use_case(mock_test_container):
    return mock_test_container.resolve(DeleteReviewUseCase)


@pytest.fixture
def mock_get_review_use_case(mock_test_container):
    return mock_test_container.resolve(GetReviewUseCase)


@pytest.fixture
def mock_get_review_list_use_case(mock_test_container):
    return mock_test_container.resolve(GetReviewListUseCase)


@pytest.fixture
def mock_count_many_use_case(mock_test_container):
    return mock_test_container.resolve(GetReviewListUseCase)


async def test_create_review_use_case(mock_create_review_use_case):
    command = CreateReviewCommandFactory.build()
    review = await mock_create_review_use_case.execute(command)
    assert review == command.review


async def test_update_review_use_case(mock_update_review_use_case):
    command = UpdateReviewCommandFactory.build()
    review = await mock_update_review_use_case.execute(command)
    assert review == command.review


async def test_delete_review_use_case(mock_delete_review_use_case):
    command = DeleteReviewCommandFactory.build()
    review = await mock_delete_review_use_case.execute(command)
    assert review.oid == command.oid


async def test_get_review_use_case(mock_get_review_use_case):
    command = GetReviewCommandFactory.build()
    review = await mock_get_review_use_case.execute(command)
    assert review.oid == command.oid


async def test_get_review_list_use_case(mock_get_review_list_use_case):
    command = GetReviewListCommandFactory.build()
    reviews, count = await mock_get_review_list_use_case.execute(command)
    assert len(reviews) <= command.pagination.limit
    assert count <= 1000
