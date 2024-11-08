from dataclasses import dataclass, field
from typing import Optional

from src.domain.base.commands import PaginationQuery, SortQuery
from src.domain.post.entities import Post


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
