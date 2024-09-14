from dataclasses import dataclass

from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    UpdateReviewCommand,
)
from src.domain.review.entities import Review
from src.domain.review.services import IReviewService


@dataclass
class CreateReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: CreateReviewCommand) -> Review:
        return await self.review_service.create(review=command.review)


@dataclass
class UpdateReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: UpdateReviewCommand) -> Review:
        return await self.review_service.update(review=command.review)


@dataclass
class DeleteReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: DeleteReviewCommand) -> Review:
        return await self.review_service.delete(oid=command.oid)
