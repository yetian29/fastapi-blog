from datetime import datetime
from uuid import uuid4

from src.domain.review.entities import Review
from src.domain.review.services import IReviewService
from tests.mocks.review.factories import ReviewFactory


class DummyReviewService(IReviewService):
    async def get_by_id(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)

    async def get_by_user_token_and_post_id(
        self, user_token: str, post_id: str
    ) -> Review:
        return ReviewFactory.build(user_token=user_token, post_id=post_id)

    async def create_or_update(self, review: Review) -> Review:
        existing_review = await self.get_by_user_token_and_post_id(
            user_token=review.user_token, post_id=review.post_id
        )
        if existing_review:
            existing_review.content = review.content
            existing_review.rating = review.rating
            return await self.update(existing_review)
        return await self.create(review)

    async def create(self, review: Review) -> Review:
        review.oid = str(uuid4())
        review.created_at = datetime.now()
        review.updated_at = datetime.now()
        return review

    async def update(self, review: Review) -> Review:
        return review

    async def delete(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)
