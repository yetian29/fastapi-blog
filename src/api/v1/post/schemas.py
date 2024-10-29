from datetime import datetime

from pydantic import BaseModel

from src.domain.post.entities import Post
from src.domain.post.value_object import PostContent, PostTitle


class PostInSchema(BaseModel):
    title: str
    content: str

    def to_entity(self, oid=None, created_at=None, updated_at=None) -> Post:
        return Post(
            oid=oid,
            title=PostTitle(self.title),
            content=PostContent(self.content),
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
