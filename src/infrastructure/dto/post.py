from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.post.entities import Post
from src.infrastructure.dto.base import BaseDto


@dataclass
class PostDto(BaseDto):
    oid: str | None
    title: str
    description: str
    created_at: datetime | None
    updated_at: datetime | None

    def __post_init__(self):
        if not self.oid:
            self.oid = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: dict | None) -> "PostDto":
        if not data:
            return None
        return PostDto(
            oid=data.get("oid"),
            title=data.get("title"),
            description=data.get("description"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(post: Post) -> "PostDto":
        return PostDto(
            oid=post.oid,
            title=post.title,
            description=post.description,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    def to_entity(self) -> Post:
        return Post(
            oid=self.oid,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
