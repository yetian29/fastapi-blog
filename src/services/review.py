from dataclasses import dataclass
from datetime import datetime

from src.domain.review.entities import Review
from src.domain.review.errors import (
    CreateReviewNotSuccessException,
    ReviewNotFoundException,
)
from src.domain.review.services import IReviewService
from src.helper.errors import fail
from src.infrastructure.dto.review import ReviewDto
from src.infrastructure.repositories.review import IReviewRepository


@dataclass
class ReviewService(IReviewService):
    repository: IReviewRepository

    async def get_by_id(self, oid: str) -> Review:
        dto = await self.repository.get_by_id(oid)
        if not dto:
            fail(ReviewNotFoundException())
        return dto.to_entity()

    async def get_by_user_id_and_post_id(
        self, user_id: str, post_id: str
    ) -> Review:
        dto = await self.repository.get_by_user_id_and_post_id(
            user_id=user_id, post_id=post_id
        )
        if not dto:
            return None
        return dto.to_entity()

    async def create(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.create(dto)
        if not dto:
            fail(CreateReviewNotSuccessException())
        return dto.to_entity()

    async def update(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.update(dto)
        return dto.to_entity()

    async def create_or_update(self, review: Review) -> Review:
        existing_review = await self.get_by_user_id_and_post_id(
            user_id=review.user_id, post_id=review.post_id
        )
        if existing_review:
            existing_review.rating = review.rating
            existing_review.content = review.content
            existing_review.updated_at = datetime.now()
            return await self.update(existing_review)

        return await self.create(review)

    async def delete(self, oid: str) -> Review:
        review = await self.get_by_id(oid)
        await self.repository.delete(oid)
        return review
