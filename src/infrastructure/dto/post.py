from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.post.entities import Post
from src.infrastructure.dto.base import BaseDto


@dataclass(frozen=True)
class PostDto(BaseDto):
    oid: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def load(data: Optional[dict]) -> Optional["PostDto"]:
        if not data:
            return None

        return PostDto(
            oid=data.get("oid"),
            title=data.get("title"),
            content=data.get("content"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(entity: Post) -> "PostDto":
        return PostDto(
            oid=entity.oid,
            title=entity.title,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> Post:
        return Post(
            oid=self.oid,
            title=self.title,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
