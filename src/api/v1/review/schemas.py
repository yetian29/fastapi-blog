from datetime import datetime

from pydantic import BaseModel, field_validator

from src.domain.review.entitties import Review


class ReviewInSchema(BaseModel):
    rating: int = 1
    content: str = ""

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: int = 1) -> int:
        if not value:
            raise ValueError("Invalid rating. Rating is required")
        elif value < 1 or value > 5:
            raise ValueError("Invalid rating. Rating has to be between 1 to 5")
        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str = "") -> str:
        if not value:
            raise ValueError("Invalid content. Content is required.")
        elif len(value) > 1024:
            raise ValueError(
                "Invalid content. Content has to be less than 1024 characters"
            )
        return value

    def to_entity(self, **kwargs) -> Review:
        return Review(rating=self.rating, content=self.content, **kwargs)


class ReviewOutSchema(BaseModel):
    oid: str
    post_id: str
    author_id: str
    rating: int
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: Review) -> "ReviewOutSchema":
        return ReviewOutSchema(
            oid=entity.oid,
            post_id=entity.post_id,
            author_id=entity.author_id,
            rating=entity.rating,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
