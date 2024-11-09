import random
from datetime import datetime
from uuid import uuid4

from src.domain.review.entitties import Review
from src.domain.review.service import IReviewService
from test.mock.factory.review import ReviewFactory


class DummyReviewService(IReviewService):
    async def get_by_oid(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)

    async def create(self, review: Review) -> Review:
        review.oid = str(uuid4())
        review.author_id = str(uuid4())
        review.created_at = datetime.now()
        review.updated_at = datetime.now()
        return review

    async def update(self, review: Review) -> Review:
        return review

    async def delete(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)

    async def get_review_list_by_post_id(
        self, post_id, sort_field, sort_order, limit, offset
    ) -> list[Review]:
        return [ReviewFactory.build() for _ in range(random.randint(0, limit))]

    async def count_many(self, post_id: str) -> int:
        return random.randint(0, 1000)
