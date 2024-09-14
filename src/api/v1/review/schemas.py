from datetime import datetime

from pydantic import BaseModel

from src.domain.review.entities import Review


class ReviewInSchema(BaseModel):
    user_id: str
    post_id: str
    rating: int
    content: str

    def to_entity(self, oid: str | None = None) -> Review:
        return Review(
            user_id=self.user_id,
            post_id=self.post_id,
            rating=self.rating,
            content=self.content,
            oid=oid,
            created_at=None,
            updated_at=None,
        )


class ReviewOutSchema(BaseModel):
    oid: str
    user_id: str
    post_id: str
    rating: int
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(review: Review) -> "ReviewOutSchema":
        return ReviewOutSchema(
            oid=review.oid,
            user_id=review.user_id,
            post_id=review.post_id,
            rating=review.rating,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
