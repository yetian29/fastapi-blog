from polyfactory.factories import DataclassFactory

from src.domain.review.commands import (
    CreateOrUpdateReviewCommand,
    DeleteReviewCommand,
)
from src.domain.review.entities import Review


class ReviewFactory(DataclassFactory[Review]):
    __model__ = Review


class CreateOrUpdateReviewCommandFactory(DataclassFactory[CreateOrUpdateReviewCommand]):
    __model__ = CreateOrUpdateReviewCommand


class DeleteReviewCommandFactory(DataclassFactory[DeleteReviewCommand]):
    __model__ = DeleteReviewCommand
