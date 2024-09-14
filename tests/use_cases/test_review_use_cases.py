import pytest

from src.domain.review.use_cases import CreateReviewUseCase
from tests.mocks.review.factories import CreateReviewCommandFactory

@pytest.fixture(scope="function")
def mock_create_review_use_case(mock_test_container):
    return mock_test_container.resolve(CreateReviewUseCase)


async def test_create_review_use_case(mock_create_review_use_case):
    command = CreateReviewCommandFactory.build()
    review = await mock_create_review_use_case.execute(command)
    assert review == command.review
    