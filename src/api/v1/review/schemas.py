from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.domain.review.entities import Review


class ReviewInSchema(BaseModel):
    content: str
    rating: int = Field(default=1, ge=1, le=5)
    
    @field_validator("rating")
    def validate_rating(cls, value):
        if not 1 <= value <= 5:
              raise ValueError("Rating must be between 1 and 5")
        return value

    def to_entity(
        self, user_token: str, post_id: str, oid: str | None = None
    ) -> Review:
        return Review(
            oid=oid,
            user_token=user_token,
            post_id=post_id,
            rating=self.rating,
            content=self.content,
            created_at=None,
            updated_at=None,
        )


class ReviewOutSchema(BaseModel):
    oid: str
    rating: int
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(review: Review) -> "ReviewOutSchema":
        return ReviewOutSchema(
            oid=review.oid,
            rating=review.rating,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )
