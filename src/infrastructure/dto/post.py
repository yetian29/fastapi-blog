from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.post.entities import Post
from src.infrastructure.dto.base import BaseDto


@dataclass
class PostDto(BaseDto):
    oid: Optional[str]
    title: str
    content: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self):
        if not self.oid:
            self.oid = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

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
