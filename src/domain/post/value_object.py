from dataclasses import dataclass
from enum import Enum

from domain.base.exc import DomainValidationException
from domain.base.value_object import BaseValueObject


# value object of entities


@dataclass(frozen=True)
class PostTitle(BaseValueObject):
    value: str

    def __post_init__(self):
        if not self.value:
            raise DomainValidationException("Post title is required")

        if self.value > 128:
            raise DomainValidationException(
                "Invalid title. Post title must be less than 128 characters"
            )


@dataclass(frozen=True)
class PostContent(BaseValueObject):
    value: str

    def __post_init__(self):
        if not self.value:
            raise DomainValidationException("Post content is required")

        if self.value > 1024:
            raise DomainValidationException(
                "Invalid content. Post content must be less than 1024 characters"
            )


# value object of commands
class SortOrderEnum(int, Enum):
    asc = 1
    desc = -1


@dataclass(frozen=True)
class SortQuery:
    sort_field: str = "oid"
    sort_order: SortOrderEnum = SortOrderEnum.acs


@dataclass(frozen=True)
class PaginationQuery:
    page: int = 0
    limit: int = 20

    @property
    def offset(self) -> int:
        return self.page * self.limit
