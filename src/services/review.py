

from dataclasses import dataclass
from src.domain.review.entities import Review
from src.domain.review.errors import ReviewNotFoundException
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
    
    async def create(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, review: Review) -> Review:
        dto = ReviewDto.from_entity(review)
        dto = await self.repository.update(dto)
        return dto.to_entity()
       
    async def delete(self, oid: str) -> Review:
        review = await self.get_by_id(oid)
        await self.repository.delete(oid)
        return review
