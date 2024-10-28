from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BaseEntity:
    oid: str
    created_at: datetime
    updated_at: datetime
