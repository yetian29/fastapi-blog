from polyfactory.factories import DataclassFactory

from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    GetReviewCommand,
    GetReviewListCommand,
    UpdateReviewCommand,
)
from src.domain.review.entitties import Review


class ReviewFactory(DataclassFactory[Review]):
    __model__ = Review


class CreateReviewCommandFactory(DataclassFactory[CreateReviewCommand]):
    __model__ = CreateReviewCommand


class UpdateReviewCommandFactory(DataclassFactory[UpdateReviewCommand]):
    __model__ = UpdateReviewCommand


class DeleteReviewCommandFactory(DataclassFactory[UpdateReviewCommand]):
    __model__ = DeleteReviewCommand


class GetReviewCommandFactory(DataclassFactory[UpdateReviewCommand]):
    __model__ = GetReviewCommand


class GetReviewListCommandFactory(DataclassFactory[UpdateReviewCommand]):
    __model__ = GetReviewListCommand
