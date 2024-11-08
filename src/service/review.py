from dataclasses import dataclass

from src.domain.review.entitties import Review
from src.domain.review.service import IReviewService
from src.helper.exc import fail
from src.infrastructure.dto.review import ReviewDto
from src.infrastructure.repositories.review import IReviewRepository
from src.service.exc import ReviewIsNotFoundException, ReviewsIsNotFoundException


@dataclass(frozen=True)
class ReviewService(IReviewService):
    repository: IReviewRepository

    async def get_by_oid(self, oid: str) -> Review:
        dto = await self.repository.get_by_oid(oid)
        if not dto:
            fail(ReviewIsNotFoundException)
        return dto.to_entity()

    async def create(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.update(dto)
        if not dto:
            fail(ReviewIsNotFoundException)
        return dto.to_entity()

    async def delete(self, oid: str) -> Review:
        review = await self.get_by_oid(oid)
        await self.repository.delete(oid)
        return review

    async def get_review_list_by_post_id(
        self, post_id: str, sort_field: str, sort_order: int, limit: int, offset: int
    ) -> list[Review]:
        review_iter = await self.repository.get_review_list_by_post_id(
            post_id, sort_field, sort_order, limit, offset
        )
        if not review_iter:
            fail(ReviewsIsNotFoundException)
        return [review.to_entity() async for review in review_iter]

    async def count_many(self, post_id: str) -> int:
        count = await self.repository.count_many(post_id)
        if not count:
            fail(ReviewsIsNotFoundException)
        return count
