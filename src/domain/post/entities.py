

from src.domain.common.base import BaseOid, BaseTime 


class Post(BaseOid, BaseTime):
    title: str
    description: str
    