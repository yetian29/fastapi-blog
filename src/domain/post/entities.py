from dataclasses import dataclass

from src.domain.base.entities import BaseEntity
from src.domain.post.value_object import PostContent, PostTitle


@dataclass
class Post(BaseEntity):
    title: PostTitle
    content: PostContent
