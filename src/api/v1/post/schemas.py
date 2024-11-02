from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from src.domain.post.entities import Post


class PostInSchema(BaseModel):
    title: str
    content: str

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if len(value) > 128:
            raise ValueError("Title must be less than 128 characters.")
        return value

    @field_validator("content")
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if len(value) > 1024:
            raise ValueError("Content must be less than 1024 characters.")
        return value

    @model_validator(mode="after")
    def check_title_or_content(self) -> "PostInSchema":
        if not self.title or not self.content:
            raise ValueError("Invalid. Title and Content are required.")
        return self

    def to_entity(
        self, oid: Optional[str] = None, created_at=None, updated_at=None
    ) -> Post:
        return Post(
            oid=oid,
            title=self.title,
            content=self.content,
            created_at=created_at,
            updated_at=updated_at,
        )


class PostOutSchema(BaseModel):
    oid: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: Post) -> "PostOutSchema":
        return PostOutSchema(
            oid=entity.oid,
            title=entity.title,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
