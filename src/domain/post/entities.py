from dataclasses import dataclass, fields
from enum import Enum

from src.domain.common.base import BaseOid, BaseTime


@dataclass
class Post(BaseOid, BaseTime):
    title: str
    description: str


PostSortFieldsEnum = Enum(
    "PostSortFieldsEnum", {field.name: field.name for field in fields(Post)}
)
