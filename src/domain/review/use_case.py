import asyncio
from dataclasses import dataclass

from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    GetReviewCommand,
    GetReviewListCommand,
    UpdateReviewCommand,
)
from src.domain.review.entitties import Review
from src.domain.review.service import IReviewService


@dataclass(frozen=True)
class CreateReviewUseCase:
    service: IReviewService

    async def execute(self, command: CreateReviewCommand) -> Review:
        return await self.service.create(review=command.review)


@dataclass(frozen=True)
class UpdateReviewUseCase:
    service: IReviewService

    async def execute(self, command: UpdateReviewCommand) -> Review:
        return await self.service.update(review=command.review)


@dataclass(frozen=True)
class DeleteReviewUseCase:
    service: IReviewService

    async def execute(self, command: DeleteReviewCommand) -> Review:
        return await self.service.delete(oid=command.oid)


@dataclass(frozen=True)
class GetReviewUseCase:
    service: IReviewService

    async def execute(self, command: GetReviewCommand) -> Review:
        return await self.service.get_by_oid(oid=command.oid)


@dataclass(frozen=True)
class GetReviewListUseCase:
    service: IReviewService

    async def execute(self, command: GetReviewListCommand) -> tuple[list[Review], int]:
        reviews, count = await asyncio.gather(
            self.service.get_review_list_by_post_id(
                post_id=command.post_id,
                sort_field=command.sort.sort_field,
                sort_order=command.sort.sort_order,
                limit=command.pagination.limit,
                offset=command.pagination.offset,
            ),
            self.service.count_many(post_id=command.post_id),
        )
        return reviews, count
