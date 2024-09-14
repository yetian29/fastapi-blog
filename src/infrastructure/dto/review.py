from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from src.domain.review.entities import Review
from src.infrastructure.dto.base import BaseDto




@dataclass
class ReviewDto(BaseDto):
    oid: str | None
    user_token: str
    post_id: str
    content: str
    created_at: datetime | None
    updated_at: datetime | None
    rating: int

    def __post_init__(self):
        if not self.oid:
            self.oid = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: dict | None) -> "ReviewDto":
        if not data:
            return None
        return ReviewDto(
            oid=data.get("oid"),
            user_token=data.get("user_token"),
            post_id=data.get("post_id"),
            rating=data.get("rating"),
            content=data.get("content"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(review: Review) -> "ReviewDto":
        return ReviewDto(
            oid=review.oid,
            user_token=review.user_token,
            post_id=review.post_id,
            rating=review.rating,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    def to_entity(self) -> Review:
        return Review(
            oid=self.oid,
            user_token=self.user_token,
            post_id=self.post_id,
            rating=self.rating,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
