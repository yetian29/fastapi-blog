
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseOid:
    oid: str | None

@dataclass
class BaseTime:
    created_at: datetime | None 
    updated_at: datetime | None 
    
    