from dataclasses import dataclass
from domain.base.entities import BaseEntity
from domain.post.value_object import PostContent, PostTitle


@dataclass(frozen=True)
class Post(BaseEntity):
    title: PostTitle
    content: PostContent
