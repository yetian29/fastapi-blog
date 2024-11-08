from dataclasses import dataclass, fields
from enum import Enum
from typing import Optional

from src.domain.base.entities import BaseEntity


@dataclass
class Review(BaseEntity):
    post_id: Optional[str] = None
    author_id: Optional[str] = None
    rating: int = 1
    content: str = ""


ReviewSortFieldsEnum = Enum(
    "ReviewSortFieldsEnum", {field.name: field.name for field in fields(Review)}
)
