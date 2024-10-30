from dataclasses import dataclass, fields
from enum import Enum

from src.domain.base.entities import BaseEntity
from src.domain.post.value_object import PostContent, PostTitle


@dataclass
class Post(BaseEntity):
    title: PostTitle
    content: PostContent


PostSortFieldsEnum = Enum(
    "PostSortFieldsEnum", {field.name: field.name for field in fields(Post)}
)
