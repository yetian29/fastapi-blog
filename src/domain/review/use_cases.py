from dataclasses import dataclass

from src.domain.review.commands import (
    CreateOrUpdateReviewCommand,
    DeleteReviewCommand,
)
from src.domain.review.entities import Review
from src.domain.review.services import IReviewService


@dataclass
class CreateOrUpdateReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: CreateOrUpdateReviewCommand) -> Review:
        return await self.review_service.create_or_update(review=command.review)


@dataclass
class DeleteReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: DeleteReviewCommand) -> Review:
        return await self.review_service.delete(oid=command.oid)
