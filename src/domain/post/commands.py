

from dataclasses import dataclass, field
from src.domain.post.entities import Post 

@dataclass
class CreatePostCommand:
    post: Post

@dataclass
class UpdatePostCommand:
    post: Post

@dataclass
class DeletePostCommand:
    oid: str

@dataclass
class GetPostCommand:
    oid: str


class SortOrderEnum(int, Enum):
    asc = 1
    desc = -1
    
    
@dataclass
class SortQuery:
    sort_field: str = "oid"
    sort_order: SortOrderEnum = SortOrderEnum.asc
    
@dataclass
class PaginationQuery:
    page: int = 0
    limit: int = 20
    
    @property
    def offset(self) -> int:
        return self.page * self.limit
    
@dataclass
class GetPostListCommand:
    search: str | None = None
    sort: SortQuery = field(default_factory=SortQuery)
    pagination: PaginationQuery = field(default_factory=PaginationQuery)