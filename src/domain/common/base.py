
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseOid:
    oid: str | None = None

@dataclass
class BaseTime:
    created_at: datetime | None = None
    updated_at: datetime | None =  None
    
    