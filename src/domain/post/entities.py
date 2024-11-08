from dataclasses import dataclass, fields
from enum import Enum

from src.domain.base.entities import BaseEntity


@dataclass
class Post(BaseEntity):
    title: str = ""
    content: str = ""


PostSortFieldsEnum = Enum(
    "PostSortFieldsEnum", {field.name: field.name for field in fields(Post)}
)
