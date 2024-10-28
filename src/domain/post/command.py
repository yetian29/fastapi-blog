from dataclasses import dataclass, field
from typing import Optional
from domain.post.entities import Post
from domain.post.value_object import PaginationQuery, SortQuery


@dataclass(frozen=True)
class CreatePostCommand:
    post: Post


@dataclass(frozen=True)
class UpdatePostCommand:
    post: Post


@dataclass(frozen=True)
class DeletePostCommand:
    oid: str


@dataclass(frozen=True)
class GetPostCommand:
    oid: str


@dataclass(frozen=True)
class GetPostListCommand:
    search: Optional[str] = None
    sort: SortQuery = field(default_factory=SortQuery)
    pagination: PaginationQuery = field(default_factory=PaginationQuery)
