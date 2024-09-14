


from datetime import datetime
from uuid import uuid4
from src.domain.review.entities import Review
from src.domain.review.services import IReviewService
from tests.mocks.review.factories import ReviewFactory


class DummyReviewService(IReviewService):

    async def get_by_id(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)
        
    async def create(self, review: Review) -> Review:
        review.oid = str(uuid4())
        review.created_at = datetime.now()
        review.updated_at = datetime.now()
        return review
    
    async def update(self, review: Review) -> Review:
        return review

    async def delete(self, oid: str) -> Review:
        return ReviewFactory.build(oid=oid)