from dataclasses import dataclass, field

from src.domain.base.commands import PaginationQuery
from src.domain.post.command import SortQuery
from src.domain.review.entitties import Review


@dataclass(frozen=True)
class CreateReviewCommand:
    review: Review


@dataclass(frozen=True)
class UpdateReviewCommand:
    review: Review


@dataclass
class DeleteReviewCommand(frozen=True):
    oid: str


@dataclass(frozen=True)
class GetReviewCommand:
    oid: str


@dataclass(frozen=True)
class GetReviewListCommand:
    post_id: str
    sort: SortQuery = field(default_factory=SortQuery)
    pagination: PaginationQuery = field(default_factory=PaginationQuery)
