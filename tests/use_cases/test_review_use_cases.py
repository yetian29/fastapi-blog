import pytest

from src.domain.review.use_cases import CreateReviewUseCase, DeleteReviewUseCase, UpdateReviewUseCase
from tests.mocks.review.factories import CreateReviewCommandFactory, DeleteReviewCommandFactory, UpdateReviewCommandFactory

@pytest.fixture(scope="function")
def mock_create_review_use_case(mock_test_container):
    return mock_test_container.resolve(CreateReviewUseCase)

@pytest.fixture(scope="function")
def mock_update_review_use_case(mock_test_container):
    return mock_test_container.resolve(UpdateReviewUseCase)

@pytest.fixture(scope="function")
def mock_delete_review_use_case(mock_test_container):
    return mock_test_container.resolve(DeleteReviewUseCase)

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