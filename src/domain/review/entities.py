

from dataclasses import dataclass
from src.domain.common.base import BaseOid, BaseTime


@dataclass
class Review(BaseOid, BaseTime):
    user_id: str
    rating: float
    content: str