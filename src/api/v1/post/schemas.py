from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.domain.post.command import GetPostListCommand
from src.domain.post.entities import Post, PostSortFieldsEnum
from src.domain.post.value_object import (
    PaginationQuery,
    PostContent,
    PostTitle,
    SortOrderEnum,
    SortQuery,
)


class PostQueryParams(BaseModel):
    search: Optional[str] = None
    sort_field: PostSortFieldsEnum = PostSortFieldsEnum.oid.value
    sort_order: SortOrderEnum = SortOrderEnum.asc
    page: int = 0
    limit: int = 20

    def to_command(self) -> GetPostListCommand:
        return GetPostListCommand(
            search=self.search,
            sort=SortQuery(self.sort_field, self.sort_order),
            pagination=PaginationQuery(self.page, self.limit),
        )


class PostInSchema(BaseModel):
    title: str
    content: str

    def to_entity(
        self, oid: Optional[str] = None, created_at=None, updated_at=None
    ) -> Post:
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
