import pytest

from src.domain.review.use_cases import (
    CreateOrUpdateReviewUseCase,
    DeleteReviewUseCase,
)
from tests.mocks.review.factories import (
    CreateOrUpdateReviewCommandFactory,
    DeleteReviewCommandFactory,
)


@pytest.fixture(scope="function")
def mock_create_or_update_review_use_case(mock_test_container):
    return mock_test_container.resolve(CreateOrUpdateReviewUseCase)


@pytest.fixture(scope="function")
def mock_delete_review_use_case(mock_test_container):
    return mock_test_container.resolve(DeleteReviewUseCase)


async def test_create_or_update_review_use_case(mock_create_or_update_review_use_case):
    command = CreateOrUpdateReviewCommandFactory.build()
    review = await mock_create_or_update_review_use_case.execute(command)
    assert review == command.review


async def test_delete_review_use_case(mock_delete_review_use_case):
    command = DeleteReviewCommandFactory.build()
    review = await mock_delete_review_use_case.execute(command)
    assert review.oid == command.oid
