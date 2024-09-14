from polyfactory.factories import DataclassFactory

from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    UpdateReviewCommand,
)
from src.domain.review.entities import Review


class ReviewFactory(DataclassFactory[Review]):
    __model__ = Review


class CreateReviewCommandFactory(DataclassFactory[CreateReviewCommand]):
    __model__ = CreateReviewCommand


class UpdateReviewCommandFactory(DataclassFactory[UpdateReviewCommand]):
    __model__ = UpdateReviewCommand


class DeleteReviewCommandFactory(DataclassFactory[DeleteReviewCommand]):
    __model__ = DeleteReviewCommand
