from datetime import datetime

from pydantic import BaseModel, field_validator

from src.domain.post.entities import Post


class PostInSchema(BaseModel):
    title: str
    content: str

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value:
            raise ValueError("InValid title. Title is required.")
        value = value.strip()
        if len(value) > 128:
            raise ValueError(
                "Invalid title. Title must be less than or equal 128 characters."
            )
        return value

    @field_validator("content")
    def validate_content(cls, value: str) -> str:
        if not value:
            raise ValueError("Invalid content. Content is required.")
        value = value.strip()
        if len(value) > 1024:
            raise ValueError(
                "Invalid content. Content must be less than or equal 1024 characters."
            )
        return value

    def to_entity(self, **kwargs) -> Post:
        return Post(title=self.title, content=self.content, **kwargs)


class PostOutSchema(BaseModel):
    oid: str
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: Post) -> "PostOutSchema":
        return PostOutSchema(
            oid=entity.oid,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
