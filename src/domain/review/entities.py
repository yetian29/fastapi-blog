from dataclasses import dataclass

from src.domain.common.base import BaseOid, BaseTime


@dataclass
class Review(BaseOid, BaseTime):
    user_token: str
    post_id: str
    rating: int
    content: str
