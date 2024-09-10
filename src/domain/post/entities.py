

from dataclasses import dataclass
from src.domain.common.base import BaseOid, BaseTime 

@dataclass
class Post(BaseOid, BaseTime):
    title: str
    description: str
    