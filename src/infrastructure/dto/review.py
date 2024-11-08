from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.review.entitties import Review
from src.infrastructure.dto.base import BaseDto


@dataclass(frozen=True)
class ReviewDto(BaseDto):
    oid: Optional[str]
    post_id: Optional[str]
    author_id: Optional[str]
    rating: int
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self):
        if not self.oid and not self.created_at and not self.updated_at:
            self.oid = str(uuid4)
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: Optional[dict]) -> Optional["ReviewDto"]:
        if not data:
            return None
        return ReviewDto(
            oid=data.get("oid"),
            post_id=data.get("post_id"),
            author_id=data.get("author_id"),
            rating=data.get("rating"),
            content=data.get("content"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(entity: Review) -> "ReviewDto":
        return ReviewDto(
            oid=entity.oid,
            post_id=entity.post_id,
            author_id=entity.author_id,
            rating=entity.rating,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> Review:
        return Review(
            oid=self.oid,
            post_id=self.post_id,
            author_id=self.author_id,
            rating=self.rating,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
