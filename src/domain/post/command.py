from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

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


class SortOrderEnum(int, Enum):
    asc = 1
    desc = -1


@dataclass(frozen=True)
class SortQuery:
    sort_field: str = "oid"
    sort_order: SortOrderEnum = SortOrderEnum.asc


@dataclass(frozen=True)
class PaginationQuery:
    page: int = 0
    limit: int = 20

    @property
    def offset(self) -> int:
        return self.page * self.limit


@dataclass(frozen=True)
class GetPostListCommand:
    search: Optional[str] = None
    sort: SortQuery = field(default_factory=SortQuery)
    pagination: PaginationQuery = field(default_factory=PaginationQuery)
