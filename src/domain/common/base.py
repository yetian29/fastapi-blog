from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseOid:
    oid: str | None


@dataclass
class BaseTime:
    created_at: datetime | None
    updated_at: datetime | None


class NotLoaded:
    def __bool__(self) -> bool:
        return False
    
    def __repr__(self) -> str:
        return "<NotLoaded>"