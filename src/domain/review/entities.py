from dataclasses import dataclass

from src.domain.common.base import BaseOid, BaseTime, NotLoaded
from src.domain.user_auth.entities import User


@dataclass
class Review(BaseOid, BaseTime):
    user_id: str | NotLoaded
    post_id: str | NotLoaded
    rating: int
    content: str
